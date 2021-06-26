# Blueprint INGLÊS

from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room

from . import chat as bp

from .. import db, socketio
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Role, Permissao, Publicacao, Tag, Comentario, PublicacaoAmei
from ..email import enviar_email
from ..formularios import formularioPublicacaoMural
from ..funcoes_auxiliares import criar_publicacao, truncar_texto





salas = {
    'ingles': []
}



@bp.route("/")
def inicio():
    return render_template("chat.html")


# Confirma conexão
@socketio.on('socket conectado')
def handle_my_custom_event():
    print("Socket conectado.")


@socketio.on('pedir mensagens')
def pedir_mensagens(sala):

    # Seleciona a sala
    sala = sala['sala']

    # Array de mensagens que será enviado para o cliente
    mensagens = []

    #
    for mensagem in salas[sala]:

        #
        usuario = mensagem['usuario']
        conteudo = mensagem['mensagem']
        dataMensagem = mensagem['dataMensagem']

        #
        mensagens.append({'usuario': usuario, 'mensagem': conteudo, 'dataMensagem': dataMensagem})

    for mensagem in mensagens:
        print(mensagem)

    print(mensagens)

    # Envia array de mensagens
    emit('carregar mensagens', mensagens)
    

@socketio.on('enviar mensagem')
def enviar_mensagem(dados):

    # Selecina os dados da mensagem
    mensagem = dados['mensagem']
    usuario = dados['usuario']
    sala = dados['sala']
    dataMensagem = dados['dataMensagem']

    # Log
    print("----")
    print(mensagem)
    print(usuario)
    print(sala)

    # Adiciona nova mensagem ao final da lista
    salas[sala].append({'usuario': usuario, 'mensagem': mensagem, 'dataMensagem': dataMensagem})

    # Se o número de mensagens for igual ou maior que 100
    if len(salas[sala]) > 100:
        # Remove a mensagem mais antiga
        salas[sala].pop()

    # Log número de mensagens
    print(f'O número de mensagens na sala "{sala}" é: {len(salas[sala])}.')

    # Emite evento para todos os clientes
    emit('exibir mensagem', {'mensagem': mensagem, 'usuario': usuario, 'dataMensagem': dataMensagem}, broadcast=True)

