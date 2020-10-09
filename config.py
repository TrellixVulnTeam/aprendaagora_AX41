import os
diretoriobase = os.path.abspath(os.path.dirname(__file__))


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

    @staticmethod
    def init_app(app):
        pass


class ConfiguracaoDesenvolvimento(Configuracao):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('BANCODEDADOS_DEV_URI') or 'sqlite:///' + os.path.join(diretoriobase, 'dados-dev.sqlite')

class ConfiguracaoTeste(Configuracao):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('BANCODEDADOS_TEST_URI') or 'sqlite://'

class ConfiguracaoProducao(Configuracao):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(diretoriobase, 'dados.sqlite')


configuracao = {
    'desenvolvimento': ConfiguracaoDesenvolvimento,
    'testagem': ConfiguracaoTeste,
    'producao': ConfiguracaoProducao,

    'padrao': ConfiguracaoDesenvolvimento
}





