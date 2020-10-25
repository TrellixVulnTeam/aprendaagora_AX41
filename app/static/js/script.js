/* Selecione a página inteira */
const pagina = document.querySelector('body');

/* Quando o DOM for carregado */
document.addEventListener('DOMContentLoaded', () => {
    
    /* ---------- COMPORTAMENTO DA BARRA DE NAVEGAÇÃO MOBILE ---------- */

    let secao_principal = document.querySelector('#secao-principal');

    let blog_botao = document.querySelector('#blog-botao');
    let idiomas_botao = document.querySelector('#idiomas-botao');
    let tech_botao = document.querySelector('#tech-botao');
    let menu_botao = document.querySelector('#menu-botao');

    const blog_icone = document.querySelector('#blog-icone');
    const idiomas_icone = document.querySelector('#idiomas-icone');
    const tech_icone = document.querySelector('#tech-icone');
    const menu_icone = document.querySelector('#menu-icone');

    blog_botao.addEventListener('click', e => {
    
        secao_principal.classList.add('margem-secao-principal');

        if (blog_botao.style.backgroundColor == 'white')
        {
            blog_icone.innerHTML = '<i class="fa fa-coffee"></i>';
            blog_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            blog_botao.style.color = 'white';

            secao_principal.classList.remove('margem-secao-principal');
        }
        else
        {   
            blog_icone.innerHTML = '<i class="fa fa-times"></i>';
            
            blog_botao.style.backgroundColor = 'white';
            blog_botao.style.color = 'black';

            idiomas_icone.innerHTML = '<i class="fa fa-language"></i>';
            idiomas_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            idiomas_botao.style.color = 'white';

            tech_icone.innerHTML = '<i class="fa fa-laptop"></i>';
            tech_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            tech_botao.style.color = 'white';

            menu_icone.innerHTML = '<i class="fa fa-ellipsis-h"></i>';
            menu_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            menu_botao.style.color = 'white';

        }

        $('#idiomas-lista').collapse('hide');
        $('#tech-lista').collapse('hide');
        $('#menu-lista').collapse('hide');
        $('#blog-lista').collapse('toggle');
    });

    idiomas_botao.addEventListener('click', e => {
    
        secao_principal.classList.add('margem-secao-principal');

        if (idiomas_botao.style.backgroundColor == 'white')
        {
            idiomas_icone.innerHTML = '<i class="fa fa-language"></i>';
            idiomas_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            idiomas_botao.style.color = 'white';

            secao_principal.classList.remove('margem-secao-principal');
            
        }
        else
        {
            idiomas_icone.innerHTML = '<i class="fa fa-times"></i>';

            idiomas_botao.style.backgroundColor = 'white';
            idiomas_botao.style.color = 'black';

            blog_icone.innerHTML = '<i class="fa fa-coffee"></i>';
            blog_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            blog_botao.style.color = 'white';

            tech_icone.innerHTML = '<i class="fa fa-laptop"></i>';
            tech_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            tech_botao.style.color = 'white';

            menu_icone.innerHTML = '<i class="fa fa-ellipsis-h"></i>';
            menu_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            menu_botao.style.color = 'white';

        }

        
        $('#blog-lista').collapse('hide');
        $('#tech-lista').collapse('hide');
        $('#menu-lista').collapse('hide');
        $('#idiomas-lista').collapse('toggle');
    });

    tech_botao.addEventListener('click', e => {
    
        secao_principal.classList.add('margem-secao-principal');

        if (tech_botao.style.backgroundColor == 'white')
        {
            tech_icone.innerHTML = '<i class="fa fa-laptop"></i>';
            tech_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            tech_botao.style.color = 'white';

            secao_principal.classList.remove('margem-secao-principal');
        }
        else
        {
            
            tech_icone.innerHTML = '<i class="fa fa-times"></i>';

            tech_botao.style.backgroundColor = 'white';
            tech_botao.style.color = 'black';

            idiomas_icone.innerHTML = '<i class="fa fa-language"></i>';
            idiomas_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            idiomas_botao.style.color = 'white';

            blog_icone.innerHTML = '<i class="fa fa-coffee"></i>';
            blog_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            blog_botao.style.color = 'white';

            menu_icone.innerHTML = '<i class="fa fa-ellipsis-h"></i>';
            menu_botao.style.backgroundColor = 'rgb(41, 186, 19)';
            menu_botao.style.color = 'white';

        }


        $('#blog-lista').collapse('hide');
        $('#idiomas-lista').collapse('hide');
        $('#menu-lista').collapse('hide');
        $('#tech-lista').collapse('toggle');
    });

    menu_botao.addEventListener('click', e => {
        
        secao_principal.classList.add('margem-secao-principal');
        
        if (menu_botao.style.backgroundColor == 'white')
        {
            menu_icone.innerHTML = '<i class="fa fa-ellipsis-h"></i>';
            menu_botao.style.backgroundColor = '#29ba13';
            menu_botao.style.color = 'white';

            secao_principal.classList.remove('margem-secao-principal');
        }
        else
        {
            menu_icone.innerHTML = '<i class="fa fa-times"></i>'

            menu_botao.style.backgroundColor = 'white';
            menu_botao.style.color = 'black';

            idiomas_icone.innerHTML = '<i class="fa fa-language"></i>';
            idiomas_botao.style.backgroundColor = '#29ba13';
            idiomas_botao.style.color = 'white';

            tech_icone.innerHTML = '<i class="fa fa-laptop"></i>';
            tech_botao.style.backgroundColor = '#29ba13';
            tech_botao.style.color = 'white';

            blog_icone.innerHTML = '<i class="fa fa-coffee"></i>';
            blog_botao.style.backgroundColor = '#29ba13';
            blog_botao.style.color = 'white';

        }

        $('#blog-lista').collapse('hide');
        $('#idiomas-lista').collapse('hide');
        $('#tech-lista').collapse('hide');
        $('#menu-lista').collapse('toggle');
    });
  
    secao_principal.addEventListener('click', e => {

        secao_principal.classList.remove('margem-secao-principal');

        $('#blog-lista').collapse('hide');
        $('#idiomas-lista').collapse('hide');
        $('#tech-lista').collapse('hide'); 
        $('#menu-lista').collapse('hide');

        blog_icone.innerHTML = '<i class="fa fa-coffee"></i>';
        blog_botao.style.backgroundColor = '#29ba13';
        blog_botao.style.color = 'white';
        
        idiomas_icone.innerHTML = '<i class="fa fa-language"></i>';
        idiomas_botao.style.backgroundColor = '#29ba13';
        idiomas_botao.style.color = 'white';

        tech_icone.innerHTML = '<i class="fa fa-laptop"></i>';
        tech_botao.style.backgroundColor = '#29ba13';
        tech_botao.style.color = 'white';

        menu_icone.innerHTML = '<i class="fa fa-ellipsis-h"></i>';
        menu_botao.style.backgroundColor = '#29ba13';
        menu_botao.style.color = 'white';
    });

    /* ---------- FIM DA CONFIGURAÇÃO DO COMPORTAMENTO DA BARRA DE NAVEGAÇÃO ---------- */



    /* ---------- FUNCIONALIDADE MODAL ----------

        Funcionalidade de exibição de publicação completa através de um modal
        Esta funcionalidade é usada nos murais dos idiomas
    */

    /* Seleciona todos os elementos com a classe '.publicacao-mural' */
    let publicacoes = document.querySelectorAll(".publicacao-mural");

    /* Adiciona um EventListener a cada publicação para que o modal da mesma seja ativado quando ela for clicada */
    detectar_clique_publicacoes(publicacoes);
    
    /* ---------- FIM FUNCIONALIDADE MODAL ---------- */



    /* ---------- PREVINIR QUE CLICK NO LINK DO AUTOR DA PUBLICAÇÃO ABRA O MODAL DA PUBLICACAO ---------- */

    /* Seleciona todos os links para as páginas dos autores das publicações */
    let links_usuarios = document.querySelectorAll(".perfil-autor-link");

    previnir_propagacao_clique_link(links_usuarios);

    /* ---------- FIM PREVENÇÃO DE CLICK NO LINK DO AUTOR ---------- */

});


