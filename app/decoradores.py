from functools import wraps
from flask import abort
from flask_login import current_user
from .modelos import Permissao

# Checa permissões genéricas
def permissao_necessaria(permissao):

    def decorador(f):
        @wraps(f)
        def funcao_decorada(*args, **kwargs):
            # Se o usuário atual NÃO possuir a permissão
            if not current_user.pode(permissao):
                # Declare um erro 403
                abort(403)
            return f(*args, **kwargs)
        return funcao_decorada
    return decorador

# Checa permissões de Administrador
def admin_necessario(f):
    return permissao_necessaria(Permissao.ADMIN)(f)

