import hashlib
from markdown import markdown
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from datetime import datetime

# Lista de Modelos
"""
    InscricaoFeuRosa
   
    Role
    Permissao

    Usuario
    Publicacao
    Tag
    Comentario

    Materia
    Curso
    Tópico
    Lição
    Questao
    Emblema

    TopicoAmei
    LicaoAmei
    QuestaoAmei
    PublicacaoAmei
    ArtigoAmei
    ComentarioAmei

    ***País
    ***Estado
    ***Cidade
"""

# Relações entre Modelos
"""
    usuarios_materias
    usuarios_cursos
    usuarios_topicos
    usuarios_licoes
    usuarios_emblemas

    instrutores_materias
    instrutores_cursos



    publicacoes_tags
    licoes_tags
    questoes_tags
"""



class InscricaoFeuRosa(db.Model):

    __tablename__ = 'inscricoes_feu_rosa'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(64))

    email = db.Column(db.String(32))

    numero_telefone = db.Column(db.String(32))

    curso = db.Column(db.String(16))

    horario = db.Column(db.String(16))





"""
##########################################################

##### ##### #      ###  ##### ##### ##### ##### 
#   # #     #     ## ## #     #   # #     #     
##### ##### #     #   # #     #   # ##### ##### 
#  #  #     #     ##### #     #   # #         # 
#   # ##### ##### #   # ##### ##### ##### ##### 

##########################################################
"""

# Relação entre USUÁRIOS e MATÉRIAS
usuarios_materias = db.Table(
    'usuarios_materias',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('materia_id', db.Integer, db.ForeignKey('materias.id'), primary_key=True)
)

# Relação entre USUÁRIOS e CURSOS
usuarios_cursos = db.Table(
    'usuarios_cursos',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True)
)

# Relação entre USUÁRIOS e TÓPICOS
usuarios_topicos = db.Table(
    'usuarios_topicos',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('topico_id', db.Integer, db.ForeignKey('topicos.id'), primary_key=True)
)

# Relação entre USUÁRIOS e LIÇÕES
usuarios_licoes = db.Table(
    'usuarios_licoes',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('licao_id', db.Integer, db.ForeignKey('licoes.id'), primary_key=True)
)

# Relação entre USUÁRIOS e QUESTÕES
usuarios_questoes = db.Table(
    'usuarios_questoes',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('questao_id', db.Integer, db.ForeignKey('questoes.id'), primary_key=True)
)

# Relação entre USUÁRIOS e EMBLEMAS
usuarios_emblemas = db.Table(

    'usuarios_emblemas',
    
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),

    db.Column('emblema_id', db.Integer, db.ForeignKey('emblemas.id'), primary_key=True)
)

# Relação entre publicações e tags
publicacoes_tags = db.Table(
    
    'publicacoes_tags',

    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),

    db.Column('publicacao_id', db.Integer, db.ForeignKey('publicacoes.id'), primary_key=True)
)

# Relação entre LIÇÕES e TAGS 
licoes_tags = db.Table(
    'licoes_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('licao_id', db.Integer, db.ForeignKey('licoes.id'), primary_key=True)
)

# Relação entre QUESTÕES e TAGS
questoes_tags = db.Table(
    'questoes_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('questao_id', db.Integer, db.ForeignKey('questoes.id'), primary_key=True)
)

"""
##########################################################

#   # ##### #   #  ###  ##### ##### ##### 
#   # #     #   # ## ## #   #   #   #   # 
#   # ##### #   # #   # #####   #   #   # 
#   #     # #   # ##### #  #    #   #   # 
##### ##### ##### #   # #   # ##### ##### 

##########################################################
"""



# Lista de permissões dos 'roles'
class Permissao:
    # Seguir murais e usuários
    SEGUIR = 1

    # Comentar em artigos do blog, lições dos cursos e publicações no mural
    COMENTAR = 2

    # Escrever publicações no mural
    ESCREVER_MURAL = 4

    # Apagar comentários, fechar discussões, etiqueta de usuário destacada 
    MODERAR_INGLES = 8
    MODERAR_FRANCES = 16
    MODERAR_ESPANHOL = 32
    MODERAR_ITALIANO = 64
    MODERAR_ALEMAO = 128
    MODERAR_JAPONES = 256
    MODERAR_CHINES = 512

    # Criar publicações destacadas e eventos no mural
    PROF_INGLES = 1024
    PROF_FRANCES = 2048
    PROF_ESPANHOL = 4096
    PROF_ITALIANO = 8192
    PROF_ALEMAO = 16384
    PROF_JAPONES = 32768
    PROF_CHINES = 65536

    # Fazer publicações no blog
    ESCREVER_BLOG = 131072


    """

    MODERAR_PORTUGUES
    MODERAR_MATEMATICA
    MODERAR_BIOLOGIA
    MODERAR_QUIMICA
    MODERAR_FISICA
    MODERAR_HISTORIA
    MODERAR_GEOGRAFIA
    MODERAR_FILOSOFIA
    MODERAR_SOCIOLOGIA
    MODERAR_ARTE


    PROF_PORTUGUES
    PROF_MATEMATICA
    PROF_BIOLOGIA
    PROF_QUIMICA
    PROF_FISICA
    PROF_HISTORIA
    PROF_GEOGRAFIA
    PROF_FILOSOFIA
    PROF_SOCIOLOGIA
    PROF_ARTE


    CRIAR_CURSO
    CRIAR_TOPICO
    CRIAR_LICAO
    CRIAR_QUESTAO
    CRIAR_ARTIGO
    CRIAR_TAG

    """

    # Permissões de administrador
    ADMIN = 262144


