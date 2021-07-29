from flask import Blueprint

# 'ingles' é o nome do Blueprint, e __name__ é o nome do módulo/pacote onde o blueprint está localizado
ingles = Blueprint('ingles', __name__)

from . import rotas, erros
from ..modelos import Permissao


@ingles.app_context_processor
def inserir_permissoes():
    return dict(Permissao=Permissao)