from flask import Blueprint

# 'inicio' é o nome do Blueprint, e __name__ é o nome do módulo/pacote onde o blueprint está localizado
inicio = Blueprint('inicio', __name__)

from . import rotas, erros
from .. modelos import Permissao


# Permissões também podem ser checadas a partir de templates, portanto a classe Permissao, juntamente com seus conteúdos, devem estar acessíveis aos templates. Para evitar ter que adicionar um argumento à cada chamada da função 'render_template()', um processador de contexto pode ser usado. Processadores de contexto tornam variáveis disponíveis para todos os templates durante a exibição dos mesmos
@inicio.app_context_processor
def inserir_permissoes():
    return dict(Permissao=Permissao)

