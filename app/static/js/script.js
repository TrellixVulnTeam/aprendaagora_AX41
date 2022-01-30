// Selecione a página inteira */
const pagina = document.querySelector('body');


/*

#####  ###  #   #  ###  ##### ##### ##### ##### ##### ##### 
   #  ## ## #   # ## ## #     #     #   #   #   #   #   #   
   #  #   # #   # #   # ##### #     #####   #   #####   #   
#  #  #####  # #  #####     # #     #  #    #   #       #   
####  #   #   #   #   # ##### ##### #   # ##### #       #   

*/

// Quando o DOM for carregado */
document.addEventListener('DOMContentLoaded', () => {
    
    
    /* --- FUNCIONALIDADE MODAL ---

        Funcionalidade de exibição de publicação completa através de um modal
        Esta funcionalidade é usada nos murais dos idiomas
    */

    // Seleciona todos os elementos com a classe '.publicacao-mural' */
    let publicacoes = document.querySelectorAll(".publicacao-mural");

    // Adiciona um EventListener a cada publicação para que o modal da mesma seja ativado quando ela for clicada */
    detectar_clique_publicacoes(publicacoes);
    
    /* --- FIM FUNCIONALIDADE MODAL --- */


    /* --- PREVINIR QUE CLICK NO LINK DO AUTOR DA PUBLICAÇÃO ABRA O MODAL DA PUBLICACAO --- */

    // Seleciona todos os links para as páginas dos autores das publicações */
    let links_usuarios = document.querySelectorAll(".perfil-autor-link");

    previnir_propagacao_clique_link(links_usuarios);

    /* --- FIM PREVENÇÃO DE CLICK NO LINK DO AUTOR --- */

});


// Detecta clique nas publicações do mural e chama a função criar_modal
function detectar_clique_publicacoes(publicacoes) {

    // Para cada elemento 'publicacao' */
    publicacoes.forEach(publicacao => {

        // Quando a publicação for clicada */
        publicacao.addEventListener('click', event => {

            // Impeça a página de aceitar pedidos vindos de cliques em outros elementos até que o modal da primeira publicação clicada seja carregado */
            pagina.addEventListener('click', previnirClick, true);

            function previnirClick(e) {
                e.stopPropagation();
                e.preventDefault();
            }
            
            // Impeça a página de rolar o conteúdo (scroll)*/
            pagina.classList.remove('body-scroll');
            pagina.classList.add('body-no-scroll');
            

            // Crie um novo pedido HTTP*/
            let pedido = new XMLHttpRequest();

            /* Pega o id da publicação cujo div foi clicado.
            'publicacao_id' é uma string mas pode ser convertido
            para int antes de ser enviado para o servidor.
            Para isso, a função parseInt() está sendo usada*/

            let json_enviado = {"publicacao_id": parseInt(publicacao.dataset.id)} ;

            // Abra o pedido com método 'POST' na rota '/ingles/publicacao/json' */
            pedido.open('POST', '/ingles/publicacao/json');

            // ??? */
            pedido.setRequestHeader('Content-Type', 'application/json');

            // Quando o pedido for respondido */
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

                    console.log(publicacao_dados);

                    // Crie o Modal do publicação */
                    criar_modal(publicacao_dados);

                    // Remova a restrição de eventos 'click' na página */
                    pagina.removeEventListener('click', previnirClick, true);

                // Se o pedido não ocorrer corretamente */
                } else {

                    // Remova a restrição de eventos 'click */
                    pagina.removeEventListener('click', previnirClick, true);

                }
            }

            // Envie o pedido para o servidor, juntamento com o id da publicação */
            pedido.send(JSON.stringify(json_enviado));
        });
    });

}

