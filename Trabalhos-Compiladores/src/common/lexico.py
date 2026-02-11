import re

class Lexico:
    def __init__(self, regras):
        self.regras = [(re.compile(padrao), tipo_token) for padrao, tipo_token in regras]

    def tokenizar(self, texto):
        pos = 0
        tokens = []
        while pos < len(texto):
            match = None
            for padrao, tipo_token in self.regras:
                match = padrao.match(texto, pos)
                if match:
                    lexema = match.group(0)
                    if tipo_token == 'WHITESPACE':
                        pos = match.end()
                        continue
                    token = (tipo_token, lexema)
                    tokens.append(token)
                    pos = match.end()
                    break
            if not match:
                raise SyntaxError(f"Caractere ilegal no índice {pos}")
        return tokens
