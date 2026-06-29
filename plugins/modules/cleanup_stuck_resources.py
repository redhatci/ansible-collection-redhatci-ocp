#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: cleanup_stuck_resources
short_description: Find namespaced resources stuck in termination
description:
  - Discovers all namespaced API resources in a Kubernetes cluster and
    identifies those stuck in termination (have finalizers and either a
    deletionTimestamp or belong to a terminating namespace).
  - Returns the list of stuck resources so they can be cleaned up by
    removing their finalizers.
  - Non-available API services are reported as warnings, not failures.
author:
  - Frederic Lepied (@flepied)
requirements:
  - kubernetes >= 11.0.0
options:
  namespace:
    description:
      - The namespace to scan for stuck resources.
    required: true
    type: str
  kubeconfig:
    description:
      - Path to the kubeconfig file.
      - If not provided, falls back to the C(KUBECONFIG) environment
        variable or in-cluster configuration.
    required: false
    type: str
  skip_api_resources:
    description:
      - List of API resources to skip during discovery.
      - Format is C(resource.group) (e.g., C(events.events.k8s.io)).
    required: false
    type: list
    elements: str
    default: []
  remove_all_finalizers:
    description:
      - When C(true), return every namespaced resource that still has
        finalizers in the target namespace.
      - When C(false), only return resources with finalizers that are
        already marked for deletion or belong to a terminating namespace.
    required: false
    type: bool
    default: false
"""

EXAMPLES = """
- name: Find stuck resources in a namespace
  redhatci.ocp.cleanup_stuck_resources:
    namespace: my-namespace
  register: stuck

- name: Show stuck resources
  ansible.builtin.debug:
    var: stuck.resources

- name: Find stuck resources, skipping events
  redhatci.ocp.cleanup_stuck_resources:
    namespace: my-namespace
    skip_api_resources:
      - events.events.k8s.io
  register: stuck
"""

RETURN = """
resources:
  description: List of resources stuck in termination.
  type: list
  elements: dict
  returned: always
  contains:
    name:
      description: Resource name.
      type: str
    resource_type:
      description: API resource type (plural name).
      type: str
    namespace:
      description: Resource namespace.
      type: str
    group:
      description: API group.
      type: str
    version:
      description: API version.
      type: str
    api_version:
      description: Full apiVersion string (group/version or version).
      type: str
    kind:
      description: Resource kind (e.g., Pod, ConfigMap).
      type: str
  sample:
    - name: my-pod
      resource_type: pods
      namespace: my-namespace
      group: ""
      version: v1
      api_version: v1
      kind: Pod
non_available_api_services:
  description: List of API service discovery warnings.
  type: list
  elements: str
  returned: always
