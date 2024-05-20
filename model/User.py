class User:
    def __init__(self, nome, password):
        self.__nome = nome
        self.__password = password

    def get_nome(self):
        return self.__nome
        
    def set_nome(self, novo_nome):
        self.__nome = novo_nome
        
    def get_password(self):
        return self.__password
        
    def set_password(self, nova_password):
        self.__password = nova_password