class Role(db.Model):

    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)

    # Nome do 'role'
    nome = db.Column(db.String(64), unique=True)

    # Apenas um "role" pode ter o atributo 'padrao' igual a True. O "role" marcado como "padrao" será o "role" atribuído a novos usuários durante a inscrição. Considerando que o app vai consultar a tabela 'roles' para encontrar o 'role' padrão, esta coluna está configurada para ter um índice, dado que isto faz a consulta ser mais rápida 
    padrao = db.Column(db.Boolean, default=False, index=True)

    # Lista de permissões de um 'role'. As permissões individuais são acessadas através de lógica binária
    permissoes = db.Column(db.Integer)

    # Relação com a tabela 'usuarios'
    usuarios = db.relationship('Usuario', backref='role', lazy='dynamic')


    # 'permissoes' é um valor inteiro que define a lista de permissoes de um 'role' de forma compacta. Considerando que SQLAlchemy vai definir este campo como None por padrão, um construtor de classe é adicionado para definir o campo 'permissoes' como sendo 0 caso um valor inicial não seja providenciado nos argumentos do construtor
    def __init__(self, **kwargs):

        super(Role, self).__init__(**kwargs)

        if self.permissoes is None:

            self.permissoes = 0


    # A função inserir_roles() não cria novos objetos 'role' diretamente. Ao invés disso, ela tenta encontrar 'roles' existentes e atulizar as permissões desses 'roles'. Um novo objeto 'role' é criado apenas para para os 'roles' que ainda não existem no banco de dados. Isso é feito de forma que a lista de 'roles' possa ser atualizada no futuro quando mudanças precisarem ser feitas. Para adicionar um novo role ou mudar a lista de permissões de um 'role', altere o dicionário 'roles' definido no topo da função e execute a função novamente. Perceba que o 'role' anônimo não precisa ser representado no banco de dados, já que ele é o 'role' que representa usuários desconhecidos e que portanto não estão no banco de dados.
    # Perceba também que inserir_roles() é um método estático, um tipo especial de método que não exige que um objeto seja criado pois ele pode ser invocado a partir da classe, escrevendo Role.inserir_roles(). Métodos estáticos não recebem um argumento 'self' como métodos de instâncias.
    @staticmethod
    def inserir_roles():

        # Define as permissões dos 'roles'
        roles = {
            'Estudante': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL
                ],
            'ModeradorIngles': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_INGLES
                ],
            'ModeradorFrances': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_FRANCES
                ],
            'ModeradorEspanhol': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_ESPANHOL
                ],
            'ModeradorItaliano': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_ITALIANO
                ],
            'ModeradorAlemao': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_ALEMAO
                ],
            'ModeradorJapones': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_JAPONES
                ],
            'ModeradorChines': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.MODERAR_CHINES
                ],
            'ProfessorIngles': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_INGLES
                ],
            'ProfessorFrances': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_FRANCES
                ],
            'ProfessorEspanhol': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_ESPANHOL
                ],
            'ProfessorItaliano': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_ITALIANO
                ],
            'ProfessorAlemao': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_ALEMAO
                ],
            'ProfessorJapones': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_JAPONES
                ],
            'ProfessorChines': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_CHINES
                ],
            'Administrador': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_MURAL,
                Permissao.ESCREVER_BLOG,
                Permissao.ADMIN
                ],       
        }

        # Define um 'role' padrão
        role_padrao = 'Estudante'

        # Para cada 'role' no dicionário 'roles'
        for r in roles:

            # Consulte o banco de dados procurando por um 'role' que tenha o nome  igual ao de um dos 'roles' definidos no dicionnário 'roles'
            role = Role.query.filter_by(nome=r).first()

            # Se NÃO existir um 'role' com o nome informado
            if role is None:
                # Crie um novo 'role'
                role = Role(nome=r)
            
            # Redefina as permissões do 'role' criado
            role.redefinir_permissoes()

            # Para cada permissão, como definidas no dicionário, pertencente ao 'role'
            for permissao in roles[r]:
                # Adicione a permissão ao 'role' criado
                role.adicionar_permissao(permissao)
            
            # Se o nome do 'role' for o role padrão, defina o atributo 'padrao' do 'role' como sendo True
            role.padrao = (role.nome == role_padrao)

            # Adiciona o 'role' recentemente criado ao banco de dados
            db.session.add(role)
        
        # Salve as alterações no banco de dados
        db.session.commit()

    # Adiciona uma permissao
    def adicionar_permissao(self, permissao):
        # Se o usuário não possuir a permissão
        if not self.tem_permissao(permissao):
            # Adicione a permissão em sua lista de permissões
            self.permissoes += permissao

    # Remove uma permissão
    def remover_permissao(self, permissao):

        # Se o usuário possuir a permissão
        if self.tem_permissao(permissao):

            # Remova a permissão de sua lista de permissões
            self.permissoes -= permissao
    
    # Redefine as permissões do usuário
    def redefinir_permissoes(self):
        self.permissoes = 0

    # Checa se o usuário possui uma permissão
    def tem_permissao(self, permissao):
        # Operação bitwise para checar se a permissão em questão está incluída nas permissões do usuário
        return self.permissoes & permissao == permissao

    def __repr__(self):
        return '<Role %r>' % self.nome


