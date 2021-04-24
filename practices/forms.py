from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField


class PracticeForm(FlaskForm):
    title = StringField('Название')
    text = TextAreaField('Текст')
