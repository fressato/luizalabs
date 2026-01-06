class Mensagem:
    def __init__(self, remetente, conteudo):
        self.remetente = remetente
        self.conteudo = conteudo

    def exibir(self):
        return f"{self.remetente}: {self.conteudo}"

if __name__ == "__main__":
    remetente = input()
    conteudo = input()
    mensagem = Mensagem(remetente, conteudo)
    print(mensagem.exibir())