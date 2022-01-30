from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileRequired

from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    BooleanField,
    SubmitField,
    TextAreaField,
    widgets
)

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp
)

from wtforms import ValidationError

from ..modelos import (
    Usuario,
    Role,
    Publicacao,
    Tag
)

from flask_pagedown.fields import PageDownField





class MultiCheckboxField(SelectMultipleField):

    """
    Um elemento de formulário do tipo 'multiple-select', entretanto isto exibe uma lista de caixas de seleção
    
    Percorrer o elemento produz os sub-elementos, permitindo exibir as caixas de marcação individuais de forma personalizada

    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# Campo que é preenchido dinamicamente através de um pedido AJAX e que inclui validação automática
class SelectFieldSemValidacao(SelectField):
    def pre_validate(self, form):
        pass

"""

NÃO IMPLEMENTADO

class SelectFieldMaterias(SelectField):

    choices=[
            ('ingles', 'Inglês'),
            ('espanhol', 'Espanhol'),
            ('frances', 'Francês'),
            ('italiano', 'Italiano'),
            ('alemao', 'Alemão'),
            ('chines', 'Chinês'),
            ('japones', 'Japonês'),
            ('russo', 'Russo'),
            ('arabe', 'Árabe'),
            ('coreano', 'Coreano'),

            ('portugues', 'Português'),
            ('matematica', 'Matemática'),
            ('biologia', 'Biologia'),
            ('quimica', 'Química'),
            ('fisica', 'Física'),
            ('historia', 'História'),
            ('geografia', 'Geografia'),
            ('filosofia', 'Filosofia'),
            ('sociologia', 'Sociologia'),
            ('arte', 'Arte'),
    ]
