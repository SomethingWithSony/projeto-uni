import tkinter as tk
from tkinter import messagebox
from model.User import *
from model.UserLinkedList import *
class View:
    def __init__(self, master): 
            self.master = master
            self.clientes = UserLinkedList() #Criação da lista de clientes

            #Frame
            self.master.resizable(False, False)
            self.frame = tk.Frame(self.master, width=100000, height=100000, bg='#323940')
            self.frame.pack()

            self.logo = tk.PhotoImage(file='Logo.png')
            self.logo = self.logo.subsample(2)
            self.logo_label = tk.Label(self.frame, image=self.logo, bg='#323940')
            self.logo_label.place(relx=1.0, anchor='ne')
            self.logo_label.pack()

            #Label + Entry para username
            self.nome_label = tk.Label(self.frame, text="Nome:", font=('Arial', 14), bg='#323940',fg='white')
            self.nome_label.pack()
            self.nome_entry = tk.Entry(self.frame, font=('Arial', 14))
            self.nome_entry.pack(pady=5)

            #Label + Entry para password
            self.password_label = tk.Label(self.frame, text="Password:", font=('Arial', 14), bg='#323940',fg='white')
            self.password_label.pack()
            self.password_entry = tk.Entry(self.frame, show="*", font=('Arial', 14))
            self.password_entry.pack(pady=5)

            #Botões de Login + registo
            self.login_button = tk.Button(self.frame, text="Login", font=('Arial', 14),fg='white', bg='#323940',)
            self.login_button.pack(pady=10, ipadx=20, ipady=5)

            self.registo_button = tk.Button(self.frame, text="Registo", font=('Arial', 14), fg='white', bg='#323940',command=self.registar,)
            self.registo_button.pack(pady=10, ipadx=20, ipady=5)


    def registar(self):
        self.tela= tk.Toplevel(self.master)
        self.tela.title("Registo")
        self.tela.configure(background="#323940")

        frame = tk.Frame(self.tela, bg= "#323940")
        frame.pack()

        self.logo = tk.PhotoImage(file='User.png')
        self.logo = self.logo.subsample(2)
        self.logo_label = tk.Label(frame, image=self.logo, bg='#323940')
        self.logo_label.place(relx=1.0, anchor='ne')
        self.logo_label.pack()

        username_label = tk.Label(frame, text="Username", font=('Arial', 14),fg='white', bg='#323940')
        username_label.pack()
        username_entry = tk.Entry(frame, font=('Arial', 14))
        username_entry.pack(pady=5)

        password_label = tk.Label(frame, text="Password:", font=('Arial', 14),fg='white', bg='#323940')
        password_label.pack()
        password_entry = tk.Entry(frame, show="*", font=('Arial', 14))
        password_entry.pack(pady=5)

        c_pass_label = tk.Label(frame,text="Comfirmar Password", font=('Arial', 14),fg='white', bg='#323940')
        c_pass_label.pack()
        c_pass_entry = tk.Entry(frame, show="*", font=('Arial', 14))
        c_pass_entry.pack(pady=5)


        self.registar_button = tk.Button(frame, text="Registo", font=('Arial', 14),fg='white',bg='#323940',command=lambda:self.registar_user(username_entry.get(), password_entry.get(), c_pass_entry.get()))
        self.registar_button.pack(pady=10, ipadx=20, ipady=5)

        self.voltar_button = tk.Button(frame, text="Voltar",font=("Arial", 14),fg="white", bg="#323940",command=self.tela.destroy,)
        self.voltar_button.pack(pady= 10, ipadx=20, ipady=5)

    def registar_user(self,username , password, c_pass):
        if username and password:
            posicao = self.clientes.find_username(username)
            if posicao != -1: # ver se o nome ja ta registado
                messagebox.showerror("Insucesso"," Este cliente já está registado")     #messagebox manda mensagem para o user
            else:
                if password != c_pass:
                        messagebox.showerror("Erro", "As senhas não coincidem")
                else:
                    self.tela.destroy
                    self.clientes.insert_last(User(username, password))
                    messagebox.showinfo("Sucesso", "Cliente registado com sucesso")
                    self.tela.destroy





    def login():
         pass