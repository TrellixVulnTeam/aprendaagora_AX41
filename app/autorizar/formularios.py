from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..modelos import Usuario



# Formulário para o usuário acessar sua conta
# O campo email usa os validadores Length() e Email(), além de DataRequired(), para garantir que o usuário informe a este campo não apenas um valor, mas um valor que seja válido
# Formulários WTF avaliarão os validadores por ordem, e no caso de uma falha de validação, a mensagem de erro mostrada será do primeiro validador que falhou
class formularioEntrar(FlaskForm):

    email = StringField('E-mail', validators=[DataRequired(message="É necessário informar o seu endereço de email."), Length(1, 64),
                                             Email()])
    senha = PasswordField('Senha', validators=[DataRequired(message="É necessário informar a sua senha.")])
    lembrar_me = BooleanField('Manter-me conectado')
    enviar = SubmitField('Entrar')

# Formulário para um visitante criar sua própria conta
class formularioInscricao(FlaskForm):

    email = StringField('Email', validators=[
        DataRequired(message="É necessário informar um endereço de email."),
        Length(1, 64),
        Email(message="O endereço de email informado é inválido.")])

    # O validador Regexp está sendo usado para garantir que o campo 'nome_usuario' começa com uma letra e contém apenas letras, números, undercores e pontos
    nome_usuario = StringField('Nome de Usuário', validators=[
        DataRequired(message="É necessário informar um nome de usuário."),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        "Seu nome de usuário deve começar com uma letra e só pode conter letras, números, pontos, e o símbolo traço baixo (a-z, A-Z, 0-9, '.' e '_').")
    ])

    # O campo 'senha' possui um validador EqualTo que testa se os campos 'senha' e 'senha2' contém o mesmo conteúdo
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        EqualTo('senha2',  message="As senhas devem ser iguais.")])
    
    senha2 = PasswordField('Confirmar senha', validators=[
        DataRequired()])

    enviar = SubmitField('Se Inscrever')


    # Quando um formulário define um método com o prefixo validate_, seguido do nome de um campo do formulário, o método é invocado juntamente com quaisquer validadores definidos normalmente. Os dois validadores abaixo garantem que emails e nomes de usuários que já estão em uso não sejam usados para criar novas contas.

    # Checha se o email já está sendo usado
    def validate_email(self, campo):
        if Usuario.query.filter_by(email=campo.data).first():
            raise ValidationError("Este email já foi cadastrado.")

    # Checa se o nome de usuário já está sendo usado
    def validate_nome_usuario(self, campo):
        if Usuario.query.filter_by(nome_usuario=campo.data).first():
            raise ValidationError("Este nome de usuário já foi cadastrado.")

# Formulário para um usuário trocar de senha
class formularioTrocarSenha(FlaskForm):

    senha_antiga = PasswordField('Senha antiga', validators=[DataRequired()])

    nova_senha = PasswordField('Nova senha', validators=[DataRequired(), EqualTo('nova_senha2', message='As senhas devem ser iguais.')])

    nova_senha2 = PasswordField('Confirme a nova senha', validators=[DataRequired()])

    enviar = SubmitField('Atualizar Senha')

# Formulário para um usuário pedir a troca de senha
class formularioPedirRedefinirSenha(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])

    enviar = SubmitField('Trocar Senha')

# Formulário para um usuário redefinir (resetar) a senha
class formularioRedefinirSenha(FlaskForm):

    senha = PasswordField('Nova senha', validators=[DataRequired(), EqualTo('senha2', message='As senhas devem ser iguais.')])

    senha2 = PasswordField('Confirmar senha', validators=[DataRequired()])

    enviar = SubmitField('Redefinir Senha')

# Formulário para um usuário trocar o email vinculado à conta
class formularioTrocarEmail(FlaskForm):

    email = StringField("Novo email", validators=[DataRequired()])

    senha = PasswordField("Senha", validators=[DataRequired()])

    enviar = SubmitField("Trocar Endereço de Email")

    def validar_email(self, campo):

        if Usuario.query.filter_by(email=campo.data.lower()).first():

            raise ValidationError("Este email á está registrado a uma conta.")




