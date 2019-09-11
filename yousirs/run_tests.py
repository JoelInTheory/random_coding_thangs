import tests
import argparse
import requests
from collections import OrderedDict
import json
try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs


import config
HOST = config.TEST_HOST
PORT = config.TEST_PORT


def parse_the_things():
    test_args = argparse.ArgumentParser()
    test_args.add_argument('--verbose',
                           action='store_true',
                           default=False,
                           help="GET on /users and /groups between tests")
    test_args.add_argument('--slow',
                           action='store_true',
                           help="wait for user input between each test")
    # so you can be all judgey
    return test_args.parse_args()


# TESTS
suite = OrderedDict()

suite['user_list_empty'] = tests.USERS_GET.RunTest(HOST, PORT, True)
suite['group_list_empty'] = tests.GROUPS_GET.RunTest(HOST, PORT, True)

suite['user_post_malformed'] = tests.USERS_POST.RunTest(HOST, PORT, 'malformed_new_user_post')
suite['user_post'] = tests.USERS_POST.RunTest(HOST, PORT, 'good_new_user_post')
suite['user_post_duplicate'] = tests.USERS_POST.RunTest(HOST, PORT, 'dupe_new_user_post')
suite['user_get_not_found'] = tests.USERS_GET_USERID.RunTest(HOST, PORT, 'user_get_not_found')
suite['user_get_ok'] = tests.USERS_GET_USERID.RunTest(HOST, PORT, 'user_get_info')
suite['user_delete_ok'] = tests.USERS_DELETE_USERID.RunTest(HOST, PORT, 'user_delete')
suite['user_delete_not_found'] = tests.USERS_DELETE_USERID.RunTest(HOST, PORT, 'user_delete_not_found')
suite['user_delete_no_id'] = tests.USERS_DELETE_USERID.RunTest(HOST, PORT, 'user_delete_no_id')
suite['user_update'] = tests.USERS_PUT_USERID.RunTest(HOST, PORT, 'user_update')
suite['user_update_userid_conflict'] = tests.USERS_PUT_USERID.RunTest(HOST, PORT, 'user_update_id_conflict')
suite['user_update_user_not_found'] = tests.USERS_PUT_USERID.RunTest(HOST, PORT, 'user_update_not_found')
suite['user_update_no_id'] = tests.USERS_PUT_USERID.RunTest(HOST, PORT, 'user_update_no_id')

suite['group_post'] = tests.GROUPS_POST.RunTest(HOST, PORT, 'good_new_group_post')
suite['group_post_malformed'] = tests.GROUPS_POST.RunTest(HOST, PORT, 'malformed_new_group_post')
suite['group_post_duplicate'] = tests.GROUPS_POST.RunTest(HOST, PORT, 'dupe_new_group_post')
suite['group_get_not_found'] = tests.GROUPS_GET_GROUPNAME.RunTest(HOST, PORT, 'group_get_not_found')
suite['group_get_info_empty'] = tests.GROUPS_GET_GROUPNAME.RunTest(HOST, PORT, 'group_get_info_empty')
suite['group_delete_ok'] = tests.GROUPS_DELETE_GROUPNAME.RunTest(HOST, PORT, 'group_delete')
suite['group_delete_not_found'] = tests.GROUPS_DELETE_GROUPNAME.RunTest(HOST, PORT, 'group_delete_not_found')
suite['group_delete_no_id'] = tests.GROUPS_DELETE_GROUPNAME.RunTest(HOST, PORT, 'group_delete_no_id')

suite['group_put_setup_groups'] = tests.GROUPS_PUT_GROUPNAME.RunTest(HOST, PORT, 'setup_groups')
suite['group_put_setup_users'] = tests.GROUPS_PUT_GROUPNAME.RunTest(HOST, PORT, 'setup_users')
suite['group_put_bad_groupname'] = tests.GROUPS_PUT_GROUPNAME.RunTest(HOST, PORT, 'put_groups_404')
suite['group_put_bad_user_in_list'] = tests.GROUPS_PUT_GROUPNAME.RunTest(HOST, PORT, 'put_bad_user_in_list')
suite['group_put_add_users_to_groups'] = tests.GROUPS_PUT_GROUPNAME.RunTest(HOST, PORT, 'put_all_the_groups')

suite['populated_group_list'] = tests.GROUPS_GET.RunTest(HOST, PORT, False)
suite['populated_user_list'] = tests.USERS_GET.RunTest(HOST, PORT, False)

sep = '-' * 100
if __name__ == '__main__':
    test_args = parse_the_things()
    for test_name, test_obj in suite.items():
        print(sep)
        result, response = test_obj.test()
        print('%s: %s' % (test_name.ljust(35), test_obj.check_message))
        if not result:
            print("ERROR RESPONSE:")
            print(json.dumps(response.json(), indent=4))
        if test_args.verbose:
            if type(response) == requests.models.Response:
                try:
                    data = parse_qs(response.request.body)
                except ValueError:
                    data = {}
                print("request: %s - %s - %s - %s" % (response.request.method,
                                                      response.status_code,
                                                      response.request.url,
                                                      data))
            for resource in ['users', 'groups']:
                print(resource.upper())
                r = requests.get('%s:%s/%s' % (HOST, PORT, resource))
                print(json.dumps(r.json(), indent=4))
        if test_args.slow:
            input("Press enter for next test")
