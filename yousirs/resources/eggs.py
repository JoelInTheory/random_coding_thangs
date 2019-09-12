from flask_restful import Resource, reqparse
from flask import request

from yousirs.models.groups import GroupsModel
from yousirs.models.user import UserModel
from yousirs.models.user_groups import UserGroupModel

from yousirs.backend.alchemy import backend as db

from sqlalchemy import exc


class Eggs(Resource):
    # show
    def get(self):
        return {"message": "get outta here!"}, 450, {'X-Sup': 'Yo'}

class Thanos(Resource):
    def patch(self):
        try:
            for mod in [UserGroupModel, UserModel, GroupsModel]:
                try:
                    mod.__table__.drop(db.engine)
                except exc.OperationalError as e:
                    continue
            db.create_all()
            return {"message": "I finally rest and watch the sun rise on a grateful universe."}, 418
        except ValueError: # noqa
            return {"message": "nope"}, 500