// Cria e exibe o modal de uma publicação que foi clicada.
function criar_modal(publicacao) {

    //console.log("Número de momentários: " + publicacao['comentarios'].length);

    // Cria o div do modal (que será a área escura) */
    let modal = document.createElement('div');

    /*
        Adiciona a classe 'modal' ao div
        Esta classe define o posicionamento e dimensões do modal para que ele ocupe a tela toda
    */
    modal.classList.add('modal-publicacao', 'modal');
    modal.setAttribute('id', 'modal-publicacao');
    

    // Seleciona a lista de publicações do mural */
    let lista_publicacoes = document.querySelector('#lista-publicacoes');

    // Anexa o modal no início da lista de publicações */
    lista_publicacoes.prepend(modal);

    /*
        Cria um div que servirá de container para a publicação
        Isto é necessário para que o botão de fechar a publicação possa ser posicionado corretamente
    */
    let container_modal = document.createElement('div');

    container_modal.setAttribute('id', 'container-modal');


    // Exibe o modal */
    ativarModal();

    // Cria o container da publicação no modal (que será a área de fundo branco) */
    let publicacao_modal = document.createElement('div');

    // Adiciona o container da publicação ao container do modal criado */
    container_modal.append(publicacao_modal);

    // Anexa o container do modal ao modal */
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

    // A classe .publicacao-modal-expandido ativa a animação de redimensionamento */
    setTimeout( () => {publicacao_modal.classList.add('publicacao-modal-expandido');}, 50 );

    // Adiciona padding ao container da publicação 1 milésimo após a animação de expansão for ativada */
    setTimeout( () => {publicacao_modal.classList.add('padding-publicacao-modal');}, 100 );
    
    // Cria o botão de fechar a publicação */
    let botao_fechar = document.createElement('span');
    botao_fechar.classList.add('botao-fechar');
    botao_fechar.innerHTML = "&times";

    // Anexa o botão de fechar ao conteúdo do modal (APÓS 1.5 MILÉSIMO) */
    setTimeout( () => {container_modal.append(botao_fechar);}, 150);
    
    // Preenche o container com os elementos da publicação */
    publicacao_modal = criar_publicacao_modal(publicacao_modal, publicacao);



    let lista_de_comentarios = criar_lista_de_comentarios(publicacao.comentarios);

    publicacao_modal.append(lista_de_comentarios);


    
    // Exibe o Modal de uma publicação que foi clicada*/
    function ativarModal() {
        // A classe .exibir-modal possui as configurações que tornam o modal visível */
        modal.classList.add('exibir-modal');
    }

    // Fecha o Modal de uma publicação que foi clicada */
    function fecharModal() {

        // Remove o conteúdo */
        publicacao_modal.textContent = '';

        // Remove o padding */
        publicacao_modal.classList.remove('padding-publicacao-modal');

        // Ativa animação de encolhimento 0.25 milésimos após o padding e o conteúdo forem removidos*/
        setTimeout( () => {publicacao_modal.classList.remove('publicacao-modal-expandido');}, 25 );

        // Remove (destroi) o modal do DOM (1.25 milésimos após a publicação começar a encolher) */
        setTimeout( () => {modal.remove();}, 150 );

        // Remove a caracteristica no-scroll */
        pagina.classList.remove('body-no-scroll');

        // Adiciona a funcionalidade de scroll */
        pagina.classList.add('body-scroll');
    }

    // Função ativada quando a janela é clicada durante a exibição de um modal */
    function janelaClicada(event) {

        // Se o elemento que ativou o evento for o modal (fundo escuro) */
        if (event.target === modal) {

            // Feche o modal da publicação */
            fecharModal();
        }
    }

    // Se o botão ou a janela for clicada */
    botao_fechar.addEventListener('click', fecharModal);
    window.addEventListener('click', janelaClicada);
    


    // Crie os elementos da publicação e preencha o container com as informações */
    function criar_publicacao_modal(publicacao_modal, publicacao) {

        console.log(publicacao);
        console.log("Comentários " + publicacao.comentarios);
        console.log("Número de comentários " + publicacao.comentarios.length);
        console.log("Número de ameis " + publicacao.n_ameis);

        // CONTAINER DA PUBLICAÇÃO */
        let container_publicacao = criar_container_publicacao();

        // ID DA PUBLICAÇÃO */
        let container_id_publicacao = criar_container_id_publicacao(publicacao);

        // TÍTULO DA PUBLICAÇÃO */
        let container_titulo_publicacao = criar_container_titulo_publicacao(publicacao);

        // SEÇÃO COM INFORMAÇÕES SOBRE A PUBLICAÇÃO (LINK DO ATOR, NOME DO AUTOR, AVATAR DO AUTOR, DATA, IDIOMA E TAGS) */
        let container_info_publicacao = criar_container_info_publicacao(publicacao);

        // SEÇÃO DO CONTEÚDO DA PUBLICAÇÃO */
        let container_conteudo_publicacao = criar_container_conteudo_publicacao(publicacao);



        // Se o cliente for o AUTOR da publicação, exibir as opções de autor */
        if (publicacao.autor_cliente)
        {
            // Cria as opções de autor (BOTÃO EDITAR E BOTÃO APAGAR) */
            let container_opcoes_autor = criar_container_opcoes_autor(publicacao_modal, publicacao, container_titulo_publicacao, container_conteudo_publicacao);

            // Anexa o container das opções de autor ao container da publicação */
            container_publicacao.append(container_opcoes_autor);
        }

        // Anexa o TÍTULO, INFORMAÇÕES e CONTEÚDO da publicação SOMENTE APÓS definir se as OPÇÕES de AUTOR serão anexadas */
        container_publicacao.append(container_id_publicacao);
        container_publicacao.append(container_titulo_publicacao);
        container_publicacao.append(container_info_publicacao);
        container_publicacao.append(container_conteudo_publicacao);


        let formulario_comentario = criar_formulario_comentario();  
        



        /* CONTAINER DO BOTÃO AMEI <3 */

        let container_interacao = document.createElement('div');
        container_interacao.classList.add('container-interacao');

        let botao_amei = document.createElement('span');
        botao_amei.classList.add('botao-amei-modal');

        let n_ameis = document.createElement('span');
        n_ameis.innerText = publicacao.n_ameis;

        let icone_coracao = document.createElement('i');
        icone_coracao.classList.add('fa', 'fa-heart', 'ml-2');

        botao_amei.append(n_ameis);
        botao_amei.append(icone_coracao);

        // Quando o botão amei for clicado
        botao_amei.addEventListener('click', () => {

            console.log("Iniciando FETCH");

            //'/publicacao/<int: publicacao_id>/interacao/<acao>'
            // assuming the backend is hosted on the same server

            fetch('/ingles/publicacao/' +  publicacao.id + '/interacao/amar', {  

                method: 'GET',

            }).then(function(resposta) {

                return resposta.json();

            }).then(function(dados) {

                console.log(dados);

            });
        });
        


        container_interacao.append(botao_amei);








        // Anexa o container da publicação (container_publicacao) ao modal (publicacao_modal) */
        publicacao_modal.append(container_publicacao);

        publicacao_modal.append(container_interacao);

        publicacao_modal.append(formulario_comentario);

        // Retorna o MODAL da PUBLICAÇÃO */
        return publicacao_modal;
    }

    // FUNÇÕES USADAS NA CRIAÇÃO DOS COMPONENTES DO MODAL */

    function criar_container_publicacao () {

        let container_publicacao = document.createElement('div');

        container_publicacao.setAttribute('id', 'container-publicacao');

        container_publicacao.classList.add('border', 'border-secondary', 'p-3');

        return container_publicacao;
    }

    // Opções do autor */
    // Esta função é extensa pois lida com as complexidades da funcionalidade de edição de publicação
    function criar_container_opcoes_autor (publicacao_modal, publicacao, titulo_publicacao, conteudo_publicacao) {


        // Cria os opções de autor (BOTÃO EDITAR E BOTÃO APAGAR) */
        let opcoes_autor = document.createElement('div');

        // Adiciona as classes de estilização ao container das opções de autor */
        opcoes_autor.classList.add('text-right', 'mb-3');

        let botao_editar = criar_botao_editar();
        
        let botao_apagar = criar_botao_apagar();

        // Anexa os botões de opções de autor ao container das opções */
        opcoes_autor.append(botao_editar);
        opcoes_autor.append(botao_apagar);

        /*
            Quando o botão de editar for clicado,
            empurre a publicação para baixo e exiba o formulário.
        */
        botao_editar.addEventListener('click', () => {

            // Esconde as opções do autor para que o cliente não crie formulários a mais ou apague a publicação durante edição (clicando no ícone) */
            opcoes_autor.style.visibility = 'hidden';


            // Crie o container do formulário de edição
            let container_formulario = document.createElement('div');

            // Crie o div que vai expandir nos eixos X,Y para exibir o formulário
            let div_formulario = document.createElement('div');

            // Crie o FORMULÁRIO de EDIÇÃO da PUBLICAÇÃO
            let formulario_edicao = document.createElement('form');


            // Adicione bordas e margem no topo do formulário 
            formulario_edicao.classList.add('mt-3', 'mb-3');

            div_formulario.classList.add('div-formulario', 'bg-light', 'border');

            container_formulario.classList.add('container-formulario-edicao');



            div_formulario.append(formulario_edicao);

            container_formulario.append(div_formulario);

            // Pré-anexa o CONTAINER DO FORMULÁRIO no CONTAINER DA PUBLICAÇÃO (efetivamente, anexado o container do formulário antes do container com a publicação em si)
            publicacao_modal.prepend(container_formulario);



            /* ------------------------------------------------ */

            // Função que cria as OPÇÕES DO AUTOR DURANTE EDIÇÃO no formulário
            function criar_container_opcoes_autor_edicao () {

                // Cria o container e os botões das opções disponíveis durante a edição 
                let opcoes_autor_edicao = document.createElement('div');
                opcoes_autor_edicao.classList.add('text-right', 'mb-3');

                let botao_salvar = document.createElement('span');
                botao_salvar.innerHTML = 'Salvar Alterações <i class="fa fa-save"></i>';
                botao_salvar.classList.add('badge', 'badge-success', 'cursor-pointer');
                botao_salvar.setAttribute('id', 'botao-salvar-edicao');

                let botao_cancelar = document.createElement('span');
                botao_cancelar.innerHTML = 'Cancelar Edição <i class="fa fa-times-circle"></i>';
                botao_cancelar.classList.add('badge', 'badge-secondary', 'cursor-pointer', 'ml-1');
                botao_cancelar.setAttribute('id', 'botao-cancelar-edicao');

                // Anexa os botões de opções de autor ao container das opções */
                opcoes_autor_edicao.append(botao_salvar);
                opcoes_autor_edicao.append(botao_cancelar);

                return opcoes_autor_edicao;
            }

            // Crie o container que conterá as OPÇÕES DO AUTOR DURANTE EDIÇÃO
            let opcoes_autor_edicao = criar_container_opcoes_autor_edicao();

            /* ------------------------------------------------ */

            // Função que cria o INPUT DO TÍTULO no formulário
            function criar_container_titulo_edicao (titulo_publicacao) {

                // Crie o container que conterá o INPUT do TÍTULO da publicação
                let container_input = document.createElement('div');
                                        
                // Cria um elemento LABEL, adiciona cor escura à fonte, define como sendo a label do campo 'titulo_input_edicao', e define a string a ser exibida no label */
                let label_input = document.createElement('label');

                // Cria um elemento INPUT, adiciona a classe .form-control (classe Bootstrap para formulários), define o id e o nome do campo, define o tipo do campo, e por fim preenche o campo com o título da publicação a ser editada */
                let titulo_input = document.createElement('input');


                // Adicione a classe .form-group (que adiciona margem abaixo do elemento) */
                container_input.classList.add('form-group');

                // Formata o label como no formulario WTF */
                label_input.classList.add('text-secondary');
                label_input.setAttribute('for', 'titulo-input-edicao');
                label_input.innerText = "Título da publicação";

                // Formata o input como no formulário WTF */
                titulo_input.classList.add('form-control');
                titulo_input.setAttribute('id', 'titulo-input-edicao');
                titulo_input.setAttribute('name', 'titulo-input-edicao');
                titulo_input.setAttribute('type', 'text');
                titulo_input.value = titulo_publicacao;


                // Anexa a LEGENDA do INPUT e o INPUT do TÍTULO  da publicação */
                container_input.append(label_input);
                container_input.append(titulo_input);

                return container_input;
            }

            // Crie o container que conterá o INPUT do TÍTULO da publicação
            let container_input = criar_container_titulo_edicao(titulo_publicacao.innerText);

            /* ------------------------------------------------ */

            // Função que cria as TAGS no formulário
            function criar_container_tags_edicao (publicacao_tags) {

                // Cria o CONTAINER que conterá as opções de TAGS
                let container_tags = document.createElement('div');
                container_tags.classList.add('row', 'row-cols-2', 'mb-3');
                container_tags.setAttribute('id', 'container-tags-edicao');


                // Crie os CONTAINERS que conterão a CAIXA DE SELEÇÃO e a LABEL da tag

                function criar_container_tag () {

                    let container = document.createElement('div');

                    container.classList.add('col', 'p-0');

                    container.style.display = 'inline-block';

                    return container;
                }

                let container_vocabulario = criar_container_tag();
                let container_gramatica = criar_container_tag();
                let container_pronuncia = criar_container_tag();
                let container_cultura = criar_container_tag();


                // Cria as CAIXAS DE SELEÇÃO para as opções de TAGS
            
                function criar_input_tag () {

                    let input = document.createElement('input');

                    input.classList.add('checkbox-tag-edicao');

                    input.setAttribute('name', 'tags');

                    input.setAttribute('type', 'checkbox');

                    return input;
                }

                let tag_vocabulario = criar_input_tag();
                let tag_gramatica = criar_input_tag();
                let tag_pronuncia = criar_input_tag();
                let tag_cultura = criar_input_tag();

                tag_vocabulario.setAttribute('id', 'tags-0-edicao');
                tag_vocabulario.setAttribute('value', '1');

                tag_gramatica.setAttribute('id', 'tags-1-edicao');
                tag_gramatica.setAttribute('value', '2');

                tag_pronuncia.setAttribute('id', 'tags-2-edicao');
                tag_pronuncia.setAttribute('value', '3');

                tag_cultura.setAttribute('id', 'tags-3-edicao');
                tag_cultura.setAttribute('value', '4');


                // Cria as LABELS das opções de TAGS

                function criar_label_tag () {

                    let label = document.createElement('label');

                    label.classList.add('form-check-label', 'badge', 'ml-1');

                    return label;
                }

                let label_vocabulario = criar_label_tag();
                let label_gramatica = criar_label_tag();
                let label_pronuncia = criar_label_tag();
                let label_cultura = criar_label_tag();

                label_vocabulario.classList.add('badge-success');
                label_vocabulario.setAttribute('for', 'tags-0-edicao');
                label_vocabulario.innerHTML = "<i class='fa fa-book'></i> Vocabulário";

                label_gramatica.classList.add('badge-primary');
                label_gramatica.setAttribute('for', 'tags-1-edicao');
                label_gramatica.innerHTML = "<i class='fa fa-cogs'></i> Gramática";

                label_pronuncia.classList.add('badge-danger');
                label_pronuncia.setAttribute('for', 'tags-2-edicao');
                label_pronuncia.innerHTML = "<i class='fa fa-headphones'></i> Pronúncia";

                label_cultura.classList.add('badge-dark');
                label_cultura.setAttribute('for', 'tags-3-edicao');
                label_cultura.innerHTML = "<i class='fa fa-globe'></i> Cultura";


                // Marca as CAIXAS DE SELEÇÃO de acordo com as tags atribuídas à publicação
                if (publicacao_tags.includes('vocabulario')) {
                    tag_vocabulario.checked = true;
                }
                if (publicacao_tags.includes('gramatica')) {
                    tag_gramatica.checked = true;
                }
                if (publicacao_tags.includes('pronuncia')) {
                    tag_pronuncia.checked = true;
                }
                if (publicacao_tags.includes('cultura')) {
                    tag_cultura.checked = true;
                }


                // Anexa os CHECKBOXES TAGS e os LABELS das TAGS
                container_vocabulario.append(tag_vocabulario);
                container_vocabulario.append(label_vocabulario);

                container_gramatica.append(tag_gramatica);
                container_gramatica.append(label_gramatica);

                container_pronuncia.append(tag_pronuncia);
                container_pronuncia.append(label_pronuncia);

                container_cultura.append(tag_cultura);
                container_cultura.append(label_cultura);

                // Anexa as tags ao container de tags
                container_tags.append(container_vocabulario);
                container_tags.append(container_gramatica);
                container_tags.append(container_pronuncia);
                container_tags.append(container_cultura);


                return container_tags;
            }

            // Cria o container que conterá as opções de TAGS 
            let container_tags = criar_container_tags_edicao(publicacao.tags);
        
            /* ------------------------------------------------ */

            // Função que cria o TEXTAREA DO CONTEÚDO no formulário
            function criar_container_conteudo_edicao (conteudo_publicacao_html) {

                // Crie o container que conterá o TEXTAREA do CONTEÚDO da publicação
                let container_textarea = document.createElement('div');
            
                // Cria um elemento LABEL
                let label_textarea = document.createElement('label');
            
                // Cria um elemento TEXTAREA
                let conteudo_textarea = document.createElement('textarea');
            
                // Adicione a classe .form-group (que adiciona margem abaixo do elemento)
                container_textarea.classList.add('form-group');
            
            
                label_textarea.classList.add('text-secondary');
                label_textarea.setAttribute('for', 'conteudo-textarea-edicao');
                label_textarea.innerHTML = "Conteudo da publicação <small class='text-primary'>(prévia da publicação abaixo)</small>";
            
            
                conteudo_textarea.classList.add('form-control');
                conteudo_textarea.setAttribute('id', 'conteudo-textarea-edicao');
                conteudo_textarea.setAttribute('name', 'conteudo-textarea-edicao');
                conteudo_textarea.setAttribute('type', 'text');
                conteudo_textarea.setAttribute('rows', '10');
            
                // Transforma o HTML em Markdown para o autor poder editar com mais controle.
                var turndownService = new TurndownService();
                var markdown = turndownService.turndown(conteudo_publicacao_html);
            
                // Textarea é preenchido com o MARKDOWN da publicação
                conteudo_textarea.value = markdown;
            
                // Anexa a LEGENDA do TEXTAREA e o TEXTAREA do CONTEÚDO da publicação
                container_textarea.append(label_textarea);
                container_textarea.append(conteudo_textarea);
            
                return container_textarea;
            
            }

            let container_textarea = criar_container_conteudo_edicao(conteudo_publicacao.innerHTML);
            
            /* ------------------------------------------------ */


            // Anexa os elementos do formulário de edição  
            formulario_edicao.append(opcoes_autor_edicao);
            formulario_edicao.append(container_input);  
            formulario_edicao.append(container_tags);
            formulario_edicao.append(container_textarea);
            


        
            /* ANIMAÇÃO DA ABERTURA DO FORMULÁRIO DE EDIÇÃO */

            // Expanda as dimensões do div_formulario após 1000 milésimos
            setTimeout(function () {

                div_formulario.classList.add('div-formulario-expandindo');
                
            }, 100);


            container_formulario.classList.add('container-formulario-edicao-expandindo');

            container_formulario.classList.remove('container-formulario-edicao');


            setTimeout(function () {

                container_formulario.classList.add('container-formulario-edicao-expandido');

                container_formulario.classList.remove('container-formulario-edicao-expandindo');

            }, 100);
            
            // FIM DA ANIMAÇÃO DA ABERTURA DO FORMULÁRIO DE EDIÇÃO */


            // PRÉVIA DA EDIÇÃO */

            
            if (typeof flask_pagedown_converter === "undefined")
            {
                flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
            }

            // Seleciona o input do título
            let titulo_input = container_input.querySelector('#titulo-input-edicao');

            // Atualiza o título da prévia quando o input do formulário de edição for alterado
            titulo_input.addEventListener('keyup', () => {
                
                titulo_publicacao.innerHTML = titulo_input.value;
            });

            // Seleciona o textarea do conteúdo  
            let conteudo_textarea = container_textarea.querySelector('#conteudo-textarea-edicao');

            // Atualiza o conteúdo da prévia quando o textarea do formulário de edição for alterado
            conteudo_textarea.addEventListener('keyup', () => {

                conteudo_publicacao.innerHTML = flask_pagedown_converter(conteudo_textarea.value);
            });

            // Seleciona as caixas de seleção das tags
            let checkbox_tags_edicao = container_tags.querySelectorAll('input');
        
            // Tags na prévia da publicação
            let tags_container =  publicacao_modal.querySelector('#tags-container');

            // Para cada caixa de seleção das tags
            for (let checkbox of checkbox_tags_edicao)
            {

                // Quando a caixa de seleção for alterada
                checkbox.addEventListener('change', ()  => {

                    // Se a caixa de seleção estiver marcada, anexar a tag
                    if (checkbox.checked == true)
                    {
                        // Adicionar a tag à prévia da publicação

                        // Se a tag for 'vocabulário'
                        if (checkbox.value == 1)
                        {
                            let tag = criar_tag_vocabulario();
                            // Anexe a tag ao container
                            tags_container.append(tag);
                        }
                        // Se a tag for 'gramática'
                        else if (checkbox.value == 2)
                        {
                            let tag = criar_tag_gramatica();
                            // Anexe a tag ao container
                            tags_container.append(tag);
                        }
                        // Se a tag for 'pronúncia'
                        else if (checkbox.value == 3)
                        {
                            let tag = criar_tag_pronuncia();
                            // Anexe a tag ao container
                            tags_container.append(tag);
                        }
                        // Se a tag for 'cultura'
                        else if (checkbox.value == 4)
                        {
                            let tag = criar_tag_cultura();
                            // Anexe a tag ao container
                            tags_container.append(tag);
                        }
                    }
                    // Se a caixa de seleção NÃO estiver marcada, remover a tag
                    else
                    {
                        // Remover a tag da prévia da publicação

                        // Se a tag for 'vocabulário'
                        if (checkbox.value == 1)
                        {
                            tags_container.querySelector('[title="Vocabulário"]').remove();
                        }
                        // Se a tag for 'gramática'
                        else if (checkbox.value == 2)
                        {
                            tags_container.querySelector('[title="Gramática"]').remove();
                        }
                        // Se a tag for 'pronúncia'
                        else if (checkbox.value == 3)
                        {
                            tags_container.querySelector('[title="Pronúncia"]').remove();
                        }
                        // Se a tag for 'cultura'
                        else if (checkbox.value == 4)
                        {
                            tags_container.querySelector('[title="Cultura"]').remove();
                        }
                    }
                });
            }

            // FIM PRÉVIA DA EDIÇÃO */


            // CONFIGURAÇÃO DAS OPÇÕES DO AUTOR DURANTE A EDIÇÃO */

            let botao_salvar = opcoes_autor_edicao.querySelector('#botao-salvar-edicao');
            // Salva as alterações na publicação, remove o formulário de edição e exibe as opções de autor
            botao_salvar.addEventListener('click', () => {

                // Array vazio que armazenará o valor das tags
                let tags_marcadas = [];

                // Para cada caixa de seleção de tag da lista de tags no formulário de edição
                for (let tag of container_tags.querySelectorAll('input'))
                {
                    // Se a caixa de seleção estiver marcada
                    if (tag.checked == true)
                    {
                        // Adiciona a tag (tecnicamente, o número inteiro que representa a tag)
                        tags_marcadas.push(tag.value);
                    }                    
                }


                // Crie um novo pedido HTTP*/
                let pedido = new XMLHttpRequest();

                /* Pega o id da publicação cujo div foi clicado.
                'publicacao_id' é uma string mas pode ser convertido
                para int antes de ser enviado para o servidor.
                Para isso, a função parseInt() está sendo usada */
                let json_enviado = {"publicacao_id": publicacao.id,"publicacao_titulo": titulo_input.value,"publicacao_conteudo": conteudo_textarea.value, "publicacao_tags": tags_marcadas};

                // Abra o pedido com método 'POST' na rota '/ingles/publicacao/json' */
                pedido.open('POST', '/ingles/publicacao/editar');

                // ??? */
                pedido.setRequestHeader('Content-Type', 'application/json');

                // Quando o pedido for respondido
                pedido.onload = function (e) {

                    // Seleciona o artigo da publicação no mural
                    let publicacao_no_mural = document.querySelector(`article[data-id='${publicacao.id}']`);

                    // Seleciona o título da publicação no mural
                    let titulo_publicacao_no_mural = publicacao_no_mural.querySelector('.titulo-publicacao-mural');

                    // Atualiza o título da publicação no mural
                    titulo_publicacao_no_mural.innerText = `${titulo_input.value}`;

                    // Atualiza o dataset 'titulo' da publicação
                    publicacao_no_mural.dataset.titulo = `${titulo_input.value}`;

                    // Seleciona a div que contém o conteúdo da publicação no mural
                    let conteudo_publicacao_no_mural = publicacao_no_mural.querySelector('.paragrafo-publicacao');

                    // Atualiza o conteúdo da publicação no mural
                    conteudo_publicacao_no_mural.innerHTML = `${flask_pagedown_converter(conteudo_textarea.value)}`;

                    // Seleciona a lista de tags da publicação no mural
                    let tags_publicacao_no_mural = publicacao_no_mural.querySelector('.tags-publicacao-mural');

                    // Esvazia a lista de tags
                    tags_publicacao_no_mural.innerHTML = '';

                    // Se a edição marcar a tag VOCABULÁRIO, adicione a tag à publicação no mural
                    if (tags_marcadas.includes('1'))
                    {
                        let span_tag = criar_tag_vocabulario();

                        tags_publicacao_no_mural.append(span_tag);
                    }

                    // Se a edição marcar a tag GRAMÁTICA, adicione a tag à publicação no mural
                    if (tags_marcadas.includes('2'))
                    {
                        let span_tag = criar_tag_gramatica();

                        tags_publicacao_no_mural.append(span_tag);
                    }

                    // Se a edição marcar a tag PRONÚNCIA, adicione a tag à publicação no mural
                    if (tags_marcadas.includes('3'))
                    {
                        let span_tag = criar_tag_pronuncia();

                        tags_publicacao_no_mural.append(span_tag);
                    }

                    // Se a edição marcar a tag CULTURA, adicione a tag à publicação no mural
                    if (tags_marcadas.includes('4'))
                    {
                        let span_tag = criar_tag_cultura();

                        tags_publicacao_no_mural.append(span_tag);
                    }
                }

                // Envie o pedido para o servidor, juntamento com o id da publicação */
                pedido.send(JSON.stringify(json_enviado));


                div_formulario.classList.remove('div-formulario-expandindo');
                
                setTimeout(function () {
                    container_formulario.classList.add('container-formulario-edicao-encolhendo');
                }, 100);


                setTimeout(function () {
                    container_formulario.remove();
                }, 1000)
                
                // Exibe as opções de autor que foi escondida quando a edição começou */
                opcoes_autor.style.visibility = 'visible';

                let aviso_alteracoes_salvas = "<div class='alert alert-success alert-dismissible fade show' role='alert'><strong>As alterações foram salvas!</strong><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div>";

                let container_aviso = document.createElement('div');

                container_aviso.innerHTML = aviso_alteracoes_salvas;

                publicacao_modal.insertBefore(container_aviso, publicacao_modal.firstChild);


                //$('.alert').alert()

            });


            let botao_cancelar = opcoes_autor_edicao.querySelector('#botao-cancelar-edicao');
            // Cancela a edição da publicação
            botao_cancelar.addEventListener('click', () => {

                // Restaura o título original da publicação */
                titulo_publicacao.innerText = publicacao.titulo;

                // Se a versão HTML do conteúdo da publicação estiver definido */
                if (publicacao.conteudo_html != undefined)
                {
                    conteudo_publicacao.innerHTML = publicacao.conteudo_html;
                }
                // Senão, utilize o conteúdo em texto-plano */
                else
                {
                    conteudo_publicacao.innerHTML = publicacao.conteudo;
                }


                // Remova a classe que expande o formulário */
                div_formulario.classList.remove('div-formulario-expandindo');
                
                setTimeout(function () {
                    container_formulario.classList.add('container-formulario-edicao-encolhendo');
                }, 100);


                setTimeout(function () {
                    container_formulario.remove();
                }, 1000)
                
                // Exibe as opções de autor que foi escondida quando a edição começou */
                opcoes_autor.style.visibility = 'visible';

            });
        
            // FIM DA CONFIGURAÇÃO DAS OPÇÕES DO AUTOR DURANTE A EDIÇÃO */

        });

    
        // Quando o botão de apagar for clicado, apagar publicação
        botao_apagar.addEventListener('click', () => {

            // Crie um novo pedido HTTP*/
            let pedido = new XMLHttpRequest();

            /* Pega o id da publicação cujo div foi clicado.
            'publicacao_id' é uma string mas pode ser convertido
            para int antes de ser enviado para o servidor.
            Para isso, a função parseInt() está sendo usada*/
            let json_enviado = {"publicacao_id": parseInt(publicacao.id)} ;

            // Abra o pedido com método 'POST' na rota '/ingles/publicacao/json' */
            pedido.open('POST', '/publicacao/apagar');

            // ??? */
            pedido.setRequestHeader('Content-Type', 'application/json');

            // Quando o pedido for respondido */
            pedido.onload = function (e) {


                /* 
                    Se o estado do pedido for DONE e o status da resposta for 200 (OK)
                    O script terá acesso à resposta em formato JSON enviado pelo servidor    
                */
                if (pedido.readyState === 4 && pedido.status === 200) {

                    // Fecha o modal da publicação
                    fecharModal();

                    // Remove a publicação do mural
                    document.querySelector(`article[data-id='${publicacao.id}']`).parentNode.parentNode.remove();


                // Se o pedido não ocorrer corretamente */
                } else {

                    console.log("Publicação não foi apagada");
                }
            }

            // Envie o pedido para o servidor, juntamento com o id da publicação */
            pedido.send(JSON.stringify(json_enviado));
        });


        // Função que cria o botão de editar publicação
        function criar_botao_editar () {

            // Cria o botão "editar publicação"
        
            let botao_editar = document.createElement('span');
        
            botao_editar.setAttribute('id', 'botao-editar-publicacao');
        
            botao_editar.innerHTML = 'Editar <i class="fa fa-pencil"></i>';
        
            botao_editar.classList.add('badge', 'badge-primary', 'cursor-pointer');
        
            return botao_editar;
        }
    
        // Função que cria o botão de apagar publicação
        function criar_botao_apagar () {

            let botao_apagar = document.createElement('span');
        
            botao_apagar.setAttribute('id', 'botao-apagar-publicacao');
        
            botao_apagar.innerHTML = 'Apagar <i class="fa fa-times-circle"></i>';
        
            botao_apagar.classList.add('badge', 'badge-danger', 'cursor-pointer', 'ml-1');
        
            return botao_apagar;
        }


        return opcoes_autor;
    }

    // Retorna o formulário de escrever comentário
    function criar_formulario_comentario () {

        // Declaração dos elementos */

        // Container para o formulário
        let div_formulario_comentario = document.createElement('div');

        // Formulário de novo comentário
        let formulario_comentario = document.createElement('form');

        // Campo de texto do formulário
        let textarea_comentario = document.createElement('textarea');

        // Container para armazenar e posicionar botão de enviar
        let container_botao_enviar = document.createElement('div');

        // Botão para enviar formulário
        let botao_enviar = document.createElement('span');



        textarea_comentario.classList.add('w-100', 'border', 'bg-white');
        textarea_comentario.placeholder = "Escreva um comentário";


        container_botao_enviar.classList.add('text-right', 'mb-1');

        botao_enviar.classList.add('text-white', 'bg-success', 'p-2', 'd-inline-block', 'font-weight-bold');
        botao_enviar.innerHTML = "Comentar <i class='fa fa-comment'></i>";




        // Anexação dos elementos */
        formulario_comentario.append(textarea_comentario);
        container_botao_enviar.append(botao_enviar);

        div_formulario_comentario.append(formulario_comentario);
        div_formulario_comentario.append(container_botao_enviar);


        // Configuração do botão de enviar comentário */
        botao_enviar.addEventListener('click', (e) => {
            
            e.preventDefault();


            // Crie um novo pedido HTTP*/
            let pedido = new XMLHttpRequest();

            /* Pega o id da publicação onde o comentário foi escrito.
            'publicacao_id' é uma string mas pode ser convertido
            para int antes de ser enviado para o servidor.
            Para isso, a função parseInt() está sendo usada*/


            let json_enviado = {"publicacao_id": publicacao.id, "conteudo": textarea_comentario.value};



            // Abra o pedido com método 'POST' na rota '/ingles/publicacao/comentar' */
            pedido.open('POST', '/ingles/publicacao/comentar');

            // ??? */
            pedido.setRequestHeader('Content-Type', 'application/json');

            // Quando o pedido for respondido */
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

                    console.log(pedido);
                    console.log(pedido.responseText);

                    let resposta = JSON.parse(pedido.responseText);

                    console.log(resposta);

                    let novo_comentario = criar_elemento_comentario (textarea_comentario.value, usuario_nome, moment());

                    document.querySelector('#lista_de_comentarios').append(novo_comentario);

                // Se o pedido não ocorrer corretamente */
                } else {

                    alert("Não foi possível criar o comentário");
                }
            }

            // Envie o pedido para o servidor, juntamento com o id da publicação, o conteúdo do comentário e o id do autor */
            console.log(json_enviado);
            pedido.send(JSON.stringify(json_enviado));

        });

        // Retorna o formulário de envio de comentário */
        return div_formulario_comentario;
    }
} // FIM FUNÇÃO CRIAR_MODAL()


