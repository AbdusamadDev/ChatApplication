from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter
from fastapi import APIRouter, Request
from dotenv import load_dotenv
import os

from ..auth.views import get_current_user

load_dotenv()
router = APIRouter(prefix="/t")
templates = Jinja2Templates(directory=f"{os.getenv('BASE_DIR')}templates")


@router.get("/chat")
async def chat_page_renderer(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.get("/signup")
async def signup_renderer(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/groups")
async def create_group_handler(request: Request):
    return templates.TemplateResponse("groups.html", {"request": request})


@router.get("/login")
async def login_handler(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
