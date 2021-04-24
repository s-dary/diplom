from flask import Blueprint, render_template

from models import Task

tasks = Blueprint('tasks', __name__, template_folder='templates')


@tasks.route('/')
def index():
    tasks_list = Task.query.all()
    return render_template('/tasks/index.html', tasks_list=tasks_list)


@tasks.route('/<id>')
def get_task(id):
    task = Task.query.filter(Task.id == id).first()
    return render_template('/tasks/task.html', task=task)
