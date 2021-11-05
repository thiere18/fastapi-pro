
from fastapi import FastAPI 
from .routers import user,post ,auth ,votes 
from fastapi.middleware.cors import CORSMiddleware

from .database import  engine
from . import models
from .config import settings

models.Base.metadata.create_all(bind=engine)

app= FastAPI()

origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get('/')
async def  root():
    return { "msg" : "wlcome to my api"}

