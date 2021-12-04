from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, SubmitField, widgets
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError

from ..modelos import Usuario, Role, Publicacao, Tag

from flask_pagedown.fields import PageDownField


class MultiCheckboxField(SelectMultipleField):

    """
    Um elemento de formulário do tipo 'multiple-select', entretanto isto exibe uma lista de caixas de seleção
    
    Percorrer o elemento produz os sub-elementos, permitindo exibir as caixas de marcação individuais de forma personalizada

    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class formularioArtigoBlog(FlaskForm):

    titulo = StringField("Título da publicação", validators=[DataRequired()])

    subtitulo = StringField("Subtítulo da publicação", validators=[DataRequired()])

    conteudo = PageDownField("Conteúdo da publicação", validators=[DataRequired()])

    foto = FileField(validators=[FileRequired()])

    tags = MultiCheckboxField("Assunto da publicação", coerce=int)

    def __init__(self, *args, **kwargs):

        super(formularioArtigoBlog, self).__init__(*args, *kwargs)

        # Seleciona as tags (TODAS!)

        """
        Como selecionar o id e o nome das tags
        """
        # tag.id será o valor do input
        # tag.nome será o label
        self.tags.choices = [(tag.id, tag.nome)
                              for tag in Tag.query.order_by(Tag.id).all()]




class formularioComentarioArtigo(FlaskForm):
    conteudo = StringField(validators=[DataRequired('É necessário digitar algo no comentário')])
    enviar = SubmitField('Enviar')
