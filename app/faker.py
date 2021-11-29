from random import randint, choice
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .modelos import Usuario, Publicacao, Tag, Comentario

# Lista de palavras relacionadas a estudo de idiomas
lista_palavras = [
    'palavra', 'verbo', 'frase', 'difícil', 'conjugação',
    'pronúncia', 'inglês', 'escola', 'estudos', 'livro',
    'cultura', 'gramática', 'vocabulário', 'fácil', 'estudantes',
    'professor', 'exercício', 'prática', 'rápido', 'devagar', 'exterior',
    'sotaque', 'poliglta', 'idioma', 'língua', 'semântica', 'linguística',
    'literatura', 'expressão', 'linguagem', 'dialeto', 'fala', 'adjetivo',
    'dicionário', 'gíria'
]

# Cria usuários
def usuarios(n_usuarios=100):

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Repita 'n_usuarios' vezes
    for i in range(n_usuarios):

        # Cria um usuário fake
        u = Usuario(
                email=fake.email(),

                nome_usuario=fake.user_name(),
                
                senha='password',
                
                confirmado=True,
                
                nome=fake.name(),
                
                sobrenome=fake.name(),
                
                localizacao=fake.city(),
                
                sobre=fake.sentence(),
                
                membro_desde=fake.past_date()
            )

        # Adiciona o usuário à sessão
        db.session.add(u)
        
    try:
        # Salva usuários no banco de dados
        db.session.commit()

    except IntegrityError:

        # Reverte alterações
        db.session.rollback()

# Cria publicações
def publicacoes(n_publicacoes=100): 

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Define o número de usuários cadastrados no sistema
    n_usuarios = Usuario.query.count()

    # Repita 'n_publicacoes' vezes
    for i in range(n_publicacoes):

        # Seleciona um usuário de forma aleatória
        u = Usuario.query.offset(randint(0, n_usuarios - 1)).first()

        # Cria um publicação com dados aleatórios
        p = Publicacao(titulo=fake.sentence(ext_word_list=lista_palavras).capitalize(),
                       conteudo=fake.sentence(ext_word_list=lista_palavras).capitalize(),
                       data=fake.past_date(),
                       autor=u,
                       idioma='ingles')

        # Repita 2 vezes
        for i in range(2):

            # Define 'id_aleatorio' de forma aleatória
            id_aleatorio = randint(1, 4)

            # Seleciona a tag no banco de dados de acordo com id aleatório criado
            t = Tag.query.filter_by(id=id_aleatorio).first()

            # Adiciona a tag aleatória à lista de tags da publicação
            p.tags.append(t)
    
        # Adiciona a publicação à sessão
        db.session.add(p)
    
    try:

        # Salva publicações no banco de dados
        db.session.commit()
    except IntegrityError:

        # Reverte alterações
        db.session.rollback()

# Cria comentários em publicações
def comentarios_publicacoes(n_comentarios=100):

    # Instância 'Faker' com linguagem definida para português-brasileiro
    fake = Faker('pt_BR')

    # Seleciona os ids das publicações existentes
    ids_publicacoes = [id for id, in db.session.query(Publicacao.id)]

    # Seleciona os ids dos usuários existentes
    ids_usuarios = [id for id, in db.session.query(Usuario.id)]

    """
    Link da solução:
    https://stackoverflow.com/questions/48466959/query-for-list-of-attribute-instead-of-tuples-in-sqlalchemy

    ids_publicacoes = db.session.query(Publicacao.id).all()

    print(ids_publicacoes)

    for id in ids_publicacoes:

        print(id[0])
    """

    print(ids_publicacoes)

    print(ids_usuarios)

    # Repita 'n_comentarios' vezes
    for i in range(n_comentarios):
        
        # Cria um comentário com conteúdo, autor e publicação aleatórios
        c = Comentario(

            # 'choice()' é uma função da biblioteca 'random' que escolhe um elemento aleatório em um vetor

            publicacao_id=choice(ids_publicacoes),

            autor_id=choice(ids_usuarios),

            conteudo=fake.sentence(ext_word_list=lista_palavras).capitalize()
        )

        # Adiciona o comentário à sessão
        db.session.add(c)
    

    try:
        # Salva comentários no banco de dados
        db.session.commit()
    except IntegrityError:
        # Reverte alterações
        db.session.rollback()
    
