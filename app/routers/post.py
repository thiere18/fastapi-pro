from .. import models,schemas
from fastapi import Response,status,HTTPException,APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import session 
from .. import models ,schemas ,oauth2
from .. database import  get_db
from typing import Optional,List
router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)
@router.get('/',status_code=status.HTTP_201_CREATED,response_model=List[schemas.Post] )
async def find_posts(db:session =Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()
    posts= db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    return posts 

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post:schemas.PostCreate, db:session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
   new_post=models.Post(owner_id=current_user.id ,**post.dict())
   print(current_user.email)
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return  new_post
   

@router.get('/{id}', response_model=schemas.Post)
async def get_post(id:int, response:Response, db:session =Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
   
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
        detail=f"post with id {id} not found")
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="That's not yours")
    return  post


@router.put('/{id}',status_code=status.HTTP_200_OK)
def update_post(id:int ,updated_post:schemas.PostCreate, db:session =Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):

    post_query= db.query(models.Post).filter(models.Post.id==id)
    post= post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id {id} not found")
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="That's not yours")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db:session =Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
   
    post_query =db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id {id} not found")
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="That's not yours")
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)