"""

import os
import traceback

from ansible.module_utils.basic import AnsibleModule

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
    from kubernetes.dynamic import DynamicClient

    HAS_KUBERNETES = True
except ImportError:
    HAS_KUBERNETES = False
    KUBERNETES_IMPORT_ERROR = traceback.format_exc()


def load_kube_config(kubeconfig):
    if kubeconfig:
        config.load_kube_config(config_file=kubeconfig)
    elif os.environ.get("KUBECONFIG"):
        config.load_kube_config(config_file=os.environ["KUBECONFIG"])
    else:
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()


def should_skip(resource_name, group, skip_list):
    key = "%s.%s" % (resource_name, group) if group else resource_name
    for skip in skip_list:
        if skip.lower() == key.lower():
            return True
    return False


def supports_patch(verbs):
    verb_set = set(verbs or [])
    return {"list", "get"}.issubset(verb_set) and bool(
        verb_set.intersection({"update", "patch"})
    )


def extract_item_metadata(item, default_namespace):
    if hasattr(item, "metadata"):
        meta = item.metadata
        return {
            "deletion_ts": getattr(meta, "deletion_timestamp", None),
            "finalizers": getattr(meta, "finalizers", None),
            "name": getattr(meta, "name", ""),
            "namespace": getattr(meta, "namespace", default_namespace),
        }
    if isinstance(item, dict):
        meta = item.get("metadata", {})
        return {
            "deletion_ts": meta.get("deletionTimestamp"),
            "finalizers": meta.get("finalizers"),
            "name": meta.get("name", ""),
            "namespace": meta.get("namespace", default_namespace),
        }
    return None


def is_stuck_resource(deletion_ts, finalizers, namespace_terminating,
                     remove_all_finalizers):
    if not finalizers:
        return False
    if remove_all_finalizers:
        return True
    if deletion_ts:
        return True
    return namespace_terminating


def find_stuck_resources(namespace, skip_api_resources, remove_all_finalizers,
                         module):
    api_client = client.ApiClient()
    core_v1 = client.CoreV1Api(api_client)
    dyn_client = DynamicClient(api_client)
    stuck = []
    warnings = []
    seen = set()

    # Check if namespace exists and whether it is terminating
    namespace_terminating = False
    try:
        ns = core_v1.read_namespace(namespace)
        ns_meta = ns.metadata if hasattr(ns, "metadata") else None
        if ns_meta is not None:
            namespace_terminating = bool(
                getattr(ns_meta, "deletion_timestamp", None)
            )
    except ApiException as e:
        if e.status == 404:
            return stuck, warnings
        raise

    # Discover namespaced API resources
    api_groups = []

    # Core API (v1)
    try:
        core_resources = core_v1.get_api_resources()
        api_groups.append(("", "v1", core_resources.resources))
    except ApiException as e:
        warnings.append("Failed to discover core API resources: %s" % str(e))

    # Named API groups
    apis_api = client.ApisApi(api_client)
    try:
        groups = apis_api.get_api_versions()
    except ApiException as e:
        module.fail_json(msg="Failed to discover API groups: %s" % str(e))
        return stuck, warnings

    for group_item in groups.groups:
        preferred = group_item.preferred_version
        group_name = group_item.name
        version = preferred.version
        try:
            # Use the raw API to get resources for this group/version
            path = "/apis/%s/%s" % (group_name, version)
            resp = api_client.call_api(
                path, "GET",
                response_type="object",
                auth_settings=["BearerToken"],
                _return_http_data_only=True,
            )
            if hasattr(resp, "get"):
                resources = resp.get("resources", [])
            elif isinstance(resp, dict):
                resources = resp.get("resources", [])
            else:
                continue
            api_groups.append((group_name, version, resources))
        except Exception as e:
            warnings.append(
                "Failed to discover resources for %s/%s: %s"
                % (group_name, version, str(e))
            )

    # Scan each API resource
    for group, version, resources in api_groups:
        if isinstance(resources, list) and len(resources) > 0:
            for res in resources:
                # Handle both object and dict
                if hasattr(res, "name"):
                    res_name = res.name
                    res_kind = getattr(res, "kind", "")
                    res_namespaced = res.namespaced
                    res_verbs = res.verbs or []
                elif isinstance(res, dict):
                    res_name = res.get("name", "")
                    res_kind = res.get("kind", "")
                    res_namespaced = res.get("namespaced", False)
                    res_verbs = res.get("verbs", [])
                else:
                    continue

                if not res_namespaced:
                    continue

                # Skip sub-resources (contain /)
                if "/" in res_name:
                    continue

                if should_skip(res_name, group, skip_api_resources):
                    continue

                if not supports_patch(res_verbs):
                    continue

                api_version = "%s/%s" % (group, version) if group else version

                try:
                    resource_api = dyn_client.resources.get(
                        api_version=api_version,
                        kind=res_kind,
                    )
                except Exception as e:
                    warnings.append(
                        "Failed to resolve %s (%s): %s"
                        % (res_name, api_version, str(e))
                    )
                    continue

                try:
                    resource_list = resource_api.get(
                        namespace=namespace,
                    )
                except ApiException as e:
                    if e.status in (404, 403):
                        continue
                    warnings.append(
                        "Failed to list %s in %s: %s"
                        % (res_name, namespace, str(e))
                    )
                    continue
                except Exception as e:
                    warnings.append(
                        "Failed to list %s in %s: %s"
                        % (res_name, namespace, str(e))
                    )
                    continue

                items = []
                if hasattr(resource_list, "items") and resource_list.items:
                    items = resource_list.items
                elif isinstance(resource_list, dict):
                    items = resource_list.get("items", [])

                for item in items:
                    meta = extract_item_metadata(item, namespace)
                    if meta is None:
                        continue

                    if not is_stuck_resource(
                        meta["deletion_ts"],
                        meta["finalizers"],
                        namespace_terminating,
                        remove_all_finalizers,
                    ):
                        continue

                    resource_key = (api_version, res_kind, meta["name"])
                    if resource_key in seen:
                        continue
                    seen.add(resource_key)

                    stuck.append({
                        "name": meta["name"],
                        "resource_type": res_name,
                        "namespace": meta["namespace"],
                        "group": group,
                        "version": version,
                        "api_version": api_version,
                        "kind": res_kind,
                    })

    return stuck, warnings


def main():
    module_args = dict(
        namespace=dict(type="str", required=True),
        kubeconfig=dict(type="str", required=False, default=None),
        skip_api_resources=dict(
            type="list", elements="str", required=False, default=[]
        ),
        remove_all_finalizers=dict(
            type="bool", required=False, default=False
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if not HAS_KUBERNETES:
        module.fail_json(
            msg="The kubernetes Python library is required. "
            "Install it with: pip install kubernetes",
            exception=KUBERNETES_IMPORT_ERROR,
        )

    namespace = module.params["namespace"]
    kubeconfig = module.params["kubeconfig"]
    skip_api_resources = module.params["skip_api_resources"]
    remove_all_finalizers = module.params["remove_all_finalizers"]

    try:
        load_kube_config(kubeconfig)
    except Exception as e:
        module.fail_json(msg="Failed to load kubeconfig: %s" % str(e))

    try:
        resources, warnings = find_stuck_resources(
            namespace, skip_api_resources, remove_all_finalizers, module
        )
    except Exception as e:
        module.fail_json(
            msg="Failed to find stuck resources: %s" % str(e),
            exception=traceback.format_exc(),
        )

    for w in warnings:
        module.warn(w)

    module.exit_json(
        changed=False,
        resources=resources,
        non_available_api_services=warnings,
    )


if __name__ == "__main__":
    main()
