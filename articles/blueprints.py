from flask import Blueprint, render_template, request
from flask_security import login_required, current_user
import markdown

from app import db
from articles.forms import ArticlesForm
from models import Article, TaskUser

articles = Blueprint('articles', __name__, template_folder='templates')


@articles.route('/')
def index():
    search = request.args.get('search')
    if search:
        article_list = Article.query.filter(Article.title.contains(search) | Article.text.contains(search)).order_by(
            Article.created.desc()).all()
    else:
        article_list = Article.query.order_by(Article.created.desc()).all()

    return render_template('/articles/index.html', article_list=article_list)


@articles.route('/create', methods=['get', 'post'])
@articles.route('/create/<id>', methods=['get', 'post'])
@login_required
def create_article(id=None):
    form = ArticlesForm()
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text'] + '\n'
        resource = request.form['resources']
        try:
            if id:
                article = Article.query.filter(Article.id == id).first()
                article.title = title
                article.text = text
                article.meta = resource
            else:
                article = Article(title=title, text=text, meta = resource)
                db.session.add(article)
            db.session.commit()
        except:
            print('Ошибка создания статьи')

    if id:
        article = Article.query.filter(Article.id == id).first()
        form.title.data = article.title
        form.text.data = article.text
    return render_template('/articles/create.html', form=form, id=id)


@articles.route('/<id>/tasks', methods=['get', 'post'])
def get_tasks(id):
    article = Article.query.filter(Article.id == id).first()
    if (request.method == 'POST') and current_user.is_authenticated:
        user_id = current_user.id
        for res in request.form:
            task_id = res.split('-')[1]
            task_user = TaskUser.query.filter(TaskUser.user_id == user_id, TaskUser.task_id == task_id).first()
            if request.form[res] == 'True':
                res_bool = True
            else:
                res_bool = False
            if task_user:
                task_user.result = res_bool
            else:
                task_user = TaskUser(user_id=user_id, task_id=task_id, result=res_bool)
                db.session.add(task_user)
        db.session.commit()
    return render_template(f'/articles/tasks.html', article=article)


@articles.route('/<id>')
def get_article(id):
    img_tag_template = '<img alt="image" class="col-md-12" src="{}">'
    article = Article.query.filter(Article.id == id).first()
    text = markdown.markdown(article.text)
    if article.meta != '':
        pictures = article.meta.split(' ')
        textparts = text.split('\n')
        img_index = 0
        for part_index, part in enumerate(textparts):
            if (part.startswith('<p>img')) or (part.startswith('img')):
                textparts[part_index] = img_tag_template.format(pictures[img_index])
                img_index += 1

        text = '\n'.join(textparts)
    return render_template('/articles/article.html', article=article, text=text)
