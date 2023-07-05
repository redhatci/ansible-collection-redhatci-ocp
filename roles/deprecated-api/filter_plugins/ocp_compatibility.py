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

        # convert k8s version to ocp version
        k8s2ocp = lambda x : f"{int(x.split('.')[0]) + 3}.{int(x.split('.')[1]) - 13}"
        # parse the API after the workload installation and write down incompatible OCP versions
        failed_versions = [ k8s2ocp(api['status']['removedInRelease']) for api in after_api ]

        # convert major.minor version to semvers' major.minor.patch
        ocp2semver = lambda x : VersionInfo.parse(x + ".0")
        # convert semver's major.minor.patch to OCP major.minor
        semver2ocp = lambda x : '.'.join(str(x).split('.')[:-1])
        # Find max version in the set of incompatible versions.
        # If the set is empty, bump the current version.
        max_version = max(failed_versions + [semver2ocp(ocp2semver(curr_version).bump_minor())], \
                          key=lambda x: ocp2semver(x))

        # build a continuous list from curr_version to max_version
        version = ocp2semver(curr_version)
        max_version_semver = ocp2semver(max_version)
        ocp_versions = {}
        status = 'compatible'
        while version <= max_version_semver:
            if semver2ocp(version) in failed_versions or status == 'not_compatible':
                ocp_versions[semver2ocp(version)] = "not_compatible"
                status = "not_compatible"
            else:
                ocp_versions[semver2ocp(version)] = "compatible"
            version = version.bump_minor()

        # convert the dictionary to JUnit test suite
        test_cases = []
        for version, status in ocp_versions.items():
            test_case = TestCase(f'Compatible with OCP-{version}', classname=f'Compatibility with OCP-{version}')

            if status == 'not_compatible':
                test_case.add_failure_info(f'The workload is not compatible with OCP-{version}')
                test_case.add_error_info(f'The workload utilizes an API that has been deprecated for OCP-{version}')

            test_cases.append(test_case)
        test_suite = TestSuite('Workload compatibility with OCP versions', test_cases)

        with open(junit_ocp_file, 'w') as f:
            TestSuite.to_file(f, [test_suite])

        return ocp_versions
