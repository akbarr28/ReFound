import streamlit as st
from utils.api import get_dashboard_stats
from utils.style import KATEGORI_EMOJI, badge_tipe, badge_status
from datetime import datetime

BASE_URL = "http://localhost:8000"


def fmt_date(s):
    try:
        return datetime.fromisoformat(s).strftime("%d %b %Y")
    except Exception:
        return s


def render():
    user = st.session_state.user or {}
    nama = user.get("nama", "User")

    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div class="rf-page-title">Selamat datang di ReFound, {nama.split()[0]}!</div>
        <div class="rf-page-sub">Platform Pelaporan Kehilangan &amp; Penemuan Barang ITS</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Memuat data..."):
        stats, code = get_dashboard_stats()

    if code != 200:
        st.error("Gagal memuat data dashboard.")
        return

    # ── Stat cards ─────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="rf-stat-blue">
            <div class="rf-stat-icon">📦</div>
            <div class="rf-stat-label">Total Lost Items</div>
            <div class="rf-stat-num">{stats['total_hilang']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="rf-stat-green">
            <div class="rf-stat-icon">📦</div>
            <div class="rf-stat-label">Total Found Items</div>
            <div class="rf-stat-num">{stats['total_ditemukan']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="rf-stat-gray">
            <div class="rf-stat-icon">📋</div>
            <div class="rf-stat-label">Completed Reports</div>
            <div class="rf-stat-num">{stats['total_selesai']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Category Statistics ───────────────────────────────────────────────────
    stat_kat = stats.get("statistik_kategori", {})
    if stat_kat:
        st.markdown('<div class="rf-card">', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:15px;font-weight:600;color:#111827;margin-bottom:1rem;">'
            'Category Statistics</div>',
            unsafe_allow_html=True
        )
        sorted_kat = sorted(stat_kat.items(), key=lambda x: -x[1])
        total = sum(stat_kat.values()) or 1
        cols = st.columns(len(sorted_kat)) if len(sorted_kat) <= 4 else st.columns(4)
        for i, (kat, jumlah) in enumerate(sorted_kat[:4]):
            emoji = KATEGORI_EMOJI.get(kat, "📦")
            pct = int(jumlah / total * 100)
            with cols[i]:
                st.markdown(f"""
                <div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                        <span style="font-size:14px;">{emoji}</span>
                        <span style="font-size:13px;font-weight:500;color:#374151;">
                            {kat.replace("_"," ").title()}
                        </span>
                        <span style="margin-left:auto;font-size:13px;font-weight:600;
                                     color:#111827;">{jumlah}</span>
                    </div>
                    <div style="background:#E5E7EB;border-radius:99px;height:5px;">
                        <div style="background:#2563EB;height:5px;border-radius:99px;
                                    width:{pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:.75rem;'></div>", unsafe_allow_html=True)

    # ── Recent Reports ────────────────────────────────────────────────────────
    laporan = stats.get("laporan_terbaru", [])
    st.markdown('<div class="rf-table-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="rf-table-title">Recent Reports</div>',
        unsafe_allow_html=True
    )

    # Header
    h1, h2, h3, h4 = st.columns([3, 3, 2, 2])
    for col, label in zip([h1, h2, h3, h4], ["BARANG", "TIPE", "STATUS", "TANGGAL"]):
        with col:
            st.markdown(f'<div class="rf-th">{label}</div>', unsafe_allow_html=True)

    if laporan:
        for i, item in enumerate(laporan):
            emoji = KATEGORI_EMOJI.get(item.get("kategori", ""), "📦")
            tipe = item.get("tipe", "")
            status = item.get("status", "")
            is_last = i == len(laporan) - 1
            border = "none" if is_last else "1px solid #E5E7EB"

            r1, r2, r3, r4 = st.columns([3, 3, 2, 2])
            with r1:
                st.markdown(f"""
                <div style="padding:.7rem .9rem;border-bottom:{border};">
                    <div class="rf-td-name">{item['nama_barang']}</div>
                    <div class="rf-td-sub">📍 {item['lokasi']}</div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                st.markdown(f"""
                <div style="padding:.7rem .9rem;border-bottom:{border};">
                    <div class="rf-td" style="padding:0;">
                        {item['lokasi']}
                    </div>
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
    else:
        st.markdown("""
        <div class="rf-empty">
            <div class="rf-empty-icon">📋</div>
            <div class="rf-empty-text">Belum ada laporan</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Quick actions ─────────────────────────────────────────────────────────
    qa1, qa2 = st.columns(2)
    with qa1:
        if st.button("Laporkan Kehilangan", use_container_width=True, type="primary"):
            st.session_state.prefill_tipe = "hilang"
            st.session_state.page = "lapor"
            st.rerun()
    with qa2:
        if st.button("Laporkan Penemuan", use_container_width=True):
            st.session_state.prefill_tipe = "ditemukan"
            st.session_state.page = "lapor"
            st.rerun()