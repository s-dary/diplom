from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField


class ArticlesForm(FlaskForm):
    title = StringField('Название')
    text = TextAreaField('Текст')
