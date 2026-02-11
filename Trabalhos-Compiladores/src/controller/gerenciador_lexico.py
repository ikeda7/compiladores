from common.lexico import Lexico

class GerenciadorLexico:
    def __init__(self):
        self.lexicos = {}

    def adicionar_lexico(self, nome, regras):
        self.lexicos[nome] = Lexico(regras)

    def obter_lexico(self, nome):
        return self.lexicos.get(nome, None)

    def tokenizar(self, nome_lexico, texto):
        lexico = self.obter_lexico(nome_lexico)
        if lexico is None:
            raise ValueError(f"Nenhum léxico encontrado com o nome {nome_lexico}")
        return lexico.tokenizar(texto)
