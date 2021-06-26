import hashlib
from markdown import markdown
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from datetime import datetime


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

    # Permissões de administrador
    ADMIN = 262144


class InscricaoFeuRosa(db.Model):
    __tablename__ = 'inscricoes_feu_rosa'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(64))

    email = db.Column(db.String(32))

    numero_telefone = db.Column(db.String(32))

    curso = db.Column(db.String(16))

    horario = db.Column(db.String(16))


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
    # Perceba também que inserir_roles() é um método estático, um tipo especial de método que não exige que um objeto seja criado pois ele pode ser invocado a partir da classe, escrevendo por exemplo Role.inserir_roles(). Métodos estáticos não recebem um argumento 'self' como métodos de instâncias.
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


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    # Dados básicos
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True,)
    nome_usuario = db.Column(db.String(25), unique=True, index=True)
    senha_hash = db.Column(db.String(128))
    
    # Informação adicional do usuário
    nome = db.Column(db.String(64))
    sobrenome = db.Column(db.String(64))
    localizacao = db.Column(db.String(64))
    sobre = db.Column(db.String(100))
    
    #  Id do 'role' do usuário
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # Conta confirmada
    confirmado = db.Column(db.Boolean, default=False)

    # Dados relacionados à datas
    membro_desde = db.Column(db.DateTime(), default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime(), default=datetime.utcnow)

    avatar_hash = db.Column(db.String(32))

    # Usuario.publicacoes retorna a lista de publicações escritas pelo usuário
    publicacoes = db.relationship('Publicacao',
                                  backref='autor',
                                  lazy='dynamic')

    # Usuario.comentarios retorna a lista de comentários escritos pelo usuário
    comentarios = db.relationship('Comentario',
                                  backref='autor',
                                  lazy='dynamic')


    publicacoes_amei = db.relationship('PublicacaoAmei',
                                       foreign_keys='PublicacaoAmei.usuario_id',
                                       backref='usuario',
                                       lazy='dynamic')

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

    @property
    def senha(self):
        raise AttributeError('senha não é um atributo de leitura')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)



    # FUNÇÕES DE AMAR PUBLICAÇÃO

    def amar_publicacao(self, publicacao):

        if not self.amou_publicacao(publicacao):

            amou = PublicacaoAmei(usuario_id=self.id, publicacao_id=publicacao.id)
            
            db.session.add(amou)

    def desfazer_amar_publicacao(self, publicacao):

        if self.amou_publicacao(publicacao):

            PublicacaoAmei.query.filter_by(
                usuario_id=self.id,
                publicacao_id=publicacao.id).delete()

    def amou_publicacao(self, publicacao):

        return PublicacaoAmei.query.filter(
                PublicacaoAmei.usuario_id == self.id,
                PublicacaoAmei.publicacao_id == publicacao.id).count() > 0


    # Este método recebe a senha e passa ela na função check_password_hash() para a comparar com a hash armazenada no modelo 'Usuario'.
    # Se retornar True, a senha está correta
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    # Gera um token para o usuário confirmar sua conta
    def gerar_token_confirmacao(self, expiracao=3600):

        s = Serializer(current_app.config['SECRET_KEY'], expiracao)
        return s.dumps({'confirmado': self.id}).decode('utf-8')
    
    def confirmar(self, token):

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            dados = s.loads(token.encode('utf-8'))
        except:
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

    @staticmethod
    def redefinir_senha(token, nova_senha):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            dados = s.loads(token.encode('utf-8'))
        except:
            return False
        
        usuario = Usuario.query.get(dados.get('id_usuario'))

        if usuario is None:
            return False

        usuario.senha = nova_senha
        
        db.session.add(usuario)

        return True

    def gerar_token_trocar_email(self, novo_email, expiracao=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiracao)
        return s.dumps(
            {'id_usuario': self.id, 'novo_email': novo_email}).decode('utf-8')

    # Redefine o email de um usuário
    # Comentar a função
    def trocar_email(self, token):

        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            dados = s.loads(token.encode('utf-8'))
        except:
            return False

        if dados.get('id_usuario') != self.id:
            return False

        novo_email = dados.get('novo_email')

        if novo_email is None:
            return False

        if self.query.filter_by(email=novo_email).first() is not None:
            return False

        self.email = novo_email
        # Redefine o 'avatar_hash' baseado no novo email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

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

    def __repr__(self):
        return '<Usuário %r>' % self.nome_usuario

