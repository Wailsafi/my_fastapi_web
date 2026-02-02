from fastapi import FastAPI, Request, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException 
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import PostCreate, PostResponse
from sqlalchemy  import select
from sqlalchemy import Session 

import models 
from database import Base, engine, get_db 

from schemas import  PostCreate, PostResponse

from typing import PostCreate, PostResponse 

from fastapi.templating import Jinja2Templates
Base.metadata.create_all(bind=engine)


app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates=Jinja2Templates(directory="templates")




posts: list[dict] = [
    {
        "id": 1,
        "author": "Wail",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "wassim",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]




@app.get("/", include_in_schema=False)   # include_in_schema : to allow the router works but it does not apear in the docs of fastapi 
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request,"home.html", {"posts":posts, "title":"home"})
@app.post("/api/posts",response_model=PostResponse, status_code=status.HTTP_201_CREATED,)
def create_post(post:PostCreate):
     new_id= max (p["id"] for p in posts)+1 if posts else 1
     new_post={
          "id":new_id,
          "author":post.author,
          "title":post.title, 
          "content":post.content,
          "date_posted":"january 31 2025",
     }
     posts.append(new_post)
     return new_post



@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts :
         if post.get("id")==post_id:
              title=post['title'][:15]
              return templates.TemplateResponse(request,"post.html", {"post":post, "title":title })

    raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail="post not found")


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return  posts 

@app.get("/api/posts/{post_id}",response_model=PostResponse)
def get_post(post_id: int):
    for post in posts :
         if post.get("id")==post_id:
               return post
    raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail="post not found")

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
















