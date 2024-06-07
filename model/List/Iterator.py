from abc import ABC, abstractmethod

class Iterator(ABC):
    @abstractmethod
    def has_next(self):
            ''' Retorna True se a iteração possuir mais elementos. '''
    @abstractmethod
    def get_next(self):
            ''' Retorna o próximo elemento na iteração. '''
    @abstractmethod
    def rewind(self):
            ''' Recomeça a iteração. Se a iteração não for
             vazia, retornará o primeiro elemento na iteração.'''

class TwoWayIterador(Iterator):
    @abstractmethod
    def has_previous(self):
             '''retorna true se o iterador tiver elementos para traz dele'''
    @abstractmethod
    def get_previous(self):
            '''retorna o elemeto diretamente atras da iteraçao'''
    @abstractmethod
    def full_forward(self):
            pass        