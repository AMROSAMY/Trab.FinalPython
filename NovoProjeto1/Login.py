import tkinter as tk
from tkinter import messagebox


class LoginPage:
    def __init__(self, root, controller):  # método construtor da classe e aceita
        self.root = root                   # dois parametros root e controller
        self.controller = controller
        
        # Definir tamanho personalizado para o frame
        self.frame = tk.Frame(self.root, width=250, height=175)
        self.frame.pack_propagate(0)

        self.label = tk.Label(self.frame, text="Página de Login", font=("Helvetica", 11, "bold"), foreground="brown")
        self.label.pack()

        self.username_label = tk.Label(self.frame, text="Username:", font=("Helvetica", 10, "bold"), foreground="brown")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.frame, text="Password:", font=("Helvetica", 10, "bold"), foreground="brown")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.frame, text="Login", command=self.login, font=("Helvetica", 10, "bold"), foreground="brown")
        self.login_button.pack()

        # Centralizar o frame na janela
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def login(self):
        # Implementação de autenticação
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin":
            self.controller.show_main_app()
        else:
            messagebox.showerror("Erro", "username ou password inválida.")
