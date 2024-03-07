from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.exc import OperationalError
from fastapi import (
    HTTPException,
    UploadFile,
    APIRouter,
    Response,
    Request,
    Depends,
    Query,
    Form,
    File,
)

from database.manager import GroupMessageManager, GroupManager, UserManager
from ..auth.views import get_current_user
from .serializers import GroupSerializer, MediaSerializer
from .. import status

from typing import Annotated
import uuid
import time
import os

router = APIRouter(prefix="/api")
UPLOAD_DIR = os.environ.get("BASE_DIR")
ALLOWED_MEDIA_TYPES = ["audio", "document", "image", "video"]
AUDIO_FORMAT = ["mp3", "ogg", "wav", "mpeg"]
IMAGE_FORMAT = ["png", "jpg", "gif", "jpeg"]
VIDEO_FORMAT = ["mp4"]
MB = 1024 * 1024


@router.get("/groups", response_class=JSONResponse)
async def get_groups(
    request: Request,
    user=Depends(get_current_user),
    page: int = Query(1, ge=1),
):
    try:
        groups = GroupManager()
        group_ids = groups.get_paginated_response(page=page, url=request.url)
        return {"groups": group_ids}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(error)}",
        )


@router.get("/messages/{group_id}", response_class=JSONResponse)
async def get_messages(
    request: Request,
    group_id: str,
    page: int = Query(1, ge=1),
    user=Depends(get_current_user),
):
    try:
        database = GroupMessageManager(table_name=group_id)
        return database.get_paginated_response(page, request.url)
    except OperationalError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operational error occurred: {str(error)}",
        )


@router.post("/groups", response_class=JSONResponse)
async def create_new_chat_group(
    serializer: GroupSerializer, user=Depends(get_current_user)
):
    try:
        unique_key = "group_" + str(uuid.uuid4())
        port = os.environ.get(
            "PROTOCOL", "http"
        ).lower()  # Default to "http" if PROTOCOL is not set
        host = os.environ.get(
            "HOST", "192.168.100.39"
        )  # Default to "192.168.100.39" if HOST is not set
        title = serializer.title
        description = serializer.description

        # Create group
        group_model = GroupManager()
        group_model.add(
            admin_id=user.get("id"),
            title=title,
            description=description,
            table_name=unique_key,
            link=f"{port}://{host}/groups/{unique_key}",
        )

        # Create message table for the group
        chat_group_model = GroupMessageManager(table_name=unique_key)
        chat_group_model.create()

        return {"detail": "Group created successfully!"}, status.HTTP_201_CREATED
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "detail": "Unexpected error occurred, please retry!",
                "description": str(error),
            },
        )


@router.get("/users", response_class=JSONResponse)
async def get_users(user=Depends(get_current_user)):
    model = UserManager()
    users = model.all()
    return {"data": users}


@router.delete("/messages/{group_id}/{message_id}")
async def delete_messages(
    request: Request, group_id: str, message_id: str, user=Depends(get_current_user)
):
    model = GroupMessageManager(table_name=group_id)
    if group_id not in model.group_ids() or not model.get(pk=message_id):
        raise HTTPException(
            detail=f"Message with id: {message_id} not found in group {group_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    message = model.get(pk=message_id)
    if str(user.get("id")) != message.get("user_id"):
        raise HTTPException(
            detail="Cannot delete other's message",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    model.delete(pk=message_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/media/{media_type}/{chat_id}/{media_id}")
async def media_handler(
    request: Request,
    media_type: str,
    chat_id: str,
    media_id: str,
):
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise HTTPException(
            detail="Invalid media type provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    file_path = os.path.join(
        os.environ.get("BASE_DIR"), f"media/{media_type}s/{chat_id}/{media_id}"
    )
    if not os.path.isfile(file_path):
        raise HTTPException(
            detail="Media file not found on server!",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return FileResponse(file_path)


@router.post("/uploads/{group_id}", response_class=JSONResponse)
async def upload_media(
    request: Request,
    group_id: str,
    type: str = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    allowed_formats = {
        "audio": AUDIO_FORMAT,
        "image": IMAGE_FORMAT,
        "video": VIDEO_FORMAT,
    }

    if type not in allowed_formats:
        raise HTTPException(
            detail="Invalid media type provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    file_format = file.filename.split(".")[-1]
    match type:
        case "audio" if file_format in AUDIO_FORMAT:
            pass
        case "image" if file_format in IMAGE_FORMAT:
            pass
        case "video" if file_format in VIDEO_FORMAT:
            pass
        case "document":
            if file.size > (100 * MB):
                raise HTTPException(
                    detail="Too heavy document to store!",
                    status_code=status.HTTP_422_UNPROCESSIBLE_ENTITY,
                )
        case _:
            raise HTTPException(
                detail=f"Invalid {type.capitalize()} file provided",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    start = time.time()
    directory = os.path.join(
        UPLOAD_DIR, f"media/{type}s/", group_id, str(user.get("id"))
    )
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file.filename)
    if os.path.exists(file_path):
        filename, file_extension = os.path.splitext(file.filename)
        count = 1
        while os.path.exists(
            os.path.join(directory, f"{filename} ({count}){file_extension}")
        ):
            count += 1
        file.filename = f"{filename} ({count}){file_extension}"
        file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    end = time.time()
    return {"message": "File added!", "elapsed_time": end - start}
