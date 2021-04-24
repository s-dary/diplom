from datetime import datetime

from flask_security import UserMixin, RoleMixin

from app import db


class TaskUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', backref=db.backref('task_user'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref=db.backref('task_user'))
    result = db.Column(db.Boolean)



role_user = db.Table('role_user',
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=role_user, backref=db.backref('users'))

    def __repr__(self):
        return f'<User : {self.email} ({self.roles})>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Role : {self.name}>'


article_task = db.Table('article_task',
                        db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                        db.Column('task_id', db.Integer, db.ForeignKey('task.id')))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    meta = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.today())
    tasks = db.relationship('Task', secondary=article_task, backref=db.backref('articles'))

    def __repr__(self):
        return f'<Article : {self.title}>'
		
class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    meta = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return f'<Practice : {self.title}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    comment = db.Column(db.Text)
    answer = db.relationship('Answer', backref='task')

    def __repr__(self):
        return f'<Task : {self.task} ({self.answer})>'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100))
    right = db.Column(db.Boolean)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return f'<Answer : {self.answer})>'
