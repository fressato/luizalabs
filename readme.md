# Desafio 1 - Sistema Bancário Simples para Luizalabs

Este projeto consiste em um sistema bancário simples desenvolvido em Python, focado em modularização e boas práticas de programação. O sistema permite realizar operações bancárias básicas como depósitos, saques, visualização de extratos, além do gerenciamento de usuários e contas.

## Funcionalidades Principais

O código foi estruturado em funções específicas para garantir clareza e reutilização:

### Operações Bancárias

*   **Depositar (`depositar`)**:
    *   Função que recebe argumentos apenas por posição (*positional only*).
    *   Valida a existência da conta antes da operação.
    *   Atualiza o saldo e registra a transação no extrato.
    *   Retorna o saldo atualizado e o histórico de extrato.

*   **Sacar (`sacar`)**:
    *   Função que recebe argumentos apenas por nome (*keyword only*).
    *   Realiza múltiplas validações: saldo suficiente, limite de valor por saque e limite diário de saques.
    *   Valida a existência da conta antes da operação.
    *   Atualiza o saldo e registra a transação.

*   **Extrato (`exibir_extrato`)**:
    *   Função híbrida que aceita argumentos posicionais (saldo) e nomeados (extrato).
    *   Exibe todas as movimentações realizadas e o saldo atual.
    *   Exige validação de conta para acesso.

### Gerenciamento de Usuários e Contas

*   **Criar Usuário (`criar_usuario`)**:
    *   Cadastra novos usuários com validação de CPF único.
    *   **Automação**: Ao criar um usuário, uma conta corrente é **automaticamente criada** e vinculada a ele.
    *   Dados armazenados: Nome, data de nascimento, CPF e endereço.

*   **Validar Conta (`validar_conta_usuario`)**:
    *   Função auxiliar criada para centralizar a validação de contas.
    *   Solicita agência e número da conta, verificando sua existência na lista de contas cadastradas.
    *   Utilizada como pré-requisito para as operações de saque, depósito e extrato.

*   **Filtrar Usuário (`filtrar_usuario`)**:
    *   Busca usuários na base de dados através do CPF.

*   **Listar Contas (`listar_contas`)**:
    *   Exibe todas as contas correntes cadastradas, mostrando agência, número da conta e titular.

## Estrutura do Código

O fluxo principal (`main`) gerencia o menu de interação com o usuário, mantendo o estado da aplicação (saldo, listas de usuários e contas, etc.) e delegando as regras de negócio para as funções modularizadas.

## Como Executar

Certifique-se de ter o Python instalado. Execute o arquivo principal no terminal:

```bash
python desafio1_solution.py
```
