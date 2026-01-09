import textwrap

def menu():
    # As três aspas (""") permitem escrever textos com várias linhas.
    # O \t dá um espaçamento (tabulação) visual no menu.
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    
    # textwrap.dedent remove os espaços em branco extras do início da linha
    # para o menu ficar alinhado à esquerda na tela.
    # input exibe o texto e espera o usuário digitar algo.
    return input(textwrap.dedent(menu_texto))


def depositar(saldo, extrato, contas, /):
    
    conta = validar_conta_usuario(contas)

    if not conta:
        return saldo, extrato

    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        # Adiciona o valor ao saldo atual
        saldo += valor
        # Adiciona a descrição da operação no texto do extrato.
        # O f"..." permite colocar variáveis dentro do texto (interpolação).
        # :.2f formata o número para ter 2 casas decimais.
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retorna o saldo atualizado e o texto do extrato atualizado.
    return saldo, extrato


def sacar(*, saldo, extrato, limite, numero_saques, limite_saques, contas):
    
    conta = validar_conta_usuario(contas)

    if not conta:
        return saldo, extrato

    valor = float(input("Informe o valor do saque: "))

    # Verificações de segurança antes de permitir o saque
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    
    elif valor > 0:
        # Se passou em todas as verificações e o valor é positivo:
        saldo -= valor  # Subtrai o valor do saldo
        extrato += f"Saque:\t\tR$ {valor:.2f}\n" # Registra no extrato
        numero_saques += 1 # Aumenta o contador de saques
        print("\n=== Saque realizado com sucesso! ===")
    
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retorna os dados atualizados
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato, contas):
    
    conta = validar_conta_usuario(contas)

    if not conta:
        return

    print("\n================ EXTRATO ================")
    
    # Verifica se a variável 'extrato' está vazia.
    # Se não estiver vazia (not extrato é falso), imprime o extrato.
    # Se estiver vazia, imprime a mensagem "Não foram realizadas...".
    print("Não foram realizadas movimentações." if not extrato else extrato)
    
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios, contas, agencia):
    cpf = input("Informe o CPF (somente número): ")
    
    # Chama a função auxiliar para ver se o CPF já existe na lista
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        # Se encontrou um usuário, avisa e encerra a função com return
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    # Se não existe, pede os outros dados
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Cria um dicionário (par chave: valor) com os dados e adiciona na lista de usuários
    novo_usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    usuarios.append(novo_usuario)

    print("=== Usuário criado com sucesso! ===")

    # Criação automática da conta
    numero_conta = len(contas) + 1
    conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": novo_usuario}
    contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    # Percorre a lista 'usuarios'. Para cada 'usuario' na lista,
    # verifica se a chave ["cpf"] é igual ao cpf informado.
    # Isso cria uma nova lista apenas com os usuários encontrados.
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    
    # Se a lista não estiver vazia, retorna o primeiro (e único) elemento [0].
    # Se estiver vazia, retorna None (vazio).
    return usuarios_filtrados[0] if usuarios_filtrados else None


def filtrar_conta(agencia, numero_conta, contas):
    conta_buscada = [conta for conta in contas if conta["agencia"] == agencia and conta["numero_conta"] == numero_conta]
    return conta_buscada[0] if conta_buscada else None


def validar_conta_usuario(contas):
    agencia = input("Informe a agência: ")
    numero_conta = int(input("Informe o número da conta: "))

    conta = filtrar_conta(agencia, numero_conta, contas)

    if not conta:
         print("\n@@@ Conta não encontrada! @@@")
         return None
    
    return conta


def listar_contas(contas):
    for conta in contas:
        # Acessa os dados dentro do dicionário conta.
        # Note que para pegar o nome, acessamos a chave ['usuario'] e depois ['nome']
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        # textwrap aqui garante que a formatação do print fique bonita
        print(textwrap.dedent(linha))


def main():
    # Definição das constantes e variáveis iniciais do programa
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    
    # Listas vazias para armazenar os dados em memória
    usuarios = []
    contas = []

    # Loop infinito: o programa roda até o usuário escolher "q" (break)
    while True:
        opcao = menu()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato, contas)
            print(f"Saldo atual:\t\tR$ {saldo:.2f}")

        elif opcao == "s":
            saldo, extrato = sacar(
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
                contas=contas,
            )
            print(f"Saldo atual:\t\tR$ {saldo:.2f}")

        elif opcao == "e":
            # Exibir extrato usa argumentos mistos:
            # saldo é posicional, extrato é nomeado.
            exibir_extrato(saldo, extrato=extrato, contas=contas)

        elif opcao == "nu":
            criar_usuario(usuarios, contas, AGENCIA)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break  # Sai do loop while e encerra o programa

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Verifica se este é o arquivo principal sendo executado e inicia o programa
if __name__ == "__main__":
    main()