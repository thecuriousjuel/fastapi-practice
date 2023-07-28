# uvicorn main:app --reload

from fastapi import FastAPI, Depends
from schemas import Blog
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

@app.post('/blog')
def create(request: Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/blog')
def get_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_blogs_via_id(id: int, db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blogs