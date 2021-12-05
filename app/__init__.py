# Adicionar comentários

from flask import Flask

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


from flask_pagedown import PageDown
from flask_login import LoginManager


from flask_uploads import configure_uploads

"""
from flask_socketio import SocketIO
"""

from config import configuracao


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()



"""
#socketio = SocketIO(logger=True, engine_logger=True, cors_allowed_origins="*")
"""


login_manager = LoginManager()
# Define qual a rota para login
login_manager.login_view = 'autorizar.entrar'
# Mensagem exibida quando o erro 403 (Proibido) for causado
login_manager.login_message = "Entre na sua conta para acessar esta página"

######################################################################



from app.blog.rotas import fotos



def criar_app(nome_configuracao):

    app = Flask(__name__)

    app.config.from_object(configuracao[nome_configuracao])

    app.config['UPLOADED_PHOTOS_DEST'] = 'app/static/imagens/artigos'

    
    configuracao[nome_configuracao].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    

    configure_uploads(app, fotos)
    

    """
    #socketio.init_app(app)
    """

    ######################################################################

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    ######################################################################

    """ BLUEPRINTS """

    # Registra o blueprint 'inicio'
    from .inicio import inicio as inicio_blueprint
    app.register_blueprint(inicio_blueprint)

    # Registra o blueprint 'autorizar'
    from .autorizar import autorizar as autorizar_blueprint
    app.register_blueprint(autorizar_blueprint, url_prefix='/autorizar')

    from .painel import painel as painel_blueprint
    app.register_blueprint(painel_blueprint, url_prefix='/painel')

    # Registra o blueprint 'ingles'
    from .ingles import ingles as ingles_blueprint
    app.register_blueprint(ingles_blueprint, url_prefix='/ingles')

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')



    """
    # Registra o blueprint 'chat'
    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    """

    ######################################################################

    return app
