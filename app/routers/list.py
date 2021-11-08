from logging import raiseExceptions
from typing import List
from fastapi import APIRouter,Depends,HTTPException, Response,status
from sqlalchemy.orm.session import Session
from .. database import get_db
from .. import models,schemas ,oauth2



router=APIRouter(
    prefix='/list',

)

@router.get('/',response_model=List[schemas.List])
def get_lists( db:Session=Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
    ps=db.query(models.List).all()
    return  ps
    
@router.post("/")
def post_list(list:schemas.ListCreate,db:Session=Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
    new_list=models.List(** list.dict())
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@router.get("/{id}")
def get_list_by_id(id:int ,db:Session=Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    list = db.query(models.List).filter(models.List.id == id).first()
    if list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
        detail=f"list with id {id} not found")
    return list

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_list(id:int,updated_list:schemas.ListCreate ,db:Session=Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    list_query=db.query(models.List).filter(models.List.id==id)
    list=list_query.first()
    if list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"list with id {id} not found")
    list_query.update(updated_list.dict(),synchronize_session=False)
    db.commit()
    return list_query.first()

@router.delete("/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_list(id:int ,db:Session=Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    list_query=db.query(models.List).filter(models.List.id == id)
    list=list_query.first()
    if list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"list with id {id} not found")
    list_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)