/* Detecta clique nas publicações do mural e chama a função criar_modal */
function detectar_clique_publicacoes(publicacoes) {

    /* Para cada elemento 'publicacao' */
    publicacoes.forEach(publicacao => {

        /* Quando a publicação for clicada */
        publicacao.addEventListener('click', event => {

            /* Impeça a página de aceitar pedidos vindos de cliques em outros elementos até que o modal da primeira publicação clicada seja carregado */
            pagina.addEventListener('click', previnirClick, true);

            function previnirClick(e) {
                e.stopPropagation();
                e.preventDefault();
            }
            
            /* Impeça a página de rolar o conteúdo (scroll)*/
            pagina.classList.remove('body-scroll');
            pagina.classList.add('body-no-scroll');
            
            /* Seleciona todos as publicacoes na lista de publicações do mural */
            let todas_publicacoes = document.querySelectorAll('.publicacao-mural');

            /* Destaque a publicação clicada ao transparecer as outras publicações 
               Desabilitei esta funcionalidade por que ela atrasada a abertura do modal e a transparência 
               destacarPublicacaoClicada(todas_publicacoes, publicacao);
            */

            /* Crie um novo pedido HTTP*/
            let pedido = new XMLHttpRequest();

            /* Pega o id da publicação cujo div foi clicado.
            'publicacao_id' é uma string mas pode ser convertido
            para int antes de ser enviado para o servidor.
            Para isso, a função parseInt() está sendo usada*/
            let json_enviado = {"publicacao_id": parseInt(publicacao.dataset.id)} ;

            /* Abra o pedido com método 'POST' na rota '/ingles/publicacao/json' */
            pedido.open('POST', '/ingles/publicacao/json');

            /* ??? */
            pedido.setRequestHeader('Content-Type', 'application/json');

            /* Quando o pedido for respondido */
            pedido.onload = function (e) {

                /* 

                    'pedido.readyState' representa o estado do pedido
                    
                    0 representa o estado UNSENT (Um cliente foi criado. Mas o método open() não foi chamado ainda).
                    1 representa o estado OPENED (O método open() foi chamado).
                    2 representa o estado HEADERS_RECEIVED (O método send() foi chamado e os cabeçalhos e status estão disponíveis.
                    3 representa o estado LOADING (Baixando e pedido.responseText contém os dados parciais).
                    4 representa o estado DONE (Operação concluída).

                    'pedido.status' é o código de status de uma resposta HTTP. Ele indica se uma requisição HTTP foi concluída corretamente. Um status 200 indica que a operação foi concluída corretamente.
                */

                /* 
                    Se o estado do pedido for DONE e o status da resposta for 200 (OK)
                    O script terá acesso à resposta em formato JSON enviado pelo servidor    
                */
                if (pedido.readyState === 4 && pedido.status === 200) {

                    /*
                        A resposta do servidor, chamado de 'pedido.responseText',  é uma string que representa um objeto (em outras palavras, pedido.responseText é o json que o servidor enviou).
                        A função JSON.parse() pode ser usada para converter essa string em um objeto JSON propriamente dito.

                        O objeto recebido representa a publicação clicada
                    */
                    let publicacao_dados = JSON.parse(pedido.responseText);

                    /*
                        O título e o autor da publicação já estão disponíveis no dataset do elemento HTML,
                        portanto eles não precisam ser enviados pelo servidor pois podem ser acessados diretamente aqui.
                    */
                    publicacao_dados.titulo = publicacao.dataset.titulo;
                    publicacao_dados.autor = publicacao.dataset.autor;

                    /* Crie o Modal do publicação */
                    criar_modal(publicacao_dados);

                    /* Remova a restrição de eventos 'click' na página */
                    pagina.removeEventListener('click', previnirClick, true);


                /* Se o pedido não ocorrer corretamente */
                } else {

                    /* Remova a restrição de eventos 'click */
                    pagina.removeEventListener('click', previnirClick, true);

                }
            }

            /* Envie o pedido para o servidor, juntamento com o id da publicação */
            pedido.send(JSON.stringify(json_enviado));
        });
    });

}

