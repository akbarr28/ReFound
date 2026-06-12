import streamlit as st
from utils.api import get_items, BASE_URL
from utils.style import KATEGORI_EMOJI, badge_tipe
from datetime import datetime


def fmt_date(s):
    try:
        return datetime.fromisoformat(s).strftime("%d %b %Y")
    except Exception:
        return s


def get_foto_url(foto_url: str) -> str:
    """Normalize foto URL — bisa full URL (Supabase) atau path lokal."""
    if not foto_url:
        return None
    if foto_url.startswith("http"):
        return foto_url  # sudah full URL dari Supabase
    return f"{BASE_URL}{foto_url}"  # path lokal: /uploads/xxx.jpg


def render():
    st.markdown("""
    <div style="margin-bottom:1.25rem;">
        <div class="rf-page-title">Cari Barang</div>
        <div class="rf-page-sub">Temukan barang hilang atau yang sudah ditemukan di kampus ITS</div>
    </div>
    """, unsafe_allow_html=True)

    # Search + Filter 
    sb1, sb2 = st.columns([4, 1])
    with sb1:
        search = st.text_input(
            "", placeholder="🔍  Search...",
            label_visibility="collapsed",
            key="browse_search"
        )
    with sb2:
        with st.expander("Filter"):
            tipe_label = st.selectbox(
                "Tipe", ["Semua", "Hilang", "Ditemukan"],
                label_visibility="collapsed", key="browse_tipe"
            )
            kat_opts = {
                "Semua Kategori": "",
                "Elektronik":     "elektronik",
                "Dokumen":        "dokumen",
                "Pakaian":        "pakaian",
                "Aksesoris":      "aksesoris",
                "Alat Tulis":     "alat_tulis",
                "Tas":            "tas",
                "Lainnya":        "lainnya",
            }
            kat_label = st.selectbox(
                "Kategori", list(kat_opts.keys()),
                label_visibility="collapsed", key="browse_kat"
            )

    tipe     = "" if tipe_label == "Semua" else tipe_label.lower()
    kategori = kat_opts.get(kat_label, "")

    # Fetch 
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

    if not items:
        st.markdown("""
        <div class="rf-empty" style="margin-top:3rem;">
            <div class="rf-empty-icon">🔍</div>
            <div class="rf-empty-text">Tidak ada hasil</div>
            <div class="rf-empty-sub">Coba ubah kata kunci atau filter</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div style="font-size:13px;color:#6B7280;margin:.25rem 0 1rem;">
        {len(items)} laporan ditemukan
    </div>
    """, unsafe_allow_html=True)

    # Grid 4 kolom 
    cols_per_row = 4
    for i in range(0, len(items), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(items):
                break
            item = items[idx]
            with cols[j]:
                tipe_v      = item.get("tipe", "")
                emoji       = KATEGORI_EMOJI.get(item.get("kategori", ""), "📦")
                foto_url    = get_foto_url(item.get("foto_url"))
                badge_color = "#DC2626" if tipe_v == "hilang" else "#16A34A"
                badge_label = tipe_v.capitalize()

                if foto_url:
                    st.markdown(f"""
                    <div style="border-radius:10px;overflow:hidden;
                                border:1px solid #E5E7EB;margin-bottom:0;">
                        <img src="{foto_url}"
                             style="width:100%;height:175px;object-fit:cover;display:block;"
                             onerror="this.parentElement.innerHTML='<div style=height:175px;background:#F3F4F6;display:flex;align-items:center;justify-content:center;font-size:44px;>{emoji}</div>'">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="height:175px;background:#F3F4F6;border-radius:10px;
                                border:1px solid #E5E7EB;display:flex;
                                align-items:center;justify-content:center;
                                font-size:44px;margin-bottom:0;">
                        {emoji}
                    </div>
                    """, unsafe_allow_html=True)

                nama   = item.get("nama_barang", "")
                lokasi = item.get("lokasi", "")
                tanggal = fmt_date(item.get("created_at", ""))

                st.markdown(f"""
                <div style="padding:.6rem .25rem .9rem;">
                    <div style="font-size:14px;font-weight:600;color:#111827;
                                margin-bottom:.3rem;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;">
                        {nama}
                    </div>
                    <div style="font-size:12px;color:#6B7280;
                                display:flex;align-items:center;gap:4px;
                                margin-bottom:.25rem;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;">
                        <span>📍</span>
                        <span style="overflow:hidden;text-overflow:ellipsis;">{lokasi}</span>
                    </div>
                    <div style="display:flex;align-items:center;
                                justify-content:space-between;margin-top:.35rem;">
                        <span style="font-size:12px;color:#9CA3AF;">{tanggal}</span>
                        <span style="background:{badge_color};color:#fff;
                                     font-size:11px;font-weight:600;
                                     padding:2px 10px;border-radius:999px;">
                            {badge_label}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:.25rem;'></div>", unsafe_allow_html=True)
