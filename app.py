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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, username, password, email):
        self.password = password
        self.username = username
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        feilds = ('id', 'username', 'password', 'email')

user_schema = UserSchema()
multi_user_schema = UserSchema(many=True)

@app.route('/user/signup', methods=["POST"])
def add_user():
    if request.content_type != 'application/json':
        return jsonify("data must be json")

    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    email = post_data.get('email')

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username, password, email, pw_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))

@app.route('/user/verify', methods=["POST"])
def verification():
    if request.content_type != 'application/json':
        return jsonify('send it as json')
    
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify('user couldnt be verified')

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("user couldnt be verified")

    return jsonify('user was verified')


@app.route('/users/get', methods=["GET"])
def get_all_users():
    users = db.session.query(User).all()
    return jsonify(multi_user_schema.dump(users))

# @app.route('/user/update/<id>', methods=["PUT"])
# def update_user(id):



if __name__ == '__main__':
    app.run(debug=True)