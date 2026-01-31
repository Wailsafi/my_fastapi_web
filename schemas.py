from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title:str=Field(min_length=1, max_length=100)
    content:str=Field(min_length=1)

    author:str=Field(min_lrngth=1, max_length=50)
    
class PostCreate(PostBase):
    pass
class PostResponse(PostBase):
    model_config=ConfigDict(from_attributes=True)  #" to allow pydantic to accept the data that is coming from the db and doesn't have a dictionary format"
    id: int 
    date_posted:str
    
    

    
     