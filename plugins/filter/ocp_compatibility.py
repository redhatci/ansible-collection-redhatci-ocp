class FilterModule(object):
    def filters(self):
        return {
            'ocp_compatibility': self.ocp_compatibility,
        }

    def ocp_compatibility(self, after_api, curr_version, junit_ocp_file):
        '''
        Parse the deprecated and to-be-deprecated API after the workload installation.
        '''
        from junit_xml import TestCase, TestSuite
        import re

        def k8s2ocp(x):
            '''
            Convert k8s version to ocp version
            '''
            return f"{int(x.split('.')[0]) + 3}.{int(x.split('.')[1]) - 13}"
        # parse the API after the workload installation and write down incompatible OCP versions
        failed_versions = {k8s2ocp(api['removedInRelease']) for api in after_api}
        version_to_removed_apis = {
            version: {api['name'] for api in after_api if k8s2ocp(api['removedInRelease']) == version}
            for version in failed_versions
        }

        # Find max version in the set of incompatible versions.
        # If the set is empty, bump the current version.
        max_version = max(failed_versions) or curr_version

        major_version = int(re.findall(r'^(\d*)\.', curr_version)[0])
        minor_version = int(re.findall(r'\.(\d*)$', curr_version)[0])
        max_minor_version = int(re.findall(r'\.(\d*)$', max_version)[0])

        ocp_versions = {}
        status = 'compatible'
        version_to_check = minor_version
        while version_to_check <= max_minor_version:
            ocp_version = str(major_version)+"."+str(version_to_check)
            if ocp_version in failed_versions:
                deprecated_apis = ", ".join(version_to_removed_apis[ocp_version])
                ocp_versions[ocp_version] = status + ", " + deprecated_apis if status != 'compatible' else deprecated_apis
                status = deprecated_apis
            elif status != 'compatible':
                ocp_versions[ocp_version] = status
            else:
                ocp_versions[ocp_version] = "compatible"
            version_to_check = version_to_check + 1

        # convert the dictionary to JUnit test suite
        test_cases = []
        for version, incompatible_apis in ocp_versions.items():
            test_case = TestCase(f'Check compatibility with OCP-{version}', classname=f'Workload Compatibility with OCP-{version}')

            if incompatible_apis != 'compatible':
                test_case.add_failure_info(f'Workload uses APIs that are no longer available in OCP-{version}: {incompatible_apis}')

            test_cases.append(test_case)
        test_suite = TestSuite('Workload Compatibility with OCP Versions', test_cases)

        with open(junit_ocp_file, 'w') as f:
            TestSuite.to_file(f, [test_suite])

        return ocp_versions
