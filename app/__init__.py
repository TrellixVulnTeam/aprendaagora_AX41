# Adicionar comentários

from flask import Flask

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown

from flask_socketio import SocketIO

from config import configuracao


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

socketio = SocketIO(logger=True, engine_logger=True, cors_allowed_origins="*")

login_manager = LoginManager()
# Define qual a rota para login
login_manager.login_view = 'autorizar.entrar'
# Mensagem exibida quando o erro 403 (Proibido) for causado
login_manager.login_message = "Entre na sua conta para acessar esta página"

pagedown = PageDown()


def criar_app(nome_configuracao):

    app = Flask(__name__)
    
    app.config.from_object(configuracao[nome_configuracao])
    
    configuracao[nome_configuracao].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    socketio.init_app(app)


    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    """ Rotas """

    # Registra o blueprint 'inicio'
    from .inicio import inicio as inicio_blueprint
    app.register_blueprint(inicio_blueprint)

    # Registra o blueprint 'autorizar'
    from .autorizar import autorizar as autorizar_blueprint
    app.register_blueprint(autorizar_blueprint, url_prefix='/autorizar')

    # Registra o blueprint 'ingles'
    from .ingles import ingles as ingles_blueprint
    app.register_blueprint(ingles_blueprint, url_prefix='/ingles')

    # Registra o blueprint 'chat'
    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint, url_prefix='/chat')

    return app