class Seguir(db.Model):

    __tablename__ = 'seguir'

    seguidor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True
    )

    seguido_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True
    )

    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Usuario(UserMixin, db.Model):

    """
        id
        email
        nome_usuario
        senha_hash
        nome
        sobrenome
        data_nascimento
        localizacao
        sobre
        twitter
        instagram
        facebook
        role_id
        confirmado
        membro_desde
        ultimo_acesso
        avatar_hash
    """

    __tablename__ = 'usuarios'

    """    
    ####   ###  ####  ##### ##### 
    #   # ## ## #   # #   # #     
    #   # #   # #   # #   # ##### 
    #   # ##### #   # #   #     # 
    ####  #   # ####  ##### ##### 
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True,)
    nome_usuario = db.Column(db.String(25), unique=True, index=True)
    senha_hash = db.Column(db.String(128))
    nome = db.Column(db.String(64))
    sobrenome = db.Column(db.String(64))
    data_nascimento = db.Column(db.Date())
    localizacao = db.Column(db.String(64))
    sobre = db.Column(db.String(100))
    twitter = db.Column(db.String(15))
    instagram = db.Column(db.String(30))
    facebook = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmado = db.Column(db.Boolean, default=False)
    membro_desde = db.Column(db.DateTime(), default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))


    """
    ##### ##### #      ###  ##### ##### ##### ##### 
    #   # #     #     ## ## #     #   # #     #     
    ##### ##### #     #   # #     #   # ##### ##### 
    #  #  #     #     ##### #     #   # #         # 
    #   # ##### ##### #   # ##### ##### ##### ##### 
    """


    # Usuario.publicacoes retorna a lista de publicações escritas pelo usuário
    notificacoes = db.relationship('Notificacao',
                                  backref='notificado',
                                  lazy='dynamic')


    # Usuario.publicacoes retorna a lista de publicações escritas pelo usuário
    publicacoes = db.relationship('Publicacao',
                                  backref='autor',
                                  lazy='dynamic')

    # Usuario.comentarios retorna a lista de comentários escritos pelo usuário
    comentarios = db.relationship('Comentario',
                                  backref='autor',
                                  lazy='subquery')

    seguidos = db.relationship(
        'Seguir',
        foreign_keys=[Seguir.seguidor_id],
        backref=db.backref('seguidor', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    seguidores = db.relationship(
        'Seguir',
        foreign_keys=[Seguir.seguido_id],
        backref=db.backref('seguido', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


    cursos = db.relationship('Curso',
                            backref='instrutor',
                            lazy='dynamic')
    

    licoes_criadas = db.relationship('Licao',
                                  backref='autor',
                                  lazy='dynamic')
    
    # Usuario.licoes retorna as lições que o usuário completou
    licoes_completadas = db.relationship('Licao',
                           secondary=usuarios_licoes,
                           lazy='subquery',
                           backref=db.backref('usuarios_que_completaram'))
    
    
    # Usuario.questoes_criadas retorna a lista de questões criadas pelo usuário
    questoes_criadas = db.relationship('Questao',
                                  backref='autor',
                                  lazy='dynamic')

    # Usuario.questoes_respondidas retorna as questões que o usuário respondeu
    questoes_respondidas = db.relationship('Questao',
                           secondary=usuarios_questoes,
                           lazy='subquery',
                           backref=db.backref('usuarios_que_responderam'))
    

    publicacoes_amei = db.relationship('PublicacaoAmei',
                                       foreign_keys='PublicacaoAmei.usuario_id',
                                       backref='usuario',
                                       lazy='dynamic')

    licoes_amei = db.relationship('LicaoAmei',
                                       foreign_keys='LicaoAmei.usuario_id',
                                       backref='usuario',
                                       lazy='dynamic')



    """ 
    ##### #   # ##### ##### 
      #   ##  #   #     #   
      #   # # #   #     #   
      #   #  ##   #     #   
    ##### #   # #####   #   
    """


    # Atribui o 'role' 'Estudante' à novos usuários, ou 'Administrador' caso o email do usuário está deinido em APRENDA_AGORA_ADMIN
    def __init__(self, **kwargs):

        super(Usuario, self).__init__(**kwargs)

        # Se o 'role' do usuário não estiver definido
        if self.role is None:

            # Caso o email do usuário seja o email do administrador
            if self.email == current_app.config['APRENDA_AGORA_ADMIN']:

                # Define o 'role' do usuário como sendo 'Administrador'
                self.role = Role.query.filter_by(nome='Administrador').first()
            
            # Senão, defina o 'role' do usuário como sendo o 'role' padrão
            if self.role is None:

                self.role = Role.query.filter_by(padrao=True).first()

        # Se o usuário tiver um email vinculado e o 'avatar_hash' não estiver definido
        if self.email is not None and self.avatar_hash is None:

            # Crie o 'avatar_hash' do usuário
            self.avatar_hash = self.gravatar_hash()
        
        # Segue a si mesmo para que as próprias publicações apareçam na linha do tempo
        self.seguir(self)


    @property
    def senha(self):
        raise AttributeError('senha não é um atributo de leitura')

    # Quando a propriedade 'senha' for definida/alterada
    @senha.setter
    def senha(self, senha):
        # Redefine 'senha_hash' baseado em 'senha'
        self.senha_hash = generate_password_hash(senha)

    @property
    def publicacoes_seguidos(self):

        return Publicacao.query.join(
                Seguir, Seguir.seguido_id == Publicacao.autor_id
            ).filter(
                Seguir.seguidor_id == self.id
            )

    """  
     ###  #   # ##### ##### #   # ##### ##### #####  ###  #####  ###  ##### 
    ## ## #   #   #   #     ##  #   #     #   #     ## ## #     ## ## #   # 
    #   # #   #   #   ##### # # #   #     #   #     #   # #     #   # #   # 
    ##### #   #   #   #     #  ##   #     #   #     ##### #     ##### #   # 
    #   # #####   #   ##### #   #   #   ##### ##### #   # ##### #   # ##### 
    """

    # Este método recebe a senha e passa ela na função check_password_hash() para a comparar com a hash armazenada no modelo 'Usuario'.
    # Se retornar True, a senha está correta
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


    # Gera um token para o usuário confirmar sua conta
    def gerar_token_confirmacao(self, expiracao=3600):

        s = Serializer(current_app.config['SECRET_KEY'], expiracao)

        return s.dumps({'confirmado': self.id}).decode('utf-8')
    

    # Confirma a conta de um usuário
    def confirmar(self, token):

        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            dados = s.loads(token.encode('utf-8'))
        except Exception as e:
            return False

        if dados.get('confirmado') != self.id:
            return False
        
        self.confirmado = True

        db.session.add(self)

        return True


    # Cria um token para redefinir a senha do usuário
    def gerar_token_redefinir_senha(self, expiracao=3600):

        # Cria o token
        s = Serializer(current_app.config['SECRET_KEY'], expiracao)

        # Retorna o token
        return s.dumps({'id_usuario': self.id}).decode('utf-8')


    # Redefine a senha do usuário
    @staticmethod
    def redefinir_senha(token, nova_senha):

        # Instância do serializador
        serializador = Serializer(current_app.config['SECRET_KEY'])

        try:
            dados = serializador.loads(token.encode('utf-8'))
        except Exception as e:
            return False
        
        # Seleciona o usuário usando o id
        usuario = Usuario.query.get(dados.get('id_usuario'))

        # Se a consulta não retornar um usuário
        if usuario is None:
            return False

        #
        usuario.senha = nova_senha
        
        db.session.add(usuario)

        return True


    # Gera o token usado na troca de email
    def gerar_token_trocar_email(self, novo_email, expiracao=3600):

        # Instância do serializador
        serializador = Serializer(current_app.config['SECRET_KEY'], expiracao)

        # Retorna um objeto serializado, contendo o id do usuário e o novo email
        return serializador.dumps(
            {'id_usuario': self.id, 'novo_email': novo_email}
        ).decode('utf-8')


    # Redefine o email de um usuário
    def trocar_email(self, token):

        # Instância do serializador
        serializador = Serializer(current_app.config['SECRET_KEY'])

        # Tente
        try:
            # Desserializa o token que contém o id do usuário e o novo email
            dados = serializador.loads(token.encode('utf-8'))

        # Se houver erro
        except Exception as e:
            
            return False

        # Se a propriedade 'id_objeto' do objeto desserializado for diferente do id deste usuário
        if dados.get('id_usuario') != self.id:

            return False

        # Seleciona o novo email
        novo_email = dados.get('novo_email')

        # Checagem de erro
        if novo_email is None:
            return False
    
        # Se já houver um usuário com o novo email digitado
        if self.query.filter_by(email=novo_email).first() is not None:

            return False

        # Redefine o email do usuário
        self.email = novo_email

        # Redefine o 'avatar_hash' baseado no novo email
        self.avatar_hash = self.gravatar_hash()

        # Adiciona o usuário à sessão 
        db.session.add(self)

        
        return True

    """
    ##### ##### ##### #   # ##### ##### 
    #     #     #     #   #   #   #   # 
    ##### ##### # ### #   #   #   ##### 
        # #     #   # #   #   #   #  #  
    ##### ##### ##### ##### ##### #   # 
    """

    def seguir(self, usuario):

        if not self.seguindo(usuario):

            s = Seguir(seguidor=self, seguido=usuario)

            db.session.add(s)

    def desfazer_seguir(self, usuario):

        seguido = self.seguidos.filter_by(seguido_id=usuario.id).first()

        if seguido:
            db.session.delete(seguido)


    def seguindo(self, usuario):

        if usuario.id is None:

            return None

        return self.seguidos.filter_by(
            seguido_id=usuario.id).first() is not None
        
    def seguido_por(self, usuario):

        if usuario.id is None:

            return False
        
        return self.seguidores.filter_by(
            seguidor_id=usuario.id).first() is not None

    """
    ##### #   # ##### ##### #####  ###  #####  ###  ##### 
      #   ##  #   #   #     #   # ## ## #     ## ## #   # 
      #   # # #   #   ##### ##### #   # #     #   # #   # 
      #   #  ##   #   #     #  #  ##### #     ##### #   # 
    ##### #   #   #   ##### #   # #   # ##### #   # ##### 
    """

    # CURSOS
    def inscrever_curso(self, curso):
        return 1

    # Desfaz a inscrição mas não apaga as lições completadas
    def desfazer_inscrever_curso(self, curso):
        return 1

    # Apaga as lições completadas
    def reiniciar_cruso(self, curso):
        return 1

    # TÓPICOS
    def amar_topico(self, topico):
        return 1

    def desfazer_amar_topico(self, topico):
        return 1

    def amou_topico(self, topico):
        return 1

    # LIÇÕES
    def amar_licao(self, licao):
        return 1

    def desfazer_amar_licao(self, licao):
        return 1

    def amou_licao(self, licao):
        return 1

    def completar_licao(self, licao):
        return 1

    def desfazer_completar_licao(self, licao):
        return 1

    def completou_licao(self, licao):
        return 1


    # QUESTÕES
    def responder_questao(self, questao):
        return 1

    def amar_questao(self, questao):
        return 1

    def desfazer_amar_questao(self, questao):
        return 1


    # PUBLICAÇÃO
    def amar_publicacao(self, publicacao):

        if not self.amou_publicacao(publicacao):

            amou = PublicacaoAmei(usuario_id=self.id, publicacao_id=publicacao.id)
            
            db.session.add(amou)

    def desfazer_amar_publicacao(self, publicacao):

        if self.amou_publicacao(publicacao):

            PublicacaoAmei.query.filter_by(

                usuario_id=self.id,

                publicacao_id=publicacao.id

            ).delete()

    def amou_publicacao(self, publicacao):

        return PublicacaoAmei.query.filter(

                PublicacaoAmei.usuario_id == self.id,

                PublicacaoAmei.publicacao_id == publicacao.id

        ).count() > 0


    # ARTIGOS
    def amar_artigo(self, artigo):
        return 1

    def desfazer_amar_artigo(self, artigo):
        return 1

    def amou_artigo(self, artigo):
        return 1


    # COMENTÁRIOS
    def amar_comentario(self, comentario):
        return 1

    def desfazer_amar_comentario(self, comentario):
        return 1


    # EMBLEMAS

    def conceder_emblema(self, emblema):
        return 1

    def revogar_emblema(self, emblema):
        return 1

    def possui_emblema(self, emblema):
        return 1


    """
    ##### #   # ##### ##### ##### ##### 
    #   # #   #   #   #   # #   # #     
    #   # #   #   #   ##### #   # ##### 
    #   # #   #   #   #  #  #   #     # 
    ##### #####   #   #   # ##### ##### 
    """

    # Um dos requisitos do serviço Gravatar é que o endereço de email através do qual o hash MD5 é obtido deve estar em letras minúsculas, por isso usamos a função 'String.lower()'
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):

        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://gravatar.com/avatar'
        
        #Se houver uma hash armazenada, use ela, senão, gere uma nova hash 
        hash = self.avatar_hash or self.gravatar_hash()

        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash,
            size=size, default=default,
            rating=rating
        )

    # Checa se o usuário pode fazer determinada ação
    def pode(self, permissao):
        # Se a 'role' do usuário NÃO for None e se a 'role' possuir a permissão, retorne True
        return self.role is not None and self.role.tem_permissao(permissao)

    # Checa se o usuário é um Administrador
    def e_administrador(self):
        # Checa se o usuário tem permissão de Adminstrador
        return self.pode(Permissao.ADMIN)

    # Atualiza o campo 'ultimo_acesso' para ser a data de quando a função é chamada
    def ping(self):
        self.ultimo_acesso = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    # String que representa o usuário
    def __repr__(self):
        return '<Usuário %r>' % self.nome_usuario



"""
##########################################################

