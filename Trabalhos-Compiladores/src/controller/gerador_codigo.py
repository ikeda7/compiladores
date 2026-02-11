class GeradorDeCodigo:
    def __init__(self):
        self.instrucoes = []

    def emitir(self, instrucao):
        self.instrucoes.append(instrucao)

    def gerar_operacao_binaria(self, operacao, esquerda, direita):
        instrucao = f"{esquerda} {operacao} {direita}"
        self.emitir(f"RESULTADO = {instrucao}")
        print(f"Operação binária gerada: {instrucao}")

    def gerar_atribuicao(self, variavel, valor):
        if isinstance(valor, str):
            valor_repr = f'"{valor}"'
        else:
            valor_repr = valor
        self.emitir(f"{variavel} = {valor_repr};")
        print(f"Atribuição gerada: {variavel} = {valor_repr}")

    def gerar_condicao(self, condicao):
        self.emitir(f"SE {condicao}")
        print(f"Condição gerada: SE {condicao}")

    def exibir_codigo(self):
        print("\nCódigo Gerado:")
        for instrucao in self.instrucoes:
            print(instrucao)
