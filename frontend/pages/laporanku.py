import streamlit as st
from utils.api import get_items, update_item, update_status, delete_item
from utils.style import KATEGORI_EMOJI, badge_tipe, badge_status
from datetime import datetime

BASE_URL = "http://localhost:8000"
KATEGORI_LIST = ["elektronik", "dokumen", "pakaian", "aksesoris", "alat_tulis", "tas", "lainnya"]
STATUS_LIST   = ["aktif", "diproses", "selesai"]


def fmt_date(s):
    try:
        return datetime.fromisoformat(s).strftime("%d %b %Y")
    except Exception:
        return s


def render():
    user = st.session_state.user or {}
    user_id = user.get("id")

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="rf-page-title">Laporan Saya</div>
        <div class="rf-page-sub">Kelola semua laporan Anda di sini.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Memuat..."):
        all_items, code = get_items(limit=100)

    if code != 200:
        st.error("Gagal memuat data.")
        return

    items = [i for i in all_items if i.get("user_id") == user_id]

    if not items:
        st.markdown("""
        <div class="rf-empty">
            <div class="rf-empty-icon">📋</div>
            <div class="rf-empty-text">Belum ada laporan</div>
            <div class="rf-empty-sub">Buat laporan pertama Anda sekarang</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buat Laporan", type="primary"):
            st.session_state.page = "lapor"
            st.rerun()
        return

    # ── Tabel laporan ─────────────────────────────────────────────────────────
    st.markdown('<div class="rf-table-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="rf-table-title">Laporan Saya</div>',
        unsafe_allow_html=True
    )

    # Header
    h1, h2, h3, h4, h5 = st.columns([3, 3, 2, 2, 1])
    for col, label in zip(
        [h1, h2, h3, h4, h5],
        ["BARANG", "TIPE", "STATUS", "TANGGAL", ""]
    ):
        with col:
            st.markdown(f'<div class="rf-th">{label}</div>', unsafe_allow_html=True)

    for i, item in enumerate(items):
        emoji  = KATEGORI_EMOJI.get(item.get("kategori", ""), "📦")
        tipe   = item.get("tipe", "")
        status = item.get("status", "")
        is_last = i == len(items) - 1
        border = "none" if is_last else "1px solid #E5E7EB"
        key    = f"item_{item['id']}"

        r1, r2, r3, r4, r5 = st.columns([3, 3, 2, 2, 1])
        with r1:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};">
                <div class="rf-td-name">{item['nama_barang']}</div>
                <div class="rf-td-sub">📍 {item['lokasi']}</div>
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
            <div style="padding:.7rem .9rem;border-bottom:{border};">
                {badge_tipe(tipe)}
            </div>
            """, unsafe_allow_html=True)
        with r4:
            st.markdown(f"""
            <div style="padding:.7rem .9rem;border-bottom:{border};
                        font-size:13px;color:#6B7280;">
                {fmt_date(item.get('created_at',''))}
            </div>
            """, unsafe_allow_html=True)
        with r5:
            st.markdown(
                f'<div style="padding:.5rem .5rem;border-bottom:{border};">',
                unsafe_allow_html=True
            )
            if st.button("...", key=f"opt_{key}", help="Kelola laporan ini"):
                st.session_state[f"expand_{key}"] = not st.session_state.get(f"expand_{key}", False)
            st.markdown("</div>", unsafe_allow_html=True)

        # Panel kelola (expand saat tombol diklik)
        if st.session_state.get(f"expand_{key}", False):
            with st.container():
                st.markdown(f"""
                <div style="background:#F9FAFB;border:1px solid #E5E7EB;
                            border-radius:8px;padding:1rem 1.25rem;margin:.25rem 0 .75rem;">
                    <div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:.75rem;">
                        Kelola: {item['nama_barang']}
                    </div>
                """, unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs(["Update Status", "Edit", "Hapus"])

                with tab1:
                    col_s, col_b = st.columns([2, 1])
                    with col_s:
                        new_status = st.selectbox(
                            "Status",
                            STATUS_LIST,
                            index=STATUS_LIST.index(status) if status in STATUS_LIST else 0,
                            key=f"sel_{key}",
                            format_func=lambda x: {"aktif": "Aktif", "diproses": "Diproses",
                                                    "selesai": "Selesai"}.get(x, x)
                        )
                    with col_b:
                        st.markdown("<div style='margin-top:1.65rem;'></div>",
                                    unsafe_allow_html=True)
                        if st.button("Simpan", key=f"upd_{key}", type="primary",
                                     use_container_width=True):
                            res, c = update_status(item["id"], new_status)
                            if c == 200:
                                st.success("Status diperbarui.")
                                st.rerun()
                            else:
                                st.error("Gagal update status.")

                with tab2:
                    with st.form(f"form_{key}"):
                        e_nama = st.text_input("Nama Barang", value=item["nama_barang"])
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_kat = st.selectbox(
                                "Kategori", KATEGORI_LIST,
                                index=KATEGORI_LIST.index(item["kategori"])
                                      if item["kategori"] in KATEGORI_LIST else 0,
                                format_func=lambda x: x.replace("_", " ").title()
                            )
                        with ec2:
                            e_lok = st.text_input("Lokasi", value=item["lokasi"])
                        e_desk = st.text_area("Deskripsi",
                                              value=item.get("deskripsi") or "", height=80)
                        if st.form_submit_button("Simpan Perubahan", type="primary",
                                                 use_container_width=True):
                            if not e_nama or not e_lok:
                                st.error("Nama dan lokasi wajib diisi.")
                            else:
                                res, c = update_item(item["id"], {
                                    "nama_barang": e_nama,
                                    "kategori": e_kat,
                                    "lokasi": e_lok,
                                    "deskripsi": e_desk or None,
                                })
                                if c == 200:
                                    st.success("Laporan diperbarui.")
                                    st.rerun()
                                else:
                                    st.error("Gagal menyimpan.")

                with tab3:
                    st.markdown(f"""
                    <div style="background:#FEF2F2;border:1px solid #FECACA;
                                border-radius:6px;padding:.75rem 1rem;
                                font-size:13px;color:#B91C1C;margin-bottom:.75rem;">
                        Laporan <strong>{item['nama_barang']}</strong> akan dihapus permanen.
                    </div>
                    """, unsafe_allow_html=True)
                    konfirm = st.checkbox("Saya yakin ingin menghapus", key=f"chk_{key}")
                    if st.button("Hapus Laporan", key=f"del_{key}",
                                 disabled=not konfirm, use_container_width=True):
                        sc = delete_item(item["id"])
                        if sc == 204:
                            st.success("Laporan dihapus.")
                            st.rerun()
                        else:
                            st.error("Gagal menghapus.")

                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)