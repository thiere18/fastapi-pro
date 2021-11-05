from sqlalchemy import create_engine
from logging import raiseExceptions
import time

from random import randrange
import psycopg2 as psy
from psycopg2.extras import RealDictCursor
from sqlalchemy.ext.declarative import declarative_base
from .config import settings 
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = settings.database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn=psy.connect(host='localhost',database='fastapi',user='postgres',
        password='saoudah', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("connexion successful")
        break
    except Exception as e:
        print("connection failed ")
        print(e)
        time.sleep(4)

# my_posts=[{"id":1, "name": "John", "description": "copin de terre"},
# {"id":2, "name": "John",  "description": "happier than ever"}]

# @app.get('/sqlalchemy')
# def my_sqlalchmy( db:session =Depends(get_db)):
#     posts= db.query(models.Post).all()

#     return {"data":posts}

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
 # cursor.execute(""" SELECT * FROM posts WHERE id=%s""",(str(id)))
    # post=cursor.fetchone()

     # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,(str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
     # cursor.execute(""" DELETE  FROM posts WHERE id = %s RETURNING *""",(int(id),))
    # index=cursor.fetchone()
    # conn.commit()