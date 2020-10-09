# Adicionar comentários

from flask import render_template
from . import inicio

@inicio.app_errorhandler(403)
def proibido(e):
    return render_template('erros/403.html'), 403

# Gerencia o erro de página não encontrada
@inicio.app_errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('erros/404.html'), 404

# Gerencia o erro interno de servidor
@inicio.app_errorhandler(500)
def erro_interno_servidor(e):
    return render_template('erros/500.html'), 500




# inicio.errorhandler invoca o gerenciador de erros para erros gerados apenas dentro do blueprint
# Para instalar gerenciadores de erros 'globais', use o decorador 'app_errorhandler'
