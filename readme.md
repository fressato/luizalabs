# Desafios Luizalabs - Python
Repositório contendo soluções para os desafios propostos no bootcamp/curso da Luizalabs.

## 📂 Estrutura do Projeto

### 1. Sistema Bancário V1 (Funcional)

Arquivo: `desafio1_solution.py`
Implementação procedural/funcional de um sistema bancário simples.
- **Funcionalidades**: Depósito, Saque, Extrato, Criação de Usuário e Conta.
- **Destaques**: Uso de argumentos posicionais e nomeados (`*args`, `**kwargs` e `/`), validações robustas.

### 2. Sistema Bancário V2 (POO)

Arquivo: `desafio2_solution.py`
Evolução do sistema bancário utilizando Orientação a Objetos.
- **Classes Principais**: `Cliente`, `PessoaFisica`, `Conta`, `ContaCorrente`, `Historico`, `Transacao`.
- **Conceitos Aplicados**:
    - Herança e Polimorfismo.
    - Classes Abstratas (`ABC`).
    - Encapsulamento com Properties.
    - Modelagem de negócios mais complexa (várias contas por cliente, histórico de transações).

### 3. Desafios de Código (Lógica)

Pasta: `desafios do código/`
Soluções para exercícios isolados de lógica de programação:
- `desafio_gagdet.py`: Exercícios com gadgets/equipamentos.
- `desafio_mensagem.py`: Manipulação de mensagens e strings.
- `desafio_robo.py`: Lógica de movimentação ou controle de robô.
- `desafio_robo_nomeador.py`: Algoritmos de nomeação automática.

## 🚀 Como Executar
Para executar qualquer um dos desafios, utilize o interpretador Python:
```bash
# Exemplo para o Sistema Bancário V2
python desafio2_solution.py