from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

# Função que envia email
def enviar_email_assinc(app, mensagem):

    with app.app_context():

        mail.send(mensagem)

# Função que prepara Thread de envio de email
def enviar_email(destino, assunto, template, **kwargs):
    
    # Log
    print("Função 'enviar_email' ativada.")


    app = current_app._get_current_object()


    # Define o assunto, o remetente (quem envia) e o destinatátio (quem recebe) 
    mensagem = Message(app.config['APRENDA_AGORA_EMAIL_PREFIXO_ASSUNTO'] + assunto,
                       sender=app.config['APRENDA_AGORA_EMAIL_AUTOR'], recipients=[destino])

    # Define o conteúdo da mensagem
    mensagem.body = render_template(template + '.txt', **kwargs)

    # Define o conteúdo da mensagem em formato HTML
    mensagem.html = render_template(template + '.html', **kwargs)


    # Cria nova Thread
    # A função da thread é 'enviar_email_assinc'
    # Os argumentos são 'app' e 'mensagem'
    thread = Thread(target=enviar_email_assinc, args=[app, mensagem])


    thread.start()
    
    return thread













