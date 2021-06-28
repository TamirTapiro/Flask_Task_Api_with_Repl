import typer
import requests, pickle
import os
import json
from tabulate import tabulate 



app = typer.Typer()
my_server = 'http://localhost:5000/api'

my_session = requests.Session()
try:
    with open('cookie', 'rb') as f:
        my_session.cookies.update(pickle.load(f))
except:
    print('No cookie')

@app.command()
def login(email, password):
    body = {'email': email, 'password': password}
    response = my_session.post(my_server + '/user/login', json=body)
    with open('cookie', 'wb') as f:
        pickle.dump(my_session.cookies, f)
    print(response.__dict__)
    print('login')

@app.command()
def logout():
    response = requests.post(my_server + '/user/logout')
    print(response.__dict__)
    print('logout')

@app.command('list-tasks')
def list_task(completed: bool = False):
    if completed:
        response = my_session.get(my_server + '/tasks/completed')
    else:
        response = my_session.get(my_server + '/tasks')
    # print(response.__dict__)
    res = json.loads(response.content)
    print(tabulate([[item['name'], '+' if item['completed'] else '-'] for item in res['tasks']], headers=['Name', 'COMPLETED']))
    # print(res)

@app.command('add-task')
def add_task(task_name):
    body = {'name': task_name}
    response = my_session.post(my_server + '/tasks/add', json=body)
    res = json.loads(response.content)['message']
    print(res)

@app.command('update-task')
def update_task(task_name, new_task_name):
    body = {'name': new_task_name}
    response = my_session.put(my_server + f'/tasks/update/{task_name}', json=body)
    res = json.loads(response.content)['message']
    print(res)

@app.command('complete-task')
def complete_task(task_name):
    response = my_session.put(my_server + f'/tasks/complete/{task_name}')
    res = json.loads(response.content)['message']
    print(res)

@app.command('undo-task')
def complete_task(task_name):
    response = my_session.put(my_server + f'/tasks/undo/{task_name}')
    res = json.loads(response.content)['message']
    print(res)

@app.command('delete-task')
def delete_task(task_name):
    response = my_session.delete(my_server + f'/tasks/delete/{task_name}')
    res = json.loads(response.content)['message']
    print(res)

if __name__ == '__main__':
    app()