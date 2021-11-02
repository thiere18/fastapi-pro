from .. import models,schemas
from fastapi import Response,status,HTTPException,APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import session 
from .. import models ,schemas
from .. database import  get_db
from typing import Optional,List
router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)
@router.get('/',status_code=status.HTTP_201_CREATED,response_model=List[schemas.Post] )
async def find_posts(db:session =Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()
    posts= db.query(models.Post).all()
    return posts 

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post:schemas.PostCreate, db:session = Depends(get_db)):
   new_post=models.Post(**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return  new_post
    # cursor.execute(""" INSERT INTO posts(title, content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    

# def find_posts(id):
#     for p in my_posts:
#         if p["id"]==id:
#             return p
      
# def delete_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id: 
#             return i


@router.get('/{id}', response_model=schemas.Post)
async def get_post(id:int, response:Response, db:session =Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s""",(str(id)))
    # post=cursor.fetchone()
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
        detail=f"post with id {id} not found")
    return  post

@router.put('/{id}',status_code=status.HTTP_200_OK)
def update_post(id:int ,updated_post:schemas.PostCreate, db:session =Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,(str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post= post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id {id} not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db:session =Depends(get_db)):
    # cursor.execute(""" DELETE  FROM posts WHERE id = %s RETURNING *""",(int(id),))
    # index=cursor.fetchone()
    # conn.commit()
    post =db.query(models.Post).filter(models.Post.id == id)
    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id {id} not found")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)