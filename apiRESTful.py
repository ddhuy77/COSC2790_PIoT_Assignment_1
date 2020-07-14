from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sensehat.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

class SENSEHAT_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recorded_time = db.Column(db.DateTime)
    temp = db.Column(db.Numeric)
    humidity = db.Column(db.Numeric)

    def __init__(self, recorded_time, temp, humidity):
        self.recorded_time = recorded_time
        self.temp = temp
        self.humidity = humidity


# class UserSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ('username', 'email')

class DataSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('recorded_time', 'temp', 'humidity')


# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

data_schema = DataSchema()
datas_schema = DataSchema(many=True)


# endpoint to create new user
# @app.route("/user", methods=["POST"])
# def add_user():
#     username = request.json['username']
#     email = request.json['email']
    
#     new_user = User(username, email)

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify(new_user)

@app.route("/data", methods=["POST"])
def add_data():
    recorded_time = request.json['recorded_time']
    temp = request.json['temp']
    humidity = request.json['humidity']
    
    new_data = SENSEHAT_data(recorded_time, temp, humidity)

    db.session.add(new_data)
    db.session.commit()

    return jsonify(new_data)


# endpoint to show all users
# @app.route("/user", methods=["GET"])
# def get_user():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
#     return jsonify(result.data)

@app.route("/data", methods=["GET"])
def get_data():
    all_datas = SENSEHAT_data.query.all()
    result = datas_schema.dump(all_datas)
    return jsonify(result.data)


# endpoint to get user detail by id
# @app.route("/user/<id>", methods=["GET"])
# def user_detail(id):
#     user = User.query.get(id)
#     return user_schema.jsonify(user)

@app.route("/data/<id>", methods=["GET"])
def data_detail(id):
    data = SENSEHAT_data.query.get(id)
    return data_schema.jsonify(data)


# endpoint to update user
# @app.route("/user/<id>", methods=["PUT"])
# def user_update(id):
#     user = User.query.get(id)
#     username = request.json['username']
#     email = request.json['email']

#     user.email = email
#     user.username = username

#     db.session.commit()
#     return user_schema.jsonify(user)

@app.route("/data/<id>", methods=["PUT"])
def data_update(id):
    data = SENSEHAT_data.query.get(id)
    recorded_time = request.json['recorded_time']
    temp = request.json['temp']
    humidity = request.json['humidity']

    data.recorded_time = recorded_time
    data.temp = temp
    data.humidity = humidity

    db.session.commit()
    return data_schema.jsonify(data)


# endpoint to delete user
# @app.route("/user/<id>", methods=["DELETE"])
# def user_delete(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()

#     return user_schema.jsonify(user)

@app.route("/data/<id>", methods=["DELETE"])
def data_delete(id):
    data = SENSEHAT_data.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return data_schema.jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)