from fastapi import FastAPI ,Response,status,HTTPException,APIRouter,Depends
from sqlalchemy.orm import session
from .. import models ,schemas,database,oauth2

router= APIRouter(prefix='/votes',tags=['votes'])

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db:session =Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote =vote_query.first()

    if (vote.dir==1):
        if (found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote =models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"successfuly added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=false)