import getpass
import sys

import click

from app import app, db, user_datastore
from articles.blueprints import articles
from practices.blueprints import practice
from tasks.blueprints import tasks



@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('This is a flask web service. ')
        click.echo('You can invoke "--help" for more information about usage. ')


@cli.command()
def create_super_user():
    username = input('Email address:')
    while username == '':
        print('Username is required!')
        username = input('Email address:')
    password = getpass.getpass('Password:')
    while password == '':
        print('Password is required!')
        password = getpass.getpass('Password:')
    password_again = getpass.getpass('Password again:')

    if password == password_again:
        user_object = user_datastore.create_user(email=username, password=password)
        role_object = user_datastore.create_role(name='Admin')
        user_datastore.add_role_to_user(user=user_object, role=role_object)
        db.session.commit()
        click.echo('ok')
    else:
        sys.exit('failed to create super user! Try again!')


@cli.command()
def start():
    app.register_blueprint(articles, url_prefix='/articles')
    app.register_blueprint(practice, url_prefix='/practice')
    app.register_blueprint(tasks, url_prefix='/tasks')
    app.run()



if __name__ == '__main__':
    cli()
