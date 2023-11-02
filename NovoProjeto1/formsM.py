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
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from contactos import BaseForm, ContactForm, GraphForm, PresentationForm
from Idades import AgeForm
from Login import LoginPage
import re

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x600')
        self.root.title("App Principal")
        self.root.configure(background="green")

        # Criação do menu
        self.menubar = tk.Menu(self.root)
        self.filemenu1 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu2 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu3 = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu2)
        self.menubar.add_command(label="Sair", command=self.exit_application)
        self.root.config(menu=self.menubar)

        # Criação dos formulários
        self.login_page = LoginPage(self.root, self)
        self.forms = [
            PresentationForm(self.root, self),  # Adicionar o Formulário de Apresentação
            ContactForm(self.root, self),  # Adicionar o Formulário de Contatos
            GraphForm(self.root, self),  # Adicionar o Formulário Gráfico
            AgeForm(self.root, self),  # Adicionar o Formulário de idades
        ]

        # Adicionar os formulários ao menu
        for i, form in enumerate(self.forms): self.filemenu2.add_command(label=f"Menu {i + 1}", command=form.show)

        # Manter uma referência ao frame atual
        self.current_frame = None

    # Começar com o Formulário 1 visível
    def show_main_app(self):  # é chamado quando a aplicação é iniciada e destroi
        self.login_page.frame.destroy()   # a página de login

        self.current_form = self.forms[0]
        self.current_form.show()

    def exit_application(self):  # método que que fecha a aplicação quando o botão sair
        self.root.destroy()   # for selecionado

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()  # inicia o loop principal da interface, permitindo que a aplicação
                     # responda aos eventos do utilizador