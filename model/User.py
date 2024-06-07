
class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password


    def get_username(self):
        return self.__username

    def set_username(self, novo_username):
        self.__username = novo_username

    def get_password(self):
        return self.__password

    def set_password(self, nova_password):
        self.__password = nova_password

    def get_songs(self):
        return self.__songs

    def set_songs(self, nova_song):
        self.__songs.insert_last(nova_song) 