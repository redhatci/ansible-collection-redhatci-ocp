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
        from semver import VersionInfo

        def k8s2ocp(x):
            '''
            Convert k8s version to ocp version
            '''
            return "{}.{}".format(int(x.split('.')[0]) + 3, int(x.split('.')[1]) - 13)
        # parse the API after the workload installation and write down incompatible OCP versions
        failed_versions = set(k8s2ocp(api['removedInRelease']) for api in after_api)
        version_to_removed_apis = {}
        for version in failed_versions:
            version_to_removed_apis[version] = set(api['name'] for api in after_api if k8s2ocp(api['removedInRelease']) == version)

        def ocp2semver(x):
            '''
            Convert major.minor version to semvers' major.minor.patch
            '''
            return VersionInfo.parse(x + ".0")

        def semver2ocp(x):
            '''
            Convert semver's major.minor.patch to OCP major.minor
            '''
            return '.'.join(str(x).split('.')[:-1])
        # Find max version in the set of incompatible versions.
        # If the set is empty, bump the current version.
        max_version = max(failed_versions | {semver2ocp(ocp2semver(curr_version).bump_minor())},
                          key=ocp2semver)

        # build a continuous list from curr_version to max_version
        version = ocp2semver(curr_version)
        max_version_semver = ocp2semver(max_version)
        ocp_versions = {}
        status = 'compatible'
        while version <= max_version_semver:
            ocp_version = semver2ocp(version)
            if ocp_version in failed_versions:
                deprecated_apis = ", ".join(version_to_removed_apis[ocp_version])
                ocp_versions[ocp_version] = status + ", " + deprecated_apis if status != 'compatible' else deprecated_apis
                status = deprecated_apis
            elif status != 'compatible':
                ocp_versions[ocp_version] = status
            else:
                ocp_versions[ocp_version] = "compatible"
            version = version.bump_minor()

        # convert the dictionary to JUnit test suite
        test_cases = []
        for version, incompatible_apis in ocp_versions.items():
            test_case = TestCase('Check compatibility with OCP-{}'.format(version), 'Workload Compatibility with OCP Versions')

            if incompatible_apis != 'compatible':
                test_case.add_failure_info('Workload uses APIs that are no longer available in OCP-{}: {}'.format(version, incompatible_apis))

            test_cases.append(test_case)
        test_suite = TestSuite('Workload Compatibility with OCP Versions', test_cases)

        with open(junit_ocp_file, 'w') as f:
            TestSuite.to_file(f, [test_suite])

        return ocp_versions
