# uvicorn main:app --reload

from fastapi import FastAPI
from schemas import Blog
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post('/blog')
def create(request: Blog):
    return request