/* Cria e exibe o modal de uma publicação que foi clicada. */
function criar_modal(publicacao) {

    /* Cria o div do modal (que será a área escura) */
    let modal = document.createElement('div');

    /*
        Adiciona a classe 'modal' ao div
        Esta classe define o posicionamento e dimensões do modal para que ele ocupe a tela toda
    */
    modal.classList.add('modal');
    

    /* Seleciona a lista de publicações do mural */
    let lista_publicacoes = document.querySelector('#lista-publicacoes');

    /* Anexa o modal no início da lista de publicações */
    lista_publicacoes.prepend(modal);

    /*
        Cria um div que servirá de container para a publicação
        Isto é necessário para que o botão de fechar a publicação possa ser posicionado corretamente
    */
    let container_modal = document.createElement('div');

    container_modal.setAttribute('id', 'container-modal');


    /* Exibe o modal */
    ativarModal();

    /* Cria o container da publicação no modal (que será a área de fundo branco) */
    let publicacao_modal = document.createElement('div');

    /* Adiciona o container da publicação ao container do modal criado */
    container_modal.append(publicacao_modal);

    /* Anexa o container do modal ao modal */
    modal.append(container_modal);

    /*
        Adiciona a classe 'publicacao-modal' ao container
        Esta classe define:
        
            borda verde-limão
            fundo branco
            largura e altura 2 px (para que a animação de redimensionamento funcione)
            overflow auto
            position, top, left, e transform definidos de forma que o container da publicação seja centralizado modal
    */
    publicacao_modal.classList.add('publicacao-modal');

    /* A classe .publicacao-modal-expandido ativa a animação de redimensionamento */
    setTimeout( () => {publicacao_modal.classList.add('publicacao-modal-expandido');}, 50 );

    /* Adiciona padding ao container da publicação 1 milésimo após a animação de expansão for ativada */
    setTimeout( () => {publicacao_modal.classList.add('padding-publicacao-modal');}, 100 );
    
    /* Cria o botão de fechar a publicação */
    let botao_fechar = document.createElement('span');
    botao_fechar.classList.add('botao-fechar');
    botao_fechar.innerHTML = "&times";

    /* Anexa o botão de fechar ao conteúdo do modal (APÓS 1.5 MILÉSIMO) */
    setTimeout( () => {container_modal.append(botao_fechar);}, 150);
    
    /* Preenche o container com os elementos da publicação */
    publicacao_modal = criar_publicacao_modal(publicacao_modal, publicacao);


    /* Crie os elementos da publicação e preencha o container com as informações */
    function criar_publicacao_modal(publicacao_modal, publicacao) {


        /* ID DA PUBLICAÇÃO */
        
        let id_publicacao = document.createElement('small');
        id_publicacao.classList.add('text-secondary', 'mb-1');
        id_publicacao.innerText = `publicação #${publicacao.id}`;

        /* TÍTULO DA PUBLICAÇÃO */

        let titulo_publicacao = document.createElement('h4');
        titulo_publicacao.innerText = publicacao.titulo;

        /* FIM DA SEÇÃO DO TÍTULO DA PUBLICAÇÃO */
        

        /* --------------------------------------------------------------------------- */


        /* SEÇÃO COM INFORMAÇÕES SOBRE A PUBLICAÇÃO (LINK DO ATOR, NOME DO AUTOR, AVATAR DO AUTOR, DATA, IDIOMA E TAGS) */


        /* Cria o container para abrigar as informações */
        let info_publicacao = document.createElement('div');
        info_publicacao.classList.add('mb-5')

        /* Cria um elemento 'âncora' que será o link para o perfil do autor */
        let link_perfil_autor = document.createElement('a');
        
        /* Cria a imagem do autor */
        let avatar_autor_publicacao = document.createElement('img');
        /* Adiciona a classe 'avatar-autor' */
        avatar_autor_publicacao.classList.add('avatar-autor');
        /* URL do avatar do autor da publicação */
        avatar_autor_publicacao.src = publicacao.avatar_autor;

        /* Cria um <span> que abrigará o nome do autor */
        let autor_publicacao = document.createElement('span');
        /* Concatena um '@' no início do nome do autor */
        autor_publicacao.innerText = '@'.concat(publicacao.autor);
        autor_publicacao.classList.add('ml-1');
        
        /* Anexa o nome e imagem do autor no elemento âncora */
        link_perfil_autor.append(avatar_autor_publicacao);
        link_perfil_autor.append(autor_publicacao);

        /* Define o link que leva à página de perfil do autor */
        /* 'publicacao.autor' é usado ao invés de 'autor_publicacao' pois 'autor_publicacao' teve um @ inserido no início da string */
        link_perfil_autor.href = '/usuario/'.concat(publicacao.autor);

        info_publicacao.append(link_perfil_autor);


        /* Cria um <span> que conterá a data da publicação */
        let data_publicacao = document.createElement('span');

        data_publicacao.innerHTML = '&middot; <i class="fa fa-history"></i> escrito '.concat(moment(publicacao.data).fromNow());

        data_publicacao_envelope = document.createElement('span');
        data_publicacao_envelope.classList.add('text-secondary', 'ml-1');
        data_publicacao_envelope.append(data_publicacao);


        /* Seleciona a string que representa o nome do idioma */
        let idioma_publicacao = publicacao.idioma;

        /* Cria um <span> que representará o ícone do idioma */
        let icone_idioma = document.createElement('span');

        /* Preenche o <span> com a bandeira correta */
        icone_idioma.innerText = selecionar_icone_idioma(idioma_publicacao);

        /* Adiciona a classe para corrigir posicionamento do ícone */
        icone_idioma.classList.add('icone-idioma-modal');

        /* Seleciona as tags da publicacao */
        let tags_publicacao = publicacao.tags;

        /* Elemento que vai envolver as tags da publicação */
        let tags_container = document.createElement('span');

        tags_container.classList.add('tags-container');

        /* Para cada tag na lista de tags da publicação, crie a tag no DOM e anexe ao container*/
        for (tag of tags_publicacao) {
            
            /* Crie um elemento <span> que representará a tag */
            let t = document.createElement('span');
            t.classList.add('badge', 'badge-pill', 'mr-1');

            /* Se a tag for 'vocabulário' */
            if (tag == 'vocabulario')
            {
                t.classList.add('badge-success');
                t.innerHTML = '<i class="fa fa-book mr-0 text-white"></i>';
            }
            /* Se a tag for 'gramática' */
            else if (tag == 'gramatica')
            {
                t.classList.add('badge-primary');
                t.innerHTML = '<i class="fa fa-cogs mr-0"></i>';
            }
            /* Se a tag for 'pronúncia' */
            else if (tag == 'pronuncia')
            {
                t.classList.add('badge-danger');
                t.innerHTML = '<i class="fa fa-headphones mr-0"></i>';
            }
            /* Se a tag for 'cultura' */
            else if (tag == 'cultura')
            {
                t.classList.add('badge-dark');
                t.innerHTML = '<i class="fa fa-globe mr-0"></i>';
            }
            
            /* Anexe a tag ao container */
            tags_container.append(t);
        }

        info_publicacao.append(data_publicacao_envelope);
        info_publicacao.append(icone_idioma);
        info_publicacao.append(tags_container);

        /* FIM DA SEÇÃO COM INFORMAÇÕES SOBRE PUBLICAÇÃO */


        /* --------------------------------------------------------------------------- */


        /* SEÇÃO DO CONTEÚDO DA PUBLICAÇÃO */
        
        /* Preencha os elemenos da publicação com seus respectivos dados */
        let conteudo_publicacao = document.createElement('div');

        /* Se a versão HTML do conteúdo da publicação estiver definido */
        if (publicacao.conteudo_html != undefined)
        {
            conteudo_publicacao.innerHTML = publicacao.conteudo_html;
        }
        /* Senão, utilize o conteúdo em texto-plano */
        else
        {
            conteudo_publicacao.innerHTML = publicacao.conteudo;
        }

        /* FIM DA SEÇÃO DO CONTEÚDO DA PUBLICAÇÃO */


        /* --------------------------------------------------------------------------- */


        let div_publicacao = document.createElement('div');
        div_publicacao.setAttribute('id', 'container-publicacao');
        div_publicacao.classList.add('border', 'border-secondary', 'p-3');


        /* Anexa o TÍTULO, INFORMAÇÕES e CONTEÚDO da publicação SOMENTE APÓS definir se as OPÇÕES de AUTOR serão anexadas */
        div_publicacao.append(id_publicacao);
        div_publicacao.append(titulo_publicacao);
        div_publicacao.append(info_publicacao);
        div_publicacao.append(conteudo_publicacao);

        publicacao_modal.append(div_publicacao);

        /* Se o cliente for o AUTOR da publicação */
        if (publicacao.autor_cliente)
        {
            /* Cria os opções de autor (BOTÃO EDITAR E BOTÃO APAGAR) */
            let opcoes_autor = document.createElement('div');
            let botao_editar = document.createElement('span');
            let botao_apagar = document.createElement('span');
    
            /* Preenche os botões com a legenda */
            botao_editar.innerHTML = 'Editar <i class="fa fa-pencil"></i>';
            botao_apagar.innerHTML = 'Apagar <i class="fa fa-times-circle"></i>';

            /* Adiciona as classes de estilização aos botões */
            botao_editar.classList.add('badge', 'badge-primary');
            botao_apagar.classList.add('badge', 'badge-danger', 'ml-1');
    
            /* Adiciona as classes de estilização ao container das opções de autor */
            opcoes_autor.classList.add('text-right', 'mb-3');

            /* Anexa os botões de opções de autor ao container das opções */
            opcoes_autor.append(botao_editar);
            opcoes_autor.append(botao_apagar);

            /* Anexa o container das opções de autor ao container da publicação */
            div_publicacao.prepend(opcoes_autor);

            

            /*
                Quando o botão de editar for clicado,
                empurre a publicação para baixo e exiba o formulário.
            */
            botao_editar.addEventListener('click', () => {

                /* Esconde as opções do autor para que o cliente não crie formulários a mais ou apague a publicação durante edição (clicando no ícone) */
                opcoes_autor.style.visibility = 'hidden';


                /* Crie o container do formulário de edição */
                let container_formulario = document.createElement('div');

            
                /* ------------------------------------------------ */

                
                /* Crie o FORMULÁRIO de EDIÇÃO da PUBLICAÇÃO */
                let formulario_edicao = document.createElement('form');

                /* Adicione bordas e margem no topo do formulário */
                formulario_edicao.classList.add('mt-3', 'mb-3');


                /* ------------------------------------------------ */


                /* Cria o container e os botões das opções disponíveis durante a edição  */
                let opcoes_autor_edicao = document.createElement('div');
                let botao_salvar = document.createElement('span');
                let botao_cancelar = document.createElement('span');

                /* Preenche os botões com a legenda */
                botao_salvar.innerHTML = 'Salvar Alterações <i class="fa fa-save"></i>';
                botao_cancelar.innerHTML = 'Cancelar Edição <i class="fa fa-times-circle"></i>';

                /* Adiciona as classes de estilização aos botões */
                botao_salvar.classList.add('badge', 'badge-success');
                botao_salvar.setAttribute('type', 'submit');

                botao_cancelar.classList.add('badge', 'badge-secondary', 'ml-1');

                /* Adiciona as classes de estilização ao container das opções de autor */
                opcoes_autor_edicao.classList.add('text-right', 'mb-3');

                /* Anexa os botões de opções de autor ao container das opções */
                opcoes_autor_edicao.append(botao_salvar);
                opcoes_autor_edicao.append(botao_cancelar);


                /* ------------------------------------------------ */
                

                /* Crie o container que conterá o INPUT do TÍTULO da publicação */
                let container_input = document.createElement('div');
                
                /* Cria um elemento LABEL, adiciona cor escura à fonte, define como sendo a label do campo 'titulo_input_edicao', e define a string a ser exibida no label */
                let label_input = document.createElement('label');
                
                /* Cria um elemento INPUT, adiciona a classe .form-control (classe Bootstrap para formulários), define o id e o nome do campo, define o tipo do campo, e por fim preenche o campo com o título da publicação a ser editada */
                let titulo_input = document.createElement('input');
                
                /* Adicione a classe .form-group (que adiciona margem abaixo do elemento) */
                container_input.classList.add('form-group');

                /* Formata o label como no formulario WTF */
                label_input.classList.add('text-secondary');
                label_input.setAttribute('for', 'titulo-input-edicao');
                label_input.innerText = "Título da publicação";

                /* Formata o input como no formulário WTF */
                titulo_input.classList.add('form-control');
                titulo_input.setAttribute('id', 'titulo-input-edicao');
                titulo_input.setAttribute('name', 'titulo-input-edicao');
                titulo_input.setAttribute('type', 'text');
                titulo_input.value = titulo_publicacao.innerText;


                /* ------------------------------------------------ */


                /* Cria o container que conterá as opções de TAGS */
                let container_tags = document.createElement('div');
                container_tags.classList.add('row', 'row-cols-2', 'mb-3');

                /* Crie os containers que conterão a CAIXA DE SELEÇÃO e a LABEL da tag */
                let container_vocabulario = document.createElement('div');
                let container_gramatica = document.createElement('div');
                let container_pronuncia = document.createElement('div');
                let container_cultura = document.createElement('div');

                /* Cria as CAIXAS DE SELEÇÃO para as opções de TAGS */
                let tag_vocabulario = document.createElement('input');
                let tag_gramatica = document.createElement('input');
                let tag_pronuncia = document.createElement('input');
                let tag_cultura = document.createElement('input');

                /* Cria as LABELS das opções de TAGS */
                let label_vocabulario = document.createElement('label');
                let label_gramatica = document.createElement('label');
                let label_pronuncia = document.createElement('label');
                let label_cultura = document.createElement('label');

                container_vocabulario.classList.add('col', 'p-0');
                container_gramatica.classList.add('col', 'p-0');
                container_pronuncia.classList.add('col', 'p-0');
                container_cultura.classList.add('col', 'p-0');

                container_vocabulario.style.display = 'inline-block';
                container_gramatica.style.display = 'inline-block';
                container_pronuncia.style.display = 'inline-block';
                container_cultura.style.display = 'inline-block';

                tag_vocabulario.classList.add('checkbox-tag-edicao');
                tag_vocabulario.setAttribute('id', 'tags-0-edicao');
                tag_vocabulario.setAttribute('name', 'tags');
                tag_vocabulario.setAttribute('type', 'checkbox');
                tag_vocabulario.setAttribute('value', '1');

                tag_gramatica.classList.add('checkbox-tag-edicao');
                tag_gramatica.setAttribute('id', 'tags-1-edicao');
                tag_gramatica.setAttribute('name', 'tags');
                tag_gramatica.setAttribute('type', 'checkbox');
                tag_gramatica.setAttribute('value', '2');

                tag_pronuncia.classList.add('checkbox-tag-edicao');
                tag_pronuncia.setAttribute('id', 'tags-2-edicao');
                tag_pronuncia.setAttribute('name', 'tags');
                tag_pronuncia.setAttribute('type', 'checkbox');
                tag_pronuncia.setAttribute('value', '3');

                tag_cultura.classList.add('checkbox-tag-edicao');
                tag_cultura.setAttribute('id', 'tags-3-edicao');
                tag_cultura.setAttribute('name', 'tags');
                tag_cultura.setAttribute('type', 'checkbox');
                tag_cultura.setAttribute('value', '4');


                label_vocabulario.classList.add('form-check-label', 'badge', 'badge-success', 'ml-1');
                label_vocabulario.setAttribute('for', 'tags-0-edicao');
                label_vocabulario.innerHTML = "<i class='fa fa-book'></i> Vocabulário";

                label_gramatica.classList.add('form-check-label', 'badge', 'badge-primary', 'ml-1');
                label_gramatica.setAttribute('for', 'tags-1-edicao');
                label_gramatica.innerHTML = "<i class='fa fa-cogs'></i> Gramática";

                label_pronuncia.classList.add('form-check-label', 'badge', 'badge-danger', 'ml-1');
                label_pronuncia.setAttribute('for', 'tags-2-edicao');
                label_pronuncia.innerHTML = "<i class='fa fa-headphones'></i> Pronúncia";

                label_cultura.classList.add('form-check-label', 'badge', 'badge-dark', 'ml-1');
                label_cultura.setAttribute('for', 'tags-3-edicao');
                label_cultura.innerHTML = "<i class='fa fa-globe'></i> Cultura";


                /* Marca as CAIXAS DE SELEÇÃO de acordo com as tags atribuídas à publicação */
                if (tags_publicacao.includes('vocabulario')) {
                    tag_vocabulario.checked = true;
                }
                if (tags_publicacao.includes('gramatica')) {
                    tag_gramatica.checked = true;
                }
                if (tags_publicacao.includes('pronuncia')) {
                    tag_pronuncia.checked = true;
                }
                if (tags_publicacao.includes('cultura')) {
                    tag_cultura.checked = true;
                }

                
                /* ------------------------------------------------ */


                /* Crie o container que conterá o TEXTAREA do CONTEÚDO da publicação */
                let container_textarea = document.createElement('div');
                /* Cria um elemento LABEL,  */
                let label_textarea = document.createElement('label');

                let conteudo_textarea = document.createElement('textarea');

                /* Adicione a classe .form-group (que adiciona margem abaixo do elemento) */
                container_textarea.classList.add('form-group');

                label_textarea.classList.add('text-secondary');
                label_textarea.setAttribute('for', 'conteudo-textarea-edicao');
                label_textarea.innerHTML = "Conteudo da publicação <small class='text-primary'>(prévia da publicação abaixo)</small>";

                conteudo_textarea.classList.add('form-control');
                conteudo_textarea.setAttribute('id', 'conteudo-textarea-edicao');
                conteudo_textarea.setAttribute('name', 'conteudo-textarea--edicao');
                conteudo_textarea.setAttribute('type', 'text');
                conteudo_textarea.setAttribute('rows', '10');

                /* Transforma o HTML em Markdown para o autor poder editar com mais controle. */
                var turndownService = new TurndownService();
                var markdown = turndownService.turndown(conteudo_publicacao.innerHTML);

                /* Textarea é preenchido com o MARKDOWN da publicação */
                conteudo_textarea.value = markdown;

                /* ------------------------------------------------ */


                /* Anexa a LEGENDA do INPUT e o INPUT do TÍTULO  da publicação */
                container_input.append(label_input);
                container_input.append(titulo_input);

                /* Anexa os CHECKBOXES TAGS e os LABELS das TAGS */
                container_vocabulario.append(tag_vocabulario);
                container_vocabulario.append(label_vocabulario);

                container_gramatica.append(tag_gramatica);
                container_gramatica.append(label_gramatica);

                container_pronuncia.append(tag_pronuncia);
                container_pronuncia.append(label_pronuncia);

                container_cultura.append(tag_cultura);
                container_cultura.append(label_cultura);

                container_tags.append(container_vocabulario);
                container_tags.append(container_gramatica);
                container_tags.append(container_pronuncia);
                container_tags.append(container_cultura);

                /* Anexa a LEGENDA do TEXTAREA e o TEXTAREA do CONTEÚDO da publicação */
                container_textarea.append(label_textarea);
                container_textarea.append(conteudo_textarea)
                
                /* ------------------------------------------------ */




                /* Anexa os elementos do formulário de edição  */
                formulario_edicao.append(opcoes_autor_edicao);
                formulario_edicao.append(container_input);  
                formulario_edicao.append(container_tags);
                formulario_edicao.append(container_textarea);
                




                /* Crie o div que vai expandir nos eixos X,Y para exibir o formulário */
                let div_formulario = document.createElement('div');
                div_formulario.classList.add('div-formulario', 'bg-light', 'border');

                div_formulario.append(formulario_edicao);

                container_formulario.append(div_formulario);

                container_formulario.classList.add('container-formulario-edicao');




                /* Pré-anexa o CONTAINER DO FORMULÁRIO no CONTAINER DA PUBLICAÇÃO (efeticamente, anexado o container do formulário antes do container com a publicação em si) */
                publicacao_modal.prepend(container_formulario);




                /* Expanda as dimensões do div_formulario após 1000 milésimos */
                setTimeout(function () {div_formulario.classList.add('div-formulario-expandindo');}, 100);


                container_formulario.classList.add('container-formulario-edicao-expandindo');

                container_formulario.classList.remove('container-formulario-edicao');


                setTimeout(function () {

                    container_formulario.classList.add('container-formulario-edicao-expandido');

                    container_formulario.classList.remove('container-formulario-edicao-expandindo');

                }, 100);
                




                /* Salva as alterações na publicação, remove o formulário de edição e exibe as opções de autor */
                botao_salvar.addEventListener('click', () => {


                    /*
                    
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    Salvar alterações no banco de dados
                    
                    */


                    /* Crie um novo pedido HTTP*/
                    let pedido = new XMLHttpRequest();

                    /* Pega o id da publicação cujo div foi clicado.
                    'publicacao_id' é uma string mas pode ser convertido
                    para int antes de ser enviado para o servidor.
                    Para isso, a função parseInt() está sendo usada*/
                    let json_enviado = {"publicacao_id": publicacao.id,"publicacao_titulo": titulo_input.value,"publicacao_conteudo": conteudo_textarea.value} ;

                    /* Abra o pedido com método 'POST' na rota '/ingles/publicacao/json' */
                    pedido.open('POST', '/ingles/publicacao/editar');

                    /* ??? */
                    pedido.setRequestHeader('Content-Type', 'application/json');

                    /* Quando o pedido for respondido */
                    pedido.onload = function (e) {

                    }

                    /* Envie o pedido para o servidor, juntamento com o id da publicação */
                    pedido.send(JSON.stringify(json_enviado));




                    div_formulario.classList.remove('div-formulario-expandindo');
                    
                    setTimeout(function () {
                        container_formulario.classList.add('container-formulario-edicao-encolhendo');
                    }, 100);


                    setTimeout(function () {
                        container_formulario.remove();
                    }, 1000)
                    
                    /* Exibe as opções de autor que foi escondida quando a edição começou */
                    opcoes_autor.style.visibility = 'visible';
                });




                /* Cancela a edição da publicação */
                botao_cancelar.addEventListener('click', () => {

                    /* Restaura o título original da publicação */
                    titulo_publicacao.innerText = publicacao.titulo;

                    /* Se a versão HTML do conteúdo da publicação estiver definido */
                    if (publicacao.conteudo_html != undefined)
                    {
                        conteudo_publicacao.innerHTML = publicacao.conteudo_html;
                    }
                    /* Senão, utilize o conteúdo em texto-plano */
                    else
                    {
                        conteudo_publicacao.innerHTML = publicacao.conteudo;
                    }


                    /* Remova a classe que expande o formulário */
                    div_formulario.classList.remove('div-formulario-expandindo');
                    
                    setTimeout(function () {
                        container_formulario.classList.add('container-formulario-edicao-encolhendo');
                    }, 100);


                    setTimeout(function () {
                        container_formulario.remove();
                    }, 1000)
                    
                    /* Exibe as opções de autor que foi escondida quando a edição começou */
                    opcoes_autor.style.visibility = 'visible';
                });




                /* PRÉVIA DA EDIÇÃO */

                if (typeof flask_pagedown_converter === "undefined")
                {
                    flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
                }

                titulo_input.addEventListener('keyup', () => {
                    
                    titulo_publicacao.innerHTML = titulo_input.value;
                })


                conteudo_textarea.addEventListener('keyup', () => {
    
                    conteudo_publicacao.innerHTML = flask_pagedown_converter(conteudo_textarea.value);
                })

            });
        }

        return publicacao_modal;
    }

    /* Exibe o Modal de uma publicação que foi clicada*/
    function ativarModal() {
        /* A classe .exibir-modal possui as configurações que tornam o modal visível */
        modal.classList.add('exibir-modal');
    }

    /* Fecha o Modal de uma publicação que foi clicada */
    function fecharModal() {

        /* Remove o conteúdo */
        publicacao_modal.textContent = '';

        /* Remove o padding */
        publicacao_modal.classList.remove('padding-publicacao-modal');

        /* Ativa animação de encolhimento 0.25 milésimos após o padding e o conteúdo forem removidos*/
        setTimeout( () => {publicacao_modal.classList.remove('publicacao-modal-expandido');}, 25 );

        /* Remove (destroi) o modal do DOM (1.25 milésimos após a publicação começar a encolher) */
        setTimeout( () => {modal.remove();}, 150 );

        /* Remove a caracteristica no-scroll */
        pagina.classList.remove('body-no-scroll');

        /* Adiciona a funcionalidade de scroll */
        pagina.classList.add('body-scroll');
    }

    /* Função ativada quando a janela é clicada durante a exibição de um modal */
    function janelaClicada(event) {

        /* Se o elemento que ativou o evento for o modal (fundo escuro) */
        if (event.target === modal) {

            /* Feche o modal da publicação */
            fecharModal();
        }
    }

    /* Se o botão ou a janela for clicada */
    botao_fechar.addEventListener('click', fecharModal);
    window.addEventListener('click', janelaClicada);
     
}

