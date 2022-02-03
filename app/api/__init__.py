from flask import Blueprint

api = Blueprint('api', __name__)

from . import (
    autenticacao,
    publicacoes,
    usuarios,
    comentarios,
    erros
)



