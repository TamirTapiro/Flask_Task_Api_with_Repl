from flask import Flask, session, request
from task.task_manager import task_manager_blueprint
from user.user_manager import user_manager_blueprint
from task.task import Task
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "TheMostSecretKeyInTheWrold"
app.permanent_session_lifetime = timedelta(minutes=120)
app.register_blueprint(task_manager_blueprint, url_prefix="/api/tasks")
app.register_blueprint(user_manager_blueprint, url_prefix="/api/user")

@app.errorhandler(404)
def request_not_found(e):
    return {'message': f'there is no such route {request.path}'}, 404

if __name__ == '__main__':
    app.run(debug=True)