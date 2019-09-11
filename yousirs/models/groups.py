from yousirs.backend.alchemy import backend as db
try:
    from user import UserModel
except:
    from .user import UserModel
import json

class GroupsModel(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    users = db.relationship('UserModel', secondary="user_groups")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by(cls, kv_dict):
        field = list(kv_dict.keys())[0]
        value = list(kv_dict.values())[0]

        if field == 'name':
            return cls.query.filter_by(name=value).first()
        else:
            return {'lol': 'wut'}

    def set_members(self, users):
        self.users = []
        self.users.extend(users)
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
