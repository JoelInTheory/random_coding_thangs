"""
DELETE /groups/<group name>
    Deletes a group.

expected:
    204 deleted - group deleted
    404 not found - groupname not found
    405 method not allowed - delete to /groups, not /groups/<id>

"""

import requests

class RunTest:
    def __init__(self, host, port, check):
        self.host = host
        self.port = port
        self.check = check
        self.check_message = None

        self.test_group_three = {"groupname": "test_group_three"}

    def check_delete_group(self, resp):
        if resp.status_code != 204:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - group deleted'
        return True

    def check_group_delete_not_found(self, resp):
        if resp.status_code != 404:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return False
        self.check_message = 'OK - expected 404 not found'
        return True

    def check_group_delete_no_id(self, resp):
        if resp.status_code != 405:
            self.check_message = 'FAIL - unexpected status code (%s)' % resp.status_code
            return false
        self.check_message = 'OK - expected 405 not allowed'
        return True

    def test(self):
        base_url = 'http://%s:%s/' % (self.host, self.port)
        method = 'DELETE'
        resource = 'groups'
        full_url = '%s%s' % (base_url, resource)
        if self.check == 'group_delete':
            r = requests.post(full_url, data = self.test_group_three)
            full_url = '%s%s/%s' % (base_url, resource, self.test_group_three['groupname']) 
            r = requests.delete(full_url)
            result = self.check_delete_group(r)
            if result:
                return result, r
            else:
                return result, r
        if self.check == 'group_delete_not_found':
            full_url = '%s%s/%s' % (base_url, resource, self.test_group_three['groupname'])
            r = requests.delete(full_url)
            return self.check_group_delete_not_found(r), r
        if self.check == 'group_delete_no_id':
            full_url = '%s%s' % (base_url, resource)
            r = requests.delete(full_url)
            return self.check_group_delete_no_id(r), r
