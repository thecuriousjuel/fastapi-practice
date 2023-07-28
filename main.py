# To start the fast API, run the below command
# uvicorn main:app --reload 

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

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

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(blog: Blog):
    return {'data' : f'Blog is created! {blog.title}'}

# Used for Debugging purpose
# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port='9000')
