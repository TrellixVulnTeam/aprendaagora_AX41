# Blueprint PAINEL

from flask import (
    render_template,
    session,
    redirect,
    url_for,
    current_app,
    flash,
    request,
    jsonify
)
from flask_login import login_required, current_user
from datetime import datetime
from . import painel as bp
from .. import db
from ..decoradores import admin_necessario, permissao_necessaria
from ..modelos import (
    Materia,
    Curso,
    Topico,
    Licao,
    Questao,
    Usuario,
    Role,
    Permissao,
    Publicacao,
    Tag,
    UsuarioAnonimo
)
from ..email import enviar_email

from .formularios import (
    formularioCursoPainel,
    formularioTopicoPainel,
    formularioLicaoPainel,
    formularioQuestaoPainel,
    formularioArtigoPainel
)

from ..funcoes_registrar import (
    registrar_curso,
    registrar_artigo,
    registrar_licao,
    registrar_topico,
    registrar_questao,
)



from flask_uploads import UploadSet, IMAGES

fotos = UploadSet('photos', IMAGES)


###############################################################
###############################################################
###############################################################


"""


### CURSOS, TÓPICOS, LIÇÕES & QUESTÕES

[ ] - Criar Curso
[ ] - Criar Tópico para um Curso
[ ] - Criar Lição para um Tópico
[ ] - Criar Questão para uma Lição
[ ] - Criar Artigo para o Blog

[ ] - Listar Matérias
[ ] - Listar Cursos
[ ] - Listar Tópicos
[ ] - Listar Lições
[ ] - Listar Questões
[ ] - Listar Artigos


[ ] - Listar Cursos de uma Matéria
[ ] - Listar Tópicos de uma Matéria
[ ] - Listar Lições de uma Matéria
[ ] - Listar Questões de uma Matéria

[ ] - Listar Tópicos de um Curso
[ ] - Listar Lições de um Curso
[ ] - Listar Questões de um Curso

[ ] - Listar Lições de um Tópico
[ ] - Listar Questões de um Tópico

[ ] - Listar Lições de uma Lição


### ARTIGOS



### PUBLICAÇÕES



### USUÁRIOS

[ ] - Visualizar lista de usuários

[ ] - Visualizar perfil de um usuários

[ ] - Editar dados do usuários

[ ] - Alterar role/permissões de um usuário

[ ] - Enviar mensagem para um usuário


### PROFESSORES




"""





# PAINEL
@bp.route('/')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def painel():

    return render_template('painel/index.html')




"""
#####################################################

#   # ##### #   #  ###  ##### ##### ##### ##### 
#   # #     #   # ## ## #   #   #   #   # #     
#   # ##### #   # #   # #####   #   #   # ##### 
#   #     # #   # ##### #  #    #   #   #     # 
##### ##### ##### #   # #   # ##### ##### ##### 

#####################################################
"""



"""

estudantes

instrutores

moderadores



"""



"""
#####################################################

#   #  ###  ##### ##### ##### #####  ###  ##### 
## ## ## ##   #   #     #   #   #   ## ## #     
# # # #   #   #   ##### #####   #   #   # ##### 
#   # #####   #   #     #  #    #   #####     # 
#   # #   #   #   ##### #   # ##### #   # ##### 

#####################################################
"""


# LISTAR MATERIAS
@bp.route('/materias')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materias():

    # Seleciona as materias
    materias = Materia.query.all()

    return render_template('painel/materias.html', materias=materias)


# PÁGINA DE UMA MATÉRIA
@bp.route('/materia/<nome_simples>')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia(nome_simples):

    # Seleciona uma materia
    materia = Materia.query.filter_by(nome_simples=nome_simples).first()

    # Seleciona os cursos de uma matéria
    cursos = materia.cursos.all()

    topicos = materia.topicos.all()
    
    licoes = materia.licoes.all()


    return render_template(
        'painel/materia.html',
        materia=materia,
        cursos=cursos,
        topicos=topicos,
        licoes=licoes
    )


