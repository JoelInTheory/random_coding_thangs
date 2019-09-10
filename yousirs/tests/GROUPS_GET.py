"""
GET /groups
    Returns list of groups and their users

expected:
    200 ok - list of groups data (if any)
    200 ok - message of no groups found (if no groups in DB)

NOTE: this isn't in the spec but it's useful for troubleshooting so, here we are

"""

import requests

class RunTest:
    def __init__(self, host, port, empty_list):
        self.host = host
        self.port = port
        self.empty_list = empty_list
        self.check_message = None

        self.expected_empty = {"message": "no groups found"}

    def verify_empty(self, resp):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        if resp.json() == self.expected_empty:
            self.check_message = 'OK - empty group list'
            return True
        self.check_message = 'FAIL - received non-empty or malformed group list'
        return False

    def verify_generic(self, resp):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        try:
            resp_json = resp.json()
        except:
            self.check_message = 'FAIL - could not parse group list to json'
        if resp_json:
            if resp_json == self.expected_empty:
                self.check_message = 'FAIL - empty list when expected populated'
                return False
            for group_name, group_info in resp_json.items():
                if (list(group_info.keys()) == ['members'] and
                    type(group_info['members']) == list):
                    self.check_message = 'OK - generic group list passes'
                    return True
        self.check_message = 'FAIL - unexpected failure on generic group check'
        return False

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        method = 'GET'
        resource = 'groups'
        full_url = '%s%s' % (base_url, resource)
        r = requests.get(full_url)
        if self.empty_list:
            return self.verify_empty(r), r
        else:
            return self.verify_generic(r), r
