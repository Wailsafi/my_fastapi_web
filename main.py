from fastapi import FastAPI, Request, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles



from fastapi.templating import Jinja2Templates




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

app=FastAPI()
templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")


@app.get("/", include_in_schema=False)   # include_in_schema : to allow the router works but it does not apear in the docs of fastapi 
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request,"home.html", {"posts":posts, "title":"home"})


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts :
         if post.get("id")==post_id:
              title=post['title'][:15]
              return templates.TemplateResponse(request,"post.html", {"post":post, "title":title })

    raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail="post not found")


@app.get("/api/posts")
def get_posts():
    return  posts 

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts :
         if post.get("id")==post_id:
               return post
    raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail="post not found")
















