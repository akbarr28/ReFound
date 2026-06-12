# ReFound - Lost & Found Campus System

Platform digital berbasis web untuk pelaporan barang hilang dan penemuan barang di lingkungan kampus Institut Teknologi Sepuluh Nopember (ITS).

---
- Deployment link: https://refound-swhtokmvwqhokcsmnc3g2b.streamlit.app/

## Daftar Isi

- [Tentang Proyek](#tentang-proyek)
- [Fitur](#fitur)
- [Tech Stack](#tech-stack)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Struktur Folder](#struktur-folder)
- [Cara Menjalankan](#cara-menjalankan)
  - [Prerequisites](#prerequisites)
  - [Setup Backend](#setup-backend)
  - [Setup Frontend](#setup-frontend)
- [Dokumentasi API](#dokumentasi-api)
- [Migrasi Database ke PostgreSQL](#migrasi-database-ke-postgresql)
- [Kontributor](#kontributor)

---

## Tentang Proyek

ReFound hadir sebagai solusi atas permasalahan kehilangan barang di kampus yang selama ini masih ditangani secara manual melalui grup WhatsApp atau media sosial. Dengan ReFound, proses pelaporan, pencarian, dan pencocokan barang menjadi lebih terpusat, terstruktur, dan efisien.

---

## Fitur

### Authentication & Security
- Register akun baru
- Login dengan JWT token
- Password hashing (bcrypt)
- Proteksi route dengan token

### Pelaporan Barang
- Laporan barang **hilang** dan **ditemukan**
- Upload foto barang
- Pilih kategori, lokasi, dan deskripsi

### Search & Filter
- Cari barang berdasarkan nama
- Filter berdasarkan tipe (hilang/ditemukan)
- Filter berdasarkan kategori barang

### Manajemen Laporan
- Edit laporan yang sudah dibuat
- Update status laporan (Aktif → Diproses → Selesai)
- Hapus laporan

### Dashboard
- Statistik total barang hilang, ditemukan, dan selesai
- Statistik per kategori barang
- Laporan terbaru

---

## Tech Stack

| Layer      | Teknologi                          |
|------------|------------------------------------|
| Backend    | FastAPI, SQLAlchemy, Uvicorn       |
| Frontend   | Streamlit                          |
| Database   | SQLite (dev) / PostgreSQL (prod)   |
| Auth       | JWT (python-jose), bcrypt          |
| HTTP       | requests, python-multipart         |

---

## Arsitektur Sistem

```
Browser (Streamlit :8501)
        │
        │  HTTP REST
        ▼
FastAPI Server (:8000)
        │
        ├── /auth      → Register, Login, JWT
        ├── /items     → CRUD Barang + Upload Foto
        └── /dashboard → Statistik & Laporan Terbaru
        │
        ▼
SQLite / PostgreSQL Database
```

---

## Struktur Folder

```
ReFound/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Entry point FastAPI
│   │   ├── database.py      # Koneksi database (SQLite/PostgreSQL)
│   │   ├── models.py        # Model tabel SQLAlchemy
│   │   ├── schemas.py       # Schema Pydantic (request/response)
│   │   ├── auth.py          # JWT & password utils
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py      # Endpoint /auth
│   │       ├── items.py     # Endpoint /items
│   │       └── dashboard.py # Endpoint /dashboard
│   ├── uploads/             # Foto yang diupload (auto-generated)
│   ├── .env                 # Konfigurasi environment (tidak di-commit)
│   ├── .gitignore
│   ├── requirements.txt
│   └── refound.db           # File database SQLite (tidak di-commit)
│
└── frontend/
    ├── pages/
    │   ├── __init__.py
    │   ├── login.py         # Halaman login
    │   ├── register.py      # Halaman register
    │   ├── dashboard.py     # Halaman dashboard
    │   ├── browse.py        # Halaman cari barang
    │   ├── lapor.py         # Halaman buat laporan
    │   └── laporanku.py     # Halaman kelola laporan
    ├── utils/
    │   ├── __init__.py
    │   ├── api.py           # Fungsi pemanggil API backend
    │   └── style.py         # CSS global dan helper UI
    ├── .streamlit/
    │   └── config.toml      # Konfigurasi tema Streamlit
    ├── app.py               # Entry point Streamlit
    ├── .gitignore
    ├── pyproject.toml
    └── uv.lock
```

---

## Cara Menjalankan

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (untuk frontend)
- Git

### Setup Backend

**1. Clone repository dan masuk ke folder backend:**
```bash
git clone <url-repository>
cd ReFound/backend
```

**2. Buat dan aktifkan virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependensi:**
```bash
pip install -r requirements.txt
```

**4. Buat file `.env`** di folder `backend/`:
```env
DATABASE_URL=sqlite:///./refound.db
SECRET_KEY=ganti_dengan_string_random_minimal_32_karakter
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**5. Jalankan server:**
```bash
uvicorn app.main:app --reload
```

Server berjalan di `http://localhost:8000`.
Dokumentasi API tersedia di `http://localhost:8000/docs`.

---

### Setup Frontend

**1. Masuk ke folder frontend:**
```bash
cd ReFound/frontend
```

**2. Install dependensi dengan uv:**
```bash
# Install uv jika belum ada
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependensi (gunakan mirror jika timeout)
uv add streamlit requests Pillow --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**3. Jalankan Streamlit:**
```bash
uv run streamlit run app.py
```

Frontend berjalan di `http://localhost:8501`.

> **Penting:** Backend harus sudah berjalan di port 8000 sebelum membuka frontend.

---

## Dokumentasi API

| Method | Endpoint                    | Deskripsi                    | 
|--------|-----------------------------|------------------------------|
| POST   | `/auth/register`            | Daftar akun baru             |
| POST   | `/auth/login`               | Login, mendapat JWT token    |
| GET    | `/auth/me`                  | Info user yang sedang login  |
| GET    | `/items/`                   | Daftar semua barang          |
| POST   | `/items/`                   | Buat laporan baru            |
| GET    | `/items/{id}`               | Detail satu barang           |
| PUT    | `/items/{id}`               | Edit laporan                 |
| PATCH  | `/items/{id}/status`        | Update status laporan        |
| DELETE | `/items/{id}`               | Hapus laporan                |
| GET    | `/dashboard/stats`          | Statistik dashboard          |

Dokumentasi lengkap dan interaktif: `http://localhost:8000/docs`

---

## Migrasi Database ke PostgreSQL

Saat ini project menggunakan SQLite untuk development lokal. Untuk beralih ke PostgreSQL:

**1. Install PostgreSQL** di komputer atau gunakan layanan cloud (Supabase, Railway, dll).

**2. Buat database baru:**
```sql
CREATE DATABASE refound_db;
```

**3. Ganti `DATABASE_URL` di file `backend/.env`:**
```env
# Hapus baris SQLite lama:
# DATABASE_URL=sqlite:///./refound.db

# Ganti dengan PostgreSQL:
DATABASE_URL=postgresql://username:password@localhost:5432/refound_db
```

**4. Install driver PostgreSQL** (jika belum ada di `requirements.txt`):
```bash
pip install psycopg2-binary
```

**5. Hapus file `refound.db`** (tidak dibutuhkan lagi):
```bash
rm refound.db
```

**6. Restart server** - SQLAlchemy akan otomatis membuat semua tabel di PostgreSQL:
```bash
uvicorn app.main:app --reload
```

> Tidak ada perubahan kode yang diperlukan. `database.py` sudah ditulis agar kompatibel dengan keduanya - `connect_args` untuk SQLite hanya aktif saat `DATABASE_URL` dimulai dengan `sqlite`.

---

## Kontributor

| Nama                        | NRP        | Peran              |
|-----------------------------|------------|--------------------|
| Mohammad Akbar H. B         | 5053241023 | Frontend (Streamlit) |
| M. Khalid Ash Shiddiqi      | 5053241030 | Backend (FastAPI)  |

**Mata Kuliah:** Pemrograman Berbasis Kerangka Kerja <br>
**Institusi:** Departemen Teknik Informatika, Fakultas Teknologi Informasi dan Komunikasi, Institut Teknologi Sepuluh Nopember (ITS) <br>
**Tahun:** 2026
