import os
diretoriobase = os.path.abspath(os.path.dirname(__file__))



"""
BANCODEDADOS_DEV_URI=postgres://ikyqqimlkzcwij:388c8055e649660d2662ba2e53c1bef1d1b8c80a6f9830b8e90a5e934408cd45@ec2-54-235-116-235.compute-1.amazonaws.com:5432/dejne5d303q1sh



FLASK_ENV=development
FLASK_APP=aprendaagora.py
FLASK_DEBUG=1
MAIL_USERNAME=aprenda.agora.contato@gmail.com
FLASK_ADMIN=aprenda.agora.contato@gmail.com

"""

class Configuracao:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'string dificil de descobrir'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    APRENDA_AGORA_EMAIL_PREFIXO_ASSUNTO = '[Aprenda Agora]'
    APRENDA_AGORA_EMAIL_AUTOR = 'Aprenda Agora aprenda.agora.contato@gmail.com'
    APRENDA_AGORA_ADMIN = os.environ.get('APRENDA_AGORA_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MURAL_PUBLICACOES_POR_PAGINA = 16

    SSL_REDIRECT = False

    @staticmethod
    def init_app(app):
        pass


class ConfiguracaoDesenvolvimento(Configuracao):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('BANCODEDADOS_DEV_URI')

class ConfiguracaoTeste(Configuracao):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('BANCODEDADOS_TEST_URI')


class ConfiguracaoProducao(Configuracao):
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('BANCODEDADOS_DEV_URI')
    
    @classmethod
    def init_app(cls, app):
        Configuracao.init_app(app)

        # enviar erros para os administradores
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None

        if getattr(cls, 'MAIL_USERNAME', None) is not None:

            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)

            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr = cls.APRENDA_AGORA_EMAIL_AUTOR,
            toaddrs = [cls.APRENDA_AGORA_ADMIN],
            subject = cls.APRENDA_AGORA_EMAIL_PREFIXO_ASSUNTO + 'Erro do Aplicativo',
            credentials = credentials,
            secure = secure
            )

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    


class ConfiguracaoHeroku(ConfiguracaoProducao):

    @classmethod
    def init_app(cls, app):

        ConfiguracaoProducao.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()

        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)

        SSL_REDIRECT = True if os.environ.get('DYNO') else False

        from werkzeug.middleware.proxy_fix import ProxyFix


        #app.wsgi_app = ProxyFix(app.wsgi_app)

        app = ProxyFix(app, x_for=1, x_host=1)

        #app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)


configuracao = {

    'desenvolvimento': ConfiguracaoDesenvolvimento,

    'testagem': ConfiguracaoTeste,

    'producao': ConfiguracaoProducao,

    'heroku': ConfiguracaoHeroku,

    'padrao': ConfiguracaoHeroku
}
