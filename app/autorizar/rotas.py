from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import autorizar
from .. import db
from ..modelos import Usuario
from ..email import enviar_email
from .formularios import formularioEntrar, formularioInscricao, formularioTrocarSenha, formularioPedirRedefinirSenha, formularioRedefinirSenha, formularioTrocarEmail


# Exige confirmação da conta para acessar páginas fora do blueprint 'autorizar'
@autorizar.before_app_request
def antes_do_pedido():

    # Se o usuário estiver conectado
    # e não for um usuário com a conta confirmada
    # e o URL pedido está fora do Blueprint de autorização
    # e o arquivo pedido não é um arquivo estático
    if current_user.is_authenticated and not current_user.confirmado and request.blueprint != 'autorizar' and request.endpoint != 'static':
        return redirect(url_for('autorizar.nao_confirmado'))


# Página que exige que o usuário confirme a conta antes de prosseguir
@autorizar.route('/naoconfirmado')
def nao_confirmado():

    # Se o usuário atual for anônimo ou já estiver confirmado
    if current_user.is_anonymous or current_user.confirmado:
        # Redireciona para o unício
        return redirect(url_for('inicio.inicio'))

    # Exibe a página com o aviso para confirmação de conta
    return render_template('autorizar/naoconfirmado.html')


# Página para o usuário acessar sua conta
@autorizar.route('/entrar', methods=['GET', 'POST'])
def entrar():

    # Seleciona o formulário de login
    formulario = formularioEntrar()

    # Se o método for POST
    if formulario.validate_on_submit():

        # Seleciona o usuário com o email informado
        usuario = Usuario.query.filter_by(email=formulario.email.data).first()
        
        # Se um usuário com o email informado existir e a senha (informada no formulário) estiver correta
        if usuario is not None and usuario.verificar_senha(formulario.senha.data):
            
            # A função login_user() recebe o usuário a ser conectado e um valor Booleano "lembrar-me" opcional
            login_user(usuario, formulario.lembrar_me.data)

            # A variável 'next' armazena o URL de uma página protegida, caso o usuário tente acessá-la sem permissão
            next = request.args.get('next')

            # Se 'next' não estiver disponível ou se 'next' não for um URL váido (um URL relativo, neste caso)
            if next is None or not next.startswith('/'):
                # Redirecione o usuário para a página inicial
                next = url_for('inicio.inicio')
            
            # Sequência POST-REDIRECT-GET
            return redirect(next)
        
        # Aviso que será exibido no topo da página
        flash("Nome de usuário e/ou senha inválido(s).")
    
    # Se o método for GET
    return render_template('autorizar/entrar.html', formulario=formulario)


# Rota para o usuário sair da conta
@autorizar.route('/sair')
@login_required
def sair():
    # A função logout_user() remove e reinicia a sessão de usuário
    logout_user()
    # Aviso que será exibido no topo da página
    flash('Você saiu da sua conta.')
    # Redireciona o usuário para a página inicial
    return redirect(url_for('inicio.inicio'))


# Página para criação de uma nova conta
@autorizar.route('/inscricao', methods=['GET', 'POST'])
def inscricao():

    # Seleciona o formulário de criação de conta
    formulario = formularioInscricao()

    # Se o método for POST
    if formulario.validate_on_submit():
        
        # Objeto 'Usuario' criado
        novo_usuario = Usuario(email=formulario.email.data,
        nome_usuario=formulario.nome_usuario.data,
        senha=formulario.senha.data)

        # O novo usuário é adicionado ao banco de dados
        db.session.add(novo_usuario)
        # As alterações no banco de dados são salvas
        db.session.commit()

        # Gera um token de confirmação
        token = novo_usuario.gerar_token_confirmacao()

        # Envia um email de confirmação de conta
        enviar_email(novo_usuario.email, 'Confirme Sua Conta',
                     'autorizar/email/confirmacao', usuario=novo_usuario, token=token)

        # Aviso que será exibido no topo da página
        flash("Um email de confirmação foi enviado para seu email.")
        # Sequência POST-REDIRECT-GET
        return redirect(url_for('inicio.inicio'))

    # Se o método for GET
    return render_template('autorizar/inscricao.html', formulario=formulario)


# Rota que confirma uma conta dado um token de confirmação
@autorizar.route('/confirmar/<token>')
@login_required
def confirmar(token):

    # Se o usuário atual já estiver confirmado
    if current_user.confirmado:
        # Redirecionar para o início
        return redirect(url_for('inicio.inicio'))

    # Se o método confirmar(token) retornar True
    if current_user.confirmar(token):
        # Salve a alteração (confirmação da conta) no banco de dados
        db.session.commit()
        # Aviso que será exibido no topo da página
        flash("Você confirmou sua conta. Obrigado!")
    else:
        # Aviso que será exibido no topo da página
        flash("O link de confirmação é inválido ou já expirou.")

    # Redireciona para a página inicial
    return redirect(url_for('inicio.inicio'))