# API
# Retorna uma lista de cursos relacionada a determidada materias
# Usado nos formulários de criação
@bp.route('/materia/selecionar_cursos', methods=['POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def selecionar_cursos(id):

    try:
        # Seleciona o JSON enviado através do pedido do cliente
        json_enviado = request.get_json()
        
        materia_nome_simples = json_enviado['materia']

        materia = Materia.query.filter_by(nome_simples=materia_nome_simples).first()

        cursos = Curso.query.filter_by(materia_id=materia.id).all()

        json_retornado = {
            "materia": materia_nome_simples,
            "cursos": [],
        }

        for c in cursos:

            objeto_curso = {
                'id': c.id,
                'nome': c.nome
            }

            json_retornado['cursos'].append(objeto_curso)


        # Retorna JSON confirmando registro do comentário
        return jsonify(json_retornado)

    except Exception as e:

        print("AJAX exceção " + str(e))
        return(str(e))


@bp.route('/materia/<int:id>/alunos', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia_alunos(id):
    return 1


@bp.route('/materia/<int:id>/instrutores', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia_instrutores(id):
    return 1


@bp.route('/materia/<int:id>/moderadores', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia_moderadores(id):
    return 1


@bp.route('/materia/<int:id>/topicos', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia_topicos(id):
    return 1


@bp.route('/materia/<int:id>/licoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia_licoes():
    return 1


@bp.route('/materia/<int:id>/questoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def materia_questoes():
    return 1




"""
#####################################################

##### #   # ##### ##### ##### ##### 
#     #   # #   # #     #   # #     
#     #   # ##### ##### #   # ##### 
#     #   # #  #      # #   #     # 
##### ##### #   # ##### ##### #####

#####################################################
"""



# LISTAR CURSOS
@bp.route('/cursos')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def cursos():

    cursos = Curso.query.all()

    return render_template('painel/cursos.html', cursos=cursos)


# PÁGINA DE UM CURSO
@bp.route('/curso/<int:id>')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso(id):

    curso = Curso.query.filter_by(id=id).first()

    return render_template('painel/curso.html', curso=curso)


# CRIAR CURSO
@bp.route('/criar_curso', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def criar_curso():

    formulario = formularioCursoPainel()

    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit():

        try:
            # Seleciona a foto
            foto = request.files['foto']

            # Formata o nome do arquivo
            nome_arquivo = foto.filename
            nome_arquivo2 = nome_arquivo.replace("'", "")
            nome_arquivo3 = nome_arquivo2.replace(" ", "_")
   
            # Se a extensão do arquivo for permitida
            if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                # Tenta salvar a foto em app/static/image/produto
                salvar_foto = fotos.save(foto, folder="cursos")
                
                # Se a foto tiver sido salva corretamente
                if salvar_foto:

                    curso = registrar_curso(formulario, nome_arquivo3)
                    
                    db.session.add(curso)

                    db.session.commit()

            flash("Artigo criado com sucesso. 🙂", 'alert-success')

        except Exception as e:

            print("\n\nErro: ", e)

            flash("Um erro ocorreu durante a criação do artigo. 🙁", 'alert-danger')

        return redirect(url_for('painel.painel'))
        

    return render_template('painel/criar_curso.html', formulario=formulario)


@bp.route('/editar_curso', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ADMIN)
def editar_curso():
    return 1


# API
# Retorna uma lista de tópicos relacionados a um determinado cursos
# Usado nos formulários de criação
@bp.route('/curso/selecionar_topicos', methods=['POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def api_curso_topicos():

    try:

        # Seleciona o JSON enviado através do pedido do cliente
        json_enviado = request.get_json()
        
        curso_id = json_enviado['curso_id']

        # Seleciona o curso
        curso = Curso.query.filter_by(id=curso_id).first()

        # Seleciona os tópicos do curso
        topicos = Topico.query.filter_by(curso_id=curso_id).all()

        # Inicializa um objeto JSON
        json_retornado = {
            "curso": curso.nome,
            "topicos": [],
        }

        # Para cada tópico do curso
        for t in topicos:

            objeto_topico = {
                'id': t.id,
                'titulo': t.titulo
            }

            json_retornado['topicos'].append(objeto_topico)


        # Retorna JSON confirmando registro do comentário
        return jsonify(json_retornado)

    except Exception as e:

        print("AJAX exceção " + str(e))
        return(str(e))



@bp.route('/curso/<int:id>/alunos', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso_alunos(id):
    return 1


@bp.route('/curso/<int:id>/instrutores', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso_instrutores(id):
    return 1


@bp.route('/curso/<int:id>/moderadores', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso_moderadores(id):
    return 1



@bp.route('/curso/<int:id>/topicos', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso_topicos(id):
    return 1


@bp.route('/curso/<int:id>/licoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso_licoes(id):
    return 1


@bp.route('/curso/<int:id>/questoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def curso_questoes(id):
    return 1




"""
#####################################################

##### ##### ##### ##### ##### ##### ##### 
  #   #   # #   #   #   #     #   # #     
  #   #   # #####   #   #     #   # ##### 
  #   #   # #       #   #     #   #     # 
  #   ##### #     ##### ##### ##### #####

#####################################################
"""


# LISTAR TÓPICOS DE UM CURSO
@bp.route('/topicos')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def topicos():

    topicos = Topico.query.all()

    return render_template('painel/topicos.html', topicos=topicos)



# PÁGINA DE UM TÓPICO
@bp.route('/topico/<int:id>')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def topico(id):

    topico = Topico.query.filter_by(id=id).first()

    return render_template('painel/topico.html', topico=topico)



# CRIAR TÓPICO PARA UM CURSO
@bp.route('/criar_topico', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def criar_topico():

    formulario = formularioTopicoPainel()

    # Se o método for POST e o cliente tiver permissão para criar tópicos de cursos
    if formulario.validate_on_submit():

        try:
            # Seleciona a foto
            foto = request.files['foto']

            # Formata o nome do arquivo
            nome_arquivo = foto.filename
            nome_arquivo2 = nome_arquivo.replace("'", "")
            nome_arquivo3 = nome_arquivo2.replace(" ", "_")
   
            # Se a extensão do arquivo for permitida
            if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                # Tenta salvar a foto em app/static/image/produto
                salvar_foto = fotos.save(foto, folder="topicos")
                
                # Se a foto tiver sido salva corretamente
                if salvar_foto:

                    topico = registrar_topico(formulario, nome_arquivo3)
                    
                    db.session.add(topico)

                    db.session.commit()

            flash("Tópico criado com sucesso. 🙂", 'alert-success')

        except Exception as e:

            print("\n\nErro: ", e)

            flash("Um erro ocorreu durante a criação do tópico. 🙁", 'alert-danger')

        return redirect(url_for('painel.painel'))

    return render_template('painel/criar_topico.html', formulario=formulario)



@bp.route('/editar_topico/<int:id>', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ADMIN)
def editar_topico(id):
    return 1



@bp.route('/topico/<int:id>/licoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def topico_licoes():
    return 1


@bp.route('/topico/<int:id>/questoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def topico_questoes():
    return 1




"""
#####################################################

#     ##### ##### ##### ##### ##### 
#       #   #     #   # #     #     
#       #   #     #   # ##### ##### 
#       #   #     #   # #         # 
##### ##### ##### ##### ##### #####

#####################################################
"""


# LISTAR LIÇÕES DE UM TÓPICO
@bp.route('/licoes')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def licoes():

    licoes = Licao.query.all()

    return render_template('painel/licoes.html', licoes=licoes)


# PÁGINA DE UMA LIÇÃO
@bp.route('/licao/<int:id>')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def licao(id):

    licao = Licao.query.filter_by(id=id).first()

    return render_template('painel/licao.html', licao=licao)


# CRIAR LIÇÃO PARA UM TÓPICO DE UM CURSO
@bp.route('/criar_licao', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def criar_licao():

    formulario = formularioLicaoPainel()

    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit():

        try:

            # Seleciona a foto
            foto = request.files['foto']

            # Formata o nome do arquivo
            nome_arquivo = foto.filename
            nome_arquivo2 = nome_arquivo.replace("'", "")
            nome_arquivo3 = nome_arquivo2.replace(" ", "_")
            
            # Se a extensão do arquivo for permitida
            if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                # Tenta salvar a foto em app/static/image/produto
                salvar_foto = fotos.save(foto, folder="licoes")
                
                # Se a foto tiver sido salva corretamente
                if salvar_foto:

                    licao = registrar_licao(formulario, nome_arquivo3)
                    
                    db.session.add(licao)

                    db.session.commit()


            flash("Lição criada com sucesso. 🙂", 'alert-success')

        except Exception as e:

            print("Erro: ", e)
            
            flash("Um erro ocorreu durante a criação da lição. 🙁", 'alert-danger')

        return redirect(url_for('painel.painel'))
        
    return render_template('painel/criar_licao.html', formulario=formulario)


@bp.route('/licao/<int:id>/questoes', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def licao_questoes():
    return 1


"""
#####################################################

 ###  #   # ##### ##### ##### ##### ##### ##### 
#   # #   # #     #       #   #   # #     #     
#   # #   # ##### #####   #   #   # ##### ##### 
 ###  #   # #         #   #   #   # #         # 
   ## ##### ##### #####   #   ##### ##### #####

#####################################################
"""



# LISTAR QUESTÕES DE DETERMINADA LIÇÃO/TÓPICO
@bp.route('/questoes')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def questoes():

    questoes = Questao.query.all()

    return render_template('painel/questoes.html', questoes=questoes)


# PÁGINA DE UMA QUESTÃO
@bp.route('/questao/<int:id>')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def questao(id):

    questao = Questao.query.filter_by(id=id).first()
    
    return render_template('painel/questao.html', questao=questao)


# CRIAR QUESTÃO PARA UMA LIÇÃO
@bp.route('/criar_questao', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def criar_questao():

    formulario = formularioQuestaoPainel()

    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit():

        try:
            questao = registrar_questao(formulario)  
            db.session.add(questao)
            db.session.commit()
            flash("Questão criada com sucesso. 🙂", 'alert-success')

        except Exception as e:
            print("Erro: ", e)
            flash("Um erro ocorreu durante a criação da questão. 🙁", 'alert-danger')
        

        return redirect(url_for('painel.painel'))
    

    return render_template('painel/criar_questao.html', formulario=formulario)



"""
#####################################################

 ###  ##### ##### ##### ##### ##### ##### 
## ## #   #   #     #   #     #   # #     
#   # #####   #     #   # ### #   # ##### 
##### #  #    #     #   #   # #   #     # 
#   # #   #   #   ##### ##### ##### ##### 

#####################################################
"""



# LISTAR ARTIGOS
@bp.route('/artigos')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def artigos():

    artigos = Publicacao.query.all()

    return render_template('painel/artigos.html', artigos=artigos)


# PÁGINA DE UM ARTIGO
@bp.route('/artigo/<int:id>')
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def artigo(id):

    artigo = Publicacao.query.filter_by(id=id).first()
    
    return render_template('painel/artigo.html', artigo=artigo)


# CRIAR ARTIGO
@bp.route('/criar_artigo', methods=['GET', 'POST'])
@login_required
@permissao_necessaria(Permissao.ESCREVER_BLOG)
def criar_artigo():

    
    formulario = formularioArtigoPainel()

    # Se o método for POST e o cliente tiver permissão para escrever no mural
    if formulario.validate_on_submit():

        try:
            # Seleciona a foto
            foto = request.files['foto']

            # Formata o nome do arquivo
            nome_arquivo = foto.filename
            nome_arquivo2 = nome_arquivo.replace("'", "")
            nome_arquivo3 = nome_arquivo2.replace(" ", "_")
            
            # Se a extensão do arquivo for permitida
            if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                # Tenta salvar a foto em app/static/imagens/
                salvar_foto = fotos.save(foto, folder="artigos")
                
                # Se a foto tiver sido salva corretamente
                if salvar_foto:

                    
                    artigo = registrar_artigo(formulario, nome_arquivo3)
                    
                    db.session.add(artigo)

                    db.session.commit()


            flash("Artigo criado com sucesso. 🙂", 'alert-success')

        except:
            flash("Um erro ocorreu durante a criação do artigo. 🙁", 'alert-danger')

        return redirect(url_for('painel.painel'))
        

    return render_template('painel/criar_artigo.html', formulario=formulario)

