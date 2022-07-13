class FilterModule(object):
    def filters(self):
        return {
            'regex_diff': self.regex_diff,
        }

    def regex_diff(self, a, b):
        '''
        To get the difference of 2 lists (items in 1 that do not exist in 2).
        Expected lists format:
        [{'testcase': 'BlaBlaTest', 'passed': False}, {'testcase': 'Bla*', 'passed': True}].
        List 1 could contain standard Python regex in the testcase field.
        '''
        from re import compile
        return [x for x in a \
            # if expected test is absent in the actual results
            if not any(compile(x.get('testcase')).search(y.get('testcase')) for y in b) \
            # or its result is not as expected
            or any(compile(x.get('testcase')).search(y.get('testcase')) \
            and x.get('passed') != y.get('passed') for y in b) ]
