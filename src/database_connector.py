from src.global_var import *
from cryptography.fernet import Fernet
import psycopg2
import uuid

conn = psycopg2.connect(database=DATABASE,
                        host=HOST,
                        user=USER,
                        password=PASSWORD,
                        port=PORT)

class Encryptor():
    def __init__(self, key=KEY) -> None:
        self.key = key
        self.fern = Fernet(self.key) 
        self.encoding: str  = 'utf-8'
    def encrypt(self, data: str) -> str:
        return self.fern.encrypt(data.encode(self.encoding)).decode(self.encoding)
    def decrypt(self, data: str) -> str:
        return self.fern.decrypt(data.encode(self.encoding)).decode(self.encoding)
    
    
class Users():
    def __init__(self) -> None:
        self.table_name: str = "users"
        self.cursor = conn.cursor()
        self.encryptor = Encryptor()
        
    def add_new_user(self, mail: str, password: str, name: str, surname: str, type: str) -> None:
        token: str = str(uuid.uuid4())
        mail = mail.replace(" ",  "").upper()  
        password = password.replace(" ",  "")
        password = self.encryptor.encrypt(password)
        name = name.replace(" ",  "").upper()  
        surname = surname.replace(" ",  "").upper()  
        type = type.replace(" ",  "").upper()  
        
        self.cursor.execute(f'INSERT INTO {self.table_name} (name, surname, mail, password, type, token) \
            VALUES (\'{name}\', \'{surname}\', \'{mail}\', \'{password}\', \'{type}\', \'{token}\')')
        conn.commit()
        
    def select_data_varchar(self, ref_column: str, value: str) -> list:
        self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE {ref_column} = \'{value}\'')
        data: list = self.cursor.fetchall()
        
        print(data)
        return data
    
    def select_data_integer(self, ref_column: str, value: str) -> list:
        self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE {ref_column} = {value}')
        data: list = self.cursor.fetchall()
        
        return data
    
    def check_user(self, mail: str, password: str) -> str:
        mail = mail.upper()
        data: list = self.select_data_varchar("mail", mail)
        
        token: str = ""
        password_: str = ""
        name : str = ""
        surname: str = ""
        
        if len(data) != 0:
            name = data[0][2]
            surname = data[0][3] 
            password_ = data[0][4]
            token = data[0][6] 
            password_ = self.encryptor.decrypt(password_)
        else:
            token = "User not Found"
            return (token, surname, name)
        
        if password == password_:
            return (token, surname, name)
        else:
            return "Invalid password or username"
        
        return None
    
    def rollback(self) -> None:
        self.cursor.execute("ROLLBACK")
        conn.commit()
    
if __name__ == '__main__':
    user = Users()
    user.select_data_varchar('surname', 'crenna')
    user.rollback()