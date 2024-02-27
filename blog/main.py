from typing import Optional
from fastapi import Depends, FastAPI, Response,status,HTTPException
from . import models,schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/blogs", status_code=status.HTTP_200_OK)
def get_blogs(limit: int = 10, published: bool = True, sort: Optional[str] = None,db:Session=Depends(get_db)):
    """
    GET ALL BLOGS
    """
    blogs = db.query(models.Blog).all()
    return blogs



@app.post("/blogs",status_code=status.HTTP_201_CREATED)
def create_blog(new_blog_data: schemas.Blog,db: Session = Depends(get_db)):
    """
    CREATE A NEW BLOG
    """
    new_blog = models.Blog(title=new_blog_data.title, body=new_blog_data.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put("/blogs/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, update_blog_data: schemas.updateBlog, db: Session = Depends(get_db)):
    """
    UPDATE A BLOG BY ID
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found")   
    # Update the blog attributes with data from update_blog_data
    # for field, value in update_blog_data.model_dump().items():
    #     setattr(blog, field, value)
    blog.update(update_blog_data)
    db.commit()
    db.refresh(blog)
    return blog

@app.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    """
    DELETE A BLOG BY ID
    """
    deleted_count = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found")
    return {"message": f"Blog with ID {id} deleted successfully"}

@app.get("/blogs/{id}",status_code=status.HTTP_200_OK)
def get_blog_by_id(id: int,response:Response, db:Session = Depends(get_db)):
    """
    GET SINGLE BLOG BY ID
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with id {id} not found")
    else:
        return blog