// Retorna um elemento que representa o comentário
function criar_elemento_comentario (comentario_conteudo, comentario_autor, comentario_data) {


    /* ----- Criação dos Elementos HTML ----- */

    // Div que conterá todos os elementos que compõe o comentário
    let comentario = document.createElement('div');

    // Se o autor do comentário for o usuário logado
    if (comentario_autor == usuario_nome) 
    {
        // Opções do autor do comentário
        let opcoes_autor = document.createElement('span');
        opcoes_autor.classList.add('opcoes-publicacao', 'm-0', 'p-0');

        let botao_editar = document.createElement('span');
        botao_editar.classList.add('btn', 'icone-editar-publicacao', 'p-0', 'pl-1');

        let botao_apagar = document.createElement('span');
        botao_apagar.classList.add('btn', 'icone-apagar-publicacao', 'p-0', 'pl-1');

        let icone_editar = document.createElement('i');
        icone_editar.classList.add('fa', 'fa-pencil');

        let icone_apagar = document.createElement('i');
        icone_apagar.classList.add('fa', 'fa-times-circle');


        botao_editar.append(icone_editar);
        botao_apagar.append(icone_apagar);

        opcoes_autor.append(botao_editar);
        opcoes_autor.append(botao_apagar);

        comentario.append(opcoes_autor);

    }

    
    // Div que conterá o conteúdo do comentário em si
    let conteudo = document.createElement('div');

    // Div que conterá informações adicionais do comentário (autor, data, número de likes no comentário)
    let rodape = document.createElement('div');

    // Tag 'a' que será o link para o perfil do autor
    let link_autor = document.createElement('a');

    // Nome de usuário do autor do comentário
    let autor_nome_usuario = document.createElement('span');

    // Data de criação do comentário
    let data = document.createElement('span');

    // Botão "amei" do comentário
    let n_amei = document.createElement('span');
    let botao_amei = document.createElement('span');
    let icone_coracao = document.createElement('i');


    /* ----- Estilização do Elementos HTML ----- */
    
    // Estilização do comentário
    comentario.classList.add('border', 'bg-white', 'mb-2', 'pl-1');

    flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;

    // Conteúdo do comentário formatado com Pagedown
    conteudo.innerHTML = flask_pagedown_converter(comentario_conteudo);


    rodape.classList.add('small');

    // Link para a página do autor do comentário
    link_autor.href = "";
    link_autor.href = `/usuario/${comentario_autor}`;

    // Nome de usuário do autor do comentário
    autor_nome_usuario.innerHTML = '@'.concat(comentario_autor);

    // Data da publicação
    data.innerHTML = '&middot; <i class="fa fa-history"></i> escrito '.concat(moment(comentario_data).fromNow());
    
    // Botão de like

    n_amei.innerText = '99';

    icone_coracao.classList.add('fa', 'fa-heart', 'ml-1', 'pr-1');

    botao_amei.classList.add('float-right', 'text-danger');


    /* ----- Anexação do Elementos ----- */


    


    link_autor.append(autor_nome_usuario);

    botao_amei.append(n_amei);
    botao_amei.append(icone_coracao);


    rodape.append(link_autor);
    rodape.append(data);
    //rodape.append(botao_amei);


    
    comentario.append(conteudo);
    comentario.append(rodape);

    return comentario;
}

