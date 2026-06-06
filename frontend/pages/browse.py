import streamlit as st
from utils.api import get_items
from utils.style import KATEGORI_EMOJI, badge_tipe, badge_status
from datetime import datetime

BASE_URL = "http://localhost:8000"


def fmt_date(s):
    try:
        return datetime.fromisoformat(s).strftime("%d %b %Y")
    except Exception:
        return s


def render():
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="rf-page-title">Cari Barang</div>
        <div class="rf-page-sub">Temukan barang hilang atau yang sudah ditemukan di kampus ITS</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="rf-card" style="padding:.85rem 1.25rem;">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns([3, 2, 2])
    with f1:
        search = st.text_input("", placeholder="Cari nama barang...",
                               label_visibility="collapsed")
    with f2:
        tipe_label = st.selectbox("", ["Semua Tipe", "Hilang", "Ditemukan"],
                                  label_visibility="collapsed")
        tipe = "" if tipe_label == "Semua Tipe" else tipe_label.lower()
    with f3:
        kat_opts = {
            "Semua Kategori": "",
            "Elektronik": "elektronik",
            "Dokumen": "dokumen",
            "Pakaian": "pakaian",
            "Aksesoris": "aksesoris",
            "Alat Tulis": "alat_tulis",
            "Tas": "tas",
            "Lainnya": "lainnya",
        }
        kat_label = st.selectbox("", list(kat_opts.keys()),
                                 label_visibility="collapsed")
        kategori = kat_opts[kat_label]
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Fetch ──────────────────────────────────────────────────────────────────
    with st.spinner("Memuat..."):
        items, code = get_items(
            tipe=tipe or None,
            kategori=kategori or None,
            search=search or None,
            limit=50,
        )

    if code != 200:
        st.error("Gagal memuat data.")
        return

    st.markdown(f"""
    <div style="font-size:13px;color:#6B7280;margin:.5rem 0 1rem;">
        Menampilkan <strong style="color:#111827;">{len(items)}</strong> laporan
    </div>
    """, unsafe_allow_html=True)

    if not items:
        st.markdown("""
        <div class="rf-empty">
            <div class="rf-empty-icon">🔍</div>
            <div class="rf-empty-text">Tidak ada hasil</div>
            <div class="rf-empty-sub">Coba ubah kata kunci atau filter</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Tabel ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="rf-table-wrap">', unsafe_allow_html=True)

    h1, h2, h3, h4, h5 = st.columns([3, 3, 2, 2, 2])
    for col, label in zip([h1,h2,h3,h4,h5],
                          ["BARANG","LOKASI","KATEGORI","TIPE","TANGGAL"]):
        with col:
            st.markdown(f'<div class="rf-th">{label}</div>', unsafe_allow_html=True)

    for i, item in enumerate(items):
        emoji   = KATEGORI_EMOJI.get(item.get("kategori", ""), "📦")
        tipe_v  = item.get("tipe", "")
        is_last = i == len(items) - 1
        border  = "none" if is_last else "1px solid #E5E7EB"

        r1, r2, r3, r4, r5 = st.columns([3, 3, 2, 2, 2])
        with r1:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};">
                <div class="rf-td-name">{item['nama_barang']}</div>
                <div class="rf-td-sub">
                    {item.get('deskripsi','')[:50] + '...'
                     if item.get('deskripsi') and len(item['deskripsi']) > 50
                     else item.get('deskripsi','') or '-'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};
                        font-size:13px;color:#374151;">
                {item['lokasi']}
            </div>
            """, unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};
                        font-size:13px;color:#374151;">
                {emoji} {item.get('kategori','').replace('_',' ').title()}
            </div>
            """, unsafe_allow_html=True)
        with r4:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};">
                {badge_tipe(tipe_v)}
            </div>
            """, unsafe_allow_html=True)
        with r5:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};
                        font-size:13px;color:#6B7280;">
                {fmt_date(item.get('created_at',''))}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)