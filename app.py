from flask import Flask, url_for, request, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Users, Article, Practice, Task, TaskUser, Role, Answer


class AdminFun:
    def is_accessible(self):
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class CheckAdmin(AdminFun, ModelView):
    pass


class HomeAdmin(AdminFun, AdminIndexView):
    pass


class TaskUserView(AdminFun, ModelView):
    column_list = ['task', 'user', 'result']


admin = Admin(app, 'На сайт', url='/', index_view=HomeAdmin(name='home'))
session = db.session
users = CheckAdmin(Users, session)
articles = CheckAdmin(Article, session)
practice = CheckAdmin(Practice, session)
tasks = CheckAdmin(Task, session)
answer = CheckAdmin(Answer, session)
result = TaskUserView(TaskUser, session)
admin.add_views(users, articles, practice, tasks, answer, result)

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)




import routes