function criar_lista_de_comentarios(comentarios) {

    let lista_de_comentarios = document.createElement('div');
    lista_de_comentarios.id = 'lista_de_comentarios';

    let n_comentarios = document.createElement('p');
    n_comentarios.style.fontSize = '18pt';
    n_comentarios.innerHTML = "<i class='fa fa-comments text-secondary'></i> " + comentarios.length + " comentários";

    lista_de_comentarios.append(n_comentarios)


    for (let comentario of comentarios)
    {

        let c = criar_elemento_comentario(comentario.conteudo, comentario.autor, comentario.data_criacao);

        lista_de_comentarios.append(c);
    }

    return lista_de_comentarios;
}


// Previne que o evento de clicar no link do autor de uma publicação abra o modal da publicação
function previnir_propagacao_clique_link(links_usuarios) {

    // Para cada elemento 'link', evite abrir o modal da publicação antes de redirecionar para a página do autor da publicação */
    links_usuarios.forEach(link => {

        // Quando o link for clicado */
        link.addEventListener('click', e => {
            
            /*
                Evitar propagação.
                Dessa forma, o evento de clicar no link não ativará o evento do elemento-pai do link, que neste caso é a publicação em si
            */
            e.stopPropagation();
        })
    });
}

// (Esta função não está sendo usada)Destaca a publicação clicada ao transparecer as outras publicações
function destacar_publicacao_clicada(todas_publicacoes, publicacao) {

    // Para cada publicação na lista de publicações */
    for (let p of todas_publicacoes)
    {
        //destacarPublicacao(p, publicacao);*/

        // Se a publicação for a publicação clicada */
        if (p.getAttribute('data-id') === publicacao.getAttribute('data-id'))
        {
            // A publicação e todos seus elementos ficarão VISÍVEIS */
            p.style.opacity = 1;

                let elementos = p.querySelectorAll('*')

                for (elemento of elementos) {

                    elemento.style.opacity = 1;
                }
        }
        // Se a publicação NÃO for a publicação clicada */
        else
        {
            /* A publicação e todos seus elementos ficarão TRANSPARENTES(até o modal for fechado) */
            p.style.opacity = 0.85;

                let elementos = p.querySelectorAll('*')

                for (elemento of elementos) {
                    elemento.style.opacity = 0.85;
                }
        }
    }
}