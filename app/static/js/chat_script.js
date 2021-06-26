/*
Lista de funcionalidades a serem implementadas
[ ] - Exibir o número de usuários na sala de bate papo quando o cliente der hover no nome da sala localizado no navbar
[ ] - Exibir uma lista com os nomes dos usuários quando o cliente clicar no nome da sala localizado no navbar
*/


document.addEventListener('DOMContentLoaded', () => {

	console.log("JavaScript carregado.");
    
	// Define a sala de bate papo
    localStorage.setItem('sala', 'ingles');

    const sala = localStorage.getItem('sala');


    /* Configura o chat */

    // Conecta sockets
    var socket = io();

    socket.on('connect', () => {

        // Confirma socket conectado
        socket.emit('socket conectado');

        // Pede as últimas 100 mensagens para exibir na tela
        socket.emit('pedir mensagens', {'sala': sala});
  
        // Seleciona o formulário de enviar mensagem
        const formMensagem = document.querySelector('#formMensagem');

        // Quando o formulário da mensagem for enviado
        formMensagem.onsubmit = () => {

            // Seleciona o conteúdo da mensagem
            const mensagem = document.querySelector('#inputMensagem').value;
        
            // Se o usuário digitou alguma coisa
            if (mensagem)
            {

                // Seleciona o nome de usuário e a sala
                const usuario = localStorage.getItem('usuario');
                const sala = localStorage.getItem('sala');

                // Seleciona e formata a informação sobre o horário e data da mensagem
                var dataMensagem = new Date();
                var dia = String(dataMensagem.getDate()).padStart(2, '0');
                var mes = String(dataMensagem.getMonth() + 1).padStart(2, '0'); //Janeiro é 0!
                var ano = dataMensagem.getFullYear();
                var horario = dataMensagem.getHours() + ":" + dataMensagem.getMinutes();
                dataMensagem = horario + ", " + dia + '/' + mes + '/' + ano;


                // Limpa o formulário de mensagem
                document.querySelector('#inputMensagem').value = '';

                // Log
                console.log(usuario);
                console.log(mensagem);
                console.log(sala);
                console.log(dataMensagem);

                // Emite evento contendo 'mensagem', 'usuario', 'sala' e 'dataMensagem'
                socket.emit('enviar mensagem', {'mensagem': mensagem, 'usuario': usuario, 'sala': sala, 'dataMensagem': dataMensagem});

                // Impede a página de recarregar
                return false;
            }
            // Se o usuário não digitou, não atualize a página
            else
            {
                return false;
            }
        }
    });

    // Carrega as últimas 100 mensagens já enviadas na sala
    socket.on('carregar mensagens', mensagens => {

        // Itera na lista de mensagens e cria uma caixa de mensagem para cada mensagem
        for (let i = 0; i < mensagens.length; i++)
        {
            criar_mensagem(mensagens[i].usuario, mensagens[i].mensagem, mensagens[i].dataMensagem);
        }
    });

    // Exibe a mensagem enviado por um usuário
    socket.on('exibir mensagem', dados => {

        criar_mensagem(dados.usuario, dados.mensagem, dados.dataMensagem);

    });

    // Cria um balão de mensagem e adiciona ao chat
    function criar_mensagem(usuario, mensagem, dataMensagem) {

        // Cria o balao que armazenará a mensagem
        const balaoMensagem = document.createElement('div');

        // Cria elemento span para armazenar mensagem
        const spanMensagem = document.createElement('span');
        // Adiciona o conteúdo da mensagem no span
        spanMensagem.innerHTML = mensagem;
        // Adiciona classe ao span da mensagem para estilização
        spanMensagem.classList.add('conteudoMensagem');

        // Cria elemento span para armazenar nome do usuario
        const spanUsuario = document.createElement('span');
        // Adiciona o nome do usuário no span
        spanUsuario.innerHTML = usuario;
        // Adiciona classe ao span do nome do usuário para estilização
        spanUsuario.classList.add('usuarioMensagem');

        

        // Cria elemento span ara armazenar data da mensagem
        const spanDataMensagem = document.createElement('span');
        // Adiciona data da mensagem no span
        spanDataMensagem.innerHTML = dataMensagem;
        // Adiciona classe ao span da data da mensagem para estilização
        spanDataMensagem.classList.add('dataMensagem');

        // Preenche div com os dados da mensagem
        balaoMensagem.append(spanMensagem);
        balaoMensagem.append(spanUsuario);
        balaoMensagem.append(spanDataMensagem);

        // Se o autor da mensagem for o cliente
        if (localStorage.getItem('usuario') == usuario)
        {
            // Posicionar caixa de mensagem à direita
            balaoMensagem.classList.add('balaoMensagemUsuario');
        }
        else
        {
            // Posicionar caixa de mensagem à esquerda
            balaoMensagem.classList.add('balaoMensagemOutroUsuario');
        }

        // Cria o container que armazenara a caixa da mensagem
        // e permitirá que a caixa seja posicionada na esquerda ou na direita
        const container = document.createElement('div');
        container.classList.add('containerMensagem');

        // Preenche container com a caixa da mensagem
        container.append(balaoMensagem);

        // Adiciona container da mensagem na lista de mensagens
        document.querySelector('#listaMensagens').append(container);
    }


    /* Configura menu lateral */

    // Define o nome de usuário e armazena no localStorage
    const botaoNomeUsuario = document.querySelector('#botaoNomeUsuario');
    botaoNomeUsuario.onclick = () => {

        const nome = document.querySelector('#inputNomeUsuario').value;
        localStorage.setItem('usuario', nome);
        console.log(localStorage.getItem('usuario'));
    };

    // Abre nav lateral
    const iconeMenu = document.querySelector('#iconeMenu');
    iconeMenu.onclick = () => {
        document.getElementById("menulateral").style.width = "50%";
        document.querySelector("#navbar").style.display = "none";
        document.querySelector("#chat").style.display = "none";
        document.querySelector("#formMensagem").style.display = "none";
        document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
    };

    // Fecha nav lateal
    const botaoFechaMenu = document.querySelector('#botaoFecharMenu');
    botaoFechaMenu.onclick = () => {
        document.getElementById("menulateral").style.width = "0";
    	document.querySelector("#navbar").style.display = "table";
        document.querySelector("#chat").style.display = "flex";
        document.querySelector("#formMensagem").style.display = "flex";
    	document.body.style.backgroundColor = "white";
    	
    };
});