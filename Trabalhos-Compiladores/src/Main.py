import sys
import os
import tkinter as tk
from view.gui import App
from controller.gerenciador_lexico import GerenciadorLexico
from controller.analisador_sintatico import AnalisadorSintatico
from utils.regras import obter_regras
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AplicacaoPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Analisadores Léxicos")
        self.app = App(root, self.encerrar_aplicacao)
        self.root.protocol("WM_DELETE_WINDOW", self.encerrar_aplicacao)

    def encerrar_aplicacao(self):
        App.stop_threads = True
        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                thread.join(timeout=1)
        try:
            self.root.destroy()
        except tk.TclError:
            pass
        finally:
            sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    aplicacao_principal = AplicacaoPrincipal(root)
    root.mainloop()
