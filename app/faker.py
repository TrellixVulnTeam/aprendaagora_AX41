from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .modelos import Usuario, Publicacao, Tag

def usuarios(n_usuarios=100):

    fake = Faker('pt_BR')
    i = 0

    while i < n_usuarios:

        u = Usuario(email=fake.email(),
                nome_usuario=fake.user_name(),
                senha='password',
                confirmado=True,
                nome=fake.name(),
                sobrenome=fake.name(),
                localizacao=fake.city(),
                sobre=fake.sentence(),
                membro_desde=fake.past_date())
        db.session.add(u)
        
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def publicacoes(n_publicacoes=100):

    fake = Faker('pt_BR')
    n_usuarios = Usuario.query.count()

    lista_palavras = [
        'palavra', 'verbo', 'frase', 'difícil', 'conjugação',
        'pronúncia', 'inglês', 'escola', 'estudos', 'livro',
        'cultura', 'gramática', 'vocabulário', 'fácil', 'estudantes',
        'professor', 'exercício', 'prática', 'rápido', 'devagar', 'exterior',
        'sotaque', 'poliglta', 'idioma', 'língua', 'semântica', 'linguística',
        'literatura', 'expressão', 'linguagem', 'dialeto', 'fala', 'adjetivo',
        'dicionário', 'gíria'
    ]


    for i in range(n_publicacoes):

        u = Usuario.query.offset(randint(0, n_usuarios - 1)).first()

        p = Publicacao(titulo=fake.sentence(ext_word_list=lista_palavras).capitalize(),
                       conteudo=fake.sentence(ext_word_list=lista_palavras).capitalize(),
                       data=fake.past_date(),
                       autor=u,
                       idioma='ingles')

        # Para cada tag selecionada no formulário

        for i in range(2):

            random_id = randint(1, 4)

            # Seleciona a tag no banco de dados de acordo com o que foi selecionado
            t = Tag.query.filter_by(id=random_id).first()

            # Adiciona a tag selecionada à lista de tags da publicação
            p.tags.append(t)
    
        db.session.add(p)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()