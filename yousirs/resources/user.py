from flask_restful import Resource, reqparse
from models.user import UserModel
from sqlalchemy import exc
import json

class Users(Resource):
    # list
    def get(self, userid = None):
        if not userid:
            user_data = UserModel.get_all()
            if user_data and user_data['users']:
                return user_data, 200
            
            return {"message": "no users found"}, 200

        lookup_data = {'userid': userid}
        user_data = UserModel.find_by(lookup_data)
        
        if not user_data:
            return {"message": "user not found"}, 404            
        return {"userid": user_data.userid,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "groups": [group.name for group in user_data.groups]}

    # create
    def post(self):
        user_parse = reqparse.RequestParser()
        user_parse.add_argument('first_name',
                                  type=str,
                                  required=True,
                                  default=None
                                  )
        user_parse.add_argument('last_name',
                                  type=str,
                                  required=True,
                                  default=None
                                  )
        user_parse.add_argument('userid',
                                type=str,
                                required=True,
                                default=None
                                )
        user_args = user_parse.parse_args()
        lookup_data = {'userid': user_args.userid} 
        user_data = UserModel.find_by(lookup_data)
        if user_data:
            return {"message": "userid '%s' already exists" % user_args.userid}, 409

        try:
            new_user = UserModel(userid = user_args.userid, id = None)
            new_user.first_name = user_args.first_name
            new_user.last_name = user_args.last_name
            new_user.save()
        except:
            return {"message": "error creating new user %s" % user_args.userid}, 500

        return {"message": "user created successfully",
                "response": {"userid": new_user.userid,
                             "first_name": new_user.first_name,
                             "last_name": new_user.last_name}}, 201

    # update
    def put(self, userid = None):
        if not userid:
            return {"message":  'The method is not allowed for the requested URL.'}, 405 

        user_parse = reqparse.RequestParser()
        user_parse.add_argument('first_name',
                                type=str,
                                required=True,
                                default=None
                                )
        user_parse.add_argument('last_name',
                                type=str,
                                required=True,
                                default=None
                                )
        user_parse.add_argument('userid',
                                type=str,
                                required=True,
                                default=None
                                )
        user_args = user_parse.parse_args()
        lookup_data = {'userid': userid} 
        user_data = UserModel.find_by(lookup_data)

        if not user_data:
            return {"message": "user not found"}, 404

        lookup_data = {'userid': user_args.userid}
        new_userid_data = UserModel.find_by(lookup_data)

        if new_userid_data:
            return {"message": "requested new userid already in use"}, 409

        try:
            user_data.userid = user_args.userid
            user_data.first_name = user_args.first_name
            user_data.last_name = user_args.last_name
            user_data.save()
        except exc.IntegrityError as e:
            return {"message": "requested new userid already in use"}, 409
        except:
            return {"message": "error updating user" % userid}, 500

        return {"message": "user updated",
                "response": {"userid": user_data.userid,
                             "first_name": user_data.first_name,
                             "last_name": user_data.last_name}}, 200



    # I MUST BREAK YOU (delete)
    def delete(self, userid = None):
        if not userid:
            return {"message":  'The method is not allowed for the requested URL.'}, 405 

        lookup_data = {"userid": userid}
        user_data = UserModel.find_by(lookup_data)

        if not user_data:
            return {"message": "user not found"}, 404

        try:
            user_data.delete()
        except:
            return {"message": "error deleting user"}, 500

        return '', 204  
