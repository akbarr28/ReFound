from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
from app.models import ItemCategory, ItemStatus, ReportType
import os, uuid, shutil

router = APIRouter(prefix="/items", tags=["Items"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def save_image_local(file: UploadFile) -> str:
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipe file tidak didukung. Gunakan: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return f"/uploads/{filename}"


# Create
@router.post("/", response_model=schemas.ItemOut, status_code=201)
def create_item(
    nama_barang: str = Form(...),
    deskripsi: Optional[str] = Form(None),
    kategori: ItemCategory = Form(...),
    lokasi: str = Form(...),
    tipe: ReportType = Form(...),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    foto_url = None
    if foto:
        foto_url = save_image_local(foto)

    item = models.Item(
        nama_barang=nama_barang,
        deskripsi=deskripsi,
        kategori=kategori,
        lokasi=lokasi,
        tipe=tipe,
        foto_url=foto_url,
        user_id=current_user.id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# Read
@router.get("/", response_model=List[schemas.ItemOut])
def get_items(
    tipe: Optional[ReportType] = Query(None),
    kategori: Optional[ItemCategory] = Query(None),
    status: Optional[ItemStatus] = Query(None),
    lokasi: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(models.Item)

    if tipe:
        q = q.filter(models.Item.tipe == tipe)
    if kategori:
        q = q.filter(models.Item.kategori == kategori)
    if status:
        q = q.filter(models.Item.status == status)
    if lokasi:
        q = q.filter(models.Item.lokasi.ilike(f"%{lokasi}%"))
    if search:
        q = q.filter(models.Item.nama_barang.ilike(f"%{search}%"))

    return q.order_by(models.Item.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    return item


# Update
@router.put("/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int,
    data: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item

@router.patch("/{item_id}/status", response_model=schemas.ItemOut)
def update_status(
    item_id: int,
    status: ItemStatus,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")

    item.status = status
    db.commit()
    db.refresh(item)
    return item

# Delete
@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")

    db.delete(item)
    db.commit()
