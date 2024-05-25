class Songs:
  def __init__(self, titulo, nome, apelido ,feat, album,ano, duracao):

      self.__titulo = titulo
      self.__nome = nome
      self.__apelido = apelido
      self.__feat = feat
      self.__album = album
      self.__ano = ano
      self.__duracao = duracao


  def get_titulo(self):
      return self.__titulo

  def set_titulo(self, novo_titulo):
      self.__titulo = novo_titulo

  def get_nome(self):
      return self.__nome

  def set_nome(self, novo_nome):
      self.__nome = novo_nome

  def get_apelido(self):
      return self.__apelido

  def set_apelido(self, novo_apelido):
      self.__apelido = novo_apelido

  def get_feat(self):
      return self.__feat

  def set_feat(self, novo_feat):
      self.__feat = novo_feat

  def get_album(self):
      return self.__album

  def set_album(self, novo_album):
      self.__album = novo_album

  def get_ano(self):
      return self.__ano

  def set_ano(self, novo_ano):
      self.__ano = novo_ano

  def get_duracao(self):
      return self.__duracao

  def set_duracao(self, novo_duracao):
      self.__duracao = novo_duracao