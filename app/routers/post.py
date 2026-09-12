
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

db_dependency = Depends(get_db)

router = APIRouter( 
    prefix="/posts",
    tags=["Posts"]
)

#@router.get("/",response_model=list[schemas.Post])
@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session = db_dependency,current_user :int = Depends(oauth2.get_current_usernew),
              limit : int=10,skip:int=0, search:str | None=""): 
    # cursor.execute("""Select * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    postswithlimit = db.query(models.Post).limit(limit).offset(skip).all()
    postswithlimitskipsearch= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts_with_grouby = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return posts_with_grouby

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session=db_dependency, current_user :int = Depends(oauth2.get_current_usernew)):
    # post_dict=post.model_dump()
    # post_dict["id"]=randrange(0, 1000000)
    # my_posts.append(post_dict)
    # now use db code below
    # cursor.execute(""" insert into posts (title,content,published) values(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title,content=post.content,published =post.published)
    print(current_user.email)
    print(current_user.id)
    new_post = models.Post(owner_id= current_user.id ,**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#@router.get("/{id}",response_model=schemas.PostOut)
#adding new post router for groupby
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id :int,db:Session=db_dependency,current_user :int = Depends(oauth2.get_current_usernew)):
    # cursor.execute(""" select * from posts where id =%s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()

    post_with_groupby = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post_with_groupby:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message ":f" post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post_with_groupby
   
        

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=db_dependency,current_user :int = Depends(oauth2.get_current_usernew)):

    # cursor.execute("""delete from posts where id =%s returning * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id==id)

    deleted_post = deleted_post_query.first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorised to  perform requested action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    #return status.HTTP_204_NO_CONTENT
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post_update: schemas.PostCreate,db:Session=db_dependency,current_user :int = Depends(oauth2.get_current_usernew)):

    # cursor.execute("""update posts set title= %s,content=%s, published =%s where id =%s returning * """,(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")


    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorised to  perform requested action")
    #post_query.update({'title':"new Title",'content':'new updated content'},synchronize_session=False)
    #we could also use post.dict instead of hardcoding updated values
    post_query.update(post_update.model_dump()   ,synchronize_session=False)
    db.commit()


    return post_query.first()