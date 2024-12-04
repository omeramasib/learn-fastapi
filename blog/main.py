from typing import List
from fastapi import FastAPI, Depends, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from . import schemas, models
from . database import engine, SessionLocal
from sqlalchemy.orm import Session
from . hashing import Hash

app = FastAPI()

# Configure CORS with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/blogs', response_model= List[schemas.ShowBlog], tags=['blogs'])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.post('/blog', status_code= status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message":"Blog Deleted Successfully"}

@app.get('/blog/{id}', status_code= status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(not blog):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return blog

@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return {"message":"Updated Successfully"}


# Create user
@app.post('/user', response_model= schemas.ShowUser, status_code= status.HTTP_201_CREATED, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password= Hash.bycrypt(request.password))
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user

# Get user
@app.get('/user/{id}', response_model= schemas.ShowUser, status_code= status.HTTP_200_OK, tags=["users"])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    return user
    



        