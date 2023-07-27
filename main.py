# To start the fast API, run the below command
# uvicorn main:app --reload 

from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name' : 'Biswajit'}}


@app.get('/about')
def about():
    return {'data' : 'About Page'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished blog'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    return {'data' : {'comments' : id}}


@app.get('/blog')
def get_blogs(limit: int=10, published: bool=True, sort: Optional[str]=None):
    if published:
        return {'data' : limit, 'published': published, 'sort': sort}
    return {'data' : limit, 'published': published, 'sort': sort}