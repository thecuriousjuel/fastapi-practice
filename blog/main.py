# uvicorn main:app --reload

from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas
import models
from database import engine, session_local
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog')
def get_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/get/{id}', status_code=200)
def get_blogs_via_id(id: int, response: Response, db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()

    # if blogs:
    #     return blogs
    
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'Details:': f'Not Found {id}'}

    if blogs:
        return blogs
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not Found {id}')


@app.delete('/blog/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if blog > 0:
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Deleted {id}')
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Blog not found with id={id}') 

# Update is a Bulk Operation
@app.put('/blog/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session=Depends(get_db)):
    req = dict(request)
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    # Delete can be done this way too.
    if blog.first():
        blog.update(req)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Updated {id}')
    
    raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Blog not found with id={id}') 
