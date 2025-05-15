const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

const frutasDisponiveis = ["maçã", "banana", "laranja", "abacaxi", "morango", "lichia"];
let carrinho = [];

function exibirMensagem(mensagem, tipo = 'bot') {
    const div = document.createElement('div');
    div.classList.add(tipo === 'bot' ? 'bot-message' : 'user-message');
    div.innerHTML = mensagem;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight; // rolar para o final
}

function enviarMensagem() {
    const mensagemUsuario = userInput.value.trim().toLowerCase();

    if (!mensagemUsuario) return;

    exibirMensagem(mensagemUsuario, 'user');
    userInput.value = ''; // limpa o campo de entrada

    if (frutasDisponiveis.includes(mensagemUsuario)) {
        exibirMensagem(`Você escolheu ${mensagemUsuario}. Quantos quilos deseja?`, 'bot');
        botFalaQuantidade(mensagemUsuario);
    } else {
        exibirMensagem(`Desculpe, não temos ${mensagemUsuario}. Tente outra fruta.`, 'bot');
    }
}

function botFalaQuantidade(fruta) {
    setTimeout(() => {
        exibirMensagem(`Quantos quilos de ${fruta} você deseja?`, 'bot');
        const quantidadeInput = document.createElement('input');
        quantidadeInput.type = 'number';
        quantidadeInput.placeholder = 'Digite a quantidade em kg';
        quantidadeInput.id = 'quantidade-input';
        chatBox.appendChild(quantidadeInput);
        
        quantidadeInput.addEventListener('blur', () => {
            const quantidade = parseFloat(quantidadeInput.value);
            if (quantidade > 0) {
                carrinho.push({ fruta, quantidade });
                exibirMensagem(`${quantidade}kg de ${fruta} adicionado ao carrinho!`, 'bot');
            } else {
                exibirMensagem("A quantidade precisa ser maior que zero.", 'bot');
            }
            quantidadeInput.remove();
            mostrarResumoCompra();
        });
    }, 1000);
}

function mostrarResumoCompra() {
    setTimeout(() => {
        let resumo = 'Resumo da Compra:\n';
        let total = 0;

        carrinho.forEach(item => {
            const preco = {
                "maçã": 3.50,
                "banana": 2.00,
                "laranja": 2.80,
                "abacaxi": 5.00,
                "morango": 6.00,
                "lichia": 9.00
            }[item.fruta];
            
            const totalItem = preco * item.quantidade;
            resumo += `${item.quantidade}kg de ${item.fruta} - R$ ${totalItem.toFixed(2)}\n`;
            total += totalItem;
        });

        resumo += `Total: R$ ${total.toFixed(2)}`;

        exibirMensagem(resumo, 'bot');
    }, 1500);
}
