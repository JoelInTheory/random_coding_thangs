"""
PUT /users/<userid>
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.

expected:
    200 updated (with response) - user updated
    404 not found - userid not found
    405 method not allowed - put to /users, not /users/<id>
    409 conflict - requested new userid already in use

"""

import requests

class RunTest:
    def __init__(self, host, port, check):
        self.host = host
        self.port = port
        self.check = check
        self.check_message = None
        
        self.new_user_four = {'first_name': 'TTTTester',
                               'last_name': 'Four',
                               'userid': 'test4'}
        self.updated_user = {}
        for user_key, user_value in self.new_user_four.items():
            self.updated_user[user_key] = 'updated_%s' % user_value

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

    def check_good_put(self, resp, user):
        if resp.status_code != 200:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False

        expected_response = {"message": "user updated", 
                             "response": {"first_name": user['first_name'], 
                                          "last_name": user['last_name'], 
                                          "userid": user['userid']
                                        }
                            }
        if resp.json() == expected_response:
            self.check_message = 'OK - put succeeded'
            return True
        self.check_message = 'FAIL - put failed'
        return False

    def check_user_put_not_found(self, resp):
        if resp.status_code != 404:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - expected 404 not found'
        return True

    def check_user_put_no_id(self, resp):
        if resp.status_code != 405:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return false
        self.check_message = 'OK - expected 405 not allowed'
        return True

    def check_user_id_conflict(self, resp):
        if resp.status_code != 409:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - expected 409 conflict'
        return True

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        method = 'PUT'
        resource = 'users'
        full_url = '%s%s' % (base_url, resource)
        if self.check == 'user_update':
            r = requests.post(full_url, data = self.new_user_four)
            first_check_res = self.check_good_post(r, self.new_user_four)
            if not first_check_res:
                return first_check_res, r
            full_url = '%s%s/%s' % (base_url, resource, self.new_user_four['userid']) 
            r = requests.put(full_url, data = self.updated_user)
            return self.check_good_put(r, self.updated_user), r

        if self.check == 'user_update_id_conflict':
            full_url = '%s%s/%s' % (base_url, resource, self.updated_user['userid'])
            r = requests.put(full_url, data = self.updated_user)
            return self.check_user_id_conflict(r), r

        if self.check == 'user_update_not_found':
            full_url = '%s%s/%s' % (base_url, resource, 'FAKE_USERNAME_SHOULDNT_EXIST') 
            r = requests.put(full_url, data = self.updated_user)
            return self.check_user_put_not_found(r), r

        if self.check == 'user_update_no_id':
            full_url = '%s%s' % (base_url, resource)
            r = requests.put(full_url, self.updated_user)
            return self.check_user_put_no_id(r), r