# Relação entre publicações e tags
publicacoes_tags = db.Table(
    
    'publicacoes_tags',

    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),

    db.Column('publicacao_id', db.Integer, db.ForeignKey('publicacoes.id'), primary_key=True)
)

class Publicacao(db.Model):

    __tablename__ = 'publicacoes'

    id = db.Column(db.Integer, primary_key=True)

    # Título da publicação em formato string
    titulo = db.Column(db.String(100))
    
    # Conteúdo da publicação em formato string
    conteudo = db.Column(db.Text)

    conteudo_html = db.Column(db.Text)
    
    data = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    idioma = db.Column(db.String(8))

    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # Publicacao.tags retorna as tags às quais ma publicação está associada
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

    # Converte texto em Markdown para HTML
    # Primeiro, a função markdown() faz uma conversão inicial para HTML
    # O resultado da conversão inicial é passado para a função clean(), juntamente com a lista de tags permitidas. A função clean() remove todas as tags não permitidas
    # A conversão final é feita com a função linkify(), uma função oferecida pelo Bleach que converte todos os URL escritos em texto-claro em tags âncora <a>
    # Este último passo é necessário por que geração automática de links não é uma ferramenta oficial do Markdown, mas é uma funcionalidade muito conveniente
    @staticmethod
    def conteudo_alterado(target, conteudo, conteudo_antigo, initiator):
        tags_permitidas = ['a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h3', 'p']

        target.conteudo_html = bleach.linkify(bleach.clean(
            markdown(conteudo, output_format='html'),
            tags=tags_permitidas, strip=True))


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
            'data': self.data,
            'idioma': self.idioma,
            'avatar_autor': self.autor.gravatar(size=50),
            'id_autor': self.autor.id,
            'comentarios': self.comentarios,
            #'ameis': self.ameis
        }


class Comentario(db.Model):

    __tablename__ = 'comentarios'
    
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text)
    conteudo_html = db.Column(db.Text)
    data = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    desativado = db.Column(db.Boolean)

    # id do autor do comentário
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # id da publicação onde o comentário foi feito
    publicacao_id = db.Column(db.Integer, db.ForeignKey('publicacoes.id'))

    @staticmethod
    def conteudo_alterado(target, conteudo, conteudo_antigo, initiator):
        tags_permitidas = ['a', 'abbr', 'b', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',]

        target.conteudo_html = bleach.linkify(bleach.clean(
            markdown(conteudo, output_format='html'),
            tags=tags_permitidas, strip=True))


class PublicacaoAmei(db.Model):

    __tablename__ = 'publicacoes_amei'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    publicacao_id = db.Column(db.Integer, db.ForeignKey('publicacoes.id'))




# As tags de uma publicação podem ser acessadas com publicacao.tags
class Tag(db.Model):
    
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(16), unique=True)

    @staticmethod
    def inserir_tags():

        # Lista de tags em formato chave-valor. O valor é o nome da tag que será armazenado
        tags = {
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
            'Series': 'series',
            'Viagem': 'viagem',
            'Entrevistas': 'entrevistas',
            'Brasil': 'brasil',
            'Estudo': 'estudo',
        }

        for t, nome in tags.items():

            # Consulte o banco de dados procurando por uma 'tag' que tenha o nome igual ao de uma das 'tags' definidas no dicionnário 'tags'
            tag = Tag.query.filter_by(nome=nome).first()

            # Se NÃO existir uma 'tag' com o nome informado
            if tag is None:
                # Crie uma nova 'tag'
                tag = Tag(nome=nome)

            db.session.add(tag)

        db.session.commit()


# Esta classe, 'UsuarioAnonimo', permite chamar a função current_user.pode() e current_user.e_administrador() sem ter que checar se o usuário está conectado. E nós informamos à Flask-Login para usar a classe 'UsuarioAnonimo', ao definirmos o atributo 'login_manager.anonymous_user'
class UsuarioAnonimo(AnonymousUserMixin):

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


login_manager.anonymous_user = UsuarioAnonimo


# Esta função é invocada sempre que o campo 'conteudo' de uma publicação for alterado
db.event.listen(Publicacao.conteudo, 'set', Publicacao.conteudo_alterado)


# Esta função é invocada sempre que o campo 'conteudo' de um comentário for alterado
db.event.listen(Comentario.conteudo, 'set', Comentario.conteudo_alterado)
