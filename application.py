import os

from flask import Flask, request, redirect, render_template, session, url_for, flash

# Framework de Banco de Dados
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

# Extensão para organização de templates
from flask_bootstrap import Bootstrap

# Extensão JS para gerar datas e horários
from flask_moment import Moment


from datetime import datetime

# Extensão para geração de formulários
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



# Aplicativo
app = Flask(__name__)

# Chave que será usada para criptografia
app.config['SECRET_KEY'] = 'string dificil de adivinhar'

# Garante que templates sejam recarregados automaticamente
app.config["TEMPLATES_AUTO_RELOAD"] = True

# URL e credenciais do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://exqdszeqeyyown:e9883196fb9334c39ae22f6ab0a9551fae2fd84a160a3eabb60fc389f05fafef@ec2-54-224-124-241.compute-1.amazonaws.com:5432/d1qrd6u769udv2'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

bootstrap = Bootstrap(app)

moment = Moment(app)


# Formulário
class FormularioNome(FlaskForm):
    nome_usuario = StringField('Qual é seu nome?', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

# Tabela Usuários
class Usuario(db.Model):
    # Nome da tabela
    __tablename__ = 'usuarios'
    # Id do registro
    id = db.Column(db.Integer, primary_key=True)
    # Nome para fazer login
    nome_login = db.Column(db.String(32), unique=True)
    # Nome exibido no app
    nome_usuario = db.Column(db.String(32), unique=True, index=True)
    
    # Hash da senha do usuário
    hash_senha = db.Column(db.String(32))

    # Referencia o id de uma das 'roles'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<Usuário %r>' % self.nome_usuario

# Tabela Roles
class Role(db.Model):
    __tablename__ = 'roles'
    # Id do registro
    id = db.Column(db.Integer, primary_key=True)
    # Nome do role
    nome = db.Column(db.String(32), unique=True)

    # Acessa todos os usuários com a 'role'
    usuarios = db.relationship('Usuario', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.nome


# Importa os objetos automaticamente para o flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Usuario=Usuario, Role=Role)

@app.route('/', methods=['GET', 'POST'])
def inicio():

    # Formulário
    formulario = FormularioNome()

    # Se o método for POST
    if formulario.validate_on_submit():

        # Checa se já existe um usuário com o nome de usuário informado
        usuario = Usuario.query.filter_by(nome_usuario=formulario.nome_usuario.data).first()

        # Se o nome de usuário informado estiver disponível
        if usuario is None:
            # Cria o objeto usuário, contendo o nome informado no formulário
            usuario = Usuario(nome_usuario=formulario.nome_usuario.data)
            # Adiciona 'usuario' na lista de modificações do banco de dados
            db.session.add(usuario)
            # Faz alteraações no banco de dados
            db.session.commit()
            # Define 'secao_gravada' como sendo falso
            session['secao_gravada'] = False
        else:
            # ??? POR QUE
            session['secao_gravada'] = True
        # ?
        session['nome_usuario'] = formulario.nome_usuario.data
        #?
        formulario.nome_usuario.data = ''
        #?
        return redirect(url_for('inicio'))
    #?
    return render_template('inicio.html',
    formulario=formulario, nome_usuario=session.get('nome_usuario'),
    secao_gravada=session.get('secao_gravada', False))


'''
@app.route('/', methods=['GET', 'POST'])
def inicio():

    # Cria (?) formulário a partir da classe 'FormularioNome'
    formulario = FormularioNome()

    # Se o método for POST
    if formulario.validate_on_submit():

        # Grava o nome do usuário armazenado na sessão
        nome_antigo = session.get('nome')

        # Se o nome antigo existir e for diferente do nome inserido no formulário
        if nome_antigo is not None and nome_antigo != formulario.nome.data:
            # O usuário trocou de nome
            flash('Você trocou de nome!')
        
        # Armazena o nome na sessão
        session['nome'] = formulario.nome.data
        # Redireciona para a função 'inicio' com um método GET
        return redirect(url_for('inicio'))

    # Se o método for GET
    # Carrega a página, juntamente com as variáveis
    return render_template('inicio.html',
    formulario=formulario,
    nome=session.get('nome'),
    current_time=datetime.utcnow())
'''

@app.route('/usuario/<nome>')
def usuario(nome):
    return render_template('usuario.html', nome=nome.capitalize())



# Erro 404 - Página Não Encontrada
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

# Erro 500 - Erro Interno do Servidor
@app.errorhandler(500)
def erro_interno(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)