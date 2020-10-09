import unittest
from flask import current_app
from app import criar_app, db

class TestagemBasica(unittest.TestCase):
    
    # Método executado antes de cada teste
    def setUp(self):
        self.app = criar_app('testagem')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    # Método executado depois de cada teste
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Checa se a instância do aplicativo existe
    def test_app_existe(self):
        self.assertFalse(current_app is None)

    # Checa se o aplicativo está executando sob a configuração de testagem
    def test_app_testando(self):
        self.assertTrue(current_app.config['TESTING'])