#   #  ###  ##### ##### ##### #####  ###  
## ## ## ##   #   #     #   #   #   ## ## 
# # # #   #   #   ##### #####   #   #   # 
#   # #####   #   #     #  #    #   ##### 
#   # #   #   #   ##### #   # ##### #   # 

##########################################################
"""

# As tags de uma publicação podem ser acessadas com publicacao.tags
class Materia(db.Model):

    """
        id
        nome
        nome_simples
        nome_foto
        cursos
        topicos
        licoes
    """
    
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(32), unique=True)

    nome_simples = db.Column(db.String(32), unique=True)

    nome_foto = db.Column(db.String(100))

    emoji = db.Column(db.String(10))


    """
        1 - IDIOMAS
        2 - ENSINO MÉDIO
    """
    tipo = db.Column(db.Integer())


    cursos = db.relationship('Curso',
                            backref='materia',
                            lazy='dynamic')

    topicos = db.relationship('Topico',
                            backref='materia',
                            lazy='dynamic')

    licoes = db.relationship('Licao',
                            backref='materia',
                            lazy='dynamic')
    

    @staticmethod
    def inserir_materias():

        # Lista de tags em formato chave-valor. O valor é o nome da tag que será armazenado
        materias = [
            {
                "nome": "Inglês",
                "nome_simples": "ingles",
                "emoji": "🇺🇸",
                "tipo": 1,
            },
            {
                "nome": "Espanhol",
                "nome_simples": "espanhol",
                "emoji": "🇪🇸",
                "tipo": 1,
            },
            {
                "nome": "Francês",
                "nome_simples": "frances",
                "emoji": "🇫🇷",
                "tipo": 1,
            },
            {
                "nome": "Italiano",
                "nome_simples": "italiano",
                "emoji": "🇮🇹",
                "tipo": 1,
            },
            {
                "nome": "Alemão",
                "nome_simples": "alemao",
                "emoji": "🇩🇪",
                "tipo": 1,
            },
            {
                "nome": "Japonês",
                "nome_simples": "japones",
                "emoji": "🇯🇵",
                "tipo": 1,
            },
            {
                "nome": "Chinês",
                "nome_simples": "chines",
                "emoji": "🇨🇳",
                "tipo": 1,
            },
            {
                "nome": "Português",
                "nome_simples": "portugues",
                "emoji": "🎠",
                "tipo": 2,
            },
            {
                "nome": "Matemática",
                "nome_simples": "matematica",
                "emoji": "📊",
                "tipo": 2,
            },
            {
                "nome": "Biologia",
                "nome_simples": "biologia",
                "emoji": "🌱",
                "tipo": 2,
            },
            {
                "nome": "Química",
                "nome_simples": "quimica",
                "emoji": "🔥",
                "tipo": 2,
            },
            {
                "nome": "Física",
                "nome_simples": "fisica",
                "emoji": "💡",
                "tipo": 2,
            },
            {
                "nome": "História",
                "nome_simples": "historia",
                "emoji": "⏳",
                "tipo": 2,
            },
            {
                "nome": "Geografia",
                "nome_simples": "geografia",
                "emoji": "🌎",
                "tipo": 2,
            },
            {
                "nome": "Filosofia",
                "nome_simples": "filosofia",
                "emoji": "💭",
                "tipo": 2,
            },
            {
                "nome": "Sociologia",
                "nome_simples": "sociologia",
                "emoji": "👥",
                "tipo": 2,
            },
            {
                "nome": "Arte",
                "nome_simples": "arte",
                "emoji": "🎨",
                "tipo": 2,
            },
        ]

        """
        
        Tópicos de IDIOMAS:
        
            Gramática
            Escrita
            Pronúncia
            Leitura
            Vocabulário
            
            Conjugação de Verbo
            Pronomes
            Verbos
            Preposição
            Advérbio
            Expressões Idiomáticas
        """

        # Para cada conjunto chave-valor
        for m in materias:

            # Consulte o banco de dados procurando por uma 'tag' que tenha o nome igual ao de uma das 'tags' definidas no dicionário 'tags'
            materia = Materia.query.filter_by(nome_simples=m['nome_simples']).first()

            # Se NÃO existir uma 'tag' com o nome informado
            if materia is None:

                # Crie uma nova 'tag'
                materia = Materia(
                    nome=m['nome'],
                    nome_simples=m['nome_simples'],
                    emoji=m['emoji'],
                    tipo=m['tipo']
                )

            # Adiciona a tag à sessão
            db.session.add(materia)

        # Salva as alterações no banco de dados
        db.session.commit()


"""
##########################################################

