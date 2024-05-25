import sqlite3

class DataBase:
    def __init__(self, db_name='app.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self): #Criação da tabela cliente
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                nome TEXT PRIMARY KEY,
                password TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    def insert_user(self, nome, password): #Inserir um novo cliente na  tabela
        try:
            self.cursor.execute('INSERT INTO User (nome, password) VALUES (?, ?)', (nome, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_user(self, nome):  #Eliminar um cliente
        self.cursor.execute('DELETE FROM User WHERE nome = ?', (nome,))
        self.conn.commit()

    def fetch_user(self): 
        self.cursor.execute('SELECT nome, password FROM user')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
