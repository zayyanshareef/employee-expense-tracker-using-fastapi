from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from connection import Base, engine, sess_db
from sqlalchemy.orm import Session
import bcrypt
import uvicorn

from repositoryuser import UserRepository
from models import UserModel

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


Base.metadata.create_all(bind=engine)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/user/signin")
def login(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/user/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/user/profile")
def signup(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.post("/signupuser")
def signup_user(
    request: Request,
    db: Session = Depends(sess_db),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    
    user_repository = UserRepository(db)
    existing_user = user_repository.get_user_by_username(username) or user_repository.get_user_by_email(email)

    if existing_user:
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "error": "Username or email already registered",
                "username": username,
                "email": email,
            },
        )

    
    user = UserModel(email=email, username=username, password=password)

    
    user_repository.create_user(user)

    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "success": "Account created successfully!", "username": username, "email": email},
    )

@app.post("/loginuser")
def login_user(
    request: Request,
    db: Session = Depends(sess_db),
    username: str = Form(...),
    password: str = Form(...),
):
   
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_username(username)
    
    if not user or not user.verify_password(password):
        
        return templates.TemplateResponse(
            "signin.html",
            {"request": request, "error": "Invalid username or password", "username": username},
        )

    # Successful login - redirect to the welcome page or return appropriate response
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