##### #   # ##### ##### ##### 
#     #   # #   # #     #   # 
#     #   # ##### ##### #   # 
#     #   # #  #      # #   # 
##### ##### #   # ##### ##### 

##########################################################
"""

class Curso(db.Model):

    """
        id
        materia_id
        instrutor_id
        nome
        descricao
        nivel
        nome_foto
    """

    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)

    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))

    instrutor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    nome = db.Column(db.String(100))

    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    descricao = db.Column(db.String(400))

    """
        Níveis matérias ensino médio: 
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        
        Níveis idiomas: 
        A1, A2, B1, B2, C1, C2
    """
    nivel = db.Column(db.Integer)

    nome_foto = db.Column(db.String(100))


    topicos = db.relationship('Topico',
                            backref='curso',
                            lazy='dynamic')
    
    licoes = db.relationship('Licao',
                            backref='curso',
                            lazy='dynamic')

    questoes = db.relationship('Questao',
                                  backref='curso',
                                  lazy='dynamic')
    
    comentarios = db.relationship('Comentario',
                                  backref='curso',
                                  lazy='dynamic')



"""
##########################################################

##### ##### ##### ##### ##### ##### 
  #   #   # #   #   #   #     #   # 
  #   #   # #####   #   #     #   # 
  #   #   # #       #   #     #   # 
  #   ##### #     ##### ##### ##### 

##########################################################
"""

class Topico(db.Model):

    """
        id
        titulo
        descricao
        nome_foto
        curso_id
        materia_id
        licoes
        comentarios
        ameis
    """

    __tablename__ = 'topicos'

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150))

    descricao = db.Column(db.String(400))

    nome_foto = db.Column(db.String(100))

    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))

    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))


    licoes = db.relationship('Licao',
                            backref='topico',
                            lazy='dynamic')

    questoes = db.relationship('Questao',
                            backref='topico',
                            lazy='dynamic')
    
    comentarios = db.relationship('Comentario',
                                  backref='topico',
                                  lazy='dynamic')
    
    ameis = db.relationship('Usuario',
                            secondary='topicos_amei',
                            backref=db.backref('topico', lazy='dynamic'))


"""
##########################################################

