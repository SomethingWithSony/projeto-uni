import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from model.User import *
from model.UserLinkedList import *

import requests
from model.DataBase import DataBase
from io import BytesIO

from dotenv import load_dotenv
import pygame
import time
import urllib.request
import tempfile

import json
from requests import post, get
import base64
import os



class View:
    def __init__(self, master): 
            self.playlist_selecionada = ""
            self.playlists = []     
            self.master = master
            self.user = UserLinkedList() 
            self.database = DataBase()
            self.load_users()


            self.user_login = None
            
            
            self.token = self.get_token()
            self.estado_reproducao = "parado"
            pygame.mixer.init()
            
            self.master.resizable(False, False)
            self.frame = tk.Frame(self.master, width=100000, height=100000, bg='#323940')
            self.frame.pack()

            self.logo = tk.PhotoImage(file='Logo.png')
            self.logo = self.logo.subsample(2)
            self.logo_label = tk.Label(self.frame, image=self.logo, bg='#323940')
            self.logo_label.place(relx=1.0, anchor='ne')
            self.logo_label.pack()

            
            self.username_label = tk.Label(self.frame, text="Username:", font=('Arial', 14), bg='#323940')
            self.username_label.pack()
            self.username_entry = tk.Entry(self.frame, font=('Arial', 14))
            self.username_entry.pack(pady=5)

            
            self.password_label = tk.Label(self.frame, text="Password:", font=('Arial', 14), bg='#323940')
            self.password_label.pack()
            self.password_entry = tk.Entry(self.frame, show="*", font=('Arial', 14))
            self.password_entry.pack(pady=5)

            
            self.login_button = tk.Button(self.frame, text="Login", font=('Arial', 14), bg='#323940',command=self.login)
            self.login_button.pack(pady=10, ipadx=20, ipady=5)

            self.registo_button = tk.Button(self.frame, text="Registo", font=('Arial', 14), bg='#323940',command=self.registar,)
            self.registo_button.pack(pady=10, ipadx=20, ipady=5)
            



    def registar(self,):
        self.frame.destroy
        self.tela= tk.Toplevel(self.master)
        self.tela.title("Registo")
        self.tela.configure(background="#323940")

        frame = tk.Frame(self.tela, bg= "#323940")
        frame.pack()

        self.main_logo = tk.PhotoImage(file='User.png')
        self.main_logo = self.main_logo.subsample(5)
        self.main_logo_label = tk.Label(frame, image=self.main_logo, bg='#323940')
        self.main_logo_label.place(relx=1.0,)
        self.main_logo_label.pack()

        username_label = tk.Label(frame, text="Username", font=('Arial', 14), bg='#323940')
        username_label.pack()
        username_entry = tk.Entry(frame, font=('Arial', 14))
        username_entry.pack(pady=5)

        password_label = tk.Label(frame, text="Password:", font=('Arial', 14), bg='#323940')
        password_label.pack()
        password_entry = tk.Entry(frame, show="*", font=('Arial', 14))
        password_entry.pack(pady=5)

        c_pass_label = tk.Label(frame,text="Comfirmar Password", font=('Arial', 14), bg='#323940')
        c_pass_label.pack()
        c_pass_entry = tk.Entry(frame, show="*", font=('Arial', 14))
        c_pass_entry.pack(pady=5)


        self.registar_button = tk.Button(frame, text="Registo", font=('Arial', 14),bg='#323940',command=lambda:self.registar_user(username_entry.get(), password_entry.get(), c_pass_entry.get()))
        self.registar_button.pack(pady=10, ipadx=20, ipady=5)

        self.voltar_button = tk.Button(frame, text="Voltar",font=("Arial", 14), bg="#323940",command=self.tela.destroy,)
        self.voltar_button.pack(pady= 10, ipadx=20, ipady=5)



    def registar_user(self,username , password, c_pass):
        if username and password:
            posicao = self.user.find_username(username)
            if posicao != -1: # ver se o username ja ta registado
                messagebox.showerror("Insucesso"," Este cliente já está registado")     
            else:
                if password != c_pass:
                        messagebox.showerror("Erro", "As senhas não coincidem")
                else:
                    self.tela.destroy()
                    if self.database.insert_user(username, password):
                        self.user.insert_last(User(username, password))
                        messagebox.showinfo("Sucesso", "User registado com sucesso")
                    else:
                        messagebox.showerror("Erro", "Este username de user já está em uso")




    def load_users(self):
        for username, password in self.database.fetch_user():
            self.user.insert_last(User(username, password))


    def login(self):
        username = self.username_entry.get()
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
                self.frame.destroy
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
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    def obter_header(self):
        return {"Authorization": "Bearer " + self.token}

    def procurar_e_exibir_faixas(self):
        nome_faixa = self.searchbar.get()
        faixas = self.procurar_faixa(nome_faixa)
        self.listbox.delete(0, tk.END)
        for faixa in faixas:
            self.listbox.insert(tk.END, (faixa['name'], faixa['artists'][0]['name'], faixa['id']))
        
    def adicionar_faixa_a_lista(self):
        faixa_selecionada = self.listbox.curselection()
        if faixa_selecionada:
            faixa = self.listbox.get(faixa_selecionada)
            self.listbox_queue.insert(tk.END, faixa)
            
            if self.playlist_selecionada:
                self.adicionar_faixa_a_playlist(self.playlist_selecionada, faixa)
            
            messagebox.showinfo("Informação", "Faixa adicionada à fila.")


    

    
    def remover_faixa_da_lista(self):
        faixa_selecionada = self.listbox_queue.curselection()
        if faixa_selecionada:
            faixa = self.listbox_queue.get(faixa_selecionada)
            self.listbox_queue.delete(faixa_selecionada)
            self.remover_faixa_da_playlist(self.playlist_selecionada, faixa)
            
            
            if pygame.mixer.music.get_busy() and faixa in self.listbox_queue.get(0, tk.END):
                pygame.mixer.music.stop()
                self.estado_reproducao = "parado"
                self.botao_reproduzir.config(text="Reproduzir")
                self.atualizar_barra_progresso()
            messagebox.showinfo("Informação", "Faixa removida da fila.")
            
    def adicionar_faixa_a_playlist(self, playlist_nome, faixa):
        # Lógica para adicionar a faixa à playlist especificada
        for playlist in self.playlists:
            if playlist['nome'] == playlist_nome:
                playlist['faixas'].append(faixa)
                break

    def remover_faixa_da_playlist(self, playlist_nome, faixa):
        # Lógica para remover a faixa da playlist especificada
        for playlist in self.playlists:
            if playlist['nome'] == playlist_nome:
                if faixa in playlist['faixas']:
                    playlist['faixas'].remove(faixa)
                break
    
    def carregar_playlist_selecionada(self, event):
        # Obter o índice da playlist selecionada
        playlist_selecionada = self.listbox_playlists.curselection()
        
        # Verificar se uma playlist está selecionada
        if playlist_selecionada:
            # Obter o nome da playlist selecionada
            playlist_nome = self.listbox_playlists.get(playlist_selecionada)
            
            # Verificar se a playlist selecionada é diferente da anterior
            if playlist_nome != self.playlist_selecionada:
                # Limpar a listbox_queue
                self.listbox_queue.delete(0, tk.END)
                
                # Atualizar a variável self.playlist_selecionada
                self.playlist_selecionada = playlist_nome
                
                # Encontrar a playlist correspondente
                for playlist in self.playlists:
                    if playlist['nome'] == playlist_nome:
                        # Adicionar as faixas da playlist à listbox_queue
                        for faixa in playlist['faixas']:
                            self.listbox_queue.insert(tk.END, faixa)
                        break
                        
                
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    self.estado_reproducao = "parado"
                    self.botao_reproduzir.config(text="Reproduzir")
                    self.atualizar_barra_progresso()



    def exibir_songs(self):

        janela_songs = tk.Toplevel(self.master)
        janela_songs.title("Playlist")
        janela_songs.configure(background="#323940", width=100000, height=100000)
        janela_songs.resizable(False, False)

        frame_barra = tk.Frame(janela_songs, bg="#323940", height=52)
        frame_barra.pack(side="top", fill='x')

        user_label = tk.Label(frame_barra, text=f"User: {self.user_login.get_username()}", font=("Arial", 14), bg="#323940", anchor='e')
        user_label.pack(fill='x', padx=10)

        largura_janela, altura_janela = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        largura_frame_esq = largura_janela * 0.50
        largura_frame_drt = largura_janela - largura_frame_esq

        frame_esq = tk.Frame(janela_songs, bg="#252526", width=largura_frame_esq, height=altura_janela)
        frame_esq.pack(side="left", fill="y")

        frame_drt = tk.Frame(janela_songs, bg="#323940", width=largura_frame_drt, height=altura_janela)
        frame_drt.pack(side="right", fill="both", expand=True)

        label_app = tk.Label(frame_barra, text="Spotmuzic", bg="#323940", anchor='n', font=("Arial", 30, "bold"),)
        label_app.pack(side="left", padx=(10, 0))

        self.searchbar = tk.Entry(frame_esq, bg="white", fg="black", font=("Arial", 14), width=30, borderwidth=0, highlightthickness=0)
        self.searchbar.place(relx=0.5, rely=0.5, anchor="center")

        search_button = tk.Button(frame_esq, text="Pesquisar", bg="#4CAF50",  font=("Arial", 14), borderwidth=0, highlightthickness=0, command=self.procurar_e_exibir_faixas)
        search_button.place(relx=0.5, rely=0.4, anchor="center")
        self.searchbar.place(relx=0.5, rely=0.3, anchor="center")

        self.searchbar.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="n")
        search_button.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="n")

        self.listbox = tk.Listbox(frame_esq, bg="white", fg="black", font=("Arial", 14), borderwidth=0, highlightthickness=0)
        self.listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        btn_adicionar = tk.Button(frame_esq, text="Adicionar", bg="#4CAF50",  font=("Arial", 14), borderwidth=0, highlightthickness=0, width=25, command=self.adicionar_faixa_a_lista)
        btn_adicionar.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        btn_remover = tk.Button(frame_esq, text="Remover", bg="#FF5733",  font=("Arial", 14), borderwidth=0, highlightthickness=0, width=25, command=self.remover_faixa_da_lista)
        btn_remover.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        label_playlists = tk.Label(frame_drt, text="Playlists", bg="#323940", font=("Arial", 16), borderwidth=0, highlightthickness=0)
        label_playlists.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        criar_playlist_button = tk.Button(frame_drt, text="Criar Playlist", bg="#4CAF50",  font=("Arial", 14), borderwidth=0, highlightthickness=0, command=self.criar_playlist)
        criar_playlist_button.place(relx=0.5, rely=0.4, anchor="center")
        criar_playlist_button.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="n")

        apagar_playlist_button = tk.Button(frame_drt, text="Apagar Playlist", bg="#FF5733",  font=("Arial", 14), borderwidth=0, highlightthickness=0, command=self.remover_playlist)
        apagar_playlist_button.place(relx=0.5, rely=0.4, anchor="center")
        apagar_playlist_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="n")

        # Listbox de queue
        self.listbox_queue = tk.Listbox(frame_drt, bg="white", fg="black", font=("Arial", 14), borderwidth=0, highlightthickness=0)
        self.listbox_queue.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

        # Listbox de playlists
        self.listbox_playlists = tk.Listbox(frame_drt, bg="white", fg="black", font=("Arial", 14), borderwidth=0, highlightthickness=0)
        self.listbox_playlists.grid(row=1, column=2, padx=10, pady=10, sticky="nw")
        self.listbox_playlists.bind("<<ListboxSelect>>", self.carregar_playlist_selecionada)
        

        botao_anterior = tk.Button(frame_drt, text="Anterior", width=2, command=self.faixa_anterior)
        botao_anterior.grid(row=2, column=0, padx=5, sticky="nsew")

        self.botao_reproduzir = tk.Button(frame_drt, text="Reproduzir", width=2, command=self.alternar_reproducao_pausa)
        self.botao_reproduzir.grid(row=2, column=1, padx=5, sticky="nsew")

        botao_proxima = tk.Button(frame_drt, text="Próxima", command=self.proxima_faixa)
        botao_proxima.grid(row=2, column=2, padx=5, sticky="nsew")

        self.variavel_progresso = tk.DoubleVar()
        barra_progresso = ttk.Progressbar(frame_drt, variable=self.variavel_progresso, maximum=100)
        barra_progresso.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.etiqueta_tempo = tk.Label(frame_drt, text="00:00 / 00:00")
        self.etiqueta_tempo.grid(row=3, column=2, sticky="w")


    

    def adicionar_playlist(self, nome_playlist):
        self.playlists.append({ "nome": nome_playlist, "faixas": [] })
        
    def criar_playlist(self):
        nome_playlist = simpledialog.askstring("Criar Playlist", "Digite o nome da playlist:")
    
        if nome_playlist:
            for playlist in self.playlists:
                if playlist["nome"] == nome_playlist:
                    messagebox.showinfo("Erro", "Uma playlist com este nome já existe")
                    return 
                
           
            self.adicionar_playlist(nome_playlist)
            self.listbox_playlists.insert(tk.END,nome_playlist)
            messagebox.showinfo("Sucesso", "Playlist Criada")
                        
    def remover_playlist(self):
        indice_selecionado = self.listbox_playlists.curselection()
        if not indice_selecionado:
            messagebox.showinfo("Erro", "Nenhuma playlist selecionada")
            return
        
        indice_selecionado = indice_selecionado[0]
        nome_selecionado = self.listbox_playlists.get(indice_selecionado)

        # Remove from the internal list of playlists
        self.playlists = [playlist for playlist in self.playlists if playlist["nome"] != nome_selecionado]

        # Remove from the Listbox
        self.listbox_playlists.delete(indice_selecionado)

        messagebox.showinfo("Sucesso", f"Playlist '{nome_selecionado}' removida")
    
    


    if 'temp_file' in globals() and temp_file:
        temp_file.close()
        os.unlink(temp_file.name)
        
    def pausar_preview(self):
        pygame.mixer.music.pause()
        self.estado_reproducao = "pausado"
        self.botao_reproduzir.config(text="Continuar")

    def continuar_preview(self):
        pygame.mixer.music.unpause()
        self.estado_reproducao = "reproduzindo"
        self.botao_reproduzir.config(text="Pausar")

    def alternar_reproducao_pausa(self):
        if self.estado_reproducao == "reproduzindo":
            self.pausar_preview()
        elif self.estado_reproducao == "pausado":
            self.continuar_preview()
        elif self.estado_reproducao == "init":
            pygame.mixer.music.play()
            self.estado_reproducao = "reproduzindo"
            self.atualizar_barra_progresso()
            self.botao_reproduzir.config(text="Pausar")
        else:
            faixa_selecionada = self.listbox_queue.curselection()
            if faixa_selecionada:
                faixa = self.listbox_queue.get(faixa_selecionada)
                faixa_id = faixa[2]
                preview_url = self.obter_preview_faixa(faixa_id)
                self.tocar_preview(preview_url)
                pygame.mixer.music.play()
                self.estado_reproducao = "reproduzindo"
                self.atualizar_barra_progresso()
                self.botao_reproduzir.config(text="Pausar")

    def proxima_faixa(self):
        faixa_selecionada = self.listbox_queue.curselection()
        if faixa_selecionada:
            proximo_indice = (faixa_selecionada[0] + 1) % self.listbox_queue.size()
            self.listbox_queue.select_clear(0, tk.END)
            self.listbox_queue.select_set(proximo_indice)
            self.listbox_queue.event_generate("<<ListboxSelect>>")
            faixa = self.listbox_queue.get(proximo_indice)
            faixa_id = faixa[2]
            preview_url = self.obter_preview_faixa(faixa_id)
            self.tocar_preview(preview_url)
            pygame.mixer.music.play()
            self.estado_reproducao = "reproduzindo"
            self.atualizar_barra_progresso()
            self.botao_reproduzir.config(text="Pausar")

    def faixa_anterior(self):
        faixa_selecionada = self.listbox_queue.curselection()
        if faixa_selecionada:
            indice_anterior = (faixa_selecionada[0] - 1) % self.listbox_queue.size()
            self.listbox_queue.select_clear(0, tk.END)
            self.listbox_queue.select_set(indice_anterior)
            self.listbox_queue.event_generate("<<ListboxSelect>>")
            faixa = self.listbox_queue.get(indice_anterior)
            faixa_id = faixa[2]
            preview_url = self.obter_preview_faixa(faixa_id)
            self.tocar_preview(preview_url)
            pygame.mixer.music.play()
            self.estado_reproducao = "reproduzindo"
            self.atualizar_barra_progresso()
            self.botao_reproduzir.config(text="Pausar")

    def verificar_estado_reproducao(self):
        if self.estado_reproducao == "reproduzindo" and not pygame.mixer.music.get_busy():
            self.estado_reproducao = "parado"
            self.botao_reproduzir.config(text="Reproduzir")
            self.proxima_faixa()
        self.master.after(1000, self.verificar_estado_reproducao)

    def atualizar_barra_progresso(self):
        if self.estado_reproducao == "reproduzindo":
            tempo_atual = pygame.mixer.music.get_pos() / 1000
            self.variavel_progresso.set(tempo_atual / duracao_faixa * 100)
            self.etiqueta_tempo.config(text=f"{self.formatar_tempo(tempo_atual)} / {self.formatar_tempo(duracao_faixa)}")
        if self.estado_reproducao != "parado":
            self.master.after(1000, self.atualizar_barra_progresso)
            

    def formatar_tempo(self,segundos):
        mins, segs = divmod(segundos, 60)
        return f"{int(mins):02}:{int(segs):02}"

    def procurar(self,event):
        if self.estado_reproducao in ["reproduzindo", "pausado"]:
            x = event.x
            largura_barra_progresso = self.barra_progresso.winfo_width()
            novo_tempo = (x / largura_barra_progresso) * duracao_faixa
            pygame.mixer.music.play(start=novo_tempo)
            if self.estado_reproducao == "pausado":
                pygame.mixer.music.pause()

        

    def procurar_faixa(self, nome):
        url = f'https://api.spotify.com/v1/search'
        headers = self.obter_header()
        query = f"?q={nome}&type=track&limit=10"
        query_url = url + query
        resultado = get(query_url, headers=headers)
        resultado_json = json.loads(resultado.content)
        if 'tracks' in resultado_json and 'items' in resultado_json['tracks'] and resultado_json['tracks']['items']:
            faixas = resultado_json['tracks']['items']
            return faixas
        else:
            messagebox.showerror("Erro", "Nenhuma faixa encontrada com este nome.")
            return []

    def obter_preview_faixa(self, faixa_id):
        url = f"https://api.spotify.com/v1/tracks/{faixa_id}"
        headers = self.obter_header()
        resultado = get(url, headers=headers)
        resultado_json = json.loads(resultado.content)
        preview_url = resultado_json['preview_url']
        return preview_url

    def tocar_preview(self, preview_url):
        global temp_file, duracao_faixa
        if preview_url:
            try:
                diretorio_temporario = os.path.join(os.getcwd(), "musicas")
                if not os.path.exists(diretorio_temporario):
                    os.makedirs(diretorio_temporario)

                temp_file = tempfile.NamedTemporaryFile(delete=False, dir=diretorio_temporario, suffix=".mp3")
                with urllib.request.urlopen(preview_url) as response:
                    temp_file.write(response.read())
                temp_file.close()

                pygame.mixer.music.load(temp_file.name)
                duracao_faixa = pygame.mixer.Sound(temp_file.name).get_length()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao tentar tocar a faixa: {e}")
        else:
            messagebox.showinfo("Informação", "Não há preview disponível para esta faixa.")



    
    
