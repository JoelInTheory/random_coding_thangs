"""
GET /groups/<groupname>
    Returns the matching group record or 404 if none exist

expected:
    200 got em
    404 not found - group not found

"""

import requests

class RunTest:
    def __init__(self, host, port, check):
        self.host = host
        self.port = port
        self.check = check
        self.check_message = None

        self.test_group_one = {"groupname": "test_group_one"}

    def check_group_not_found(self, resp):
        if resp.status_code != 404:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - expected 404 not found'
        return True

    def check_group_get(self, resp, expected_list):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        try:
            resp_json = resp.json()
        except:
            self.check_message = 'FAIL - could not parse response as json'
            return False
        if resp_json == expected_list:
            self.check_message = 'OK - list matches expected'
            return True

        self.check_message = 'FAIL - unexpected group detail response'
        return False

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        method = 'GET'
        resource = 'groups'
        if self.check == 'group_get_not_found':
            full_url = '%s%s/%s' % (base_url, resource, 'FAKE_GROUP_SHOUDNT_EXIST')
            r = requests.get(full_url)
            return self.check_group_not_found(r), r

        if self.check == 'group_get_info_empty':
            full_url = '%s%s/%s' % (base_url, resource, self.test_group_one['groupname'])
            r = requests.get(full_url)
            return self.check_group_get(r, []), r

        if self.check == 'group_get_info_populated':
            return
