from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name' : 'Biswajit'}}


@app.get('/about')
def about():
    return {'data' : 'About Page'}