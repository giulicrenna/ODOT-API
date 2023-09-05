from fastapi import FastAPI
from src.database_connector import Users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

api = FastAPI()
user = Users()

origins: list = ['190.2.104.63:8100', '190.2.104.63', '0.0.0.0', '0.0.0.0:8100']

api.add_middleware(HTTPSRedirectMiddleware)
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify specific HTTP headers
)


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
        user.add_new_user(mail, password, name, surname, type)
        return {"Status" : "User register succesfully"}
    
    except Exception as e:
        return {"Exception": str(e)}
        
@api.get("/login")
async def login(mail: str,
                password: str) -> dict:
    status, token, surname, name = user.check_user(mail, password)
    json: dict = {"status" : status,
            "token" : token,
            "name": name,
            "surname": surname}
    return json
    
    
"""
uvicorn main:api --host 0.0.0.0 --port 8100 --ssl-keyfile certs/cert.key --ssl-certfile certs/cert.crt  
"""