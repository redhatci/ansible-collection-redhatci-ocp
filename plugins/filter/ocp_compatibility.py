class FilterModule:
    def filters(self):
        return {
            'ocp_compatibility': self.ocp_compatibility,
        }

    def ocp_compatibility(self, removed_in_release_api, curr_version, junit_ocp_file):
        '''
        Parse the deprecated and to-be-deprecated API after the workload installation.
        '''
        from junit_xml import TestCase, TestSuite, to_xml_report_file
        from collections import defaultdict

        def k8s2ocp(k8s_version):
            '''
            Convert k8s version to ocp version
            '''
            k8s_major, k8s_minor = map(int, k8s_version.split('.'))
            ocp_major, ocp_minor = k8s_major + 3, k8s_minor - 13
            return f"{ocp_major}.{ocp_minor}"

        def bump_ocp_version(version):
            '''
            Bump the input version major.minor
            Ex: bump_version("4.10") -> 4.11
            '''
            major, minor = map(int, version.split('.'))
            return f"{major}.{minor + 1}"

        def ocp_to_str(version):
            '''
            Convert OCP version to a sortable string format.
            Example: "4.11" -> "04.11", "4.6" -> "04.06"
            '''
            major, minor = version.split('.')
            return f"{int(major):02d}.{int(minor):02d}"

        # parse the API after the workload installation and write down incompatible OCP versions
        failed_versions = {k8s2ocp(api['removedInRelease']) for api in removed_in_release_api}
        version_to_removed_apis = defaultdict(list)
        for api in removed_in_release_api:
            release = k8s2ocp(api['removedInRelease'])
            name = api['name']
            service_accounts = api['serviceAccounts']

            version_to_removed_apis[release].append((name, service_accounts))

        # Find max version in the set of incompatible versions.
        # If the set is empty, bump the current version.
        max_version = max(failed_versions | {bump_ocp_version(curr_version)}, key=ocp_to_str)

        # build a continuous list from curr_version to max_version
        version = curr_version
        compatibility = {}
        status = 'compatible'
        while version <= max_version:
            if version in failed_versions:
                incompatible_apis = ', '.join(
                    f"{name} (service accounts: {', '.join(service_accounts)})"
                    for name, service_accounts in version_to_removed_apis[version]
                )
                # making sure to carry the incompatible versions
                # from the previous releases
                compatibility[version] = status + ", " + incompatible_apis if status != 'compatible' else incompatible_apis
                status = incompatible_apis
            elif status != 'compatible':
                compatibility[version] = status
            else:
                compatibility[version] = "compatible"
            version = bump_ocp_version(version)

        # convert the dictionary to JUnit test suite
        test_cases = []
        for version, incompatible_apis in compatibility.items():
            test_case = TestCase(f'Check compatibility with OCP-{version}', classname=f'Workload Compatibility with OCP-{version}')

            if incompatible_apis != 'compatible':
                test_case.add_failure_info(f'Workload uses APIs that are no longer available in OCP-{version}: {incompatible_apis}')

            test_cases.append(test_case)
        test_suite = TestSuite('Workload Compatibility with OCP Versions', test_cases)

        with open(junit_ocp_file, "w", encoding="utf-8") as f:
            to_xml_report_file(f, [test_suite])

        return compatibility
