from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager



# Lista de permissões dos 'roles'
class Permissao:
    # Seguir murais e usuários
    SEGUIR = 1

    # Comentar em artigos do blog, lições dos cursos e publicações no mural
    COMENTAR = 2

    # Apagar comentários, fechar discussões, etiqueta de usuário destacada 
    MODERAR_INGLES = 4
    MODERAR_FRANCES = 8
    MODERAR_ESPANHOL = 16
    MODERAR_ITALIANO = 32
    MODERAR_ALEMAO = 64
    MODERAR_JAPONES = 128
    MODERAR_CHINES = 256

    # Criar publicações destacadas e eventos no mural
    PROF_INGLES = 512
    PROF_FRANCES = 1024
    PROF_ESPANHOL = 2048
    PROF_ITALIANO = 4096
    PROF_ALEMAO = 8192
    PROF_JAPONES = 16384
    PROF_CHINES = 32768

    # Fazer publicações no blog
    ESCREVER_BLOG = 65536

    # Permissões de administrador
    ADMIN = 131072

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    # Apenas um "role" pode ter o atributo 'padrao' igual a True. O "role" marcado como "padrao" será o "role" atribuído a novos usuários durante a inscrição. Considerando que o app vai consultar a tabela 'roles' para encontrar o 'role' padrão, esta coluna está configurada para ter um índice, dado que isto faz a consulta ser mais rápida 
    padrao = db.Column(db.Boolean, default=False, index=True)
    permissoes = db.Column(db.Integer)
    # Relação com a tabea 'usuarios'
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
                Permissao.COMENTAR
                ],
            'ModeradorIngles': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_INGLES
                ],
            'ModeradorFrances': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_FRANCES
                ],
            'ModeradorEspanhol': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_ESPANHOL
                ],
            'ModeradorItaliano': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_ITALIANO
                ],
            'ModeradorAlemao': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_ALEMAO
                ],
            'ModeradorJapones': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_JAPONES
                ],
            'ModeradorChines': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.MODERAR_CHINES
                ],
            'ProfessorIngles': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_INGLES
                ],
            'ProfessorFrances': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_FRANCES
                ],
            'ProfessorEspanhol': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_ESPANHOL
                ],
            'ProfessorItaliano': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_ITALIANO
                ],
            'ProfessorAlemao': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_ALEMAO
                ],
            'ProfessorJapones': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_JAPONES
                ],
            'ProfessorChines': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
                Permissao.ESCREVER_BLOG,
                Permissao.PROF_CHINES
                ],
            'Administrador': [
                Permissao.SEGUIR,
                Permissao.COMENTAR,
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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True,)
    nome_usuario = db.Column(db.String(64), unique=True, index=True)
    senha_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmado = db.Column(db.Boolean, default=False)

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

    @property
    def senha(self):
        raise AttributeError('senha não é um atributo de leitura')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # Este método recebe a senha e passa ela na função check_password_hash() para a comparar com a hash armazenada no modelo 'Usuario'.
    # Se retornar True, a senha está correta
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

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
        db.session.add(self)
        return True



    # Checa se o usuário pode fazer determinada ação
    def pode(self, permissao):
        # Se a 'role' do usuário NÃO for None e se a 'role' possuir a permissão, retorne True
        return self.role is not None and self.role.tem_permissao(permissao)

    # Checa se o usuário é um Administrador
    def e_administrador(self):
        # Checa se o usuário tem permissão de Adminstrador
        return self.pode(Permissao.ADMIN)

    def __repr__(self):
        return '<Usuário %r>' % self.nome_usuario

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
