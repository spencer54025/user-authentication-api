from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    username = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.password = password
        self.username = username

class UserSchema(ma.Schema):
    class Meta:
        feilds = ('username', 'password')

user_schema = UserSchema()



if __name__ == '__main__':
    app.run(debug=True)