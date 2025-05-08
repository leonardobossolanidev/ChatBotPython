import time
from datetime import datetime

# Banco de frutas e estoques (em kg)
estoque = {
    "maçã": {"preco": 3.50, "disponivel": 10},
    "banana": {"preco": 2.00, "disponivel": 15},
    "laranja": {"preco": 2.80, "disponivel": 12},
    "abacaxi": {"preco": 5.00, "disponivel": 5},
    "morango": {"preco": 6.00, "disponivel": 8},
    "lichia": {"preco": 9.00, "disponivel": 4}
}

carrinho = []
desconto_ativo = False

def exibir_menu():
    print("\n--- MENU DE FRUTAS ---")
    for fruta, info in estoque.items():
        print(f"{fruta.capitalize():<10} - R$ {info['preco']:.2f}/kg (Disponível: {info['disponivel']}kg)")

def calcular_total():
    total = sum(item['preco'] * item['quantidade'] for item in carrinho)
    if desconto_ativo:
        total *= 0.9
    return total

def registrar_compra(fruta, quantidade):
    preco_kg = estoque[fruta]["preco"]
    estoque[fruta]["disponivel"] -= quantidade
    carrinho.append({"fruta": fruta, "quantidade": quantidade, "preco": preco_kg})

def remover_item():
    if not carrinho:
        bot_fala("O carrinho está vazio.")
        return
    exibir_resumo()
    fruta_remover = obter_input_usuario("Digite o nome da fruta que deseja remover: ").lower()
    for i, item in enumerate(carrinho):
        if item['fruta'] == fruta_remover:
            estoque[fruta_remover]['disponivel'] += item['quantidade']
            del carrinho[i]
            bot_fala(f"{fruta_remover} removido do carrinho.")
            return
    bot_fala("Fruta não encontrada no carrinho.")

def aplicar_cupom():
    global desconto_ativo
    cupom = obter_input_usuario("Digite o cupom de desconto: ").strip().upper()
    if cupom == "FRUTA10":
        desconto_ativo = True
        bot_fala("Cupom aplicado! 10% de desconto ativado.")
    else:
        bot_fala("Cupom inválido.")

def exibir_resumo():
    print("\n--- RESUMO DA COMPRA ---")
    for item in carrinho:
        total_item = item["preco"] * item["quantidade"]
        print(f"{item['quantidade']}kg de {item['fruta']} - R$ {total_item:.2f}")
    if desconto_ativo:
        print("Desconto aplicado: 10%")
    print(f"Total a pagar: R$ {calcular_total():.2f}")

def salvar_recibo():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("recibo.txt", "w", encoding="utf-8") as f:
        f.write(f"Recibo de Compra - {agora}\n\n")
        for item in carrinho:
            total_item = item["preco"] * item["quantidade"]
            f.write(f"{item['quantidade']}kg de {item['fruta']} - R$ {total_item:.2f}\n")
        if desconto_ativo:
            f.write("Desconto aplicado: 10%\n")
        f.write(f"\nTotal pago: R$ {calcular_total():.2f}\n")
    bot_fala("Recibo salvo em 'recibo.txt'.")

def adicionar_nova_fruta():
    bot_fala("Entrando no modo administrador...")
    fruta = obter_input_usuario("Nome da nova fruta: ").strip().lower()
    try:
        preco = float(obter_input_usuario("Preço por kg: "))
        quantidade = float(obter_input_usuario("Quantidade em kg: "))
    except ValueError:
        bot_fala("Valores inválidos.")
        return
    estoque[fruta] = {"preco": preco, "disponivel": quantidade}
    bot_fala(f"{fruta.capitalize()} adicionada ao estoque.")

def escolher_pagamento():
    print("\nMétodos de pagamento:")
    print("1 - Cartão de Crédito")
    print("2 - PIX")
    print("3 - Dinheiro")
    opcao = obter_input_usuario("Escolha uma opção: ").strip()
    if opcao == "1":
        bot_fala("Pagamento no crédito aprovado! 💳")
    elif opcao == "2":
        bot_fala("Chave PIX: frutas@bot.com ✅")
    elif opcao == "3":
        bot_fala("Pagamento em dinheiro confirmado! 💵")
    else:
        bot_fala("Opção inválida, considerando pagamento em dinheiro.")
        time.sleep(1)

def simular_entrega():
    bairro = obter_input_usuario("Informe seu bairro para estimativa de entrega: ").strip().capitalize()
    tempo_entrega = 30  # Simulação simples
    bot_fala(f"Entrega estimada para o bairro {bairro}: {tempo_entrega} minutos. 🚚")

def bot_fala(mensagem):
    print(f"\n🤖 Bot: {mensagem}")
    time.sleep(1)

def obter_input_usuario(pergunta):
    try:
        return input(pergunta)
    except KeyboardInterrupt:
        bot_fala("Encerrando o atendimento.")
        exit()

def iniciar_bot():
    bot_fala("Olá! Sou seu assistente virtual de vendas de frutas.")
    
    if obter_input_usuario("Você é administrador? (sim/não): ").lower() == "sim":
        adicionar_nova_fruta()

    while True:
        exibir_menu()
        fruta = obter_input_usuario("\nQual fruta deseja comprar? (ou 'sair'): ").strip().lower()
        if fruta == "sair":
            break
        if fruta not in estoque:
            bot_fala(f"Desculpe, não temos '{fruta}'.")
            continue

        try:
            quantidade = float(obter_input_usuario(f"Quantos kg de {fruta}? "))
            if quantidade <= 0:
                bot_fala("A quantidade precisa ser maior que zero.")
                continue
            if quantidade > estoque[fruta]["disponivel"]:
                bot_fala(f"Desculpe, só temos {estoque[fruta]['disponivel']}kg de {fruta}.")
                continue
        except ValueError:
            bot_fala("Por favor, insira um número válido.")
            continue

        registrar_compra(fruta, quantidade)
        bot_fala(f"{quantidade}kg de {fruta} adicionado ao carrinho.")

        acao = obter_input_usuario("Deseja: [1] Comprar mais, [2] Remover item, [3] Cupom, [4] Finalizar: ").strip()
        if acao == "2":
            remover_item()
        elif acao == "3":
            aplicar_cupom()
        elif acao == "4":
            break

    if carrinho:
        exibir_resumo()
        escolher_pagamento()
        simular_entrega()
        salvar_recibo()
        bot_fala("Obrigado pela compra! Até a próxima! 🍓🍍🍌")
    else:
        bot_fala("Nenhuma compra foi realizada. Até logo!")

if __name__ == "__main__":
    iniciar_bot()
