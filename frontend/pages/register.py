import streamlit as st
from utils.api import register


def render():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:2rem; margin-top:2rem;">
            <div style="width:56px;height:56px;background:#0074CC;border-radius:14px;
                        display:inline-flex;align-items:center;justify-content:center;
                        font-size:28px;margin-bottom:1rem;">📝</div>
            <div style="font-size:24px;font-weight:700;color:#101828;">Buat Akun Baru</div>
            <div style="font-size:14px;color:#667085;margin-top:.35rem;">
                Bergabung dengan ReFound ITS
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_register"):
            nama = st.text_input("Nama Lengkap", placeholder="Mohammad Akbar")
            email = st.text_input("Email ITS", placeholder="nama@its.ac.id")
            password = st.text_input("Password", type="password", placeholder="Min. 8 karakter")
            konfirmasi = st.text_input("Konfirmasi Password", type="password",
                                       placeholder="Ulangi password")
            submitted = st.form_submit_button("Daftar", use_container_width=True, type="primary")

        if submitted:
            if not nama or not email or not password:
                st.error("Semua field wajib diisi.")
            elif password != konfirmasi:
                st.error("Password dan konfirmasi tidak cocok.")
            elif len(password) < 8:
                st.error("Password minimal 8 karakter.")
            else:
                with st.spinner("Membuat akun..."):
                    data, code = register(nama, email, password)
                if code == 201:
                    st.success(f"Akun berhasil dibuat! Silakan masuk, {data['nama']}.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(data.get("detail", "Gagal membuat akun."))

        st.markdown("""
        <div style="text-align:center;margin-top:1.25rem;font-size:14px;color:#667085;">
            Sudah punya akun?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Masuk di sini", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()