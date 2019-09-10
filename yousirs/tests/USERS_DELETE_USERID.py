"""
DELETE /users/<userid>
    Deletes a user record. Returns 404 if the user doesn't exist

expected:
    204 deleted - user deleted
    404 not found - userid not found
    405 method not allowed - delete to /users, not /users/<id>

"""

import requests

class RunTest:
    def __init__(self, host, port, check):
        self.host = host
        self.port = port
        self.check = check
        self.check_message = None

        self.new_user_three = {'first_name': 'TTTester',
                               'last_name': 'Three',
                               'userid': 'test3'}

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

    def check_delete_user(self, resp):
        if resp.status_code != 204:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - user deleted'
        return True

    def check_user_delete_not_found(self, resp):
        if resp.status_code != 404:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - expected 404 not found'
        return True

    def check_user_delete_no_id(self, resp):
        if resp.status_code != 405:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return false
        self.check_message = 'OK - expected 405 not allowed'
        return True

    def test(self):
        base_url = 'http://%s:%s/' % (self.host, self.port)
        method = 'DELETE'
        resource = 'users'
        full_url = '%s%s' % (base_url, resource)
        if self.check == 'user_delete':
            r = requests.post(full_url, data = self.new_user_three)
            first_check_res = self.check_good_post(r, self.new_user_three)
            if not first_check_res:
                return first_check_res, r.json()
            full_url = '%s%s/%s' % (base_url, resource, self.new_user_three['userid']) 
            r = requests.delete(full_url)
            result = self.check_delete_user(r)
            if result:
                return result, r
            else:
                return result, r
        if self.check == 'user_delete_not_found':
            full_url = '%s%s/%s' % (base_url, resource, self.new_user_three['userid']) 
            r = requests.delete(full_url)
            return self.check_user_delete_not_found(r), r
        if self.check == 'user_delete_no_id':
            full_url = '%s%s' % (base_url, resource)
            r = requests.delete(full_url)
            return self.check_user_delete_no_id(r), r 