#     ##### #####  ###  ##### 
#       #   #     ## ## #   # 
#       #   #     #   # #   # 
#       #   #     ##### #   # 
##### ##### ##### #   # ##### 

##########################################################
"""


class Licao(db.Model):

    """
        id
        titulo
        subtitulo
        conteudo
        conteudo_html
        nome_foto
        n_palavras
        data
        autor_id
        topico_id
        curso_id
        materia_id
    """

    __tablename__ = 'licoes'

    # DADOS BÁSICOS
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100))
    subtitulo = db.Column(db.String(100))
    conteudo = db.Column(db.Text)
    conteudo_html = db.Column(db.Text)
    nome_foto = db.Column(db.String(100))
    n_palavras = db.Column(db.Integer)
    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # CHAVES ESTRANGEIRAS
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    topico_id = db.Column(db.Integer, db.ForeignKey('topicos.id'))
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))


    # Publicacao.tags retorna as tags às quais a publicação está associada
    tags = db.relationship('Tag',
                           secondary=licoes_tags,
                           lazy='subquery',
                           backref=db.backref('licoes'))

    questoes = db.relationship('Questao',
                                  backref='licao',
                                  lazy='dynamic')

    comentarios = db.relationship('Comentario',
                                  backref='licao',
                                  lazy='dynamic')
    
    ameis = db.relationship('Usuario',
                            secondary='licoes_amei',
                            backref=db.backref('licao', lazy='dynamic'))


    def __init__(self, **kwargs):

        super(Licao, self).__init__(**kwargs)

        self.n_palavras =  len(self.conteudo.split())

    # Converte texto em Markdown para HTML
    # Primeiro, a função markdown() faz uma conversão inicial para HTML
    # O resultado da conversão inicial é passado para a função clean(), juntamente com a lista de tags permitidas. A função clean() remove todas as tags não permitidas
    # A conversão final é feita com a função linkify(), uma função oferecida pelo Bleach que converte todos os URL escritos em texto-claro em tags âncora <a>
    # Este último passo é necessário por que geração automática de links não é uma ferramenta oficial do Markdown, mas é uma funcionalidade muito conveniente
    @staticmethod
    def conteudo_alterado(target, conteudo, conteudo_antigo, initiator):

        # Define as tags permitidas no Markdown
        tags_permitidas = ['a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h3', 'p']

        atributos_permitidos = {'*': ['class'],
                                'a': ['href', 'rel'],
                                'img': ['src', 'alt']
        }

        # Atualiza o número de palavras
        target.n_palavras =  len(conteudo.split())

        target.conteudo_html = bleach.linkify(
                               bleach.clean(
                                    markdown(conteudo, output_format='html'),
                                    tags=tags_permitidas,
                                    attributes=atributos_permitidos,
                                    strip=False)
        )


"""
##########################################################

 ###  #   # ##### ##### #####  ###  ##### 
#   # #   # #     #       #   ## ## #   # 
#   # #   # ##### #####   #   #   # #   # 
 ###  #   # #         #   #   ##### #   # 
   ## ##### ##### #####   #   #   # ##### 

##########################################################
"""

class Questao(db.Model):


    """
        titulo
        enunciado

        opcaoa
        opcaob
        opcaoc
        opcaod
        opcaoe

        explicacao
        explicacao_html

        autor_id
        topico_id
        curso_id
        materia_id
        
        tags

        comentarios

        ameis

        tipo

        (CAMPOS DE QUESTÕES DO ENEM)
        ano
        prova
        dia
    """

    __tablename__ = 'questoes'

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150))
    enunciado = db.Column(db.Text)

    # A opção 'a' é sempre a correta. Na hora da exibição das opções, as opções devem ser embaralhadas 
    opcaoa = db.Column(db.Text)
    opcaob = db.Column(db.Text)
    opcaoc = db.Column(db.Text)
    opcaod = db.Column(db.Text)
    opcaoe = db.Column(db.Text)

    explicacao = db.Column(db.Text)
    explicacao_html = db.Column(db.Text)

    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    topico_id = db.Column(db.Integer, db.ForeignKey('topicos.id'))
    licao_id = db.Column(db.Integer, db.ForeignKey('licoes.id'))
    

    # Publicacao.tags retorna as tags às quais a publicação está associada
    tags = db.relationship('Tag',
                            secondary=questoes_tags,
                           lazy='subquery',
                           backref=db.backref('questoes'))

    comentarios = db.relationship('Comentario',
                                  backref='questao',
                                  lazy='dynamic')
    
    ameis = db.relationship('Usuario',
                            secondary='questoes_amei',
                            backref=db.backref('questao', lazy='dynamic'))

    
    # 0 - Questão de múltipla escolha
    # 1 - Questão dissertativa
    tipo = db.Column(db.Integer)

    enem = db.Column(db.Boolean)

    # Atributos próprios das questões do enem
    ano = db.Column(db.Integer)
    prova = db.Column(db.String(10)) # azul, amarelo, etc
    dia = db.Column(db.Integer) # 1 ou 2


"""
##########################################################

##### #   # ####  #     ##### #   #  ###  
#     ## ## #   # #     #     ## ## ## ## 
##### # # # ####  #     ##### # # # #   # 
#     #   # #   # #     #     #   # ##### 
##### #   # ####  ##### ##### #   # #   # 

##########################################################
"""

class Emblema(db.Model):

    __tablename__ = 'emblemas'
    
    # Dados básicos
    
    id = db.Column(db.Integer, primary_key=True)

    # Nome do Emblema
    nome = db.Column(db.String(100))

    # Descrição do Emblema
    descricao = db.Column(db.String(200))

    # Data que o emblema foi criado
    data_criacao = db.Column(db.Date())

    # Nome da imagem do emblema no sistema
    nome_imagem = db.Column(db.String(100))



"""
##########################################################

##### #   # ####  #     ##### #####  ###  #####  ###  ##### 
#   # #   # #   # #       #   #     ## ## #     ## ## #   # 
##### #   # ####  #       #   #     #   # #     #   # #   # 
#     #   # #   # #       #   #     ##### #     ##### #   # 
#     ##### ####  ##### ##### ##### #   # ##### #   # ##### 

