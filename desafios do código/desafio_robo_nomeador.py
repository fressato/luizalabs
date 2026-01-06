# RoboNomeador 3000 - Núcleo em Python (POO)

class Robo:
    def __init__(self, modelo1: str, modelo2: str):
        # O construtor armazena os estados (dados) do objeto
        self.modelo1 = modelo1
        self.modelo2 = modelo2

    def nome_completo(self) -> str:
        # O método processa os dados e retorna o nome formatado
        return f"{self.modelo1}-{self.modelo2}"

# Lê a entrada padrão e separa em dois modelos usando espaço como separador
entrada = input().strip()
modelos = entrada.split()

if len(modelos) != 2:
    print("Entrada invalida: devem ser dois modelos separados por espaço.")
else:
    modelo1, modelo2 = modelos

    # Implementação da lógica de POO:
    # 1. Criamos uma instância (objeto) da classe Robo
    novo_robo = Robo(modelo1, modelo2)
    
    # 2. Chamamos o método nome_completo() e exibimos o resultado
    print(novo_robo.nome_completo())