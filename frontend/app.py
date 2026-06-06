import streamlit as st
from utils.style import GLOBAL_CSS
from utils.api import get_me

st.set_page_config(
    page_title="ReFound — Lost & Found ITS",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "dashboard"


def go_to(page: str):
    st.session_state.page = page
    st.rerun()


def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding: 1.5rem 1rem 1rem; border-bottom: 1px solid #EAECF0; margin-bottom: .5rem;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:38px;height:38px;background:#0074CC;border-radius:10px;
                            display:flex;align-items:center;justify-content:center;
                            font-size:20px;color:white;">🔍</div>
                <div>
                    <div style="font-size:16px;font-weight:700;color:#101828;line-height:1.2;">ReFound</div>
                    <div style="font-size:11px;color:#667085;">Lost & Found ITS</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.token:
            user = st.session_state.user or {}
            nama = user.get("nama", "User")

            # User info
            st.markdown(f"""
            <div style="padding: .75rem 1rem; margin: .5rem 0;
                        background:#F5F7FA; border-radius:10px;">
                <div style="font-size:13px;font-weight:600;color:#101828;">{nama}</div>
                <div style="font-size:11px;color:#667085;">{user.get("email","")}</div>
            </div>
            """, unsafe_allow_html=True)

            # Menu items
            st.markdown('<div class="rf-section" style="padding:0 .5rem;">Menu</div>',
                        unsafe_allow_html=True)

            menu_items = [
                ("dashboard", "🏠", "Dashboard"),
                ("browse",    "🔍", "Cari Barang"),
                ("lapor",     "➕", "Buat Laporan"),
                ("laporanku", "📋", "Laporan Saya"),
            ]

            for key, icon, label in menu_items:
                active = st.session_state.page == key
                style = (
                    "background:#EBF4FF;color:#0074CC;font-weight:600;"
                    if active else
                    "color:#344054;font-weight:500;"
                )
                if st.button(
                    f"{icon}  {label}",
                    key=f"nav_{key}",
                    use_container_width=True,
                ):
                    go_to(key)
                # Override style via markdown setelah button
                st.markdown(f"""
                <style>
                [data-testid="stButton"] button[kind="secondary"] {{
                    text-align: left !important;
                    justify-content: flex-start !important;
                    border: none !important;
                    background: transparent !important;
                }}
                </style>""", unsafe_allow_html=True)

            st.markdown("<hr style='border:none;border-top:1px solid #EAECF0;margin:1rem 0;'>",
                        unsafe_allow_html=True)
            st.markdown('<div class="rf-section" style="padding:0 .5rem;">Akun</div>',
                        unsafe_allow_html=True)
            if st.button("🚪  Keluar", use_container_width=True, key="nav_logout"):
                logout()
        else:
            menu_items = [
                ("login",    "🔑", "Masuk"),
                ("register", "📝", "Daftar"),
            ]
            for key, icon, label in menu_items:
                if st.button(f"{icon}  {label}", key=f"nav_{key}",
                             use_container_width=True):
                    go_to(key)


# ── Router halaman ────────────────────────────────────────────────────────────
def render_page():
    page = st.session_state.page

    # Halaman yang butuh login
    protected = {"dashboard", "browse", "lapor", "laporanku"}
    if page in protected and not st.session_state.token:
        go_to("login")
        return

    if page == "login":
        from pages.login import render
    elif page == "register":
        from pages.register import render
    elif page == "dashboard":
        from pages.dashboard import render
    elif page == "browse":
        from pages.browse import render
    elif page == "lapor":
        from pages.lapor import render
    elif page == "laporanku":
        from pages.laporanku import render
    else:
        from pages.dashboard import render

    render()


# ── Main ──────────────────────────────────────────────────────────────────────
render_sidebar()
render_page()