/* Previne que o evento de clicar no link do autor de uma publicação abra o modal da publicação */
function previnir_propagacao_clique_link(links_usuarios) {

    /* Para cada elemento 'link', evite abrir o modal da publicação antes de redirecionar para a página do autor da publicação */
    links_usuarios.forEach(link => {

        /* Quando o link for clicado */
        link.addEventListener('click', e => {
            
            /*
                Evitar propagação.
                Dessa forma, o evento de clicar no link não ativará o evento do elemento-pai do link, que neste caso é a publicação em si
            */
            e.stopPropagation();
        })
    });
}

/* Destaca a publicação clicada ao transparecer as outras publicações */
function destacar_publicacao_clicada(todas_publicacoes, publicacao) {

    /* Para cada publicação na lista de publicações */
    for (let p of todas_publicacoes)
    {
        /*destacarPublicacao(p, publicacao);*/

        /* Se a publicação for a publicação clicada */
        if (p.getAttribute('data-id') === publicacao.getAttribute('data-id'))
        {
            /* A publicação e todos seus elementos ficarão VISÍVEIS */
            p.style.opacity = 1;

                let elementos = p.querySelectorAll('*')

                for (elemento of elementos) {

                    elemento.style.opacity = 1;
                }
        }
        /* Se a publicação NÃO for a publicação clicada */
        else
        {
            /* A publicação e todos seus elementos ficarão TRANSPARENTES
            (até o modal for fechado) */
            p.style.opacity = 0.85;

                let elementos = p.querySelectorAll('*')

                for (elemento of elementos) {
                    elemento.style.opacity = 0.85;
                }
        }
    }
}

function selecionar_icone_idioma(idioma) {

    if (idioma == 'ingles')
    {
        return '🇺🇸';
    }
    else if (idioma == 'espanhol')
    {
        return '🇪🇸';
    }
    else if (idioma == 'frances')
    {
        return '🇫🇷';
    }
    else if (idioma == 'italiano')
    {
        return '🇮🇹';
    }
    else if (idioma == 'alemao')
    {
        return '🇩🇪';
    }
    else if (idioma == 'japones')
    {
        return '🇯🇵';
    }
    else if (idioma == 'chines')
    {
        return '🇨🇳';
    }
}

