import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils.regras import obter_regras
from controller.gerenciador_lexico import GerenciadorLexico
from controller.analisador_sintatico import AnalisadorSintatico
import threading


class App:
    parar_threads = False

    def __init__(self, root, callback_sair):
        self.root = root
        self.gerenciador = GerenciadorLexico()
        self.callback_sair = callback_sair

        self.root.title("Gerador de Analisadores Léxicos")
        self.root.configure(bg="#2E2E2E")

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#2E2E2E")
        estilo.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        estilo.configure("TButton", background="#3C3F41", foreground="#FFFFFF")
        estilo.configure("Treeview", background="#3C3F41", foreground="#FFFFFF", fieldbackground="#3C3F41")
        estilo.map("TButton", background=[("active", "#555555")])

        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.numeros_linha = tk.Text(
            self.top_frame, width=4, padx=3, takefocus=0, border=0,
            background='#3C3F41', foreground="#FFFFFF", state='disabled'
        )
        self.numeros_linha.pack(side=tk.LEFT, fill=tk.Y)

        self.texto_entrada = tk.Text(
            self.top_frame, wrap=tk.WORD, undo=True, background='#3C3F41',
            foreground="#FFFFFF", insertbackground="#FFFFFF"
        )
        self.texto_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.texto_entrada.bind("<KeyRelease>", self.atualizar_numeros_linha)

        self.scrollbar = ttk.Scrollbar(self.top_frame, command=self.sincronizar_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_entrada.config(yscrollcommand=self.scrollbar.set)
        self.numeros_linha.config(yscrollcommand=self.scrollbar.set)

        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.arvore = ttk.Treeview(
            self.bottom_frame, columns=("Lexema", "Token", "Erro", "Linha", "Coluna inicial", "Coluna final"),
            show="headings", height=8
        )
        self.arvore.heading("Lexema", text="Lexema")
        self.arvore.heading("Token", text="Token")
        self.arvore.heading("Erro", text="Erro")
        self.arvore.heading("Linha", text="Linha")
        self.arvore.heading("Coluna inicial", text="Coluna Inicial")
        self.arvore.heading("Coluna final", text="Coluna Final")
        self.arvore.pack(fill=tk.BOTH, expand=True)

        self.info_frame = ttk.Frame(root)
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.arvore_tabela_simbolos = ttk.Treeview(
            self.info_frame, columns=("Nome", "Tipo"), show="headings", height=8
        )
        self.arvore_tabela_simbolos.heading("Nome", text="Nome")
        self.arvore_tabela_simbolos.heading("Tipo", text="Tipo")
        self.arvore_tabela_simbolos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.arvore_codigo = ttk.Treeview(
            self.info_frame, columns=("Código",), show="headings", height=8
        )
        self.arvore_codigo.heading("Código", text="Código")
        self.arvore_codigo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.inner_button_frame = ttk.Frame(self.button_frame)
        self.inner_button_frame.pack(side=tk.TOP, expand=True)

        self.botao_abrir = ttk.Button(self.inner_button_frame, text="Abrir", command=self.abrir_arquivo)
        self.botao_abrir.pack(side=tk.LEFT, padx=5)

        self.botao_salvar = ttk.Button(self.inner_button_frame, text="Salvar", command=self.salvar_arquivo)
        self.botao_salvar.pack(side=tk.LEFT, padx=5)

        self.botao_tokenizar = ttk.Button(
            self.inner_button_frame, text="Tokenizar", command=self.tokenizar_entrada_threaded
        )
        self.botao_tokenizar.pack(side=tk.LEFT, padx=5)

        self.botao_limpar = tk.Button(
            self.inner_button_frame, text="Limpar", command=self.limpar_texto,
            bg='#1E90FF', fg='white', activebackground='#4682B4', activeforeground='white'
        )
        self.botao_limpar.pack(side=tk.LEFT, padx=5)

        self.botao_fechar = tk.Button(
            self.inner_button_frame,
            text="Fechar",
            command=self.sair_aplicacao,
            bg='#FF6347', fg='white', activebackground='#CD5C5C', activeforeground='white'
        )
        self.botao_fechar.pack(side=tk.LEFT, padx=5)

    def sair_aplicacao(self):
        App.parar_threads = True
        self.callback_sair()

    def atualizar_numeros_linha(self, event=None):
        contagem_linhas = self.texto_entrada.index('end').split('.')[0]
        self.numeros_linha.config(state='normal')
        self.numeros_linha.delete(1.0, tk.END)
        for i in range(1, int(contagem_linhas)):
            self.numeros_linha.insert(tk.END, f"{i}\n")
        self.numeros_linha.config(state='disabled')

    def sincronizar_scroll(self, *args):
        self.texto_entrada.yview(*args)
        self.numeros_linha.yview(*args)

    def abrir_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if caminho_arquivo:
            with open(caminho_arquivo, 'r') as arquivo:
                conteudo = arquivo.read()
                self.texto_entrada.delete(1.0, tk.END)
                self.texto_entrada.insert(tk.END, conteudo)

    def salvar_arquivo(self):
        caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if caminho_arquivo:
            with open(caminho_arquivo, 'w') as arquivo:
                conteudo = self.texto_entrada.get(1.0, tk.END)
                arquivo.write(conteudo)

    def tokenizar_entrada(self):
        if App.parar_threads:
            return

        nome_lexer = "lexer_atual"
        texto_entrada = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto_entrada:
            messagebox.showwarning("Aviso", "O texto de entrada não pode ficar vazio.")
            return

        try:
            regras = obter_regras("LALG")
            self.gerenciador.adicionar_lexico(nome_lexer, regras)
            tokens = self.gerenciador.tokenizar(nome_lexer, texto_entrada)

            print(f"[DEBUG] Tokens gerados: {tokens}")

            for item in self.arvore.get_children():
                self.arvore.delete(item)
            for item in self.arvore_tabela_simbolos.get_children():
                self.arvore_tabela_simbolos.delete(item)
            for item in self.arvore_codigo.get_children():
                self.arvore_codigo.delete(item)

            linha_atual = 1
            coluna_atual = 1
            for tipo_token, lexema in tokens:
                linha = linha_atual
                col_inicio = coluna_atual
                col_fim = col_inicio + len(lexema) - 1

                coluna_atual = col_fim + 1
                if '\n' in lexema:
                    linhas = lexema.split('\n')
                    linha_atual += len(linhas) - 1
                    coluna_atual = len(linhas[-1]) + 1

                self.arvore.insert("", "end", values=(lexema, tipo_token, "", linha, col_inicio, col_fim))

            parser = AnalisadorSintatico(self.gerenciador.obter_lexico(nome_lexer))
            parser.parse(tokens)

            print(f"[DEBUG] Tabela de símbolos após o parsing: {parser.semantic_analyzer.symbol_table.get_all_symbols()}")

            for nome, tipo_simbolo in parser.semantic_analyzer.symbol_table.get_all_symbols():
                print(f"[DEBUG] Adicionando à tabela de símbolos: Nome={nome}, Tipo={tipo_simbolo}")
                self.arvore_tabela_simbolos.insert("", "end", values=(nome, tipo_simbolo))

            self.arvore_tabela_simbolos.update()

            for instrucao in parser.code_generator.instructions:
                self.arvore_codigo.insert("", "end", values=(instrucao,))

            messagebox.showinfo("Sucesso", "Análise concluída com sucesso!")

        except ValueError as e:
            if not App.parar_threads:
                messagebox.showerror("Erro", str(e))
        except SyntaxError as e:
            if not App.parar_threads:
                messagebox.showerror("Erro", str(e))

    def tokenizar_entrada_threaded(self):
        thread = threading.Thread(target=self.tokenizar_entrada)
        thread.daemon = True
        thread.start()

    def limpar_texto(self):
        self.texto_entrada.delete("1.0", tk.END)
        for item in self.arvore.get_children():
            self.arvore.delete(item)
        for item in self.arvore_tabela_simbolos.get_children():
            self.arvore_tabela_simbolos.delete(item)
        for item in self.arvore_codigo.get_children():
            self.arvore_codigo.delete(item)
        self.atualizar_numeros_linha()
