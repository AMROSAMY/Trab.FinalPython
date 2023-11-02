import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
import sys
import numpy as np
import re

class BaseForm:
    def __init__(self, master, controller, title): # metodo construtor da classe e aceita
        self.master = master                       # neste caso 3 parametros
        self.controller = controller
        self.frame = tk.Frame(self.master, background="green")
        self.label = tk.Label(self.frame, text=title, background="green")

    def show(self):
        # Esconder o formulário atualmente visível
        self.controller.current_form.hide()

        # Mostrar este formulário
        self.frame.pack(fill='both', expand=True)
        self.label.pack()

        # Atualizar o formulário atualmente visível
        self.controller.current_form = self

    def hide(self):
        self.frame.pack_forget()

class PresentationForm(BaseForm):
    def __init__(self, master, controller):
        super().__init__(master, controller, "Formulário de Apresentação")

        self.frame.configure(background="green")

        # Título de apresentação centrado no topo
        self.label.configure(font=("Helvetica", 30, "bold"), foreground="red")
        self.label.pack(pady=30)

        presentation_text = """Trabalho Final:   UFCD 10794   'Programação Avançada com Python'


Grupo de trabalho:   Ângelo Veiga
                                   Nuno Martins
                                   Américo Moreira
                                   Armando Pinheiro
                                   """

        presentation_label = tk.Label(self.frame, text=presentation_text, font=("Helvetica", 16, "bold"), foreground="brown", justify="left", bg="light grey")
        presentation_label.pack(pady=30)

        # Carregar a imagem e adiciona ao formulário
        image_frame = tk.Frame(self.frame)
        image = Image.open("Logo_IEFP_Horizontal_1_c.png")
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(image_frame, image=photo)
        image_label.image = photo
        image_label.pack(side='top')

        # Adicionar o texto
        text_label = tk.Label(image_frame,
                              text="DELEGAÇÃO REGIONAL DO NORTE\nCENTRO DE EMPREGO E FORMAÇÃO PROFISSIONAL DE VILA NOVA DE GAIA",
                              font=("Helvetica", 10, "bold"), foreground="black", justify="left")
        text_label.pack(side=tk.TOP)

        # Empacota frame da imagem no canto inferior esquerdo
        image_frame.pack(side=tk.LEFT, padx=5, pady=5)

        presentation_label.pack(pady=70)

