"""
POST /users
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code

expected:
    201 created - user created
    409 conflict - userid already in use
    400 bad request - missing params (probably!)


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
        self.new_user_two = {'first_name': 'TTester',
                             'last_name': 'Two',
                             'userid': 'test2'}
        self.bad_user_data = {'first_name': 'fouroh',
                              'userid': 'fourohnine'}
    def check_400(self, resp):
        if resp.status_code == 400:
            self.check_message = 'OK - expected 400 received'
            return True
        self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        return False

    def check_good_post(self, resp, user):
        if resp.status_code != 201:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        expected_response = {"message": "user created successfully", 
                             "response": {"first_name": user['first_name'],
                                          "last_name": user['last_name'],
                                          "userid": user['userid']}
                            }
        if resp.json() != expected_response:
            self.check_message = 'FAIL - unexpected post create response'
            return False
        self.check_message = 'OK - user create successful'
        return True

    def check_dupe_post(self, resp):
        if resp.status_code == 409:
            self.check_message = 'OK - expected 409 received'
            return True
        self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        return False

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        method = 'POST'
        resource = 'users'
        full_url = '%s%s' % (base_url, resource)
        if self.check == 'malformed_new_user_post':
            r = requests.post(full_url, data = self.bad_user_data)
            return self.check_400(r), r
        if self.check == 'good_new_user_post':
            r = requests.post(full_url, data = self.new_user_one)
            return self.check_good_post(r, self.new_user_one), r
        if self.check == 'dupe_new_user_post':
            r = requests.post(full_url, data = self.new_user_two)
            first_check_res = self.check_good_post(r, self.new_user_two)
            if not first_check_res:
                return first_check_res, r
            r = requests.post(full_url, data = self.new_user_two)
            return self.check_dupe_post(r), r
