from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from sqlalchemy.orm import Session

from database.database import get_db
from models.file import File
from schemas.file import FileResponse as FileResponseSchema
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


@router.get("/", response_model=list[FileResponseSchema])
def get_files(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    files = (
        db.query(File)
        .filter(File.user_id == current_user.id)
        .all()
    )

    return files
@router.get("/{file_id}", response_model=FileResponseSchema)
def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file = db.query(File).filter(
        File.id == file_id
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file"
        )

    return file


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file = db.query(File).filter(
        File.id == file_id
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file"
        )

    upload_dir = Path(__file__).resolve().parent.parent / "uploads"
    file_path = upload_dir / file.filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="File content not found"
        )

    return FileResponse(
        path=file_path,
        filename=file.filename
    )