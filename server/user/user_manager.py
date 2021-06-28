from flask import Blueprint, request, jsonify, session
import pymongo
from bson.json_util import dumps
from db_handler import users_collection
from dataclasses import FrozenInstanceError
import json
from user.user import User
user_manager_blueprint = Blueprint('user_manager','user_manager_blueprint')



def response(message, statusCode):
    return jsonify({'message': message}), statusCode    

@user_manager_blueprint.route('/login', methods=['POST'])
def login():
    cred = request.get_json()
    try:
        user_json = users_collection.find_one({'$and': [{'email': cred['email']}, {'password': cred['password']}]})
        user = User(**user_json)

        if user is None:
            return response('email or password are incorect', 404)
        else:
            if 'user' in session:
                return response(f'{session["user"]} already logged in', 203)
            else:
                session['user'] = user.email
                return response(f'{user.email} is logged in.', 200)
    except:
        return response('Oops! somthing went wrong.', 404)

@user_manager_blueprint.route('/logout', methods=['POST'])
def logout():
    if 'user' not in session:
        return response('there is no logged in user', 404)
    else:
        user = session['user']
        session.pop('user', None)
        return response(f'{user} logged out succesfuly', 200)

@user_manager_blueprint.route('/register', methods=['POST'])
def register():
    cred = request.get_json()
    
    try:
        user = User(**cred)
        db_result =  users_collection.find_one({'email': user.email})
        if db_result is None:
            users_collection.insert_one(user.__dict__)
            return response(f'{user.email} has been registered succefully', 200) 
        else:
            return response(f'user {user.email} already exists in the system', 409)

    except TypeError as typeErr:
        return response(str(typeErr).replace("__init__()", ""), 400)
    except FrozenInstanceError as instErr:
        return response(str(instErr).replace("__init__()", ""), 400)
    