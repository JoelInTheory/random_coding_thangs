"""
PUT /groups/<group name>
    Updates the membership list for the group. The body of the request should
    be a JSON list describing the group's members.

expected:
    200 created - group populated
    400 bad request - missing params (probably!)
    409 conflict - you made a PUT with at least one
                   user that doesn't exist
                   great job


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
        self.test_groups = {'good': [{'first_name': 'the',
                                      'last_name': 'good',
                                      'userid': 'blondie'}],
                            'bad': [{'first_name': 'the',
                                     'last_name': 'bad',
                                     'userid': 'angeleyes'}],
                            'ugly': [{'first_name': 'the',
                                      'last_name': 'bad',
                                      'userid': 'tuco'},
                                     {'first_name': 'the',
                                      'last_name': 'bad',
                                      'userid': 'joel'}]}

    def setup_test_groups(self):
        base_url = '%s:%s/groups' % (self.host, self.port)
        for group in self.test_groups.keys():
            group_url = '%s/%s' % (base_url, group)
            r = requests.delete(group_url)
            if r.status_code not in [404, 204]:
                return False
            data = {'groupname': group}
            r = requests.post(base_url, data=data)
            if r.status_code != 201:
                return False
            r = requests.get(group_url)
            if r.status_code != 200 or r.json() != []:
                return False
        return True

    def setup_test_users(self):
        base_url = '%s:%s/users' % (self.host, self.port)
        for group_users in self.test_groups.values():
            for user in group_users:
                user_url = '%s/%s' % (base_url, user['userid'])
                r = requests.delete(user_url)
                if r.status_code not in [404, 204]:
                    return False
                r = requests.post(base_url, data=user)
                if r.status_code != 201:
                    return False
        return True

    def check_400(self, resp):
        if resp.status_code == 400:
            self.check_message = 'OK - expected 400 received'
            return True
        self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        return False

    def check_404(self, resp):
        if resp.status_code != 404:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        self.check_message = 'OK - got expected 404'
        return True

    def check_bad_users_in_list(self, resp):
        if resp.status_code != 409:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
        self.check_message = 'OK - expected 409 with message: %s' % resp.json()['unprocessable_userids']
        return True

    def test(self):
        base_url = '%s:%s/' % (self.host, self.port)
        # method = 'PUT'
        resource = 'groups'
        full_url = '%s%s' % (base_url, resource)

        if self.check == 'setup_groups':
            setup_res = self.setup_test_groups()
            if setup_res:
                self.check_message = 'OK - groups for put tests recreated'
                return True, {}
            self.check_message = 'FAIL - groups not setup correctly for put tests'
            return False, {}

        if self.check == 'setup_users':
            setup_res = self.setup_test_users()
            if setup_res:
                self.check_message = 'OK - users for put tests recreated'
                return True, {}
            self.check_message = 'FAIL - users not setup correctly for put tests'
            return False, {}

        if self.check == 'put_groups_404':
            data = list(self.test_groups.keys())
            r = requests.put('%s/%s' % (full_url, 'FAKE_GROUP'), json=data)
            return self.check_404(r), r.json()

        if self.check == 'put_bad_user_in_list':
            incorrect_users = ['FAKE_USER1_NO', 'FAKE_USER2_NO']
            group = 'ugly'
            ugly_users = [user['userid'] for user in self.test_groups['ugly']]
            data = ugly_users + incorrect_users
            r = requests.put('%s/%s' % (full_url, group), json=data)
            return self.check_bad_users_in_list(r), r.json()

        if self.check == 'put_all_the_groups':
            for group, group_users in self.test_groups.items():
                data = [user['userid'] for user in group_users]
                r = requests.put('%s/%s' % (full_url, group), json=data)
                if r.status_code != 200:
                    self.check_message = 'FAIL - unexpected status code (%s)' % r.status_code
                    return False, r
                r = requests.get('%s/%s' % (full_url, group))
                if sorted(r.json()) != sorted(data):
                    self.check_message = 'FAIL - group check %s does not match expected' % group
                    return False, r
            self.check_message = 'OK - all groups appear to match expected'
            return True, r
