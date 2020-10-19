import os
import click
from flask_migrate import Migrate
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