# Rota que reenvia o email de confirmação de conta
@autorizar.route('/confirmar')
@login_required
def reenviar_confirmacao():

    # Gera o token de confirmação de conta usando o usuário conectado (objeto current_user)
    token = current_user.gerar_token_confirmacao()
    # Envia o email de confirmação
    enviar_email(current_user.email, 'Confirme Sua Conta', 'autorizar/email/confirmacao', usuario=current_user, token=token)
    # Aviso que será exibido no topo da página
    flash("Um novo email de confirmação foi enviado para seu endereço de email.")
    # Redireciona para a página inicial
    return redirect(url_for('inicio.inicio'))


@autorizar.route('/trocar_senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():

    formulario = formularioTrocarSenha()

    # Se o método for POST
    if formulario.validate_on_submit():

        if current_user.verificar_senha(formulario.senha_antiga.data):

            current_user.senha = formulario.nova_senha.data

            db.session.add(current_user)

            db.session.commit()

            # Aviso que será exibido no topo da página
            flash("Sua senha foi atualizada.")

            return redirect(url_for('inicio.inicio'))
        else:
            # Aviso que será exibido no topo da página
            flash("Senha incorreta.")
    return render_template("autorizar/trocar_senha.html", formulario=formulario)


# Rota que redefine (reseta) a senha do usuário caso ele esqueça qual é a senha
@autorizar.route('/redefinir_senha', methods=['GET, POST'])
@login_required
def redefinir_senha_pedido():

    # Se o usuário estiver logado e tentar acessar rota
    if not current_user.is_anonymous('inicio.inicio'):
        # Redirecione para a rota 'inicio'
        # O usuário conectado é redirecionado para o início por que se ele está conectado, presume-se que ele sabe a própria senha
        return redirect(url_for('inicio.inicio'))

    formulario = formularioPedirRedefinirSenha()

    if formulario.validate_on_submit():

        # Seleciona o usuário cujo email é igual ao email informado no formulário
        usuario = Usuario.query.filter_by(email=formulario.email.data.lower()).first()
        
        # Se houver um usuário com o email informado
        if usuario:

            # Gera um token para o usuário redefinir sua senha
            token = usuario.gerar_token_redefinir_senha()

            enviar_email(usuario.email, 'Redefina Sua Senha', 'autorizar/email/redefinir_senha', usuario=usuario, token=token)

        # Aviso que será exibido no topo da página
        flash("Um email com instruções sobre como redefinir sua senha foi enviado para seu email.")
        return redirect(url_for('autorizar.login'))
    return render_template('autorizar/redefinir_senha.html', formulario=formulario)


@autorizar.route('/redefinir_senha/<token>', methods=['GET, POST'])
def redefinir_senha(token):

    # Se o usuário estiver logado e tentar acessar rota
    if not current_user.is_anonymous:
        # Redirecione para a rota 'inicio'
        # O usuário conectado é redirecionado para o início por que se ele está conectado, presume-se que ele sabe a própria senha
        return redirect(url_for('inicio.inicio'))

    # Seleciona o formulário
    formulario = formularioRedefinirSenha()

    # Se o método for POST
    if formulario.validate_on_submit():

        # Se o método redefinir_senha() retornar True (ou seja, se a senha for redefinida)
        if Usuario.redefinir_senha(token, formulario.senha.data):
            # Salve as alterações no banco de dados
            db.session.commit()
            # Aviso que será exibido no topo da página
            flash("Sua senha foi atualizada.")
            # Redirecione o usuário para a rota 'inicio'
            return redirect(url_for('inicio.inicio'))
        # Se o método não funcionar
        else:
            # Redirecione o usuário para a rota 'inicio'
            return redirect(url_for('inicio.inicio'))


@autorizar.route('/trocar_email', methods=['GET', 'POST'])
@login_required
def trocar_email_pedido():

    formulario = formularioTrocarEmail()

    if formulario.validate_on_submit():

        if current_user.verificar_senha(formulario.senha.data):

            novo_email = formulario.email.data.lower()

            token = current_user.gerar_token_trocar_email(novo_email)

            enviar_email(novo_email, 'Confirme Seu Endereço de Email', 'autorizar/email/trocar_email', usuario=current_user, token=token)

            # Aviso que será exibido no topo da página
            flash("Um email com instruções sobre como confirmar seu novo email foi enviado para você. Cheque a caixa de entrada do seu email.")

            return redirect(url_for('inicio.inicio'))
        else:
            # Aviso que será exibido no topo da página
            flash("Email e/ou senha inválido(s). Tente novamente.")
    return render_template('autorizar/trocar_email.html', formulario=formulario)


@autorizar.route('/trocar_email/<token>')
@login_required
def trocar_email(token):

    if current_user.trocar_email(token):

        db.session.commit()
        flash("O endereço de email vinculado à conta foi trocado.")

    else:

        flash("Ação inválida.")

    return redirect(url_for('inicio.inicio'))