import os
import click
from flask_migrate import Migrate, upgrade
from app import criar_app, db
from app.modelos import Permissao, Role, Usuario, Publicacao, Tag

app = criar_app(os.getenv('FLASK_CONFIG') or 'padrao')
migrate = Migrate(app, db)


# Flask Shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Permissao=Permissao, Role=Role, Usuario=Usuario, Publicacao=Publicacao, Tag=Tag)

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
    app.run()


@app.cli.command()
def deploy():

    # Executa tarefas de implementaçao (deploy)
    # migrar banco de dados para a última revisão
    upgrade()

    # criar ou atualizar os roles dos usuários
    Role.inserir_roles()

    # garantir que todos os usuários estão seguindo a si mesmos
    # NÃO IMPLEMENTADO AINDA
    # Usuario.adicionar_seguir_si_mesmo()




