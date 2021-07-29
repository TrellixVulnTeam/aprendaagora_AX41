

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


    /********************************************************************************/
    /********************************************************************************/
    /********************************************************************************/


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


    /********************************************************************************/
    /********************************************************************************/
    /********************************************************************************/



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


    /********************************************************************************/
    /********************************************************************************/
    /********************************************************************************/


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


    /********************************************************************************/
    /********************************************************************************/
    /********************************************************************************/

    

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


    /********************************************************************************/
    /********************************************************************************/
    /********************************************************************************/
  
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

});