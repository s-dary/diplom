from flask import Blueprint, render_template, request
from flask_security import login_required, current_user
import markdown

from app import db
from practices.forms import PracticeForm
from models import Practice

practice = Blueprint('practices', __name__, template_folder='templates')


@practice.route('/')
def index():
    search = request.args.get('search')
    if search:
        practice_list = Practice.query.filter(Practice.title.contains(search) | Practice.text.contains(search)).order_by(
            Practice.created.desc()).all()
    else:
        practice_list = Practice.query.order_by(Practice.created.desc()).all()

    return render_template('/practice/index.html', practice_list=practice_list)


@practice.route('/create', methods=['get', 'post'])
@practice.route('/create/<id>', methods=['get', 'post'])
@login_required
def create_practice(id=None):
    form = PracticeForm()
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text'] + '\n'
        resource = request.form['resources']
        try:
            if id:
                practice = Practice.query.filter(Practice.id == id).first()
                practice.title = title
                practice.text = text
                practice.meta = resource
            else:
                practice = Practice(title=title, text=text, meta = resource)
                db.session.add(practice)
            db.session.commit()
        except:
            print('Ошибка создания')

    if id:
        practice = Practice.query.filter(Practice.id == id).first()
        form.title.data = practice.title
        form.text.data = practice.text
    return render_template('/practices/create.html', form=form, id=id)


@practice.route('/<id>')
def get_practice(id):
    img_tag_template = '<img alt="image" class="col-md-12" src="{}">'
    practice = Practice.query.filter(Practice.id == id).first()
    text = markdown.markdown(practice.text)
    if practice.meta != '':
        pictures = practice.meta.split(' ')
        textparts = text.split('\n')
        img_index = 0
        for part_index, part in enumerate(textparts):
            if (part.startswith('<p>img')) or (part.startswith('img')):
                textparts[part_index] = img_tag_template.format(pictures[img_index])
                img_index += 1

        text = '\n'.join(textparts)
    return render_template('/practices/practice.html', practice=practice, text=text)
