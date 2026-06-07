import streamlit as st
from utils.style import GLOBAL_CSS

st.set_page_config(
    page_title="ReFound — Lost & Found ITS",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# CSS tambahan untuk sidebar nav
st.markdown("""
<style>
/* Semua tombol sidebar rata tengah */
[data-testid="stSidebar"] .stButton > button {
    text-align: center !important;
    justify-content: center !important;
}
/* Tombol aktif (div highlight) juga rata tengah */
.rf-nav-active {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("token", None), ("user", None), ("page", "dashboard")]:
    if key not in st.session_state:
        st.session_state[key] = default


def go_to(page: str):
    st.session_state.page = page
    st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;
                    padding:1.25rem 1rem 1rem;
                    border-bottom:1px solid #E5E7EB;margin-bottom:.75rem;">
            <div style="width:36px;height:36px;background:#2563EB;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;">
                <span style="color:#fff;font-size:18px;font-weight:700;">R</span>
            </div>
            <div>
                <div style="font-size:15px;font-weight:700;color:#111827;line-height:1.2;">
                    ReFound
                </div>
                <div style="font-size:11px;color:#9CA3AF;">Lost & Found ITS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.token:
            user  = st.session_state.user or {}
            nama  = user.get("nama", "User")
            email = user.get("email", "")
            initial = nama[0].upper() if nama else "U"

            # User info
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;
                        padding:.65rem .85rem;margin:.25rem .5rem .75rem;
                        background:#F9FAFB;border-radius:8px;">
                <div style="width:32px;height:32px;border-radius:50%;
                            background:#E5E7EB;display:flex;align-items:center;
                            justify-content:center;font-size:13px;font-weight:600;
                            color:#374151;flex-shrink:0;">
                    {initial}
                </div>
                <div style="overflow:hidden;">
                    <div style="font-size:13px;font-weight:600;color:#111827;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                        {nama}
                    </div>
                    <div style="font-size:11px;color:#9CA3AF;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                        {email}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Label MENU
            st.markdown(
                '<div style="font-size:11px;font-weight:600;color:#9CA3AF;'
                'text-transform:uppercase;letter-spacing:.06em;'
                'padding:.25rem .85rem .4rem;">Menu</div>',
                unsafe_allow_html=True
            )

            menu = [
                ("dashboard", "Dashboard"),
                ("browse",    "Cari Barang"),
                ("lapor",     "Buat Laporan"),
                ("laporanku", "Laporan Saya"),
            ]
            for key, label in menu:
                active = st.session_state.page == key
                if active:
                    # Aktif: highlight biru, teks tetap center via CSS
                    st.markdown(f"""
                    <div class="rf-nav-active"
                         style="background:#EFF6FF;border-radius:8px;
                                padding:.55rem .85rem;margin:.15rem .5rem;
                                font-size:14px;font-weight:600;color:#2563EB;
                                text-align:center;">
                        {label}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button(label, key=f"nav_{key}", use_container_width=True):
                        go_to(key)

            # Divider + AKUN
            st.markdown("""
            <div style="border-top:1px solid #E5E7EB;margin:1rem .5rem .5rem;"></div>
            <div style="font-size:11px;font-weight:600;color:#9CA3AF;
                        text-transform:uppercase;letter-spacing:.06em;
                        padding:.25rem .85rem .4rem;">Akun</div>
            """, unsafe_allow_html=True)

            if st.button("Akun", key="nav_akun", use_container_width=True):
                pass

            if st.button("Keluar", key="nav_logout", use_container_width=True):
                st.session_state.token = None
                st.session_state.user  = None
                st.session_state.page  = "login"
                st.rerun()

        else:
            st.markdown(
                '<div style="font-size:11px;font-weight:600;color:#9CA3AF;'
                'text-transform:uppercase;letter-spacing:.06em;'
                'padding:.25rem .85rem .4rem;">Akun</div>',
                unsafe_allow_html=True
            )
            if st.button("Masuk",  key="nav_login",    use_container_width=True):
                go_to("login")
            if st.button("Daftar", key="nav_register", use_container_width=True):
                go_to("register")


# ── Router ────────────────────────────────────────────────────────────────────
def render_page():
    page = st.session_state.page
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


render_sidebar()
render_page()