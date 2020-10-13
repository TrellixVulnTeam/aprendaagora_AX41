from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from .modelos import Usuario, Role, Publicacao, Tag






# Formulário genérico para publicações nos murais 
# O idioma deve ser definido através de um argumento, chamado 'idioma', quando uma instância do formulário for criada na rota
class formularioPublicacaoMural(FlaskForm):

    titulo = StringField("Título da publicação", validators=[DataRequired()])
    conteudo = TextAreaField("Conteúdo da publicação", validators=[DataRequired()])
    tags = SelectMultipleField("Assuntos", coerce=int)

    def __init__(self, idioma, *args, **kwargs):

        super(formularioPublicacaoMural, self).__init__(*args, *kwargs)

        # Seleciona as tags (TODAS!)
        self.tags.choices = [(tag.id, tag.nome)
                              for tag in Tag.query.order_by(Tag.nome).all()]

        self.idioma = idioma