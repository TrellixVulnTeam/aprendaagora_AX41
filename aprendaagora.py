import os
import click


from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from flask_migrate import Migrate, upgrade
from app import criar_app, db  #, socketio
from app.modelos import Permissao, Role, Usuario, Publicacao, Tag

app = criar_app(os.getenv('FLASK_CONFIG') or 'padrao')

migrate = Migrate(app, db)


# Flask Shell
@app.shell_context_processor
def make_shell_context():

    return dict(
        db=db,
        Permissao=Permissao,
        Role=Role,
        Usuario=Usuario,
        Publicacao=Publicacao,
        Tag=Tag
    )


# Command line interface
@app.cli.command()
@click.argument('testes_nomes', nargs=-1)
def teste(testes_nomes):

    """ Executa os testes """
    import unittest

    if testes_nomes:
        testes = unittest.TestLoader().loadTestsFromNames(testes_nomes)
    else:
        testes = unittest.TestLoader().discover('testes')
    unittest.TextTestRunner(verbosity=2).run(testes)



@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):

    """Start the application under the code profiler."""

    from werkzeug.contrib.profiler import ProfilerMiddleware
    
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    
    """
    #socketio.run(app)
    """

    app.run()



@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.inserir_roles()

    # ensure all users are following themselves
    #User.add_self_follows()




