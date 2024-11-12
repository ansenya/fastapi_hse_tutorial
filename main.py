from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

import db
import models

app = FastAPI(
    title="FastAPI tutorial",
    summary="There can be some text about the app",
    description="Description?",
    version="1.0.0",
    openapi_tags=[
        {"name": "hello-world", "description": "Some endpoints for acquaintance with FastAPI"},
        {"name": "users", "description": "Some endpoints to work with users"},
        {"name": "html", "description": "HTML endpoints"},
    ],
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "This is a localhost endpoint"},
        {"url": "http://hipahopa.ru:8000", "description": "This is a production endpoint"},
    ],
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


# Hello-world Endpoints
@app.get(path="/acquaintance/hello-world",
         response_model=models.Message,
         tags=["hello-world"],
         description="Returns a hello world message",
         response_description="Hello world message")
def read_root():
    return {"message": "Hello, World!"}


@app.get(path="/acquaintance/greet/{name}",
         response_model=models.Message,
         tags=["hello-world"],
         description="Returns a greeting message with the user's name",
         response_description="Hello name message")
def greet(name: str):
    return {"message": f"Hello, {name}!"}


# User Endpoints
@app.post(path="/users/create", response_model=models.User, tags=["users"])
def create_user(request_user: models.RequestUser):
    saved_user = models.User(**request_user.model_dump())
    saved_user = db.save_model(saved_user)
    return saved_user


@app.get(path="/users/{id}",
         responses={
             200: {"model": models.User, "description": "Found user"},
             404: {"model": models.Message, "description": "User not found"}
         },
         tags=["users"])
def get_user(id: int):
    user = db.get_by_id(id)
    if user is None:
        return models.Message(message="User not found")
    return user


@app.get(path="/users", responses={200: {"model": list[models.Page], "description": "Found users"}}, tags=["users"])
def get_users(page: int = Query(1, ge=1),
              page_size: int = Query(5, le=10), ):
    users = db.get_all(page, page_size)
    return users


# HTML Endpoints
@app.get("/html", response_class=HTMLResponse, tags=["html"])
async def get_homepage():
    html_content = """
    <html>
        <head>
            <title>Homepage</title>
        </head>
        <body>
            <h1>Welcome to FastAPI!</h1>
            <p>This is a simple HTML response.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get(path="/html/users", response_class=HTMLResponse, tags=["html"])
async def get_users_page():
    return HTMLResponse(open("templates/users.html", 'r').read())
