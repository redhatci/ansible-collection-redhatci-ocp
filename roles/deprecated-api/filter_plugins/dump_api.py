class FilterModule(object):
    def filters(self):
        return {
            'dump_api': self.dump_api,
        }

    def read_api(self, api_json):
        from collections import defaultdict
        dict = defaultdict(list)
        for api in api_json:
            api_name = api['metadata']['name']
            request_count = api['status']['requestCount']
            removed_in_release = api['status']['removedInRelease']
            user_agents = set()
            user_names = set()

            for nodes_info in api['status']['last24h']:
                if nodes_info["requestCount"] > 0:
                    for node_info in nodes_info['byNode']:
                        if 'byUser' in node_info:
                            for user_info in node_info['byUser']:
                                user_agents.add(user_info['userAgent'])
                                user_names.add(user_info['username'])

            dict[api_name, request_count] = [removed_in_release,\
                ','.join(user_agents),
                ','.join(user_names)]
        return dict


    def k8s2ocp(self, kver):
        return "OCP-" + str(float(kver) + 2.87)


    def dump_api(self, before_api, after_api, csv_file):
        '''
        Take the output of two commands, `oc get -o json apirequestcounts`,
        before and after running the workload.
        Compute the API _used by the workload_ that will be removed
        in subsequent OCP versions.
        '''
        import csv
        before_data = self.read_api(before_api)
        after_data = self.read_api(after_api)
        dict_data = []
        for api in after_data:
            # remove the API used by OCP from the consideration
            if api not in before_data:
                api_name, request_count = api
                removed_in_release, user_agents, user_names = after_data[api]
                dict_data.append({'API': api_name,\
                    'REQUESTCOUNT': request_count,\
                    'REMOVEDINRELEASE': self.k8s2ocp(removed_in_release),\
                    'USERAGENTS': user_agents,\
                    'USERNAMES': user_names})

        csv_columns = ['API','REQUESTCOUNT', 'REMOVEDINRELEASE', 'USERAGENTS', 'USERNAMES']
        csvfile = open(csv_file, 'w+')
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
        csvfile.close()
        return dict_data
