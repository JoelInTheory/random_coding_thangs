"""
GET /users/<userid>
    Returns the matching user record or 404 if none exist

expected:
    200 got em
    404 not found - userid not found

"""

import requests


class RunTest:
    def __init__(self, host, port, check):
        self.host = host
        self.port = port
        self.check = check
        self.check_message = None

        self.new_user_one = {'first_name': 'Tester',
                             'last_name': 'One',
                             'userid': 'test1'}

    def check_user_not_found(self, resp):
        if resp.status_code != 404:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - expected 404 not found'
        return True

    def check_user_get(self, resp, user):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        expected_response = {"first_name": user['first_name'],
                             "last_name": user['last_name'],
                             "userid": user['userid'],
                             "groups": []
                             }
        # FIXME: just check if groups is list for now
        resp_json = resp.json()
        if type(resp_json.get('groups')) == list:
            resp_json['groups'] = []
            if resp_json == expected_response:
                self.check_message = 'OK - user matches'
                return True
            else:
                self.check_message = 'FAIL - user get failure'
                return False
        else:
            self.check_message = 'FAIL - groups is not a list for user'
            return False

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        # method = 'GET'
        resource = 'users'
        if self.check == 'user_get_not_found':
            full_url = '%s%s/%s' % (base_url, resource, 'FAKE_USER_SHOUDNT_EXIST')
            r = requests.get(full_url)
            return self.check_user_not_found(r), r

        if self.check == 'user_get_info':
            full_url = '%s%s/%s' % (base_url, resource, self.new_user_one['userid'])
            r = requests.get(full_url)
            return self.check_user_get(r, self.new_user_one), r
