# Blueprint INÍCIO

from flask import render_template, session, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import inicio as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import Usuario, Role, Permissao
from ..email import enviar_email
from .formularios import formularioEditarPerfil, formularioEditarPerfilAdmin

"""  ROTAS COMUNS  """

# Página de Login
@bp.route('/', methods=['GET', 'POST'])
def inicio():
    # Se o método for GET
    return render_template('inicio.html', current_time=datetime.utcnow())

# Exibe a página de perfil do usuário conectado
@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    return render_template('usuario.html', usuario=current_user._get_current_object())

# Exibe a página de perfil de um usuário qualquer
@bp.route('/usuario/<nome_usuario>')
def usuario(nome_usuario):

    usuario_atual = current_user._get_current_object()
    
    if usuario_atual.nome_usuario == nome_usuario:
        return redirect(url_for('inicio.perfil'))

    # Seleciona o usuário no banco de dados ou retorna um erro 404
    usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first_or_404()

    # Exibe a página de usuário, fornecendo os dados do usuário como argumentoss
    return render_template('usuario.html', usuario=usuario)


@bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():

    formulario = formularioEditarPerfil()

    if formulario.validate_on_submit():

        current_user.nome_usuario = formulario.nome_usuario.data
        current_user.nome = formulario.nome.data
        current_user.sobrenome = formulario.sobrenome.data
        current_user.localizacao = formulario.localizacao.data
        current_user.sobre = formulario.sobre.data

        db.session.add(current_user._get_current_object())
        db.session.commit()

        flash("As alterações no seu perfil foram salvas.")

        return redirect(url_for('inicio.perfil'))
    
    formulario.nome_usuario.data = current_user.nome_usuario
    formulario.nome.data = current_user.nome
    formulario.sobrenome.data = current_user.sobrenome
    formulario.localizacao.data = current_user.localizacao
    formulario.sobre.data = current_user.sobre

    return render_template('editar_perfil.html', formulario=formulario)




"""  ROTAS DOS PROFESSORES E DOS ADMINS  """

# Rota para um Professor escrever no Blog
@bp.route('/escrever')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def apenas_professores():
    return "Apenas Professores!"

# Rota do painel do Administrador

# De forma prática, o decorador 'route' deve ser declarado primeiro quando se está usando vários decoradores em uma função view. Os decoradores restantes devem ser declarados na orde que eles precisam ser avaliado quando a função view for chamada. Neste caso, o usuário deve estar conectado primeiro, considerando que o usuário deve ser redirecionado para a página de login caso ele não esteja conectado.
@bp.route('/admin')
@login_required
@admin_necessario
def apenas_admins():
    return "Apenas Administradores!"

# Rota para um Administrador editar a conta de outro usuário

@bp.route('/editar-perfil/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_necessario
def editar_perfil_admin(id):

    # Se não houver um usuário com o id informado, retornar erro 404
    usuario = Usuario.query.get_or_404(id)

    formulario = formularioEditarPerfilAdmin(usuario=usuario)

    # Se o método for POST
    if formulario.validate_on_submit():
        
        usuario.email =  formulario.email.data
        usuario.nome_usuario = formulario.nome_usuario.data
        usuario.confirmado = formulario.confirmado.data

        # Quando o formulário é enviado, o id é extraído do atributo 'data' e é usado em uma consulta ao banco de dados para carregar o objeto 'role' selecionado através de seu id. O argumento coerce=int usado 
        usuario.role = Role.query.get(formulario.role.data)
        usuario.nome = formulario.nome.data
        usuario.sobrenome = formulario.sobrenome.data
        usuario.localizacao = formulario.localizacao.data
        usuario.sobre = formulario.sobre.data

        db.session.add(usuario)
        db.session.commit()
        
        flash("As alterações no perfil foram salvas.")

        print("Método POST")

        return redirect(url_for('.usuario', nome_usuario=usuario.nome_usuario))
    
    # Se o método for GET
    # Preencha o formulário com as informações do usuário cujo perfil deve ser editado
    formulario.email.data = usuario.email
    formulario.nome_usuario.data = usuario.nome_usuario
    formulario.confirmado.data = usuario.confirmado
    formulario.role.data = usuario.role_id
    formulario.nome.data = usuario.nome
    formulario.sobrenome.data = usuario.sobrenome
    formulario.localizacao.data = usuario.localizacao
    formulario.sobre.data = usuario.sobre

    # Exibe a página com o formulário para editar o perfil
    return render_template('editar_perfil.html', formulario=formulario, usuario=usuario)
