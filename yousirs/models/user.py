from backend.alchemy import backend as db
import json

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    groups = db.relationship('GroupsModel', secondary="user_groups")

    def __init__(self, userid, id = None):
        self.userid = userid
        self.id = id

    @classmethod
    def find_by(cls, kv_dict):
        field = kv_dict.keys()[0]
        value = kv_dict.values()[0]
       
        # FIXME: fix these placeholder  filter bys
        if field == 'userid':
            return cls.query.filter_by(userid=value).first()
        elif field == 'first_name':
            return cls.query.filter_by(first_name=value).all()
        elif field == 'last_name':
            return cls.query.filter_by(last_name=value).all()
        elif field == 'full_name':
            return cls.query.filter_by(last_name=value, first_name=value).all()
        else:
            return {'lol': 'wut'}

    @classmethod
    def find_users(cls, users_list):
        users = cls.query.filter(cls.userid.in_(users_list)).all()
        return users

    @classmethod
    def get_all(cls):
        user_list = []
        for user in cls.query.all():
            user_dict = {'userid': user.userid,
                         'first_name': user.first_name,
                         'last_name': user.last_name}
            user_groups = [group.name for group in user.groups]
            user_dict['groups'] = user_groups
            user_list.append(user_dict)
        return {'users': user_list}

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
