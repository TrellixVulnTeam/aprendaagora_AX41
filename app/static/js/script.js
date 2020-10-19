

/* Quando o DOM for carregado */
document.addEventListener('DOMContentLoaded', () => {


    /* ---------- COMPORTAMENTO DA BARRA DE NAVEGAÇÃO MOBILE ---------- */

    let blog_botao = document.querySelector('#blog-botao');
    let idiomas_botao = document.querySelector('#idiomas-botao');
    let tech_botao = document.querySelector('#tech-botao');
    let menu_botao = document.querySelector('#menu-botao');

    const blog_icone = document.querySelector('#blog-icone');
    const idiomas_icone = document.querySelector('#idiomas-icone');
    const tech_icone = document.querySelector('#tech-icone');
    const menu_icone = document.querySelector('#menu-icone');

    let secao_principal = document.querySelector('#secao-principal');

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

    /* Para cada elemento 'publicacao' */
    publicacoes.forEach(publicacao => {

        /* Quando a publicação for clicada */
        publicacao.addEventListener('click', event => {
        
            /* Selecione a página inteira */
            let pagina = document.querySelector('body');

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

            /*
                Para cada publicação na lista de publicações
                
            */
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

            /* Crie um novo pedido HTTP*/
            let pedido = new XMLHttpRequest();

            /* Pega o id da publicação cujo div foi clicado.
            'publicacao_id' é uma string mas pode ser convertido
            para int antes de ser enviado para o servidor.
            Para isso, a função parseInt() está sendo usada*/
            let json_enviado = {'publicacao_id': parseInt(publicacao.dataset.id)} ;

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

                    /* Crie o elemento modal */
                    criar_modal(publicacao_dados);

                    /* Remova a restrição de eventos 'click' na página */
                    pagina.removeEventListener('click', previnirClick, true);


                /* Se o pedido não ocorrer corretamente */
                } else {

                    /* Remova a restrição de eventos 'click */
                    pagina.removeEventListener('click', previnirClick, true);

                }
            }

            /* Envia o objeto JSON para o servidor */
            pedido.send(JSON.stringify(json_enviado));
        });
    });

    /* ---------- FIM FUNCIONALIDADE MODAL ---------- */

    /* ---------- PREVINIR QUE CLICK NO LINK DO AUTOR DA PUBLICAÇÃO ABRA O MODAL ---------- */

    /* Seleciona todos os links para as páginas dos autores das publicações */
    let links_usuarios = document.querySelectorAll(".perfil-autor-link");

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

    /* ---------- FIM PREVENÇÃO DE CLICK NO LINK DO AUTOR ---------- */

});


/* Cria e exibe o modal de uma publicação que foi clicada. */

function criar_modal(publicacao) {

    /* 
        !!!
        A imagem de fundo e a lista de publicações sofrem interferência no posicionamento deles quando o modal é criado. Por isso, eu removi a imagem de fundo e a barra de scroll
    */

    /* Seleciona a página inteira (body) */
    let pagina = document.querySelector('body');

    /* Cria o div do modal (que será a área escura) */
    let modal = document.createElement('div');

    /* Adiciona a classe 'modal' ao div */
    modal.classList.add('modal');

    /* Seleciona a lista de publicações da página */
    let lista_publicacoes = document.querySelector('#lista-publicacoes');

    /* Anexa o modal no início da página 'body' */
    lista_publicacoes.prepend(modal);

    /*
        Cria um div que servirá de container para a publicação
        Isto é necessário para que o botão de fechar a publicação possa ser posicionado corretamente
    */
    let container_modal = document.createElement('div');

    /*
    /* Adiciona a classe '.container-modal 
    container_modal.classList.add('bg-primary');
    */

    /* Exibe o modal */
    ativarModal();

    /* Cria o div do conteúdo do modal (que será a área de fundo branco) */
    let conteudo_modal = document.createElement('div');

    /* Adiciona o conteúdo do modal ao container criado */
    container_modal.append(conteudo_modal);

    /* Anexa o conteúdo do modal no mural */
    modal.append(container_modal);

    /* Adiciona a classe 'conteudo-modal' ao div */
    conteudo_modal.classList.add('conteudo-modal');

    /* A classe .conteudo-modal-expandido ativa a animação de redimensionamento*/
    setTimeout( () => {conteudo_modal.classList.add('conteudo-modal-expandido');}, 50 );

    /* Adiciona padding ao div 0.5 milésimo após a animação de expansão for ativada */
    setTimeout( () => {conteudo_modal.classList.add('padding-modal');}, 100 );
    
    /* Cria o botão de fechar a publicação */
    let botao_fechar = document.createElement('span');
    botao_fechar.classList.add('botao-fechar');
    botao_fechar.innerHTML = "&times";

    /* Anexa o botão de fechar ao conteúdo do modal (APÓS 3 MILÉSIMOS) */
    setTimeout( () => {container_modal.append(botao_fechar);}, 300);
    
    /* Crie os elementos HTML que representarão aa publicação */
    let titulo_publicacao = document.createElement('h4');
    let conteudo_publicacao = document.createElement('p');
    let autor_publicacao = document.createElement('p');
    let data_publicacao = document.createElement('p');
    let avatar_autor_publicacao = document.createElement('img');

    /* Preencha os elemenos da publicação com seus respectivos dados */
    titulo_publicacao.innerText = publicacao.titulo;
    conteudo_publicacao.innerText = publicacao.conteudo;
    autor_publicacao.innerText = publicacao.autor
    /* URL do avatar do autor da publicação */
    avatar_autor_publicacao.src = publicacao.avatar_autor;
    /* Data da publicação gerada dinamicamente */
    data_publicacao.innerHTML = moment(publicacao.data).fromNow();

    /* Anexe os elementos da publicação ao conteúdo do modal */
    conteudo_modal.append(titulo_publicacao);
    conteudo_modal.append(conteudo_publicacao);
    conteudo_modal.append(autor_publicacao);
    conteudo_modal.append(data_publicacao);
    conteudo_modal.append(avatar_autor_publicacao);

    /* Exibe o Modal de uma publicação que foi clicada*/
    function ativarModal() {
        modal.classList.add('exibir-modal');
    }

    /* Fecha o Modal de uma publicação que foi clicada */
    function fecharModal() {


        conteudo_modal.textContent = '';

        conteudo_modal.classList.remove('padding-modal');

        /*conteudo_modal.classList.remove('conteudo-modal-expandido');*/

        setTimeout( () => {conteudo_modal.classList.remove('conteudo-modal-expandido');}, 25 );

        /* Remove (destroi) o modal do DOM () */
        setTimeout( () => {modal.remove();}, 250 );

        /* Exibe todos as publicações transparentes da página (alterando a opacidade) */
        let todas_publicacoes = document.querySelectorAll('.publicacao-mural');

        for (let p of todas_publicacoes) {

            p.style.opacity = 1;
        
            let elementos = p.querySelectorAll('*')

                        for (elemento of elementos) {

                            elemento.style.opacity = 1;
                        }
                        
        }

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


