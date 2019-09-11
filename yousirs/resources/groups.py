from flask_restful import Resource, reqparse
from flask import request
from yousirs.models.groups import GroupsModel
from yousirs.models.user import UserModel

from sqlalchemy import exc

import json

class Groups(Resource):
    # show
    def get(self, groupname = None):
        if groupname:
            lookup_data = {'name': groupname}
            group_data = GroupsModel.find_by(lookup_data)

            if group_data:
                user_list = [user.userid for user in group_data.users]
                return user_list, 200
            return {"message": "group not found"}, 404

        else:
            group_data = GroupsModel.query.all()
            group_resp = {}
            for group in group_data:
                group_members = [user.userid for user in group.users]
                group_resp[group.name] = {"members": group_members}

            if group_resp:
                return group_resp, 200
            else:
                return {"message": "no groups found"}, 200

        return {"message": "group not found"}, 404

    # create
    def post(self):
        group_parse = reqparse.RequestParser()
        group_parse.add_argument('groupname',
                                 type=str,
                                 required=True,
                                 default=None
                                 )
        group_args = group_parse.parse_args()
        lookup_data = {'name': group_args.groupname}
        group_data = GroupsModel.find_by(lookup_data)
        if group_data:
            return {"message": "groupname %s already exists" % group_data.name}, 409

        new_group = GroupsModel(group_args.groupname)
        try:
            new_group.save()
        except exc.IntegrityError as e:
            return {"message": "groupname %s already exists" % group_data.name}, 409
        except:
            return {"message": "error creating group"}, 500

        return {"message": "group created successfully",
                "response": {"groupname": new_group.name}}, 201


    # update
    def put(self, groupname = None):
        if not groupname:
            return {"message": "not authorized for this resource"}, 405

        lookup_data = {"name": groupname}
        group_data = GroupsModel.find_by(lookup_data)
        if not group_data:
            return {"message": "group not found"}, 404

        user_ids = request.json
        if (not user_ids or type(user_ids) != list):
            return {"message": "you must provide a valid JSON formatted list of user IDs"}, 400

        # check all users are valid
        user_records = UserModel.find_users(user_ids)
        found_ids = [user.userid for user in user_records]
        missing_ids = set(user_ids).difference(set(found_ids))
        if missing_ids:
            return {"message": "you have provided at least one incorrect userid",
                    "unprocessable_userids": list(missing_ids)}, 409

        try:
            group_data.set_members(user_records)
            return {"message": "group membership updated"}, 200
        except:
            return {"message": "group membership update failed with an unknown error"}, 500

    def delete(self, groupname = None):
        if not groupname:
            return {"message": "not authorized for this resource"}, 405

        lookup_data = {'name': groupname}
        group_data = GroupsModel.find_by(lookup_data)

        if not group_data:
            return {"message": "group %s not found" % groupname}, 404

        try:
            group_data.delete()
        except:
            return {"message": "error deleting group entry"}, 500

        return '', 204
