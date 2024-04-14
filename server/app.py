#!/usr/bin/env python3
from flask import Flask, request, session, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
api = Api(app)

# Configure your database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)

# Create the database tables (this is optional if you're using SQLite and the database file doesn't exist yet)
with app.app_context():
    db.create_all()
    
class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Simulated password hashing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create a new User object
        new_user = User(username=username, hashed_password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'username': new_user.username
        })

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return jsonify({
                'id': user.id,
                'username': user.username
            })
        else:
            return '', 204

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Simulated password hashing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if user exists and password matches
        user = User.query.filter_by(username=username, hashed_password=hashed_password).first()
        if user:
            # Simulated session storage
            session['user_id'] = user.id
            return jsonify({
                'id': user.id,
                'username': user.username
            })

        return 'Invalid username or password', 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return '', 200

api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
