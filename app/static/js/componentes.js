


// Retorna o emoji da bandeira do idioma
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



// Funções que criam tags estilo "pílula"
function criar_tag_vocabulario () {

    let span_tag = document.createElement('span');
    span_tag.classList.add('badge', 'badge-pill', 'badge-success', 'mr-1');
    span_tag.setAttribute('data-toggle', 'tooltip');
    span_tag.setAttribute('data-placement', 'top');
    span_tag.setAttribute('title', 'Vocabulário');

    let icone_tag = document.createElement('i');
    icone_tag.classList.add('fa', 'fa-book', 'mr-0');

    span_tag.append(icone_tag);

    return span_tag;
}

function criar_tag_gramatica () {

    let span_tag = document.createElement('span');
    span_tag.classList.add('badge', 'badge-pill', 'badge-primary', 'mr-1');
    span_tag.setAttribute('data-toggle', 'tooltip');
    span_tag.setAttribute('data-placement', 'top');
    span_tag.setAttribute('title', 'Gramática');

    let icone_tag = document.createElement('i');
    icone_tag.classList.add('fa', 'fa-cogs', 'mr-0');

    span_tag.append(icone_tag);

    return span_tag;
}

function criar_tag_pronuncia () {

    let span_tag = document.createElement('span');
    span_tag.classList.add('badge', 'badge-pill', 'badge-danger', 'mr-1');
    span_tag.setAttribute('data-toggle', 'tooltip');
    span_tag.setAttribute('data-placement', 'top');
    span_tag.setAttribute('title', 'Pronúncia');

    let icone_tag = document.createElement('i');
    icone_tag.classList.add('fa', 'fa-headphones', 'mr-0');

    span_tag.append(icone_tag);

    return span_tag;
}

function criar_tag_cultura () {

    let span_tag = document.createElement('span');
    span_tag.classList.add('badge', 'badge-pill', 'badge-dark', 'mr-1');
    span_tag.setAttribute('data-toggle', 'tooltip');
    span_tag.setAttribute('data-placement', 'top');
    span_tag.setAttribute('title', 'Cultura');

    let icone_tag = document.createElement('i');
    icone_tag.classList.add('fa', 'fa-globe', 'mr-0');

    span_tag.append(icone_tag);

    return span_tag;
}



// Funções que criam os componentes de uma publicação no modal
function criar_container_id_publicacao (publicacao) {

    let id_publicacao = document.createElement('small');

    id_publicacao.classList.add('text-secondary', 'mb-1');

    id_publicacao.innerText = `publicação #${publicacao.id}`;

    return id_publicacao;
}

function criar_container_titulo_publicacao (publicacao) {

    let titulo_publicacao = document.createElement('h4');

    titulo_publicacao.innerText = publicacao.titulo;

    return titulo_publicacao;
}

function criar_container_info_publicacao (publicacao) {

    /* Cria o container para abrigar as informações */
    let info_publicacao = document.createElement('div');

    /* Adiciona MARGEM ABAIXO */
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

    /* Adiciona MARGEM À ESQUERDA do nome do autor */
    autor_publicacao.classList.add('ml-1');

    /* Anexa o avatar do autor ao elemento âncora */
    link_perfil_autor.append(avatar_autor_publicacao);

    /* Anexa o nome do autor ao elemento âncora */
    link_perfil_autor.append(autor_publicacao);

    /* Define o link que leva à página de perfil do autor */
    /* 'publicacao.autor' é usado ao invés de 'autor_publicacao' pois 'autor_publicacao' teve um @ inserido no início da string */
    link_perfil_autor.href = '/usuario/'.concat(publicacao.autor);

    /* Anexa o link do perfil do autor no container 'info_publicacao' */
    info_publicacao.append(link_perfil_autor);

    /* Crie um <span> que conterá a data da publicação */
    let data_publicacao = document.createElement('span');

    /* Defina a string que indicará a data da publicação */
    data_publicacao.innerHTML = '&middot; <i class="fa fa-history"></i> escrito '.concat(moment(publicacao.data).fromNow());

    /* Crie o container que conterá a data da publicação */
    data_publicacao_envelope = document.createElement('span');

    /* Define a cor da fonte como sendo cinza e com margem à esquerda */
    data_publicacao_envelope.classList.add('text-secondary', 'ml-1');

    /* Anexa a data ao container da data */
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

    /* A classe .tags-container adiciona margem à esquerda e posiciona o elemento relativamente 1px do bottom */
    tags_container.classList.add('tags-container');
    tags_container.setAttribute('id', 'tags-container');

    /* Para cada tag na lista de tags da publicação, crie a tag no DOM e anexe ao container*/
    for (tag of tags_publicacao) {
        
        /* Crie um elemento <span> que representará a tag */
        let t = document.createElement('span');
        t.classList.add('badge', 'badge-pill', 'mr-1');
        // Atributos necessários para exibição do 'tooltip' com o nome da tag
        t.setAttribute('data-toggle', 'tooltip');
        t.setAttribute('data-placement', 'top');


        /* Define a cor e o conteúdo da tags */
    
        /* Se a tag for 'vocabulário' */
        if (tag == 'vocabulario')
        {
            t.classList.add('badge-success');
            t.innerHTML = '<i class="fa fa-book mr-0 text-white"></i>';
            t.setAttribute('title', 'Vocabulário');
        }
        /* Se a tag for 'gramática' */
        else if (tag == 'gramatica')
        {
            t.classList.add('badge-primary');
            t.innerHTML = '<i class="fa fa-cogs mr-0"></i>';
            t.setAttribute('title', 'Gramática');
        }
        /* Se a tag for 'pronúncia' */
        else if (tag == 'pronuncia')
        {
            t.classList.add('badge-danger');
            t.innerHTML = '<i class="fa fa-headphones mr-0"></i>';
            t.setAttribute('title', 'Pronúncia');
        }
        /* Se a tag for 'cultura' */
        else if (tag == 'cultura')
        {
            t.classList.add('badge-dark');
            t.innerHTML = '<i class="fa fa-globe mr-0"></i>';
            t.setAttribute('title', 'Cultura');
        }
        
        /* Anexe a tag ao container */
        tags_container.append(t);
    }

    /* Anexa a DATA, o ÍCONE DO IDIOMA e as TAGs da publicação */
    info_publicacao.append(data_publicacao_envelope);
    info_publicacao.append(icone_idioma);
    info_publicacao.append(tags_container);

    /* Retorna o elemento */
    return info_publicacao;
}

function criar_container_conteudo_publicacao (publicacao) {

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

    return conteudo_publicacao;
}