##########################################################
"""

class Publicacao(db.Model):

    """
        id
        titulo
        subtitulo
        conteudo
        conteudo_html
        nome_foto
        n_palavras
        data_Criacao
        tipo
        idioma
        autor_id
        tags
        comentarios
        ameis
    """


    __tablename__ = 'publicacoes'

    # Dados básicos
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    # Usado em artigos do blog e lições (não é usado para publicações no mural)
    subtitulo = db.Column(db.String(100))
    conteudo = db.Column(db.Text)
    conteudo_html = db.Column(db.Text)
    nome_foto = db.Column(db.String(100))
    n_palavras = db.Column(db.Integer)
    #! alterar nome para 'data_criacao' em todas as menções
    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    """
        Tipo de Publicação

        1 - publiação mural
        2 - artigo no blog
    """
    tipo = db.Column(db.Integer)

    idioma = db.Column(db.String(8))

    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))


    # Publicacao.tags retorna as tags às quais a publicação está associada
    tags = db.relationship('Tag',
                           secondary=publicacoes_tags,
                           lazy='subquery',
                           backref=db.backref('publicacoes'))

    comentarios = db.relationship('Comentario',
                                  backref='publicacao',
                                  lazy='dynamic')
    
    ameis = db.relationship('Usuario',
                            secondary='publicacoes_amei',
                            backref=db.backref('publicacao', lazy='dynamic'))



    def __init__(self, **kwargs):

        super(Publicacao, self).__init__(**kwargs)

        self.n_palavras =  len(self.conteudo.split())



    # Converte texto em Markdown para HTML
    # Primeiro, a função markdown() faz uma conversão inicial para HTML
    # O resultado da conversão inicial é passado para a função clean(), juntamente com a lista de tags permitidas. A função clean() remove todas as tags não permitidas
    # A conversão final é feita com a função linkify(), uma função oferecida pelo Bleach que converte todos os URL escritos em texto-claro em tags âncora <a>
    # Este último passo é necessário por que geração automática de links não é uma ferramenta oficial do Markdown, mas é uma funcionalidade muito conveniente
    @staticmethod
    def conteudo_alterado(target, conteudo, conteudo_antigo, initiator):

        # Define as tags permitidas no Markdown
        tags_permitidas = ['a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h3', 'p']

        atributos_permitidos = {'*': ['class'],
                                'a': ['href', 'rel'],
                                'img': ['src', 'alt']
        }

        target.n_palavras =  len(conteudo.split())

        target.conteudo_html = bleach.linkify(
                               bleach.clean(
                                    markdown(conteudo, output_format='html'),
                                    tags=tags_permitidas,
                                    attributes=atributos_permitidos,
                                    strip=False)
        )


    # Retorna um dicionário representando dados da publicação que o cliente não consegue acessar localmente
    def json(self):

        # Declara um array vazio
        publicacao_tags = []

        # Para cada tag atribuída à publicação
        for tag in self.tags:
            # Adicione o nome da tag ao array
            publicacao_tags.append(tag.nome)

        # data = moment.create(self.data)

        # Retorne um objeto contendo as informações da publicação
        return {
            'id': self.id,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'conteudo_html': self.conteudo_html,
            'tags': publicacao_tags,
            'data_criacao': self.data_criacao,
            'idioma': self.idioma,
            'avatar_autor': self.autor.gravatar(size=50),
            'id_autor': self.autor.id,
            'comentarios': self.comentarios,
            #'ameis': self.ameis
        }

"""
##########################################################

#####  ###  ##### 
  #   ## ## #     
  #   #   # # ### 
  #   ##### #   # 
  #   #   # ##### 

##########################################################
"""

class Tag(db.Model):
    
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(128), unique=True)

    materia = db.Column(db.Integer, db.ForeignKey('materias.id'))

    @staticmethod
    def inserir_tags():

        # Lista de tags em formato chave-valor. O valor é o nome da tag que será armazenado
        tags = {
            'Series': 'series',
            'Viagem': 'viagem',
            'Entrevistas': 'entrevistas',
            'Brasil': 'brasil',
            'Estudo': 'estudo',

            'Vocabulario': 'vocabulario',
            'Gramatica': 'gramatica',
            'Pronuncia': 'pronuncia',
            'Cultura': 'cultura',

            'Ingles': 'ingles',
            'Frances': 'frances',
            'Espanhol': 'espanhol',
            'Italiano': 'italiano',
            'Alemao': 'alemao',
            'Japones': 'japones',
            'Chines': 'chines',
            'Russo': 'russo',
            'Coreano': 'coreano',
            'Árabe': 'arabe',
            'Hindi': 'hindi',

            'Tecnologia': 'tecnologia',
            'Ciências da Computação': 'ciências da computação',
            'Desenvolvimento Web': 'desenvolvimento web',
            'Inteligência Artificial': 'artificial',
            'Front-End': 'front-end',
            'Back-End': 'back-end',
            'Segurança Digital': 'segurança digital',
            'Desenvolvimento de Games': 'desenvolvimento de games',
            'Robótica': 'robotica',


            'Portugues': 'portugues',
            'Matematica': 'matematica',
            'Biologia': 'biologia',
            'Quimica': 'quimica',
            'Fisica': 'fisica',
            
            'Historia': 'historia',
            'Geografia': 'geografia',
            'Filosofia': 'filosofia',
            'Sociologia': 'sociologia',

            'Arte': 'arte',
            'Educacao Fisica': 'educacao-fisica',
        }

        """
        
        Tópicos de IDIOMAS 
        
        Gramática
        Escrita
        Pronúncia
        Leitura
        Vocabulário
        
        Conjugação de Verbo
        Pronomes
        Verbos
        Preposição
        Advérbio
        Expressões Idiomáticas


        Tópicos de TECNOLOGIA



        """

        # Para cada conjunto chave-valor
        for t, nome in tags.items():

            # Consulte o banco de dados procurando por uma 'tag' que tenha o nome igual ao de uma das 'tags' definidas no dicionário 'tags'
            tag = Tag.query.filter_by(nome=nome).first()

            # Se NÃO existir uma 'tag' com o nome informado
            if tag is None:

                # Crie uma nova 'tag'
                tag = Tag(nome=nome)

            # Adiciona a tag à sessão
            db.session.add(tag)

        # Salva as alterações no banco de dados
        db.session.commit()

"""
##########################################################

