import datetime
from typing import Optional
from pydantic import BaseModel


class Blog (BaseModel):
    title:str
    body:str
    published:bool
    
class updateBlog(BaseModel):
    title:Optional[str]
    body:Optional[str]
    published:Optional[bool]
    