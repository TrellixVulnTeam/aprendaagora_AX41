from flask import (
    render_template,
    session,
    redirect,
    url_for,
    current_app,
    flash,
    request,
    jsonify,
    make_response
)

from ..modelos import (
    InscricaoFeuRosa,
    Usuario,
    Role,
    Permissao,
    Publicacao,
    Tag,
    UsuarioAnonimo
)

from .formularios import (
    formularioEditarPerfil,
    formularioEditarPerfilAdmin,
    formularioInscricaoFeuRosa
)

from flask_login import login_required, current_user
from datetime import datetime
from . import inicio as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..email import enviar_email


"""
##########################################################

##### ##### ####  ##### #####       ##### ##### ##### #####  ###  ##### ##### 
#   # #     #   # #     #           #     #   # #       #   ## ##   #   #     
##### ##### #   # ##### #####       ##### #   # #       #   #   #   #   ##### 
#  #  #     #   # #         #           # #   # #       #   #####   #       # 
#   # ##### ####  ##### #####       ##### ##### ##### ##### #   # ##### #####

##########################################################
"""

# Página no Instagram
@bp.route('/instagram')
def pagina_instagram():
    return redirect("https://www.instagram.com/aprendaagora")

# Canal no Youtube
@bp.route('/youtube')
def canal_youtube():
    return redirect("https://www.youtube.com/channel/UCo-122KSpoYersHovXL3Tow")

# Grupo no Facebook
@bp.route('/facebook')
def grupo_facebook():
    return redirect("https://www.facebook.com/groups/aprendaagora")


"""
##########################################################

##### ##### #####  ###  #####       ##### ##### #   # #   # #   # ##### 
#   # #   #   #   ## ## #           #     #   # ## ## #   # ##  # #     
##### #   #   #   #   # #####       #     #   # # # # #   # # # # ##### 
#  #  #   #   #   #####     #       #     #   # #   # #   # #  ##     # 
#   # #####   #   #   # #####       ##### ##### #   # ##### #   # #####

##########################################################
"""

@bp.route('/')
def inicio():

    pagina = request.args.get('pagina', 1, type=int)

    exibir_seguidos = False

    if current_user.confirmado:
        exibir_seguidos = bool(request.cookies.get('exibir_seguidos', ''))

    """
    if exibir_seguidos:
        consulta = current_user.publicacoes_seguidos
    else:
        consulta = Publicacao.query.all()
    """
    
    consulta = Publicacao.query.all()

    print(type(consulta))
    
    """
    paginacao = consulta.order_by(
        Publicacao.data_criacao.desc()
    ).paginate(
        pagina,
        per_page=current_app.config['MURAL_PUBLICACOES_POR_PAGINA'],
        error_out=False
    )
    """

    #publicacoes = paginacao.items

    publicacoes = consulta

    return render_template(
        'inicio/inicio.html',
        publicacoes=publicacoes,
        exibir_seguidos=exibir_seguidos,
        #paginacao=paginacao
    )



@bp.route('/exibir_todos')
@login_required
def exibir_todos():

    resposta = make_response(redirect(url_for('.inicio')))
    resposta.set_cookie('exibir_seguidos', '', max_age=30*24*60*60)
    return resposta


@bp.route('/exibir_seguidos')
@login_required
def exibir_seguidos():

    resposta = make_response(redirect(url_for('.inicio')))
    resposta.set_cookie('exibir_seguidos', '1', max_age=30*24*60*60)
    return resposta



# Página de uma publicação
@bp.route('/publicacao/<int:id>')
def publicacao(id):

    # Seleciona uma publicação com o id informado
    publicacao = Publicacao.query.get_or_404(id)

    # Exibe a página da publicação
    return render_template('publicacao.html', publicacao=publicacao)



# Página de Inscrição para os cursos em FEU ROSA/ONLINE
@bp.route('/inscricao_curso', methods=['GET', 'POST'])
def inscricao_curso():

    # Seleciona o formulário de inscrição
    formulario = formularioInscricaoFeuRosa()

    # Se o método for POST
    if formulario.validate_on_submit():

        # Cria uma nova inscrição e envia para o banco de dados
        nova_inscricao = InscricaoFeuRosa(
                            nome=formulario.nome.data,
                            email=formulario.email.data,
                            numero_telefone=formulario.numero_telefone.data,
                            curso=formulario.opcao_curso.data,
                            horario=formulario.horario.data
        )

        db.session.add(nova_inscricao)
        db.session.commit()

        return render_template('autorizar/confirmar_inscricao.html')

    # Se o método for GET
    return render_template('temporario.html', formulario=formulario)



@bp.route('/equipe')
def equipe():
    return render_template('inicio/equipe.html')


@bp.route('/contato')
def contato():
    return render_template('blog/index.html')


@bp.route('/sobre')
def sobre():
    return render_template('blog/index.html')


@bp.route('/loja')
def loja():
    return render_template('blog/index.html')




"""
##########################################################

##### ##### ##### ##### ##### #     
#   # #     #   # #       #   #     
##### ##### ##### #####   #   #     
#     #     #  #  #       #   #     
#     ##### #   # #     ##### ##### 

##########################################################
"""


# Exibe a página de perfil do usuário conectado
@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():

    # Seleciona o usuário no banco de dados ou retorna um erro 404
    usuario = Usuario.query.filter_by(

            nome_usuario=current_user._get_current_object().nome_usuario
    ).first_or_404()

    # Seleciona as publicacoes do usuário
    publicacoes = usuario.publicacoes.order_by(
            Publicacao.data_criacao.desc()
    ).all()

    # Exibe a página de perfil do usuário
    return render_template(
            'inicio/usuario.html',
            usuario=current_user._get_current_object(),
            publicacoes=publicacoes
    )