"""

class formularioArtigoPainel(FlaskForm):

    titulo = StringField("Título da publicação", validators=[DataRequired()])

    subtitulo = StringField("Subtítulo da publicação", validators=[DataRequired()])

    conteudo = PageDownField("Conteúdo da publicação", validators=[DataRequired()])

    foto = FileField(validators=[FileRequired()])

    tags = MultiCheckboxField("Assunto da publicação", coerce=int)

    def __init__(self, *args, **kwargs):

        super(formularioArtigoPainel, self).__init__(*args, *kwargs)

        # Seleciona as tags (TODAS!)

        """
        Como selecionar o id e o nome das tags
        """
        # tag.id será o valor do input
        # tag.nome será o label
        self.tags.choices = [(tag.id, tag.nome)
                              for tag in Tag.query.order_by(Tag.id).all()]


class formularioCursoPainel(FlaskForm):

    # Campos
    """
        materia
        nome
        nivel
        instrutor
        descricao
        foto
    """

    materia = SelectField(
        'Matéria/Área do Conhecimento',
        choices=[
            ('ingles', 'Inglês'),
            ('espanhol', 'Espanhol'),
            ('frances', 'Francês'),
            ('italiano', 'Italiano'),
            ('alemao', 'Alemão'),
            ('chines', 'Chinês'),
            ('japones', 'Japonês'),
            ('russo', 'Russo'),
            ('arabe', 'Árabe'),
            ('coreano', 'Coreano'),

            ('portugues', 'Português'),
            ('matematica', 'Matemática'),
            ('biologia', 'Biologia'),
            ('quimica', 'Química'),
            ('fisica', 'Física'),
            ('historia', 'História'),
            ('geografia', 'Geografia'),
            ('filosofia', 'Filosofia'),
            ('sociologia', 'Sociologia'),
            ('arte', 'Arte'),
        ]
    )

    nome = StringField("Nome do curso", validators=[DataRequired()])

    nivel = SelectField(
        'Nível do Curso',
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10 (1º Ano)'),
            ('11', '11 (2º Ano)'),
            ('12', '12 (3º Ano)'),
        ]
    )

    instrutor = SelectField(
        "Instrutor",
        choices=[
            ('ramon', 'Ramon'),
            ('rodrigo', 'Rodrigo'),
        ]
    )

    descricao = StringField("Descrição", validators=[DataRequired()])

    foto = FileField(validators=[FileRequired()])

    enviar = SubmitField('Criar Curso')


class formularioTopicoPainel(FlaskForm):


    materia = SelectField(
        'Matéria/Área do Conhecimento',
        choices=[
            ('ingles', 'Inglês'),
            ('espanhol', 'Espanhol'),
            ('frances', 'Francês'),
            ('italiano', 'Italiano'),
            ('alemao', 'Alemão'),
            ('chines', 'Chinês'),
            ('japones', 'Japonês'),
            ('russo', 'Russo'),
            ('arabe', 'Árabe'),
            ('coreano', 'Coreano'),

            ('portugues', 'Português'),
            ('matematica', 'Matemática'),
            ('biologia', 'Biologia'),
            ('quimica', 'Química'),
            ('fisica', 'Física'),
            ('historia', 'História'),
            ('geografia', 'Geografia'),
            ('filosofia', 'Filosofia'),
            ('sociologia', 'Sociologia'),
            ('arte', 'Arte'),
        ]
    )

    # A classe 'SelectField' valida as opções automaticamente, e caso a opção seleciona não seja válida, a classe interrompe o envio do formulário
    curso = SelectFieldSemValidacao(
        'Curso',
        choices=[
            ('', ''),
        ],
    )

    titulo = StringField("Título do Tópico", validators=[DataRequired()])

    descricao = TextAreaField("Descrição do Tópico", validators=[DataRequired()])

    foto = FileField(validators=[FileRequired()])

    enviar = SubmitField('Criar Tópico')


class formularioLicaoPainel(FlaskForm):

    materia = SelectField(
        'Matéria/Área do Conhecimento',
        choices=[
            ('ingles', 'Inglês'),
            ('espanhol', 'Espanhol'),
            ('frances', 'Francês'),
            ('italiano', 'Italiano'),
            ('alemao', 'Alemão'),
            ('chines', 'Chinês'),
            ('japones', 'Japonês'),
            ('russo', 'Russo'),
            ('arabe', 'Árabe'),
            ('coreano', 'Coreano'),

            ('portugues', 'Português'),
            ('matematica', 'Matemática'),
            ('biologia', 'Biologia'),
            ('quimica', 'Química'),
            ('fisica', 'Física'),
            ('historia', 'História'),
            ('geografia', 'Geografia'),
            ('filosofia', 'Filosofia'),
            ('sociologia', 'Sociologia'),
            ('arte', 'Arte'),
        ]
    )

    curso = SelectFieldSemValidacao(
        'Curso',
        choices=[
            ('', ''),
        ],
    )

    topico = SelectFieldSemValidacao(
        'Tópico',
        choices=[
            ('', ''),
        ],
    )

    titulo = StringField("Título da lição")

    subtitulo = StringField("Subtítulo da lição")

    foto = FileField(validators=[FileRequired()])

    conteudo = TextAreaField("Conteúdo")

    enviar = SubmitField('Criar Curso')


class formularioQuestaoPainel(FlaskForm):

    materia = SelectField(
        'Matéria/Área do Conhecimento',
        choices=[
            ('ingles', '🇺🇸 Inglês'),
            ('espanhol', '🇪🇸 Espanhol'),
            ('frances', '🇫🇷 Francês'),
            ('italiano', '🇮🇹 Italiano'),
            ('alemao', '🇩🇪 Alemão'),
            ('chines', '🇨🇳 Chinês'),
            ('japones', '🇯🇵 Japonês'),

            ('portugues', '🎠 Português'),
            ('matematica', '📊 Matemática'),
            ('biologia', '🌱 Biologia'),
            ('quimica', '🔥 Química'),
            ('fisica', '💡 Física'),
            ('historia', '⏳ História'),
            ('geografia', '🌎 Geografia'),
            ('filosofia', '💭 Filosofia'),
            ('sociologia', '👥 Sociologia'),
            ('arte', '🎨 Arte'),
        ]
    )

    curso = SelectFieldSemValidacao(
        'Curso',
        choices=[
            ('', ''),
        ],
    )

    topico = SelectFieldSemValidacao(
        'Tópico',
        choices=[
            ('', ''),
        ],
    )

    licao = SelectFieldSemValidacao(
        'Lição',
        choices=[
            ('', ''),
        ],
    )

    titulo = StringField("Título da Questão", validators=[DataRequired()])

    enunciado = TextAreaField("Enunciado da Questão", validators=[DataRequired()])
    
    nivel = SelectField('Nível',
        choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ])

    opcaoa = StringField("Opção A (Opção correta)")
    opcaob = StringField("Opção B")
    opcaoc = StringField("Opção C")
    opcaod = StringField("Opção D")
    opcaoe = StringField("Opção E")

    explicacao = TextAreaField("Explicação da Resolução")
    
    enem = BooleanField("Questão do Enem")

    ano = SelectField(
        'Ano',
        choices=[
            ('2005', '2005'),
            ('2006', '2006'),
            ('2007', '2007'),
            ('2008', '2008'),
            ('2009', '2009'),
            ('2010', '2010'),
            ('2011', '2011'),
            ('2012', '2012'),
            ('2013', '2013'),
            ('2014', '2014'),
            ('2015', '2015'),
            ('2016', '2016'),
            ('2017', '2017'),
            ('2018', '2018'),
            ('2019', '2019'),
            ('2020', '2020'),
            ('2021', '2021'),
        ]
    )

    prova = SelectField(
        'Prova',
        choices=[
            ('azul', 'azul'),
            ('amarela', 'amarela'),
            ('verde', 'verde'),
            ('cinza', 'cinza'),
            ('branca', 'branca'),
        ]
    )

    dia = SelectField(
        'Dia',
        choices=[
            ('1', '1'),
            ('2', '2'),
        ]
    )

    tags = MultiCheckboxField("Assunto da Questão", coerce=int)

    def __init__(self, *args, **kwargs):

        super(formularioQuestaoPainel, self).__init__(*args, *kwargs)

        # Seleciona as tags (TODAS!)

        # Como selecionar o id e o nome das tags
        # tag.id será o valor do input
        # tag.nome será o label
        self.tags.choices = [(tag.id, tag.nome)
                              for tag in Tag.query.order_by(Tag.id).all()]

    enviar = SubmitField('Criar Questão')
