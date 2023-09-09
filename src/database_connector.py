from src.global_var import *
from cryptography.fernet import Fernet
import psycopg2
import uuid


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
        self.conn = psycopg2.connect(database=DATABASE,
                        host=HOST,
                        user=USER,
                        password=PASSWORD,
                        port=PORT)
        self.table_name: str = "users"
        self.cursor = self.conn.cursor()
        self.encryptor = Encryptor()
        
    def add_new_user(self, mail: str, password: str, name: str, surname: str, type: str) -> str:
        try:
            token: str = str(uuid.uuid4())
            mail = mail.replace(" ",  "").upper()  
            password = password.replace(" ",  "")
            password = self.encryptor.encrypt(password)
            name = name.replace(" ",  "").upper()  
            surname = surname.replace(" ",  "").upper()  
            type = type.replace(" ",  "").upper()  

            self.cursor.execute(f'INSERT INTO {self.table_name} (name, surname, mail, password, type, token) \
                VALUES (\'{name}\', \'{surname}\', \'{mail}\', \'{password}\', \'{type}\', \'{token}\')')
            self.conn.commit()
            return "ok"
        except psycopg2.InterfaceError:
            return "bad"
        
    def select_data_varchar(self, ref_column: str, value: str) -> list:
        try:
            self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE {ref_column} = \'{value}\'')
            data: list = self.cursor.fetchall()
            
            print(data)
            return data
        except psycopg2.InterfaceError as e:
            return [e]
        
    def select_data_integer(self, ref_column: str, value: str) -> list:
        try:
            self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE {ref_column} = {value}')
            data: list = self.cursor.fetchall()

            return data
        except:
            return []
        
    def check_user(self, mail: str, password: str) -> str:
        try:
            mail = mail.upper()
            data: list = self.select_data_varchar("mail", mail)
            
            token: str = ""
            password_: str = ""
            name : str = ""
            surname: str = ""
            type: str = ""
            status: str = "bad"
            
            if len(data) != 0:
                password_ = data[0][4]
                password_ = self.encryptor.decrypt(password_)
                print(password)
                
                if password == password_ and len(password) > 1:
                    name = data[0][2]
                    surname = data[0][3] 
                    token = data[0][6] 
                    type = data[0][5]
                    status = "ok"
                else:
                    status = "Invalid password or username" 
            else:
                status = "User not Found"
            
            
            return (status, token, surname, name, type)
        except Exception as e:
            return {'Exception': e}
            
    def rollback(self) -> None:
        self.cursor.execute("ROLLBACK")
        self.conn.commit()
    
if __name__ == '__main__':
    user = Users()
    user.select_data_varchar('surname', 'crenna')
    user.rollback()