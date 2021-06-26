from flask import Blueprint

# 'chat' é o nome do Blueprint, e __name__ é o nome do módulo/pacote onde o blueprint está localizado
chat = Blueprint('chat', __name__)

from . import rotas
#from . import rotas, erros


from ..modelos import Permissao

@chat.app_context_processor
def inserir_permissoes():
    return dict(Permissao=Permissao)