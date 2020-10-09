import unittest
import time
from app import criar_app, db
from app.modelos import Usuario, UsuarioAnonimo, Role, Permissao


class TesteModeloUsuario(unittest.TestCase):
    
    def setUp(self):
        self.app = criar_app('testagem')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.inserir_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def teste_senha_setter(self):
        u = Usuario(senha='gato')
        self.assertTrue(u.senha_hash is not None)

    def teste_senha_bloqueada(self):
        u = Usuario(senha='gato')
        with self.assertRaises(AttributeError):
            u.senha

    def teste_senha_verificacao(self):
        u = Usuario(senha='gato')
        self.assertTrue(u.verificar_senha('gato'))
        self.assertFalse(u.verificar_senha('cachorro'))

    def teste_senha_salts_sao_aleatorios(self):
        u = Usuario(senha='gato')
        u2 = Usuario(senha='gato')
        self.assertTrue(u.senha_hash != u2.senha_hash)

    def teste_token_confirmacao_valido(self):
        u = Usuario(senha='gato')
        db.session.add(u)
        db.session.commit()
        token = u.gerar_token_confirmacao()
        self.assertTrue(u.confirmar(token))
    
    def teste_token_confirmacao_invalido(self):
        u1 = Usuario(senha='gato')
        u2 = Usuario(senha='cachorro')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.gerar_token_confirmacao()
        self.assertFalse(u2.confirmar(token))

    def teste_token_confirmacao_expirado(self):
        u = Usuario(senha='gato')
        db.session.add(u)
        db.session.commit()
        token = u.gerar_token_confirmacao(1)
        time.sleep(2)
        self.assertFalse(u.confirmar(token))







    
    def teste_role_usuario(self):
        u = Usuario(email='joao@exemplo.com', senha='gato')
        self.assertTrue(u.pode(Permissao.SEGUIR))
        self.assertTrue(u.pode(Permissao.COMENTAR))
        self.assertFalse(u.pode(Permissao.MODERAR_INGLES))
        self.assertFalse(u.pode(Permissao.MODERAR_FRANCES))
        self.assertFalse(u.pode(Permissao.MODERAR_ESPANHOL))
        self.assertFalse(u.pode(Permissao.MODERAR_ITALIANO))
        self.assertFalse(u.pode(Permissao.MODERAR_ALEMAO))
        self.assertFalse(u.pode(Permissao.MODERAR_JAPONES))
        self.assertFalse(u.pode(Permissao.MODERAR_CHINES))
        self.assertFalse(u.pode(Permissao.PROF_INGLES))
        self.assertFalse(u.pode(Permissao.PROF_FRANCES))
        self.assertFalse(u.pode(Permissao.PROF_ESPANHOL))
        self.assertFalse(u.pode(Permissao.PROF_ITALIANO))
        self.assertFalse(u.pode(Permissao.PROF_ALEMAO))
        self.assertFalse(u.pode(Permissao.PROF_JAPONES))
        self.assertFalse(u.pode(Permissao.PROF_CHINES))
        self.assertFalse(u.pode(Permissao.ESCREVER_BLOG))
        self.assertFalse(u.pode(Permissao.ADMIN))

    def teste_usuario_anonimo(self):
        u = UsuarioAnonimo()
        self.assertFalse(u.pode(Permissao.SEGUIR))
        self.assertFalse(u.pode(Permissao.COMENTAR))
        self.assertFalse(u.pode(Permissao.MODERAR_INGLES))
        self.assertFalse(u.pode(Permissao.MODERAR_FRANCES))
        self.assertFalse(u.pode(Permissao.MODERAR_ESPANHOL))
        self.assertFalse(u.pode(Permissao.MODERAR_ITALIANO))
        self.assertFalse(u.pode(Permissao.MODERAR_ALEMAO))
        self.assertFalse(u.pode(Permissao.MODERAR_JAPONES))
        self.assertFalse(u.pode(Permissao.MODERAR_CHINES))
        self.assertFalse(u.pode(Permissao.PROF_INGLES))
        self.assertFalse(u.pode(Permissao.PROF_FRANCES))
        self.assertFalse(u.pode(Permissao.PROF_ESPANHOL))
        self.assertFalse(u.pode(Permissao.PROF_ITALIANO))
        self.assertFalse(u.pode(Permissao.PROF_ALEMAO))
        self.assertFalse(u.pode(Permissao.PROF_JAPONES))
        self.assertFalse(u.pode(Permissao.PROF_CHINES))
        self.assertFalse(u.pode(Permissao.ESCREVER_BLOG))
        self.assertFalse(u.pode(Permissao.ADMIN))



