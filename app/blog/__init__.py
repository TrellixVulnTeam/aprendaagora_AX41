from flask import Blueprint

# 'blog' é o nome do Blueprint, e __name__ é o nome do módulo/pacote onde o blueprint está localizado
blog = Blueprint('blog', __name__, template_folder='templates')



from . import rotas, erros
from ..modelos import Permissao


@blog.app_context_processor
def inserir_permissoes():
    return dict(Permissao=Permissao)
