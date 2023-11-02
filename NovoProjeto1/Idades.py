import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AgeForm:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.frame = tk.Frame(self.master, background="green")
        self.label = tk.Label(self.frame, text="Gráfico Relação de Idades", background="green")

        # Título de apresentação centrado no topo
        self.label.configure(font=("Helvetica", 25, "bold"), foreground="brown", bg="light grey")
        self.label.pack(pady=20)

        self.canvas = None

    def show(self):
        # Esconder o formulário atualmente visível
        self.controller.current_form.hide()

        # Mostrar este formulário
        self.frame.pack(fill='both', expand=True)
        self.label.pack()

        # Atualizar o formulário atualmente visível
        self.controller.current_form = self

        # Criar o gráfico de distribuição de idades
        self.create_age_distribution_plot()

    def hide(self):
        self.frame.pack_forget() # oculta o formulário da interface

    def create_age_distribution_plot(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()

        # Consultar as idades dos contatos
        cursor.execute("SELECT idade FROM contacts;")
        ages = [row[0] for row in cursor.fetchall()]

        # Fechar a conexão com o banco de dados
        conn.close()

        # Definir os intervalos de idade
        age_intervals = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        # Conta quantos contatos estão em cada intervalo
        age_counts = [0] * (len(age_intervals) - 1)
        for age in ages:
            for i in range(len(age_intervals) - 1):
                if age_intervals[i] <= age < age_intervals[i + 1]:
                    age_counts[i] += 1

        # Verifica se o gráfico já existe
        if self.canvas:
            self.canvas.get_tk_widget().destroy()  # Destruir o widget antigo

        # Cria o gráfico de barras
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar([f"{age_intervals[i]}-{age_intervals[i + 1]}" for i in range(len(age_intervals) - 1)], age_counts, color='purple')
        ax.set_xlabel('Intervalo de Idades', fontdict={'fontsize': 11, 'color': 'brown', 'weight': 'bold'})
        ax.set_ylabel('Número de Pessoas', fontdict={'fontsize': 11, 'color': 'brown', 'weight': 'bold'})
        ax.set_title('Distribuição de Idades', fontdict={'fontsize': 11, 'color': 'brown', 'weight': 'bold'})
        plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para melhor legibilidade

        # Menos espaço vertical em branco
        plt.subplots_adjust(top=0.4, bottom=0.3)

        # Incorporar o gráfico na janela tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Mostrar o gráfico
        plt.tight_layout()
