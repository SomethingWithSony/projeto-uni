import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
# from PIL import Image, ImageTk
from model.User import *
from model.UserLinkedList import *
from model.Songs import *
import requests
from model.Database import DataBase
from io import BytesIO
import webbrowser

import json
from requests import post, get
import base64
import os
from dotenv import load_dotenv

class View:
    def __init__(self, master): 
            self.master = master
            self.user = UserLinkedList() #Criação da lista de clientes
            self.database = DataBase()
            self.load_users()

            self.user_login = None

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
            self.login_button = tk.Button(self.frame, text="Login", font=('Arial', 14),fg='white', bg='#323940',command=self.login)
            self.login_button.pack(pady=10, ipadx=20, ipady=5)

            self.registo_button = tk.Button(self.frame, text="Registo", font=('Arial', 14), fg='white', bg='#323940',command=self.registar,)
            self.registo_button.pack(pady=10, ipadx=20, ipady=5)

    def registar(self,):
        self.frame.destroy
        self.tela= tk.Toplevel(self.master)
        self.tela.title("Registo")
        self.tela.configure(background="#323940")

        frame = tk.Frame(self.tela, bg= "#323940")
        frame.pack()

        #Sem a 2 imagem ele nao apaga a inicial

        #self.logo = tk.PhotoImage(file='User.png')
        #self.logo = self.logo.subsample(2)
        #self.logo_label = tk.Label(frame, image=self.logo, bg='#323940')
        #self.logo_label.place(relx=1.0,)
        #self.logo_label.pack()

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
            posicao = self.user.find_username(username)
            if posicao != -1: # ver se o nome ja ta registado
                messagebox.showerror("Insucesso"," Este cliente já está registado")     #messagebox manda mensagem para o user
            else:
                if password != c_pass:
                        messagebox.showerror("Erro", "As senhas não coincidem")
                else:
                    self.tela.destroy()
                    self.user.insert_last(User(username, password))
                    messagebox.showinfo("Sucesso", "Cliente registado com sucesso")

    def load_users(self):
        for nome, password in self.database.fetch_user():
            self.users.insert_last(User(nome, password))

    def registar_users(self, nome, password, password_repetida):
        if password != password_repetida:
            messagebox.showerror("Erro", "As passwords não coincidem")
            return

        if self.database.insert_user(nome, password):
            self.user.insert_last(User(nome, password))
            messagebox.showinfo("Sucesso", "User registado com sucesso")
        else:
            messagebox.showerror("Erro", "Este nome de user já está em uso")

    def login(self):
        token = self.get_token()

        # self.search_artist(token, "kendrik")
        username = self.nome_entry.get()
        password = self.password_entry.get()
        posicao = self.user.find_username(username)
        if posicao == -1:
            messagebox.showerror("Erro de Login", "Username não encontrado")
        else:
            user = self.user.get(posicao)
            if user.get_password() == password:
                self.user_login = user
                messagebox.showinfo("Login", "Login efetuado com sucesso")
                self.exibir_songs()
            else:
                messagebox.showerror("Erro de Login", "Senha incorreta")

    def get_token(self):
        load_dotenv()
        
        client_id = os.getenv("CLIENT_ID")
        client_secret  = os.getenv("CLIENT_SECRET")
        
        auth_string = client_id + ":" + client_secret 
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        url = "https://accounts.spotify.com/api/token"
        # "Basic " tem que ter um whitespace se não da erro
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    def get_header(self, token):
        return {"Authorization": "Bearer " + token}

    def search_artist(self,token, name):
        url = f'https://api.spotify.com/v1/search'
        headers = self.get_header(token)
        query = f"?q={name}&type=artist&limit=1"
        
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)
        print(json_result)

    def exibir_songs(self):
        
        url = f'https://api.spotify.com/v1/search'
        
        


        janela_songs = tk.Toplevel(self.master)
        janela_songs.title("Playlist")
        janela_songs.configure(background="#323940", width=100000, height=100000)  
        # frames para separar as sessoes
        self.frame_barra = tk.Frame(self.master, bg="#000000", height=52)
        self.frame_barra.pack(side="top", fill="X")

        largura_janela, altura_janela = self.master.winfo_sreenwidth(), self.master.winfo_screenheight()
        largura_frame_esq = largura_janela * 0.20
        largura_frame_drt = largura_janela - largura_frame_esq

        self.frame_esq = tk.Frame(self.master , bg ="#404040", width=largura_frame_esq, height=altura_janela)
        self.frame_esq.pack(side="left", fill="y")

        self.frame_drt = tk.Frame(self.master, bg="303030", width=largura_frame_drt, height=altura_janela)
        self.frame_drt.pack(side="left", padx=(10,0), pady=5)
        #nome da app do canto superior esq
        self.label_app = tk.Label(self.frame_barra, text="Spotmuzic", bg="white", font=("Arial", 18, "bold"))
        self.label_app.pack(side="left", padx=(10,0), pady=5)
        #criar a search bar e colocala no meio da label 
        self.searchbar= tk.Entry(self.frame_barra, bg="404040", fg="white", font=("Arial",14), width=40, borderwidth=0, highlightthickness=0)
        self.searchbar.place(relx=0.5, rely=0.5, anchor="center")

        user_label = tk.Label(janela_songs, text=f"User: {self.user_login.get_nome()}", font=("Arial", 14), bg="#323940", anchor='e')
        user_label.pack(fill='x', padx=10)  # Alinha à direita e preenche horizontalmente

        scroll = tk.Scrollbar(janela_songs, orient='vertical')
        canvas = tk.Canvas(janela_songs, yscrollcommand=scroll.set)
        scroll.config(command=canvas.yview)
        scroll.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas_frame = tk.Frame(canvas, background="#ffe76c")
        canvas.create_window((0,0), window=canvas_frame, anchor='nw')

