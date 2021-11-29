from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..modelos import Usuario, Role, Publicacao, Role


class formularioInscricaoFeuRosa(FlaskForm):

    nome = StringField("Nome e sobrenome",
                       validators=[DataRequired(message='É necessário informar seu nome e sobrenome'),
                                   Length(0, 40)])
    
    email = StringField("Email",
                        validators=[DataRequired(message='É necessário informar seu email (que será usado para envio de materiais de estudo).'),
                                    Length(1, 64),
                                    Email(message='Endereço de email inválido. Digite seu email corretamente.')])

    numero_telefone = StringField("Número de Telefone (WhatsApp)",
                                  validators=[DataRequired(message='É necessário informar seu número de telefone (WhatsApp) para podermos entrar em contato com você.'),
                                              Length(1, 64)])

    opcao_curso = RadioField("Opção de Curso (escolha apenas um curso)", choices=[('ingles','Inglês 🇺🇸'),
                                      ('frances','Francês 🇫🇷'),
                                      ('programacao', 'Programação 💻')])

    horario = RadioField("Horário do Curso (escolha apenas um horário)", choices=[('segunda', 'Segunda-Feira, de 20:00 até 22:00'), ('terça', 'Terça-Feira, de 20:00 até 22:00'), ('quarta', 'Quarta-Feira, de 20:00 até 22:00'), ('quinta', 'Quinta-Feira, de 20:00 até 22:00'), ('domingo1', 'Domingo, de 14:00 até 16:00'), ('domingo2', 'Domingo, de 16:30 até 18:30')])

    enviar = SubmitField("Se Inscrever")

class formularioEditarPerfil(FlaskForm):

    nome_usuario = StringField("Nome de usuário", validators=[Length(0, 20)])

    nome = StringField("Nome", validators=[Length(0, 64)])
    
    sobrenome = StringField("Sobrenome", validators=[Length(0, 64)])
    
    localizacao = StringField("Localização", validators=[Length(0, 64)])
    
    sobre = TextAreaField("Sobre mim", validators=[Length(0, 100)])
    
    enviar = SubmitField("Salvar alterações")

class formularioEditarPerfilAdmin(FlaskForm):

    email = StringField("Email",
            validators=[DataRequired(),
                        Length(1, 64),
                        Email()])

    nome_usuario = StringField("Nome de Usuário",
            validators=[DataRequired(),
                        Length(1, 64),
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                        "Seu nome de usuário deve começar com uma letra e só pode conter letras, números, pontos, e o símbolo traço baixo (a-z, A-Z, 0-9, '.' e '_').")])

    confirmado = BooleanField("Confirmado")

    # A classe 'SelectField' deve ter as opções definidas no atributo 'choices'. Elas devem ser recebidas como sendo uma lista de tuplas, cada uma consistindo de dois valures: um identificador para a opção e o texto a ser exibido no item.
    # A lista 'choices' é definida no construtor do formulário, onde os valores são obtidos a partir do modelo 'Role', através de uma consulta que ordena todos os 'roles' alfabeticamente.
    # O identificador de cada tupla é definido como sendo o id de cada 'role', e por estes serem inteiros, nós usamos o argumento 'coerce=int' para que os valores nas opções sejam armazenamos como sendo inteiros, e não strings, que é o padrão.
    role = SelectField("Role", coerce=int)

    nome = StringField("Nome", validators=[Length(0, 64)])

    sobrenome = StringField("Sobrenome", validators=[Length(0, 64)])

    localizacao = StringField("Localização", validators=[Length(0, 64)])

    sobre = TextAreaField("Sobre", validators=[Length(0, 100)])

    enviar = SubmitField("Salvar alterações")

    # Para implementar a lógica de validação do email e do nome de usuário, o construtor do formulário recebe o objeto 'Usuario' como argumento e salva ele em uma variável, que é mais tarde usado nos métodos de validação personalizados
    def __init__(self, usuario, *args, **kwargs):

        super(formularioEditarPerfilAdmin, self).__init__(*args, **kwargs)
        
        self.role.choices = [(role.id, role.nome)
                              for role in Role.query.order_by(Role.nome).all()]

        self.usuario = usuario

    # Declara ValidationError se o email não puder ser usado
    def validar_email(self, campo):

        # Se o email informado no formulário for diferente do email do usuario da conta sendo alterada e, alem disso, já houver uma outra conta vinculada ao email informado no formulário
        if campo.data != self.usuario.email and Usuario.query.filter_by(email=campo.data).first():
            # Indique o ERRO
            raise ValidationError("Email já está vinculado a uma conta.")

    # Declara ValidationError se o email não puder ser usado
    def validar_nome_usuario(self, campo):

        # Se o nome de usuário informado no formulário for diferente do nome de usuário do usuario da conta sendo alterada e, além disso, já houver uma outra conta usando o nome de usuário informado no formulário
        if campo.data != self.usuario.nome_usuario and Usuario.query.filter_by(nome_usuario=campo.data).first():
            # Indique o ERRO
            raise ValidationError("Este nome de usuário já está sendo usado.")

