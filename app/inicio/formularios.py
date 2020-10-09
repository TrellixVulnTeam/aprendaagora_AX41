from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FormularioNome(FlaskForm):
    nome_usuario = StringField('Qual é se nome?', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
