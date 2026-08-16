"""Interface desktop da reconstrução demonstrativa."""

import tkinter as tk
from tkinter import messagebox, ttk

from database import (
    cadastrar_agendamento,
    cadastrar_cliente,
    cadastrar_profissional,
    cadastrar_servico,
    cancelar_agendamento,
    listar_agendamentos,
    listar_opcoes,
)
from services import texto_obrigatorio, validar_data_hora, validar_email, validar_preco


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Agendamentos")
        self.geometry("980x620")
        self.configure(bg="#07192c")
        self._criar_interface()
        self.atualizar_agenda()

    def _criar_interface(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=30)

        titulo = tk.Label(self, text="Gestão de Agendamentos", bg="#07192c", fg="white", font=("Segoe UI", 24, "bold"))
        titulo.pack(anchor="w", padx=28, pady=(24, 12))

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True, padx=28, pady=(0, 26))

        self.aba_agenda = ttk.Frame(abas, padding=18)
        self.aba_clientes = ttk.Frame(abas, padding=18)
        self.aba_profissionais = ttk.Frame(abas, padding=18)
        self.aba_servicos = ttk.Frame(abas, padding=18)
        self.aba_novo = ttk.Frame(abas, padding=18)
        abas.add(self.aba_agenda, text="Agenda")
        abas.add(self.aba_novo, text="Novo agendamento")
        abas.add(self.aba_clientes, text="Clientes")
        abas.add(self.aba_profissionais, text="Profissionais")
        abas.add(self.aba_servicos, text="Serviços")

        colunas = ("id", "cliente", "profissional", "servico", "inicio", "status")
        self.tabela = ttk.Treeview(self.aba_agenda, columns=colunas, show="headings")
        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna.capitalize())
            self.tabela.column(coluna, width=135, anchor="center")
        self.tabela.pack(fill="both", expand=True)

        botoes = ttk.Frame(self.aba_agenda)
        botoes.pack(fill="x", pady=(14, 0))
        ttk.Button(botoes, text="Atualizar", command=self.atualizar_agenda).pack(side="left")
        ttk.Button(botoes, text="Cancelar selecionado", command=self.cancelar_selecionado).pack(side="left", padx=8)

        self.campos = {}
        for linha, (chave, rotulo) in enumerate((("nome", "Nome"), ("telefone", "Telefone"), ("email", "E-mail"))):
            ttk.Label(self.aba_clientes, text=rotulo).grid(row=linha, column=0, sticky="w", pady=8)
            entrada = ttk.Entry(self.aba_clientes, width=50)
            entrada.grid(row=linha, column=1, sticky="ew", padx=12, pady=8)
            self.campos[chave] = entrada
        ttk.Button(self.aba_clientes, text="Cadastrar cliente", command=self.salvar_cliente).grid(row=3, column=1, sticky="e", pady=16)
        self.aba_clientes.columnconfigure(1, weight=1)

        self._formulario_profissional()
        self._formulario_servico()
        self._formulario_agendamento()

    def _formulario_profissional(self):
        self.profissional_nome = ttk.Entry(self.aba_profissionais, width=50)
        self.profissional_especialidade = ttk.Entry(self.aba_profissionais, width=50)
        for linha, (rotulo, campo) in enumerate((("Nome", self.profissional_nome), ("Especialidade", self.profissional_especialidade))):
            ttk.Label(self.aba_profissionais, text=rotulo).grid(row=linha, column=0, sticky="w", pady=8)
            campo.grid(row=linha, column=1, sticky="ew", padx=12, pady=8)
        ttk.Button(self.aba_profissionais, text="Cadastrar profissional", command=self.salvar_profissional).grid(row=2, column=1, sticky="e", pady=16)
        self.aba_profissionais.columnconfigure(1, weight=1)

    def _formulario_servico(self):
        self.servico_nome = ttk.Entry(self.aba_servicos, width=50)
        self.servico_preco = ttk.Entry(self.aba_servicos, width=50)
        self.servico_duracao = ttk.Entry(self.aba_servicos, width=50)
        campos = (("Nome", self.servico_nome), ("Preço", self.servico_preco), ("Duração em minutos", self.servico_duracao))
        for linha, (rotulo, campo) in enumerate(campos):
            ttk.Label(self.aba_servicos, text=rotulo).grid(row=linha, column=0, sticky="w", pady=8)
            campo.grid(row=linha, column=1, sticky="ew", padx=12, pady=8)
        ttk.Button(self.aba_servicos, text="Cadastrar serviço", command=self.salvar_servico).grid(row=3, column=1, sticky="e", pady=16)
        self.aba_servicos.columnconfigure(1, weight=1)

    def _formulario_agendamento(self):
        self.agenda_cliente = ttk.Combobox(self.aba_novo, state="readonly")
        self.agenda_profissional = ttk.Combobox(self.aba_novo, state="readonly")
        self.agenda_servico = ttk.Combobox(self.aba_novo, state="readonly")
        self.agenda_inicio = ttk.Entry(self.aba_novo)
        campos = (("Cliente", self.agenda_cliente), ("Profissional", self.agenda_profissional), ("Serviço", self.agenda_servico), ("Data e hora (DD/MM/AAAA HH:MM)", self.agenda_inicio))
        for linha, (rotulo, campo) in enumerate(campos):
            ttk.Label(self.aba_novo, text=rotulo).grid(row=linha, column=0, sticky="w", pady=8)
            campo.grid(row=linha, column=1, sticky="ew", padx=12, pady=8)
        ttk.Button(self.aba_novo, text="Carregar cadastros", command=self.carregar_opcoes).grid(row=4, column=0, sticky="w", pady=16)
        ttk.Button(self.aba_novo, text="Confirmar agendamento", command=self.salvar_agendamento).grid(row=4, column=1, sticky="e", pady=16)
        self.aba_novo.columnconfigure(1, weight=1)
        self.opcoes = {}

    def atualizar_agenda(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        try:
            for item in listar_agendamentos():
                self.tabela.insert("", "end", values=(item["id"], item["cliente"], item["profissional"], item["servico"], item["inicio"], item["status"]))
        except Exception as erro:
            messagebox.showwarning("Banco indisponível", f"Configure o MySQL para carregar a agenda.\n\n{erro}")

    def salvar_cliente(self):
        try:
            nome = texto_obrigatorio(self.campos["nome"].get(), "Nome")
            telefone = texto_obrigatorio(self.campos["telefone"].get(), "Telefone")
            email = validar_email(self.campos["email"].get())
            cadastrar_cliente(nome, telefone, email)
            for campo in self.campos.values():
                campo.delete(0, "end")
            messagebox.showinfo("Sucesso", "Cliente cadastrado.")
        except Exception as erro:
            messagebox.showerror("Não foi possível cadastrar", str(erro))

    def salvar_profissional(self):
        try:
            nome = texto_obrigatorio(self.profissional_nome.get(), "Nome")
            cadastrar_profissional(nome, self.profissional_especialidade.get().strip())
            self.profissional_nome.delete(0, "end")
            self.profissional_especialidade.delete(0, "end")
            messagebox.showinfo("Sucesso", "Profissional cadastrado.")
        except Exception as erro:
            messagebox.showerror("Não foi possível cadastrar", str(erro))

    def salvar_servico(self):
        try:
            nome = texto_obrigatorio(self.servico_nome.get(), "Nome")
            preco = validar_preco(self.servico_preco.get())
            duracao = int(self.servico_duracao.get())
            if duracao <= 0:
                raise ValueError("A duração deve ser maior que zero.")
            cadastrar_servico(nome, preco, duracao)
            for campo in (self.servico_nome, self.servico_preco, self.servico_duracao):
                campo.delete(0, "end")
            messagebox.showinfo("Sucesso", "Serviço cadastrado.")
        except Exception as erro:
            messagebox.showerror("Não foi possível cadastrar", str(erro))

    def carregar_opcoes(self):
        try:
            self.opcoes = {tabela: listar_opcoes(tabela) for tabela in ("clientes", "profissionais", "servicos")}
            for tabela, combo in (("clientes", self.agenda_cliente), ("profissionais", self.agenda_profissional), ("servicos", self.agenda_servico)):
                combo["values"] = [f'{item["id"]} — {item["nome"]}' for item in self.opcoes[tabela]]
            messagebox.showinfo("Cadastros", "Opções carregadas.")
        except Exception as erro:
            messagebox.showerror("Não foi possível carregar", str(erro))

    def salvar_agendamento(self):
        try:
            if not all((self.agenda_cliente.get(), self.agenda_profissional.get(), self.agenda_servico.get())):
                raise ValueError("Selecione cliente, profissional e serviço.")
            cliente_id = int(self.agenda_cliente.get().split(" — ", 1)[0])
            profissional_id = int(self.agenda_profissional.get().split(" — ", 1)[0])
            servico_id = int(self.agenda_servico.get().split(" — ", 1)[0])
            inicio = validar_data_hora(self.agenda_inicio.get())
            cadastrar_agendamento(cliente_id, profissional_id, servico_id, inicio)
            self.agenda_inicio.delete(0, "end")
            self.atualizar_agenda()
            messagebox.showinfo("Sucesso", "Agendamento confirmado.")
        except Exception as erro:
            messagebox.showerror("Não foi possível agendar", str(erro))

    def cancelar_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showinfo("Agenda", "Selecione um agendamento.")
            return
        agendamento_id = self.tabela.item(selecao[0], "values")[0]
        try:
            cancelar_agendamento(agendamento_id)
            self.atualizar_agenda()
        except Exception as erro:
            messagebox.showerror("Não foi possível cancelar", str(erro))


if __name__ == "__main__":
    Aplicacao().mainloop()
