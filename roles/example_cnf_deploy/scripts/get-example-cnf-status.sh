#!/bin/sh
#
# Copyright (C) 2024 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Description: A shell script that collects logs and information from the
# workloads deployed by example-cnf

set -x

echo "--- Pod status ---"
echo
echo "> Pod list"
$OC_BINARY get pods -n "$APP_NAMESPACE" -o wide
echo

APP_PODS=$($OC_BINARY get pods -n "$APP_NAMESPACE" -o custom-columns=POD:.metadata.name --no-headers)
for POD in $APP_PODS; do
    echo ">> Details of pod $POD"
    echo
    echo ">>> Description of pod $POD"
    $OC_BINARY describe pod -n "$APP_NAMESPACE" "$POD"
    echo
    echo ">>> JSON output of pod $POD"
    $OC_BINARY get pod -n "$APP_NAMESPACE" "$POD" -o json
    echo
    echo ">>> Logs from pod $POD"
    $OC_BINARY logs -n "$APP_NAMESPACE" "$POD"
    echo
done

echo
echo "--- CR status ---"
CRS="cnfappmac testpmd trexconfig trexapp"
for CR in $CRS; do 
   echo "> Status of $CR"
   $OC_BINARY get "$CR" -n "$APP_NAMESPACE"
   echo
   $OC_BINARY get "$CR" -n "$APP_NAMESPACE" -o json
done

echo
echo "--- SRIOV resources status ---"
echo "> SRIOV pod list"
$OC_BINARY get pods -n "$SRIOV_NAMESPACE" -o wide
echo

SRIOV_RESOURCES="sriovnetworknodepolicy sriovnetworknodestate sriovnetwork"
for SRIOV_RESOURCE in $SRIOV_RESOURCES; do 
    echo "> Status of $SRIOV_RESOURCE"
    $OC_BINARY get "$SRIOV_RESOURCE" -n "$SRIOV_NAMESPACE"
    echo
    $OC_BINARY get "$SRIOV_RESOURCE" -n "$SRIOV_NAMESPACE" -o json
done

echo
echo "--- NetworkAttachmentDefinition resources status ---"
echo "> NetworkAttachmentDefinition list"
$OC_BINARY get network-attachment-definition -n "$APP_NAMESPACE" -o wide
echo

NET_ATTACH_DEFS=$($OC_BINARY get network-attachment-definition -n "$APP_NAMESPACE" -o custom-columns=NAME:.metadata.name --no-headers)
for NET_ATTACH_DEF in $NET_ATTACH_DEFS; do
    echo ">> JSON output of NetworkAttachmentDefinition $NET_ATTACH_DEF"
    $OC_BINARY get network-attachment-definition -n "$APP_NAMESPACE" "$NET_ATTACH_DEF" -o json
    echo
done

echo
echo "End of script"