# Exibe a página de perfil de um usuário qualquer
@bp.route('/usuario/<nome_usuario>')
def usuario(nome_usuario):

    # Seleciona o usuário no banco de dados ou retorna um erro 404
    usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first_or_404()

    # Se o usuário atual estiver conectado
    if current_user.is_authenticated:

        # Se o usuário atual for usuário da página acessada
        if (current_user._get_current_object().nome_usuario == nome_usuario):

            # Redirecione para a rota 'perfil'
            return redirect(url_for('inicio.perfil'))

    # Seleciona as publicações do usuário
    publicacoes = usuario.publicacoes.order_by(Publicacao.data_criacao.desc()).all()

    # Exibe a página de usuário, fornecendo os dados do usuário como argumentos
    return render_template(
            'inicio/usuario.html',
            usuario=usuario,
            publicacoes=publicacoes
    )


# Rota para o usuário conectado editar seu perfil
@bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():

    # Seleciona o formulário de editar perfil
    formulario = formularioEditarPerfil()

    # Se o método for POST (se estiver salvando as alterações)
    if formulario.validate_on_submit():

        # Define os dados do usuário
        current_user.nome_usuario = formulario.nome_usuario.data
        current_user.nome = formulario.nome.data
        current_user.sobrenome = formulario.sobrenome.data
        current_user.localizacao = formulario.localizacao.data
        current_user.sobre = formulario.sobre.data

        # Adiciona o usuário alterado
        db.session.add(current_user._get_current_object())

        # Salva as alterações no banco de dados
        db.session.commit()

        # Mensagem de aviso
        flash("As alterações no seu perfil foram salvas. 🙂", 'alert-success')

        # Redireciona para a página de perfil
        return redirect(url_for('inicio.perfil'))

    # Atribui os dados do usuário aos campos do formulário
    formulario.nome_usuario.data = current_user.nome_usuario
    formulario.nome.data = current_user.nome
    formulario.sobrenome.data = current_user.sobrenome
    formulario.localizacao.data = current_user.localizacao
    formulario.sobre.data = current_user.sobre

    # Exibe a página de editar perfil
    return render_template(
            'autorizar/editar_perfil.html',
            formulario=formulario,
            usuario=current_user
    )


@bp.route('/publicacao/apagar', methods=['POST'])
@login_required
def apagar_publicacao():

    try:
        # Seleciona o JSON enviado através do pedido do cliente
        json_enviado = request.get_json()

        # Seleciona o id da publicação
        publicacao_id = json_enviado["publicacao_id"]

        # Seleciona a publicação através do ID
        publicacao = Publicacao.query.get_or_404(publicacao_id)

        # Se o usuário que fez o pedido de exclusão (current_user) não for o autor da publicação
        if current_user != publicacao.autor:
            # Abortar operação
            abort(404)

        # Apaga a publicação
        db.session.delete(publicacao)

        # Salva as alterações
        db.session.commit()

        print("Publicação apagada")

        # Define o objeto JSON que será enviado de volta ao cliente
        confirmar_exclusao = {"apagado": True}

        # Envia o objeto JSON ao cliente
        return  jsonify(confirmar_exclusao)


    # Se houver uma excessão
    except Exception as e:

        print("AJAX exceção " + str(e))
        return(str(e))



@bp.route('/seguir/<nome_usuario>')
@login_required
@permissao_necessaria(Permissao.SEGUIR)
def seguir(nome_usuario):
    
    usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()

    # Checa se o usuário existe
    if usuario is None:

        flash('Usuário inválido.',  'alert-primary')

        return redirect(url_for('.inicio'))

    # Checa se o usário já é seguido
    if current_user.seguindo(usuario):

        flash('Você já está seguindo este usuário.',  'alert-primary')

        return redirect(url_for('.usuario', nome_usuario=nome_usuario))


    current_user.seguir(usuario)

    db.session.commit()

    flash(f"Você agora está seguindo {nome_usuario}.",  'alert-primary')

    return redirect(url_for('.usuario', nome_usuario=nome_usuario))


@bp.route('/desfazer_seguir/<nome_usuario>')
@login_required
@permissao_necessaria(Permissao.SEGUIR)
def desfazer_seguir(nome_usuario):
    
    usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()

    # Checa se o usuário existe
    if usuario is None:

        flash('Usuário inválido.',  'alert-primary')

        return redirect(url_for('.inicio'))

    # Checa se o usário não é seguido
    if not current_user.seguindo(usuario):

        flash('Você não está seguindo este usuário.',  'alert-primary')

        return redirect(url_for('.usuario', nome_usuario=nome_usuario))


    current_user.desfazer_seguir(usuario)

    db.session.commit()

    flash(f"Você parou de seguir {nome_usuario}.",  'alert-primary')

    return redirect(url_for('.usuario', nome_usuario=nome_usuario))



@bp.route('/seguidores/nome_usuario')
def seguidores(nome_usuario):
    return 1

@bp.route('/seguidos')
@login_required
def seguidos(nome_usuario):
    return 1



"""
  @@    @@    @@  
  @@    @@    @@  
  @@    @@    @@  
                  
  @@    @@    @@  

Transferir a rota abaixo para o blueprint admin
"""

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

        flash("As alterações no perfil foram salvas. 🙂", 'alert-success')

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
    return render_template(
        'admin/editar_perfil.html',
        formulario=formulario,
        usuario=usuario
    )
