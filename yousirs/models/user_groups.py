from backend.alchemy import backend as db
import json

class UserGroupModel(db.Model):
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    users_row_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    groups_row_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


    users = db.relationship('UserModel',
                            backref=db.backref("user_groups", 
                                               cascade="all, delete-orphan"))
    groups = db.relationship('GroupsModel',
                             backref=db.backref("user_groups", 
                                                cascade="all, delete-orphan"))

    def __init__(self, name = None):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
