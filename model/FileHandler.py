from model.User import *
from model.Songs import *
from model.UserLinkedList import *
import json
import os
import datetime

class FileHandler:

    def save_data_to_json(self, users):
        data = {
            'users': []
        }

        for user in users.iterator():
            user_data = {
                'nome': user.get_nome(),
                'password': user.get_password(),
                'songs': []
            }

            songs = user.get_songs()
            for songs in songs.iterator():
                songs_data = {
                    'Name': songs.get_nome(),
                    'Artist': songs.get_artista(),
                    'feat.': songs.get_feat(),    
                    'Album': songs.get_album(),                
                    'Year': songs.get_ano(),
                    'Duration': songs.get_duracao(),
                }
                user_data['Songs'].append(songs_data)

            data['users'].append(user_data)

        with open("data.json", 'w') as file:
            json.dump(data, file)

    def read_data_from_json(self):
        user = UserLinkedList()
        if not os.path.exists("data.json"):
            with open("data.json", 'w') as file:
                # Cria um arquivo vazio se ele não existir
                json.dump({}, file)
                return UserLinkedList()
        else:
            with open("data.json", 'r') as file:
                data = json.load(file)

            for user_data in data['Users']:
                user = User(user_data['nome'], user_data['password'])

                songs_data = user_data['Songs']
                for songs_data in songs_data:
                    songs = Songs(songs_data['Name'], songs_data['Artist'], songs_data['feat.'],songs_data['Album'],songs_data['Year'],songs_data['Duration'])
                    user.set_songs(songs)

                user.insert_last(user)

            return user

    def clean_file(self):
        with open("data.json", 'w') as file:
            file.write("")
