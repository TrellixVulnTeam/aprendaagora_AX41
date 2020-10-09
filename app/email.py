from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def enviar_email_assinc(app, mensagem):
    with app.app_context():
        mail.send(mensagem)

def enviar_email(destino, assunto, template, **kwargs):
    
    # Log
    print("Função 'enviar_email' ativada.")

    app = current_app._get_current_object()

    mensagem = Message(app.config['APRENDA_AGORA_EMAIL_PREFIXO_ASSUNTO'] + assunto,
                       sender=app.config['APRENDA_AGORA_EMAIL_AUTOR'], recipients=[destino])

    mensagem.body = render_template(template + '.txt', **kwargs)

    mensagem.html = render_template(template + '.html', **kwargs)

    thread = Thread(target=enviar_email_assinc, args=[app,mensagem])
    thread.start()
    return thread













