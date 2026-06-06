import streamlit as st
from utils.api import create_item

KATEGORI_LIST = ["elektronik", "dokumen", "pakaian", "aksesoris", "alat_tulis", "tas", "lainnya"]
KATEGORI_LABEL = {
    "elektronik": "Elektronik",
    "dokumen":    "Dokumen",
    "pakaian":    "Pakaian",
    "aksesoris":  "Aksesoris",
    "alat_tulis": "Alat Tulis",
    "tas":        "Tas",
    "lainnya":    "Lainnya",
}


def render():
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="rf-page-title">Buat Laporan</div>
        <div class="rf-page-sub">Laporkan barang hilang atau yang Anda temukan</div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_side = st.columns([2, 1])

    with col_form:
        st.markdown('<div class="rf-card">', unsafe_allow_html=True)

        prefill = st.session_state.pop("prefill_tipe", None)
        tipe_default = ["hilang", "ditemukan"].index(prefill) \
                       if prefill in ["hilang", "ditemukan"] else 0

        with st.form("form_laporan", clear_on_submit=True):
            # Tipe
            st.markdown(
                '<div class="rf-section-label">Tipe Laporan</div>',
                unsafe_allow_html=True
            )
            tipe = st.radio(
                "",
                ["hilang", "ditemukan"],
                index=tipe_default,
                horizontal=True,
                format_func=lambda x: "Saya kehilangan barang"
                                      if x == "hilang" else "Saya menemukan barang",
                label_visibility="collapsed",
            )

            # Detail
            st.markdown(
                '<div class="rf-section-label" style="margin-top:1rem;">Detail Barang</div>',
                unsafe_allow_html=True
            )
            nama_barang = st.text_input(
                "Nama Barang *",
                placeholder="Contoh: Dompet kulit cokelat, Charger laptop..."
            )
            lc, rc = st.columns(2)
            with lc:
                kategori = st.selectbox(
                    "Kategori *",
                    KATEGORI_LIST,
                    format_func=lambda x: KATEGORI_LABEL.get(x, x)
                )
            with rc:
                lokasi = st.text_input(
                    "Lokasi *",
                    placeholder="Contoh: Perpustakaan lantai 2, Gedung D3"
                )
            deskripsi = st.text_area(
                "Deskripsi",
                placeholder="Ciri-ciri barang, warna, merek, kondisi...",
                height=100,
            )

            # Foto
            st.markdown(
                '<div class="rf-section-label" style="margin-top:.5rem;">Foto (opsional)</div>',
                unsafe_allow_html=True
            )
            foto = st.file_uploader(
                "", type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed"
            )
            if foto:
                st.image(foto, width=280)

            st.markdown("<div style='margin-top:.75rem;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "Kirim Laporan", use_container_width=True, type="primary"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not nama_barang or not lokasi:
                st.error("Nama barang dan lokasi wajib diisi.")
            else:
                with st.spinner("Mengirim..."):
                    data, code = create_item(
                        nama_barang=nama_barang,
                        deskripsi=deskripsi,
                        kategori=kategori,
                        lokasi=lokasi,
                        tipe=tipe,
                        foto=foto,
                    )
                if code == 201:
                    st.success(f"Laporan '{data['nama_barang']}' berhasil dikirim!")
                    st.balloons()
                else:
                    st.error(data.get("detail", "Gagal mengirim laporan."))

    with col_side:
        st.markdown("""
        <div class="rf-card">
            <div style="font-size:14px;font-weight:600;color:#111827;margin-bottom:.85rem;">
                Tips Laporan yang Baik
            </div>
            <div style="font-size:13px;color:#374151;line-height:1.9;">
                <div style="margin-bottom:.5rem;">
                    <strong>Nama Barang</strong><br>
                    Sebutkan nama spesifik beserta warna atau merek.
                </div>
                <div style="margin-bottom:.5rem;">
                    <strong>Lokasi</strong><br>
                    Tulis lokasi selengkap mungkin, termasuk lantai atau ruangan.
                </div>
                <div style="margin-bottom:.5rem;">
                    <strong>Deskripsi</strong><br>
                    Sertakan ciri unik agar mudah dikenali pemiliknya.
                </div>
                <div>
                    <strong>Foto</strong><br>
                    Foto mempercepat proses pencocokan barang.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)