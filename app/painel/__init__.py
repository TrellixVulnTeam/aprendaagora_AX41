from flask import Blueprint

# 'ingles' é o nome do Blueprint, e __name__ é o nome do módulo/pacote onde o blueprint está localizado
painel = Blueprint('painel', __name__)


from . import rotas, erros
from ..modelos import Permissao


@painel.app_context_processor
def inserir_permissoes():
    return dict(Permissao=Permissao)