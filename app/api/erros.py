from flask import jsonify
from app.excecoes import ErroDeValidacao
from . import api

def pedido_incorreto(mensagem):
    resposta = jsonify({'erro': 'pedido incorreto', 'mensagem': mensagem})
    resposta.status_code = 400
    return resposta

def nao_autorizado(mensagem):
    resposta = jsonify({'erro': 'não autorizado', 'mensagem': mensagem})
    resposta.status_code = 401
    return resposta

def proibido(mensagem):
    resposta = jsonify({'erro': 'proibido', 'mensagem': mensagem})
    resposta.status_code = 403
    return resposta

@api.errorhandler(ErroDeValidacao)
def erro_validacao(e):
    return pedido_incorreto(e.args[0])