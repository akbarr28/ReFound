from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_hilang = db.query(models.Item).filter(models.Item.tipe == models.ReportType.hilang).count()
    total_ditemukan = db.query(models.Item).filter(models.Item.tipe == models.ReportType.ditemukan).count()
    total_selesai = db.query(models.Item).filter(models.Item.status == models.ItemStatus.selesai).count()

    laporan_terbaru = (
        db.query(models.Item)
        .order_by(models.Item.created_at.desc())
        .limit(5)
        .all()
    )

    # Statistik per kategori
    rows = (
        db.query(models.Item.kategori, func.count(models.Item.id))
        .group_by(models.Item.kategori)
        .all()
    )
    statistik_kategori = {str(row[0].value): row[1] for row in rows}

    return {
        "total_hilang": total_hilang,
        "total_ditemukan": total_ditemukan,
        "total_selesai": total_selesai,
        "laporan_terbaru": laporan_terbaru,
        "statistik_kategori": statistik_kategori,
    }
