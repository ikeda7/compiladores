import sys
import os
import tkinter as tk
from view.gui import App
from controller.gerenciador_lexico import GerenciadorLexico
from controller.analisador_sintatico import AnalisadorSintatico
from utils.regras import obter_regras

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    def encerrar_aplicacao():
        root.destroy()
        sys.exit(0)

    root = tk.Tk()
    app = App(root, quit_callback=encerrar_aplicacao)
    root.mainloop()

    gerenciador_lexico = GerenciadorLexico()
    gerenciador_lexico.add_lexer("LALG", obter_regras("LALG"))

    texto_entrada = "var x, y: integer"

    tokens = gerenciador_lexico.tokenize("LALG", texto_entrada)
    print("Tokens gerados:", tokens)

    analisador = AnalisadorSintatico(gerenciador_lexico.get_lexer("LALG"))
    try:
        analisador.parse(tokens)
        print("Análise sintática concluída com sucesso!")
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")
