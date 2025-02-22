from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

def get_posts():
    return {"data":"this is yout posts"}