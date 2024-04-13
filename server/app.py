#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Login(Resource):
    def post(self):
        try:
            print("Inside Login resource")
            data = request.get_json()
            username = data.get('username')
            print("Username:", username)

            user = User.query.filter_by(username=username).first()
            print("User:", user)

            if user:
                session['user_id'] = user.id
                print("User ID in session:", session['user_id'])
                return jsonify(user.serialize()), 200
            else:
                return {'message': 'User not found'}, 404
        except Exception as e:
            print("Exception:", e)
            return {'message': str(e)}, 500
        
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        try:
            print("Inside CheckSession resource")
            if 'user_id' in session:
                user_id = session['user_id']
                print("User ID in session:", user_id)
                user = User.query.get(user_id)
                print("User:", user)

                if user:
                    return jsonify(user.serialize()), 200
                else:
                    return {}, 401
            else:
                return {}, 401
        except Exception as e:
            print("Exception:", e)
            return {'message': str(e)}, 500


api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
