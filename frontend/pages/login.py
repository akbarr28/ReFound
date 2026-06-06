import streamlit as st
from utils.api import login


def render():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:2rem; margin-top:2rem;">
            <div style="width:56px;height:56px;background:#0074CC;border-radius:14px;
                        display:inline-flex;align-items:center;justify-content:center;
                        font-size:28px;margin-bottom:1rem;">🔍</div>
            <div style="font-size:24px;font-weight:700;color:#101828;">Masuk ke ReFound</div>
            <div style="font-size:14px;color:#667085;margin-top:.35rem;">
                Platform Lost & Found Kampus ITS
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_login"):
            email = st.text_input("Email", placeholder="nama@its.ac.id")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Masuk", use_container_width=True, type="primary")

        if submitted:
            if not email or not password:
                st.error("Email dan password wajib diisi.")
            else:
                with st.spinner("Memverifikasi..."):
                    data, code = login(email, password)
                if code == 200:
                    st.session_state.token = data["access_token"]
                    from utils.api import get_me
                    user_data, _ = get_me()
                    st.session_state.user = user_data
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error(data.get("detail", "Email atau password salah."))

        st.markdown("""
        <div style="text-align:center;margin-top:1.25rem;font-size:14px;color:#667085;">
            Belum punya akun?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Daftar sekarang", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()