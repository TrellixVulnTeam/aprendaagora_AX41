from functools import wraps
from flask import g
from .erros import proibido

def permissao_necessaria(permissao):
    def decorador(f):
        @wraps(f)
        def funcao_decorada(*args, **kwargs):
            if not g.current_user.pode(permissao):
                return proibido('O usuário não possui permissão para essa ação.')
            return f(*args, **kwargs)
        return funcao_decorada
    return decorador