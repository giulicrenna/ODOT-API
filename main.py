from fastapi import FastAPI
from src.database_connector import Users

api = FastAPI()

@api.get("/")
async def root() -> None:
    return {"Status" : "Ok"}

@api.post("/register")
async def register(mail: str,
                   password: str,
                   type: str,
                   name: str,
                   surname: str) -> dict:
    try:
        user = Users()
        user.add_new_user(mail, password, name, surname, type)
        return {"Status" : "User register succesfully"}
    except Exception as e:
        return {"Exception": str(e)}
        
@api.get("/login")
async def login(mail: str,
                password: str) -> dict:
    user = Users()
    token: str = user.check_user(mail, password)
    
    return {"status" : token}