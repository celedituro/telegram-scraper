from fastapi import FastAPI, HTTPException
from .database import Database
            
app = FastAPI()
db = Database()
db.create_message_table()
db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

