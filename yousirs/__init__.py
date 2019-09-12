import os

from flask import Flask
from flask_restful import Api

from yousirs.resources.user import Users
from yousirs.resources.groups import Groups
from yousirs.resources.eggs import Eggs, Thanos

from yousirs.backend.alchemy import backend

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection

app = Flask(__name__)

DB_URL = os.environ.get('DATABASE_URL')
if DB_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
else:
    # assuming local sqlite
    app_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(app_dir, 'backend/data/you_sirs.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_file

    # ensure sqlite is enforcing DB schema
    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

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


api.add_resource(Eggs, '/easter/eggs')
api.add_resource(Thanos, '/easter/eggs/snap')

@app.route("/", methods=["GET"])
def respond_with_repo():
    return {"message": "check out https://github.com/JoelInTheory/random_coding_thangs"}, 426
