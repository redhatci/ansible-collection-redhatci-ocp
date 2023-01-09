class FilterModule(object):
    def filters(self):
        return {
            'regex_diff': self.regex_diff,
        }

    def regex_diff(self, expected, actual):
        '''
        To get the difference between two lists (items in 'expected' that are not present in 'actual').
        The lists should be in the following format:
        [{'testcase': 'BlaBlaTest', 'passed': False}, {'testcase': 'Bla*', 'passed': True}].
        The 'expected' list may contain standard Python regex in the 'testcase' field.
        '''
        from re import compile
        failed_tests = []
        for ex_case in expected:
            absent = True
            for ac_case in actual:
                # check if the expected testcase is present in the actual results
                if compile(ex_case.get('testcase')).search(ac_case.get('testcase')):
                    absent = False
                    # if it's present but the result is not as expected
                    if ex_case['passed'] != ac_case['passed']:
                        failed_tests.append({'failed_expectation': ex_case, 'actual_result': ac_case})
            # if expected test is absent in the actual results
            if absent:
                failed_tests.append({'expected_testcase_absent': ex_case})
        return failed_tests
