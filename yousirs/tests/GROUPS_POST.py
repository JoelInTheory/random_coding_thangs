"""
POST /groups
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code. The body should contain
    a `name` parameter

expected:
    201 created - group created
    409 conflict - groupname already in use
    400 bad request - missing params (probably!)


"""

import requests

class RunTest:
    def __init__(self, host, port, check):
        self.host = host
        self.port = port
        self.check = check
        self.check_message = None

        self.good_post_template = {"message": "group created successfully", 
                                   "response": {}
                                  }
        self.test_group_one = {"groupname": "test_group_one"}
        self.test_group_two = {"groupname": "test_group_two"}
        self.bad_group_data = {"bad_key_is": "bad"}

    def check_400(self, resp):
        if resp.status_code == 400:
            self.check_message = 'OK - expected 400 received'
            return True
        self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        return False

    def check_good_post(self, resp, group):
        if resp.status_code != 201:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        try:
            resp_json = resp.json()
        except:
            self.check_message = 'FAIL - could not parse response to json'
            return False
        expected_response = self.good_post_template
        expected_response['response'] = group
        if expected_response == resp_json:
            self.check_message = 'OK - group create successful'
            return True

        self.check_message = 'FAIL - unexpected group post response'
        return False

    def check_dupe_post(self, resp):
        if resp.status_code == 409:
            self.check_message = 'OK - expected 409 received'
            return True
        self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        return False

    def test(self):
        base_url = 'http://%s:%s/' % (self.host, self.port)
        method = 'POST'
        resource = 'groups'
        full_url = '%s%s' % (base_url, resource)
        if self.check == 'malformed_new_group_post':
            r = requests.post(full_url, data = self.bad_group_data)
            return self.check_400(r), r
        if self.check == 'good_new_group_post':
            r = requests.post(full_url, data = self.test_group_one)
            return self.check_good_post(r, self.test_group_one), r
        if self.check == 'dupe_new_group_post':
            r = requests.post(full_url, data = self.test_group_two)
            first_check_res = self.check_good_post(r, self.test_group_two)
            if not first_check_res:
                return first_check_res, r
            r = requests.post(full_url, data = self.test_group_two)
            return self.check_dupe_post(r), r
