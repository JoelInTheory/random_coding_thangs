"""
GET /users
    Returns list of users and their groups

expected:
    200 ok - list of user data (if any)
    200 ok - message of no users found (if no users in DB)

NOTE: this isn't in the spec but it's useful for troubleshooting so, here we are

"""

import requests

class RunTest:
    def __init__(self, host, port, empty_list):
        self.host = host
        self.port = port
        self.empty_list = empty_list
        self.check_message = None

        self.expected_empty = {"message": "no users found"}
        self.user_keys = ['first_name',
                          'last_name',
                          'userid',
                          'groups']

    def verify_empty(self, resp):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        if resp.json() == self.expected_empty:
            self.check_message = 'OK - empty user list'
            return True
        self.check_message = 'FAIL - received non-empty or malformed user list'
        return False

    def verify_generic(self,resp):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        if not resp.json().keys() == ["users"]:
            self.check_message = 'FAIL - top level response wrong'
            return False
        users = resp.json().get('users')
        if not type(users) == list:
            self.check_message = 'FAIL - users is not a list'
            return False
        for user in users:
            if not user.keys() == self.user_keys:
                self.check_message = 'FAIL - a user response is unexpected'
                return False
            if type(user.get('groups')) != list:
                self.check_message = 'FAIL - groups for user is not a list'
                return False
        self.check_message = 'OK - generic user list response passes'
        return True

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        method = 'GET'
        resource = 'users'
        full_url = '%s%s' % (base_url, resource)
        print(full_url)
        r = requests.get(full_url)
        if self.empty_list:
            return self.verify_empty(r), r
        else:
            return self.verify_generic(r), r
