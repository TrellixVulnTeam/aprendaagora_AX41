import os
import click


from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from flask_migrate import Migrate, upgrade

from app import criar_app, db  #, socketio

from app import faker

from app.modelos import (
    InscricaoFeuRosa,
    Permissao,
    Role,
    Usuario,
    Materia,
    Curso,
    Topico,
    Licao,
    Questao,
    Tag,
    Publicacao,
    Comentario,
    Emblema,
    TopicoAmei,
    LicaoAmei,
    QuestaoAmei,
    PublicacaoAmei,
    ComentarioAmei
)


app = criar_app(os.getenv('FLASK_CONFIG') or 'padrao')

migrate = Migrate(app, db)


# Flask Shell
@app.shell_context_processor
def make_shell_context():

    return dict(
        db=db,
        InscricaoFeuRosa=InscricaoFeuRosa,
        Permissao=Permissao,
        Role=Role,
        Usuario=Usuario,
        Materia=Materia,
        Curso=Curso,
        Topico=Topico,
        Licao=Licao,
        Questao=Questao,
        Tag=Tag,
        Publicacao=Publicacao,
        Comentario=Comentario,
        Emblema=Emblema,
        TopicoAmei=TopicoAmei,
        LicaoAmei=LicaoAmei,
        QuestaoAmei=QuestaoAmei,
        PublicacaoAmei=PublicacaoAmei,
        ComentarioAmei=ComentarioAmei,
        faker=faker
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

    print("\n\nComando click 'deploy' chamado.\n\n")
    
    """Run deployment tasks."""
    # migrate database to latest revision
    #upgrade()

    # create or update user roles
    Role.inserir_roles()
    
    Tag.inserir_tags()

    Materia.inserir_materias()

    
    ramon = Usuario(nome='ramon', nome_usuario='ramon',email='ramon@gmail.com',senha='1234')
    role_admin = Role.query.filter_by(nome='Administrador').first()
    ramon.role = role_admin
    ramon.confirmado = True

    joao = Usuario(nome='joao', nome_usuario='joao',email='joao@gmail.com',senha='1234')
    joao.confirmado = True

    db.session.add(ramon)
    db.session.add(joao)
    db.session.commit()
    

    # ensure all users are following themselves
    #User.add_self_follows()



@app.cli.command()
def reiniciar():

    print("\n\nComando click 'reiniciar' chamado.\n\n")

    db.drop_all()
    db.create_all()





@app.cli.command()
def fakear():

    print("\n\nComando click 'fakear' chamado.\n\n")

    faker.cursos()
    faker.topicos()
    faker.licoes()
    faker.usuarios()
    faker.publicacoes()
    faker.comentarios_publicacoes()
