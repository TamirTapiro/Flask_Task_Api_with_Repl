from datetime import datetime
from flask import Blueprint, request, session, jsonify
from db_handler import tasks_collection
from pymongo.collection import ReturnDocument
from task.task import Task
from bson import json_util, ObjectId
import json

task_manager_blueprint = Blueprint('task_manager','task_manager_blueprint')

def response(message, statusCode = 200):
    return jsonify({'message': message}), statusCode  

def get_tasks(additional_filters= None):
    results = {'user': session['user']}
    filters = {'$and': [{'owner': session['user']}]}
    if additional_filters is not None:
        for key, value in additional_filters.items():
            filters['$and'].append({key:value})
        print(filters)
    try:
        results['tasks'] = list(tasks_collection.find(filters, {'_id': False}))

        print(results)
        if results is not None:
            return json.dumps(results, default=json_util.default)
        else:
            raise 
    except:
        return response('some error eccured.', 404)

@task_manager_blueprint.before_request
def before_request_callback():
        if not 'user' in session:
            return response('You must login before use this API.', 405)

@task_manager_blueprint.route('/', methods=['GET'])
def get_all_tasks():
    return get_tasks()

@task_manager_blueprint.route('/completed', methods=['GET'])
def get_all_completed_tasks():
    filters = {'completed': True}
    return get_tasks(filters)

@task_manager_blueprint.route('/add', methods=['POST'])
def add_task():
    t = request.get_json()
    print(t)
    if tasks_collection.find_one({'$and': [{'owner': session['user']}, {'name': t['name']}]}) is not None:
        return response('task already exist. if you want to update this task, please try route: /update', 203)
    
    t['owner'] = session['user']
    task = Task(**t)
    print(task)
    tasks_collection.insert(task.__dict__)
    return response(f'added new task - [{task.name}]')

# @task_manager_blueprint.route('/update/<id_or_name>', methods=['PUT'])
# def update_task(id_or_name):
#     if 'name' not in request.get_json().keys():
#         return response('request must have body with a new name', 403)
#     new_name = request.get_json()['name']
#     update_field = {'$set': {'name': new_name, 'last_updated': datetime.now()}}
#     if ObjectId.is_valid(id_or_name):
#         obj_id = ObjectId(id_or_name)

#         t = tasks_collection.find_one_and_update(
#             {'_id': obj_id},
#             update_field,
#             return_document = ReturnDocument.BEFORE
#         )
#     else:
#         t = tasks_collection.find_one_and_update(
#             {'name': id_or_name},
#             update_field,
#             return_document = ReturnDocument.BEFORE
#         )
#     if t is None:
#         return response(f'{id_or_name} is not valid id, nor a task name.', 400)
#     else:
#         task = Task(**t)
#         return response(f'{id_or_name} has been updated from [{task.name}] to [{new_name}].')

@task_manager_blueprint.route('/update/<id_or_name>', methods=['PUT'])
def update_task(id_or_name):
    if 'name' not in request.get_json().keys():
        return response('request must have body with a new name', 403)
    new_name = request.get_json()['name']
    update_field = {'$set': {'name': new_name, 'last_updated': datetime.now()}}
    if ObjectId.is_valid(id_or_name):
        obj_id = ObjectId(id_or_name)
        t = tasks_collection.find_one({'_id': obj_id})
    else:
        t = tasks_collection.find_one({'name': id_or_name})
    if t is None:
        return response(f'{id_or_name} is not valid id, nor a task name.', 400)
    else:
        task = Task(**t)
        if task.completed == True:
            return response(f'task [{id_or_name}] is completed. you cannot update a completed task.')
        else:
            t = tasks_collection.find_one_and_update(
            {'name': id_or_name},
            update_field
        )
            task = Task(**t)
            return response(f'{id_or_name} has been updated from [{task.name}] to [{new_name}].')

@task_manager_blueprint.route('/complete/<id_or_name>', methods=['PUT'])
def complete_task(id_or_name):
    update_field = {'$set': {'completed': True, 'last_updated': datetime.now()}}
    if ObjectId.is_valid(id_or_name):
        obj_id = ObjectId(id_or_name)

        t = tasks_collection.find_one_and_update(
            {'_id': obj_id},
            update_field,
            return_document = ReturnDocument.BEFORE
        )
    else:
        t = tasks_collection.find_one_and_update(
            {'name': id_or_name},
            update_field,
            return_document = ReturnDocument.BEFORE
        )
    if t is None:
        return response(f'{id_or_name} is not valid id, nor a task name.', 400)
    else:
        task = Task(**t)
        if task.completed == True:
            return response(f'{id_or_name} is already completed.', 203)
    return response(f'{id_or_name} has been updated to completed.')

@task_manager_blueprint.route('/undo/<id_or_name>', methods=['PUT'])
def undo_task(id_or_name):
    update_field = {'$set': {'completed': False, 'last_updated': datetime.now()}}
    if ObjectId.is_valid(id_or_name):
        obj_id = ObjectId(id_or_name)
        t = tasks_collection.find_one_and_update(
            {'_id': obj_id},
            update_field,
            return_document = ReturnDocument.BEFORE
        )
    else:
        t = tasks_collection.find_one_and_update(
            {'name': id_or_name},
            update_field,
            return_document = ReturnDocument.BEFORE
        )
    if t is None:
        return response(f'{id_or_name} is not valid id, nor a task name.', 400)
    else:
        task = Task(**t)
        if task.completed == False:
            return response(f'{id_or_name} is already incomplete.', 203)
    return response(f'{id_or_name} has been updated to incomplete.')

@task_manager_blueprint.route('/delete/<id_or_name>', methods=['DELETE'])
def delete_task(id_or_name):
    if ObjectId.is_valid(id_or_name):
        obj_id = ObjectId(id_or_name)
        t = tasks_collection.find_one_and_delete(
            {'_id': obj_id}
        )
        
    else:
        t = tasks_collection.find_one_and_delete(
            {'name': id_or_name},
        )
    print(t)
    if t is None:
        return response(f'{id_or_name} is not valid id, nor a task name.', 400)
    else:
        return response(f'{id_or_name} has been deleted.')