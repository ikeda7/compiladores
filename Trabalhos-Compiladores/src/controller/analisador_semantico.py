class TabelaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def adicionar_simbolo(self, nome, tipo_simbolo):
        if nome in self.simbolos:
            raise Exception(f"Erro Semântico: Símbolo '{nome}' já está declarado.")
        self.simbolos[nome] = tipo_simbolo

    def obter_simbolo(self, nome):
        return self.simbolos.get(nome, None)

    def obter_todos_simbolos(self):
        return self.simbolos.items()

    def __str__(self):
        return str(self.simbolos)


class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()

    def declarar_variavel(self, nome, tipo_var):
        tipos_validos = ["int", "float", "char", "string", "bool"]

        if not nome.strip():
            raise Exception(f"Erro Semântico: Nome de variável inválido '{nome}'.")
        if not nome.isidentifier():
            raise Exception(f"Erro Semântico: Nome de variável inválido '{nome}'. Deve seguir as convenções de nomenclatura.")

        if tipo_var not in tipos_validos:
            raise Exception(f"Erro Semântico: Tipo inválido '{tipo_var}'. Tipos válidos são: {', '.join(tipos_validos)}.")

        self.tabela_simbolos.adicionar_simbolo(nome, tipo_var)
        print(f"Variável declarada: {nome} com tipo: {tipo_var}")

    def verificar_variavel(self, nome):
        if not nome.strip():
            raise Exception(f"Erro Semântico: Nome de variável inválido '{nome}'.")
        if self.tabela_simbolos.obter_simbolo(nome) is None:
            raise Exception(f"Erro Semântico: Variável '{nome}' não está declarada.")
        print(f"Variável '{nome}' está declarada.")

    def verificar_tipo(self, nome, tipo_esperado):
        tipo_atual = self.tabela_simbolos.obter_simbolo(nome)
        if tipo_atual is None:
            raise Exception(f"Erro Semântico: Variável '{nome}' não está declarada.")
        if tipo_atual != tipo_esperado:
            raise Exception(f"Erro Semântico: Incompatibilidade de tipo para a variável '{nome}'. Esperado '{tipo_esperado}', obtido '{tipo_atual}'.")

    def validar_atribuicao(self, nome, valor):
        tipo_atual = self.tabela_simbolos.obter_simbolo(nome)
        if tipo_atual is None:
            raise Exception(f"Erro Semântico: Variável '{nome}' não está declarada.")

        if isinstance(valor, int) and tipo_atual != "int":
            raise Exception(f"Erro Semântico: Não é possível atribuir int a '{nome}' do tipo '{tipo_atual}'.")
        elif isinstance(valor, float) and tipo_atual != "float":
            raise Exception(f"Erro Semântico: Não é possível atribuir float a '{nome}' do tipo '{tipo_atual}'.")
        elif isinstance(valor, str):
            if tipo_atual == "char" and len(valor) > 1:
                raise Exception(f"Erro Semântico: Valor '{valor}' é muito longo para o tipo 'char'.")
            elif tipo_atual not in ["string", "char"]:
                raise Exception(f"Erro Semântico: Não é possível atribuir string a '{nome}' do tipo '{tipo_atual}'.")
        elif isinstance(valor, bool) and tipo_atual != "bool":
            raise Exception(f"Erro Semântico: Não é possível atribuir bool a '{nome}' do tipo '{tipo_atual}'.")
        print(f"Atribuição validada: {nome} = {valor}")

    def obter_tabela_simbolos(self):
        return self.tabela_simbolos
