from controller.analisador_semantico import AnalisadorSemantico
from controller.gerador_codigo import GeradorDeCodigo

class AnalisadorSintatico:
    def __init__(self, lexico):
        self.lexico = lexico
        self.tokens = []
        self.pos = 0
        self.analisador_semantico = AnalisadorSemantico()
        self.gerador_codigo = GeradorDeCodigo()

    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        while self.pos < len(self.tokens):
            self._funcoes()
        self.gerador_codigo.display_code()

    def _match(self, tipo_token_esperado):
        self._skip_whitespace()
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == tipo_token_esperado:
            self.pos += 1
        else:
            raise SyntaxError(f"Erro de sintaxe: esperado {tipo_token_esperado}, encontrado {self.tokens[self.pos]}")

    def _skip_whitespace(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('WHITESPACE', 'NEWLINE'):
            self.pos += 1

    def _funcoes(self):
        while self.pos < len(self.tokens):
            self._skip_whitespace()
            if self.pos >= len(self.tokens):
                break

            if self.tokens[self.pos][0] == 'VAR':
                self._decl_var_var()
            elif self.tokens[self.pos][0] == 'TYPE':
                self._match('TYPE')
                self._match('IDENTIFIER')
                self._match('LPAREN')
                self._match('RPAREN')
                self._bloco()
            elif self.tokens[self.pos][0] == 'IDENTIFIER':
                self._expressao()
            else:
                raise SyntaxError(f"Declaração ou função esperada, encontrado {self.tokens[self.pos]}")

    def _bloco(self):
        self._match('LBRACE')
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'RBRACE':
            self._stmt()
        self._match('RBRACE')

    def _stmt(self):
        self._skip_whitespace()

        if self.tokens[self.pos][0] == 'VAR':
            self._decl_var_var()
        elif self.tokens[self.pos][0] == 'IDENTIFIER':
            self._expressao()
        elif self.tokens[self.pos][0] == 'RETURN':
            self._match('RETURN')
            valor = self._exp()
            self.gerador_codigo.emit(f"RETURN {valor}")
            self._match('SEMICOLON')
        elif self.tokens[self.pos][0] == 'RBRACE':
            return
        else:
            raise SyntaxError(f"Declaração ou expressão esperada, encontrado {self.tokens[self.pos]}")

    def _if_stmt(self):
        self._match('IF')
        self._match('LPAREN')
        self._exp()
        self._match('RPAREN')
        self._bloco()

    def _decl_var(self):
        self._match('TYPE')
        identificadores = self._lista_identificadores()

        if self.tokens[self.pos][0] != 'SEMICOLON':
            raise SyntaxError(f"Erro de sintaxe: esperado ';', encontrado {self.tokens[self.pos]}")

        self._match('SEMICOLON')

        for identificador in identificadores:
            self.analisador_semantico.declare_variable(identificador, self.tokens[self.pos - 1][1])

        for identificador in identificadores:
            self.gerador_codigo.emit(f"DECLARE {identificador} AS {self.tokens[self.pos - 1][1]}")

    def _decl_var_var(self):
        self._match('VAR')
        identificadores = self._lista_identificadores()
        self._match('COLON')

        if self.tokens[self.pos][0] != 'TYPE':
            raise SyntaxError(f"Erro de sintaxe: esperado um tipo, encontrado {self.tokens[self.pos]}")

        tipo_var = self.tokens[self.pos][1]
        self._match('TYPE')

        print(f"[DEBUG] Declarando variáveis: {identificadores} com tipo {tipo_var}")

        for identificador in identificadores:
            self.analisador_semantico.declare_variable(identificador, tipo_var)

        for identificador in identificadores:
            self.gerador_codigo.emit(f"DECLARE {identificador} AS {tipo_var}")

        if self.tokens[self.pos][0] != 'SEMICOLON':
            raise SyntaxError(f"Erro de sintaxe: esperado ';', encontrado {self.tokens[self.pos]}")

        self._match('SEMICOLON')

    def _lista_identificadores(self):
        identificadores = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'IDENTIFIER':
            identificador = self.tokens[self.pos][1].strip()
            identificadores.append(identificador)
            self._match('IDENTIFIER')
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'COMMA':
                self._match('COMMA')
        return identificadores

    def _expressao(self):
        variavel = self.tokens[self.pos][1]
        self._match('IDENTIFIER')

        if self.tokens[self.pos][0] == 'ASSIGN':
            self._match('ASSIGN')
            valor = self._exp()
            self.gerador_codigo.generate_assignment(variavel, valor)

        if self.tokens[self.pos][0] != 'SEMICOLON':
            raise SyntaxError(f"Erro de sintaxe: esperado SEMICOLON, encontrado {self.tokens[self.pos]}")

        self._match('SEMICOLON')

    def _exp(self):
        self._skip_whitespace()

        if self.tokens[self.pos][0] in ('NUMBER', 'IDENTIFIER', 'STRING', 'BOOLEAN'):
            esquerda = self.tokens[self.pos][1]
            self.pos += 1
        else:
            raise SyntaxError(f"Expressão esperada, encontrado {self.tokens[self.pos]}")

        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
            operador = self.tokens[self.pos][1]
            self.pos += 1

            if self.tokens[self.pos][0] in ('NUMBER', 'IDENTIFIER', 'STRING', 'BOOLEAN'):
                direita = self.tokens[self.pos][1]
                self.pos += 1
            else:
                raise SyntaxError(f"Operando esperado após operador, encontrado {self.tokens[self.pos]}")

            self.gerador_codigo.generate_binary_operation(operador, esquerda, direita)
            esquerda = "RESULT"

        return esquerda

    def _chamada_funcao(self):
        nome_funcao = self.tokens[self.pos][1]
        self._match('FUNCTION')
        self._match('LPAREN')

        argumentos = []
        while self.tokens[self.pos][0] != 'RPAREN':
            if self.tokens[self.pos][0] in ('IDENTIFIER', 'NUMBER', 'STRING'):
                argumentos.append(self.tokens[self.pos][1])
                self.pos += 1
            if self.tokens[self.pos][0] == 'COMMA':
                self._match('COMMA')
        self._match('RPAREN')

        self.gerador_codigo.emit(f"CALL {nome_funcao} WITH {', '.join(argumentos)}")

        self._match('SEMICOLON')
