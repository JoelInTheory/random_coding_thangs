#!/usr/bin/env python2
"""
MIT License

Copyright (c) 2019 Joel Preas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import os

from flask import Flask
from flask_restful import Api

from resources.user import Users
from resources.groups import Groups

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection

app = Flask(__name__)
app_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(app_dir, 'backend/data/you_sirs.db') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_file
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

api = Api(app)

# instantiate db
@app.before_first_request
def create_tables():
    backend.create_all()

# ensure sqlite is enforcing DB schema
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# ROUTES
api.add_resource(Users, '/users',
                        '/users/',
                        '/users/<string:userid>')

api.add_resource(Groups, '/groups',
                         '/groups/',
                         '/groups/<string:groupname>')


if __name__ == '__main__':
    from backend.alchemy import backend
    backend.init_app(app)
    app.run(debug=True)