class GraphForm(BaseForm):
    def __init__(self, master, controller):
        super().__init__(master, controller, "Formulário Gráfico")

        self.frame.configure(background="green")

        # Título centrado no topo
        self.label.configure(font=("Helvetica", 25, "bold"), foreground="brown", bg="light grey", width=20)
        self.label.pack(pady=40)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=20, pady=20)

        # Chama a função plot_decades para criar o gráfico ao iniciar o formulário
        self.plot()

    def show(self):
        # Mostrar o formulário e plotar o gráfico de décadas
        super().show()
        self.plot()

    def plot(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()

        # Consultar as idades dos contatos
        cursor.execute("SELECT idade FROM contacts;")
        ages = [row[0] for row in cursor.fetchall()]

        # Calcular o valor médio das idades
        average_age = np.mean(ages)

        conn.close()

        # Plotar o gráfico
        self.ax.clear()  # Limpar o gráfico anterior
        self.ax.bar(["Média de Idades"], [average_age], color='purple')

        # Adicionar título ao gráfico
        self.ax.set_title("Média de Idades", color='brown')

        self.canvas.draw()

class ContactForm(BaseForm):
    def __init__(self, master, controller):
        super().__init__(master, controller, "Formulario de Contato")
        self.frame.configure(background="green")

        # Título centrado no topo
        self.label.configure(font=("Helvetica", 25, "bold"), foreground="brown", bg="light grey", width=20)
        self.label.pack(pady=40)

        # Criar o objeto de estilo
        self.style = ttk.Style()

        # Definir o estilo para labels
        self.style.configure("TLabel", font=("Helvetica", 12, "bold"))

        # Definir o estilo para o formulário (cor de fundo, cor do texto, e tamanho)
        self.style.configure("TLabel", foreground="Brown", background="light grey", width=8)

        # Criar os widgets para entrada de dados
        self.name_frame = tk.Frame(self.frame)
        self.name_label = ttk.Label(self.name_frame, text="Nome:", style="TLabel")
        self.name_entry = ttk.Entry(self.name_frame, style="TEntry", font=("Helvetica", 10), foreground="blue")

        self.phone_frame = tk.Frame(self.frame)
        self.phone_label = ttk.Label(self.phone_frame, text="Telefone:", style="TLabel")
        self.phone_entry = ttk.Entry(self.phone_frame, style="TEntry", font=("Helvetica", 10), foreground="blue")

        self.idade_frame = tk.Frame(self.frame)
        self.idade_label = ttk.Label(self.idade_frame, text="Idade:", style="TLabel")
        self.idade_entry = ttk.Entry(self.idade_frame, style="TEntry", font=("Helvetica", 10), foreground="blue")

        # Disposição dos widgets
        self.name_frame.pack(pady=5, padx=20)
        self.name_label.pack(side="left")
        self.name_entry.pack(side="left")

        self.phone_frame.pack(pady=5, padx=20)
        self.phone_label.pack(side="left")
        self.phone_entry.pack(side="left")

        self.idade_frame.pack(pady=5, padx=20)
        self.idade_label.pack(side="left")
        self.idade_entry.pack(side="left")

        # Carregar a imagem e adicionar ao formulário
        self.image_frame = tk.Frame(self.frame)
        self.image = Image.open("cartao_postal_militar.png")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.frame, image=self.photo)
        self.image_label.pack(side='left')

        self.button_width = 14

        # Criar os botões usando o estilo personalizado
        self.add_button = tk.Button(self.frame, text="Adicionar contato", command=self.add_contact, bg="light grey", fg="brown", font=("Helvetica", 11, "bold"), width=self.button_width)
        self.delete_button = tk.Button(self.frame, text="Eliminar contato", command=self.delete_contact, bg="light grey", fg="brown", font=("Helvetica", 11, "bold"), width=self.button_width)
        self.update_button = tk.Button(self.frame, text="Atualizar contato", command=self.update_contact, bg="light grey", fg="brown", font=("Helvetica", 11, "bold"), width=self.button_width)
        self.list_button = tk.Button(self.frame, text="Listar contatos", command=self.update_contacts_list, bg="light grey", fg="brown", font=("Helvetica", 11, "bold"), width=self.button_width)
        self.pdf_button = tk.Button(self.frame, text="Gerar PDF", command=self.gerar_pdf, bg="light grey", fg="brown", font=("Helvetica", 11, "bold"), width=self.button_width)
        self.clear_button = tk.Button(self.frame, text="Limpar", command=self.clear_entries, bg="light grey", fg="brown", font=("Helvetica", 11, "bold"), width=self.button_width)

        # Cria uma frame para os botões e dados
        self.buttons_and_data_frame = tk.Frame(self.frame, bg="green")
        self.buttons_and_data_frame.pack(side="left")

        # Arranja os widgets no formulário
        self.add_button.pack(side="top", pady=10, padx=40, fill="x")
        self.delete_button.pack(side="top", pady=10, padx=40, fill="x")
        self.update_button.pack(side="top", pady=10, padx=40, fill="x")
        self.list_button.pack(side="top", pady=10, padx=40, fill="x")
        self.pdf_button.pack(side="top", pady=10, padx=40, fill="x")
        self.clear_button.pack(side="top", pady=10, padx=40, fill="x")

        # Criar um estilo personalizado para os itens da Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground="brown")

        # Criar a treeview para listar os contatos
        self.contacts_treeview = ttk.Treeview(self.buttons_and_data_frame, columns=("Nome", "Telefone", "Idade"), show="headings")
        self.contacts_treeview.heading("Nome", text="Nome")
        self.contacts_treeview.heading("Telefone", text="Telefone")
        self.contacts_treeview.heading("Idade", text="Idade")

        # Definir a âncora (anchor) para centralizar as colunas de Telefone e Idade
        self.contacts_treeview.column("Telefone", anchor="center")
        self.contacts_treeview.column("Idade", anchor="center")

        # Aplicar o estilo personalizado aos cabeçalhos
        self.contacts_treeview.tag_configure("evenrow", background="coral", font=("Helvetica", 10), foreground="blue")
        self.contacts_treeview.tag_configure("oddrow", background="lightblue", font=("Helvetica", 10), foreground="blue")

        self.contacts_treeview.pack(padx=70, pady=40, expand=True, fill="both")

        # Conectar ao banco de dados
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()

        # Criar a tabela de contatos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                idade INT NOT NULL
            );
        """)
        self.update_contacts_list()

    def validate_phone_number(self, phone_number):
        if re.match(r'^\d{9}$', phone_number):
            return True
        else:
            return  False

    def validate_age(self, age):
        try:
            age = int(age)
            if 10 <= age <= 110:
                return True
            else:
                return False
        except ValueError:
                return False

    def add_contact(self):
        # Pegar os dados dos widgets de entrada
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        idade = self.idade_entry.get()

        if not self.validate_phone_number(phone):
            tk.messagebox.showwarning('Erro', 'Número de telefone inválido.')
            return

        if not self.validate_age(idade):
            tk.messagebox.showwarning('Erro', 'Idade inválida.')
            return

        # Inserir os dados na tabela
        self.cursor.execute("""
            INSERT INTO contacts (name, phone, idade) VALUES (?, ?, ?);
        """, (name, phone, idade))
        self.conn.commit()

        # Limpar os widgets de entrada
        self.clear_entries()

        # Atualizar a lista de contatos
        self.update_contacts_list()

    def delete_contact(self):
        # Selecionar contacto para apagar
        selected_contact = self.contacts_treeview.selection()[0]
        selected_contact_name = self.contacts_treeview.item(selected_contact, 'values')[0]

        # Eliminar o contato do banco de dados
        self.cursor.execute("""
            DELETE FROM contacts WHERE name = ?;
        """, (selected_contact_name,))
        self.conn.commit()

        # Atualizar a lista de contatos
        self.update_contacts_list()

    def update_contact(self):
        # Verifica se algum contato está selecionado
        if not self.contacts_treeview.selection():
            tk.messagebox.showwarning('Erro', 'Selecione um contato para atualizar.')
            return

        # Pegar o contato selecionado e os novos dados
        selected_contact = self.contacts_treeview.selection()[0]
        selected_contact_name = self.contacts_treeview.item(selected_contact, 'values')[0]
        new_name = self.name_entry.get()
        new_phone = self.phone_entry.get()
        new_idade = self.idade_entry.get()

        # Atualizar o contato no banco de dados
        self.cursor.execute("""
            UPDATE contacts SET name = ?, phone = ?, idade = ? WHERE name = ?;
        """, (new_name, new_phone, new_idade, selected_contact_name))
        self.conn.commit()

        # Limpar os widgets de entrada
        self.clear_entries()

        # Atualizar a lista de contatos
        self.update_contacts_list()

    def clear_entries(self):
        # Limpar os widgets de entrada
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.idade_entry.delete(0, 'end')

    def centralize_data(self, data):
        # Limpar a lista de contatos
        self.contacts_treeview.delete(*self.contacts_treeview.get_children())

        # Adicionar os contatos à lista centrando os dados
        for i, row in enumerate(data):
            id, nome, telefone, idade = row
            if i % 2 == 0:
                self.contacts_treeview.insert('', 'end', values=(nome.center(0), telefone.center(42), str(idade).center(45)), tags=("evenrow",))
            else:
                self.contacts_treeview.insert('', 'end', values=(nome.center(0), telefone.center(42), str(idade).center(45)), tags=("oddrow",))

    def update_contacts_list(self):
        # Pegar a lista de contatos do banco de dados
        self.cursor.execute("SELECT * FROM contacts;")
        contacts = self.cursor.fetchall()

        # Chama o método centralize_data para atualizar a exibição dos contatos
        self.centralize_data(contacts)

    def gerar_pdf(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()

        # Consultar os dados do banco de dados
        cursor.execute("SELECT * FROM contacts;")
        data = cursor.fetchall()
        print(data)

        # Fechar a conexão com o banco de dados
        conn.close()

        if not data:
            # Verifica se os dados estão vazios
            tk.messagebox.showwarning('Atenção', 'Os dados estão vazios. Adicione contatos antes de gerar o PDF.')
            return

        # Gerar o PDF
        c = canvas.Canvas("lista_contatos.pdf")
        c.setFont("Helvetica-Bold", 24)
        c.drawString(220, 770, "Lista de Contatos")
        c.setFont("Helvetica", 14)
        y = 750
        for row in data:
            id, nome, telefone, idade = row  # Utiliza os índices corretos de acordo com a estrutura da tabela
            c.drawString(100, y, f'ID: {id}, Nome: {nome}, Telefone: {telefone}, Idade: {idade}')
            y -= 20
        data_hora_atual = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(100, 50, f"Gerado em: {data_hora_atual}")
        c.drawString(500, 50, f"Página 1")
        c.save()
        tk.messagebox.showinfo('Sucesso', 'PDF gerado com sucesso')