##### ##### #   # ##### #   # #####  ###  ##### ##### ##### 
#     #   # ## ## #     ##  #   #   ## ## #   #   #   #   # 
#     #   # # # # ##### # # #   #   #   # #####   #   #   # 
#     #   # #   # #     #  ##   #   ##### #  #    #   #   # 
##### ##### #   # ##### #   #   #   #   # #   # ##### ##### 

##########################################################
"""

class Comentario(db.Model):

    __tablename__ = 'comentarios'
    
    # Dados básicos
    
    id = db.Column(db.Integer, primary_key=True)
    
    conteudo = db.Column(db.Text)
    
    conteudo_html = db.Column(db.Text)
    
    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    desativado = db.Column(db.Boolean)

    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    topico_id = db.Column(db.Integer, db.ForeignKey('topicos.id'))
    licao_id = db.Column(db.Integer, db.ForeignKey('licoes.id'))
    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    publicacao_id = db.Column(db.Integer, db.ForeignKey('publicacoes.id'))


    # Função para ser chamada quando o conteúdo de um comentário for alterado
    @staticmethod
    def conteudo_alterado(target, conteudo, conteudo_antigo, initiator):

        # Define as tags permitidas no Markdown
        tags_permitidas = ['a', 'abbr', 'b', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',]

        target.conteudo_html = bleach.linkify(
                               bleach.clean(
                                    markdown(conteudo, output_format='html'),
                                    tags=tags_permitidas, strip=True)
                            )






"""
##########################################################

#   # ##### ##### ##### ##### ##### #####  ###  #####  ###  ##### 
##  # #   #   #     #   #       #   #     ## ## #     ## ## #   # 
# # # #   #   #     #   #####   #   #     #   # #     #   # #   # 
#  ## #   #   #     #   #       #   #     ##### #     ##### #   # 
#   # #####   #   ##### #     ##### ##### #   # ##### #   # ##### 

##########################################################
"""

"""
  @@    @@    @@  
  @@    @@    @@  
  @@    @@    @@  
                  
  @@    @@    @@  
"""


class Notificacao(db.Model):

    """
    
    Eventos que criam uma notificacao

    Completar um tópico
    Completar um curso

    Receber um emblema

    Criar uma publicação
    Ter a publicação comentada
    Ter a publicação banida/excluida
    Ter a publicação amada
    
    Mensagem do sistema
    
    """

    id = db.Column(db.Integer, primary_key=True)

    conteudo = db.Column(db.String)

    notificado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    lida = db.Column(db.Boolean)


"""
##########################################################

##### #   # ##### ##### #####  ###  ##### ##### ##### ##### 
  #   ##  #   #   #     #   # ## ## #     #   # #     #     
  #   # # #   #   ##### ##### #   # #     #   # ##### ##### 
  #   #  ##   #   #     #  #  ##### #     #   # #         # 
##### #   #   #   ##### #   # #   # ##### ##### ##### ##### 

##########################################################
"""

class TopicoAmei(db.Model):

    __tablename__ = 'topicos_amei'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    topico_id = db.Column(db.Integer, db.ForeignKey('topicos.id'))


class LicaoAmei(db.Model):

    __tablename__ = 'licoes_amei'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    licao_id = db.Column(db.Integer, db.ForeignKey('licoes.id'))


class QuestaoAmei(db.Model):

    __tablename__ = 'questoes_amei'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'))


class PublicacaoAmei(db.Model):

    __tablename__ = 'publicacoes_amei'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    publicacao_id = db.Column(db.Integer, db.ForeignKey('publicacoes.id'))


class ComentarioAmei(db.Model):

    __tablename__ = 'comentarios_amei'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    comentario_id = db.Column(db.Integer, db.ForeignKey('comentarios.id'))



"""
##########################################################

#     ##### #####  ###  
#     #   #    #  ## ## 
#     #   #    #  #   # 
#     #   # #  #  ##### 
##### ##### ####  #   # 

##########################################################
"""

"""
  @@    @@    @@  
  @@    @@    @@  
  @@    @@    @@  
                  
  @@    @@    @@  
"""

# LOJA

# Pedidos

"""

class Pedido(db.Model):

    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    pedido_local = db.Column(db.String)

    telefone = db.Column(db.String)

    entrega_status = db.Column(db.Boolean)

    pedido_data = db.Column(db.DateTime, default=datetime.utcnow)

    entrega_id = db.Column(db.Integer, db.ForeignKey('entregas.id'))


class PedidoItem(db.Model):

    __tablename__ = 'pedidos_itens'

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))

    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'))

    quantidade = db.Column(db.SmallInteger)


class Produto(db.Model):

    __tablename__ = 'produtos'
"""

#class Entrega(db.Model)
# Produto

# Produto Caracteristicas

# Produto Visita


"""
##########################################################

##### ##### #   # ##### ##### ##### 
#     #   # ##  # #       #   #     
#     #   # # # # #####   #   # ### 
#     #   # #  ## #       #   #   # 
##### ##### #   # #     ##### ##### 

##########################################################
"""


# Esta classe, 'UsuarioAnonimo', permite chamar a função current_user.pode() e current_user.e_administrador() sem ter que checar se o usuário está conectado. E nós informamos à Flask-Login para usar a classe 'UsuarioAnonimo', ao definirmos o atributo 'login_manager.anonymous_user'
class UsuarioAnonimo(AnonymousUserMixin):

    confirmado = False

    # Um usuário anônimo não possui permissões
    def pode(self, permissoes):
        return False

    # Um usuário anônimo não é Administrador
    def e_administrador(self):
        return False


# O decorador login_manager.user_loader registra a função com Flask-Login, que o chamará quando precisar acessar informação sobre um usuário conectado.  A função recebe o id do usuário e retorna o objeto usuario, ou None se o id do usuário for inválido ou algum outro erro ocorrer
@login_manager.user_loader
def carregar_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))


# Define o modelo que representa 'anonymous_user'
login_manager.anonymous_user = UsuarioAnonimo


# Esta função é invocada sempre que o campo 'conteudo' de uma publicação for alterado
db.event.listen(Publicacao.conteudo, 'set', Publicacao.conteudo_alterado)


# Esta função é invocada sempre que o campo 'conteudo' de um comentário for alterado
db.event.listen(Comentario.conteudo, 'set', Comentario.conteudo_alterado)
