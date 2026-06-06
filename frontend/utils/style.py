GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

:root {
    --blue:        #2563EB;
    --blue-light:  #EFF6FF;
    --blue-dark:   #1D4ED8;
    --green:       #16A34A;
    --green-light: #F0FDF4;
    --red:         #DC2626;
    --red-light:   #FEF2F2;
    --gray-50:     #F9FAFB;
    --gray-100:    #F3F4F6;
    --gray-200:    #E5E7EB;
    --gray-400:    #9CA3AF;
    --gray-500:    #6B7280;
    --gray-700:    #374151;
    --gray-900:    #111827;
    --white:       #FFFFFF;
    --sidebar-w:   260px;
    --radius:      8px;
    --shadow:      0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
}

/* ── Layout ───────────────────────────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1100px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--gray-200) !important;
}
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Tombol sidebar jadi nav items ───────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius) !important;
    color: var(--gray-700) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: .55rem .85rem !important;
    margin-bottom: 2px !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--gray-100) !important;
    color: var(--gray-900) !important;
}

/* ── Card ─────────────────────────────────────────────────────── */
.rf-card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

/* ── Stat card berwarna ───────────────────────────────────────── */
.rf-stat-blue  { background:#2563EB; color:#fff; border-radius:var(--radius); padding:1.25rem 1.5rem; }
.rf-stat-green { background:#16A34A; color:#fff; border-radius:var(--radius); padding:1.25rem 1.5rem; }
.rf-stat-gray  { background:#6B7280; color:#fff; border-radius:var(--radius); padding:1.25rem 1.5rem; }
.rf-stat-icon  { font-size:28px; margin-bottom:.5rem; opacity:.9; }
.rf-stat-num   { font-size:32px; font-weight:700; line-height:1; margin-bottom:.25rem; }
.rf-stat-label { font-size:13px; opacity:.85; font-weight:500; }

/* ── Badge ────────────────────────────────────────────────────── */
.rf-badge {
    display:inline-block; padding:3px 12px;
    border-radius:999px; font-size:12px; font-weight:600;
}
.rf-badge-hilang    { background:#DC2626; color:#fff; }
.rf-badge-ditemukan { background:#16A34A; color:#fff; }
.rf-badge-aktif     { background:#2563EB; color:#fff; }
.rf-badge-diproses  { background:#D97706; color:#fff; }
.rf-badge-selesai   { background:#16A34A; color:#fff; }

/* ── Tabel ────────────────────────────────────────────────────── */
.rf-table-wrap {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
}
.rf-table-title {
    font-size:15px; font-weight:600; color:var(--gray-900);
    padding:1rem 1.25rem; border-bottom:1px solid var(--gray-200);
    background: var(--white);
}
.rf-th {
    font-size:11px; font-weight:600; color:var(--gray-500);
    text-transform:uppercase; letter-spacing:.05em;
    padding:.65rem 1rem;
    border-bottom:1px solid var(--gray-200);
    background: var(--gray-50);
}
.rf-td {
    font-size:13px; color:var(--gray-700);
    padding:.75rem 1rem;
    border-bottom:1px solid var(--gray-200);
    vertical-align:middle;
}
.rf-td-name   { font-weight:600; color:var(--gray-900); font-size:13px; }
.rf-td-sub    { font-size:11px; color:var(--gray-400); margin-top:1px; }
.rf-tr-last td { border-bottom:none; }

/* ── Page header ──────────────────────────────────────────────── */
.rf-page-title { font-size:22px; font-weight:700; color:var(--gray-900); margin:0; }
.rf-page-sub   { font-size:14px; color:var(--gray-500); margin-top:3px; }

/* ── Section label ────────────────────────────────────────────── */
.rf-section-label {
    font-size:13px; font-weight:600; color:var(--gray-700);
    margin-bottom:.5rem; margin-top:1.25rem;
}

/* ── Tombol utama ─────────────────────────────────────────────── */
.stButton > button {
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* ── Input ────────────────────────────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stSelectbox > div {
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

/* ── Empty state ──────────────────────────────────────────────── */
.rf-empty {
    text-align:center; padding:3rem 1rem; color:var(--gray-400);
}
.rf-empty-icon { font-size:40px; margin-bottom:.75rem; }
.rf-empty-text { font-size:15px; font-weight:600; color:var(--gray-500); }
.rf-empty-sub  { font-size:13px; margin-top:.25rem; }
</style>
"""

KATEGORI_ICON = {
    "elektronik": "laptop",
    "dokumen":    "file-text",
    "pakaian":    "shirt",
    "aksesoris":  "watch",
    "alat_tulis": "pen-tool",
    "tas":        "briefcase",
    "lainnya":    "package",
}

KATEGORI_EMOJI = {
    "elektronik": "💻",
    "dokumen":    "📄",
    "pakaian":    "👕",
    "aksesoris":  "⌚",
    "alat_tulis": "✏️",
    "tas":        "👜",
    "lainnya":    "📦",
}


def badge_tipe(tipe: str) -> str:
    label = tipe.capitalize()
    return f'<span class="rf-badge rf-badge-{tipe}">{label}</span>'


def badge_status(status: str) -> str:
    label = status.capitalize()
    return f'<span class="rf-badge rf-badge-{status}">{label}</span>'