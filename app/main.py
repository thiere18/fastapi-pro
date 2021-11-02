from logging import raiseExceptions
from typing import Optional,List
from fastapi import FastAPI ,Response,status,HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2 as psy
from psycopg2.extras import RealDictCursor
import time
from .routers import user,post
from sqlalchemy.orm import session 
from . import models ,schemas
from .database import  engine,get_db
from . import models

models.Base.metadata.create_all(bind=engine)

app= FastAPI()




# while True:
#     try:
#         conn=psy.connect(host='localhost',database='fastapi',user='postgres',
#         password='saoudah', cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("connexion successful")
#         break
#     except Exception as e:
#         print("connection failed ")
#         print(e)
#         time.sleep(4)


# my_posts=[{"id":1, "name": "John", "description": "copin de terre"},
# {"id":2, "name": "John",  "description": "happier than ever"}]

# @app.get('/sqlalchemy')
# def my_sqlalchmy( db:session =Depends(get_db)):
#     posts= db.query(models.Post).all()

#     return {"data":posts}

@app.get('/')
async def  root():
    return { "msg" : "welcome to my api"}
app.include_router(post.router)
app.include_router(user.router)


