import os

from flask import Flask
from flask_restful import Api

from yousirs.resources.user import Users
from yousirs.resources.groups import Groups
from yousirs.backend.alchemy import backend

from sqlalchemy import event
from sqlalchemy.engine import Engine

app = Flask(__name__)
DB_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

backend.init_app(app)

api = Api(app)

# instantiate db
@app.before_first_request
def create_tables():
    backend.create_all()


# ROUTES
api.add_resource(Users, '/users',
                        '/users/',
                        '/users/<string:userid>')

api.add_resource(Groups, '/groups',
                         '/groups/',
                         '/groups/<string:groupname>')
