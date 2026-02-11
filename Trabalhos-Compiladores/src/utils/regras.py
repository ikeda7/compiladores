import re

especificacao_tokens = [
    (r'[ \t]+', 'ESPACO_EM_BRANCO'),
    (r'return', 'RETORNO'),
    (r'\n', 'NOVA_LINHA'),
    (r'int|float|char|string|bool|string', 'TIPO'),
    (r'var', 'VAR'),
    (r'printf|scanf|from', 'FUNCAO'),
    (r':', 'DOIS_PONTOS'),
    (r';', 'PONTO_E_VIRGULA'),
    (r',', 'VIRGULA'),
    (r'\(', 'PARENTESE_ESQUERDO'),
    (r'\)', 'PARENTESE_DIREITO'),
    (r'\{', 'CHAVE_ESQUERDA'),
    (r'\}', 'CHAVE_DIREITA'),
    (r'\[', 'COLCHETE_ESQUERDO'),
    (r'\]', 'COLCHETE_DIREITO'),
    (r'\+', 'MAIS'),
    (r'-', 'MENOS'),
    (r'\*', 'MULTIPLICACAO'),
    (r'/', 'DIVISAO'),
    (r'=', 'ATRIBUICAO'),
    (r'==', 'IGUAL'),
    (r'!=', 'DIFERENTE'),
    (r'<', 'MENOR'),
    (r'>', 'MAIOR'),
    (r'<=', 'MENOR_IGUAL'),
    (r'>=', 'MAIOR_IGUAL'),
    (r'&&', 'E_LOGICO'),
    (r'\|\|', 'OU_LOGICO'),
    (r'!', 'NAO_LOGICO'),
    (r'//.*', 'COMENTARIO'),
    (r'/\*[\s\S]*?\*/', 'COMENTARIO_MULTILINHA'),
    (r'"([^"\\]|\\.)*"', 'STRING'),
    (r"'([^'\\]|\\.)*'", 'CARACTERE'),
    (r'true|false', 'BOOLEANO'),
    (r'[A-Za-z_][A-Za-z0-9_]*', 'IDENTIFICADOR'),
    (r'\d+(\.\d*)?', 'NUMERO'),
    (r'.', 'ILEGAL'),
]

def obter_regras(nome_conjunto_regras):
    if nome_conjunto_regras == "LALG":
        return especificacao_tokens
    else:
        raise ValueError(f"Conjunto de regras '{nome_conjunto_regras}' não encontrado.")
