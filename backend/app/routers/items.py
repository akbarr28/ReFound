from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
from app.models import ItemCategory, ItemStatus, ReportType
import os, uuid
from supabase import create_client
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/items", tags=["Items"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME  = "uploads"

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


def save_image_supabase(file: UploadFile) -> str:
    """Upload gambar ke Supabase Storage, return public URL."""

    # Validasi ekstensi
    filename_raw = file.filename or ""
    ext = filename_raw.rsplit(".", 1)[-1].lower() if "." in filename_raw else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipe file tidak didukung. Gunakan: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    unique_filename = f"{uuid.uuid4()}.{ext}"

    # Baca isi file
    contents = file.file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="File kosong.")

    logger.info(f"Uploading {unique_filename} ({len(contents)} bytes) to Supabase...")

    # Validasi env
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di environment!")
        raise HTTPException(status_code=500, detail="Konfigurasi storage belum diset.")

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase.storage.from_(BUCKET_NAME).upload(
            path=unique_filename,
            file=contents,
            file_options={"content-type": file.content_type or "image/jpeg"}
        )
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{unique_filename}"
        logger.info(f"Upload sukses: {public_url}")
        return public_url

    except Exception as e:
        logger.error(f"Supabase upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gagal upload foto: {str(e)}")


# ── Create ────────────────────────────────────────────────────────────────────

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

    # Cek foto valid: ada, punya filename, dan bukan file kosong
    if foto and foto.filename and foto.filename.strip() != "":
        logger.info(f"Foto diterima: {foto.filename}, content_type: {foto.content_type}")
        foto_url = save_image_supabase(foto)
    else:
        logger.info("Tidak ada foto yang diupload.")

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


# ── Read ──────────────────────────────────────────────────────────────────────

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


# ── Update ────────────────────────────────────────────────────────────────────

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


# ── Delete ────────────────────────────────────────────────────────────────────

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
