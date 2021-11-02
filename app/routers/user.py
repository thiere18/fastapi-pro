

from sys import prefix
from .. import models,schemas
from fastapi import FastAPI ,Response,status,HTTPException,APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import session 
from .. import models ,schemas ,utils
from .. database import  engine,get_db
from logging import raiseExceptions
from typing import Optional,List
router=APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_post(user: schemas.UserCreate, db:session = Depends(get_db)):
    hased_pass =utils.hash(user.password)
    user.password =hased_pass
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user
 

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int, db:session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raiseExceptions(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"user with id {id} not found"
        )
    return user