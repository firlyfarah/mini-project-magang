import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
import plotly.graph_objects as go
import base64
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Dashboard Keuangan BPSDM JATIM Bidang Fungsional ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIDEBAR STYLE
st.markdown("""
<style>
/* 1. Background Sidebar & Lebar */
[data-testid="stSidebar"] {
    background-color: #0b2a4a;
    width: 270px !important;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-headerNoPadding"] {
    color: white !important;
}

/* 3. Menghilangkan spasi antar elemen default Streamlit */
[data-testid="stSidebar"] .stElementContainer {
    margin-bottom: -15px !important; 
}

/* 4. Styling Dasar Tombol Menu */
[data-testid="stSidebar"] .stButton > button {
    background-color: transparent;
    color: #cbd5e1;
    border: none;
    width: 100%;
    text-align: left;
    padding: 8px 15px !important; 
    font-size: 15px;
    font-weight: 800 !important; 
    border-radius: 8px;
    display: flex;
    justify-content: flex-start;
    transition: all 0.2s;
}

/* 5. Efek Hover */
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
}

/* 6. Efek AKTIF 
div[data-active="true"] button {
    background-color: white !important; 
    color: #ff8c00 !important; 
    border: none !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
}

/* 7. Profile Box 
.profile-box {
    text-align: center;
    padding: 10px 0;
    margin-bottom: 30px;
}
.profile-box img {
    border-radius: 50%;
    width: 80px; 
    border: 2px solid rgba(255,255,255,0.2);
}
.profile-box h4 { color: white; font-size: 16px; margin-top: 10px; font-weight: bold; }
.profile-box p { color: #cbd5e1; font-size: 12px; margin-top: -5px; }

/* 8. Mengatur Garis Tipis (HR) */
hr {
    margin: 10px 0px 25px 0px !important; 
    border: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1) !important; 
}

/* Penyesuaian jarak antar tombol agar lebih rapat lagi */
[data-testid="stSidebar"] .stElementContainer {
    margin-bottom: -12px !important; 
}
            
/* Styling untuk Kotak/Card Dashboard */
.stMetric {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
}

    [data-testid="stHeader"] {
    background: rgba(0,0,0,0);
    color: rgba(0,0,0,0);
}

.main-title {
    margin-top: -80px !important; 
}

.chart-card {
    background-color: #ffffff;
    padding: 10px; 
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
    overflow: hidden; 
}

div[data-testid="stVerticalBlock"] > div[style*="border"] {
    background-color: white !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    padding: 20px !important;
}

/* CSS cadangan agar container st.container punya style kotak */
.styled-container {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #edf2f7;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
                     
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def set_page(page_name):
    st.session_state.page = page_name

# LOAD DATA

@st.cache_data
def load_data():
    return pd.read_csv("data_keuangan_clean_final.csv")

df = load_data()

#SIDEBAR
with st.sidebar:

    st.markdown("""
    <div class="profile-box">
        <img src="https://cdn-icons-png.flaticon.com/512/847/847969.png">
        <h4>Staf Keuangan</h4>
        <p>BPSDM Jatim</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Data Transaksi", "Scan Kwitansi", "Profile"], 
        icons=["speedometer2", "file-earmark-text", "qr-code-scan", "person-circle"], 
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {
                "padding": "0!important", "background-color": "#0B2A4A", "border-radius": "0px"
            },
            "icon": {
                "color": "#ffffff", "font-size": "18px"
            }, 
            "nav-link": {
                "font-size": "16px", "text-align": "left", "margin": "0px", "padding": "12px 15px","color": "#ffffff","--hover-color": "rgba(255,255,255,0.1)","white-space": "nowrap"        
            },
            "nav-link-selected": {
                "background-color": "#ffffff19", "color": "#FFFFFF", "font-weight": "600","border-radius": "8px", "margin": "5px 10px",            
            }
        }
    )
    st.session_state.page = selected

st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# DASHBOARD
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
    .stMetric { background-color: #f8fafc; padding: 5px; border-radius: 5px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

if st.session_state.page == "Dashboard":
    img_base64 = get_base64_of_bin_file("assets/logo_bpsdm_jatim.png")

    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 80px; margin-right: 25px;">
            <div>
                <h2 style="margin: 0; color: #1e3a8a; font-size: 30px; font-weight: 800; line-height: 1.2;">
                    Dashboard Monitoring Keuangan BPSDM JATIM
                </h2>
                <p style="margin: 0; color: #64748b; font-size: 16px; font-weight: 500;">
                    Bidang Pengembangan Kompetensi Fungsional dan Sosial Kultural
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    list_bulan = ["Semua Bulan"] + list(df["BULAN"].unique())
    selected_bulan = st.selectbox("Pilih Periode", list_bulan)
    df_f = df.copy() if selected_bulan == "Semua Bulan" else df[df["BULAN"] == selected_bulan].copy()

    m1, m2, m3, m4 = st.columns(4)
    tp = df_f[['PAJAK_PPH_21_5/15%', 'PAJAK_PPH_22_1,5%', 'PAJAK_PPH_23_2%', 'PAJAK_PPN_11/12%']].sum().sum()
    m1.metric("TOTAL SPJ", f"Rp {df_f['NOMINAL_SPJ'].sum():,.0f}")
    m2.metric("TOTAL TRANSFER", f"Rp {df_f['NOMINAL_TRANSFER'].sum():,.0f}")
    m3.metric("JUMLAH TRANSAKSI", f"{df_f.shape[0]} Nota")
    m4.metric("TOTAL PAJAK", f"Rp {tp:,.0f}")

    c1, c2, c3 = st.columns([3.5, 3, 3.5])

    with c1:
        with st.container(border=True):
            df_rek = df_f.groupby("KODE_REKENING_KET")["NOMINAL_SPJ"].sum().reset_index().sort_values("NOMINAL_SPJ")
            fig_bar = px.bar(df_rek.tail(8), x="NOMINAL_SPJ", y="KODE_REKENING_KET", 
                             orientation='h', title="<b>10 Alokasi Terbesar</b>",
                             color="NOMINAL_SPJ", color_continuous_scale='Blues')
            fig_bar.update_xaxes(title_text="") 
            fig_bar.update_yaxes(title_text="")
            fig_bar.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with c2:
        with st.container(border=True):
            pajak_vals = [df_f['PAJAK_PPH_21_5/15%'].sum(), df_f['PAJAK_PPH_22_1,5%'].sum(), 
                          df_f['PAJAK_PPH_23_2%'].sum(), df_f['PAJAK_PPN_11/12%'].sum()]
            df_p = pd.DataFrame({'Jenis': ['PPh 21', 'PPh 22', 'PPh 23', 'PPN'], 'Nilai': pajak_vals})
            fig_pie = px.pie(df_p[df_p['Nilai']>0], values='Nilai', names='Jenis', hole=0.5, 
                             title="<b>Komposisi Pajak</b>",
                             color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_pie.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=50), 
                                  legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
            st.plotly_chart(fig_pie, use_container_width=True)

    with c3:
        with st.container(border=True):
            df_sun = df_f.dropna(subset=['SUB_KEGIATAN']).copy()
            df_sun_agg = df_sun.groupby(['SUB_KEGIATAN'])['NOMINAL_SPJ'].sum().reset_index()
            fig_sun = px.sunburst(df_sun_agg, path=['SUB_KEGIATAN'], values='NOMINAL_SPJ',
                                  title="<b>Sub Kegiatan</b>", color='NOMINAL_SPJ', 
                                  color_continuous_scale='Blues')
            fig_sun.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_sun, use_container_width=True)

    c4, c5 = st.columns([7, 3])

    with c4:
        with st.container(border=True):
            df_trend = df_f.groupby("TANGGAL_KWITANSI")[["NOMINAL_SPJ"]].sum().reset_index()
            fig_trend = px.area(df_trend, x="TANGGAL_KWITANSI", y="NOMINAL_SPJ", title="<b>Tren Realisasi</b>")
            fig_bar.update_xaxes(title_text="") 
            fig_bar.update_yaxes(title_text="")
            fig_trend.update_traces(line_color='#1e40af')
            fig_trend.update_layout(height=229, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_trend, use_container_width=True)

    with c5:
            with st.container(border=True):
                st.markdown("<small><b>Top 5 Transaksi</b></small>", unsafe_allow_html=True)
                top_5 = df_f.nlargest(5, 'NOMINAL_SPJ')[['NAMA', 'NOMINAL_SPJ']]
                st.dataframe(top_5, use_container_width=True, hide_index=True, height=180)


# HALAMAN DATA TRANSAKSI
elif st.session_state.page == "Data Transaksi":

    img_base64 = get_base64_of_bin_file("assets/logo_bpsdm_jatim.png")

    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 80px; margin-right: 25px;">
            <div>
                <h2 style="margin: 0; color: #1e3a8a; font-size: 30px; font-weight: 800; line-height: 0;">
                    Data Transaksi Terintegrasi
                </h2>
                <p style="margin: 0; color: #64748b; font-size: 16px; font-weight: 500;">
                    Bidang Pengembangan Kompetensi Fungsional dan Sosial Kultural
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    search_query = st.text_input("Cari data (Nama, Kegiatan, Nominal, atau Keterangan lainnya...)", placeholder="Ketik kata kunci di sini...")

    if search_query:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)
        df_filtered = df[mask]
        
        st.write(f"Menampilkan {len(df_filtered)} hasil pencarian untuk: **'{search_query}'**")
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.write(f"Menampilkan semua data ({len(df)} transaksi)")
        st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data Lengkap (CSV)",
        data=csv,
        file_name='data_transaksi_bpsdm.csv',
        mime='text/csv',
    )

# HALAMAN SCAN KWITANSI
elif st.session_state.page == "Scan Kwitansi":
    img_base64 = get_base64_of_bin_file("assets/logo_bpsdm_jatim.png")
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 80px; margin-right: 25px;">
            <div>
                <h2 style="margin: 0; color: #1e3a8a; font-size: 30px; font-weight: 800;">Scan Kwitansi</h2>
                <p style="margin: 0; color: #64748b; font-size: 14px;">Bidang Pengembangan Kompetensi Fungsional dan Sosial Kultural</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    folder = "data/scan_kwitansi"
    os.makedirs(folder, exist_ok=True)

    with st.expander("📤 Upload File Baru", expanded=True):
        bulan_upload = st.selectbox("Simpan ke Periode Bulan:", df["BULAN"].unique(), key="upload_month")
        uploaded_files = st.file_uploader("Pilih PDF Kwitansi", type="pdf", accept_multiple_files=True)

        if st.button("Simpan File"):
            if uploaded_files:
                for file in uploaded_files:
                    new_filename = f"{bulan_upload}_{file.name}"
                    save_path = os.path.join(folder, new_filename)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                st.success(f"✅ {len(uploaded_files)} File berhasil diupload ke periode {bulan_upload}")
                st.rerun() 

    st.divider()

    # filter
    st.markdown("### 🔍 Daftar Arsip Kwitansi")
    c1, c2 = st.columns(2)
    with c1:
        list_bulan = ["Semua Bulan"] + list(df["BULAN"].unique())
        bulan_search = st.selectbox("Filter Berdasarkan Bulan", list_bulan)
    with c2:
        kode_search = st.text_input("Cari Nama File / Kode")

    if os.path.exists(folder):
        files = os.listdir(folder)
        
        hasil = []
        for f in files:
            match_bulan = (bulan_search == "Semua Bulan") or (bulan_search.lower() in f.lower())
            match_kode = kode_search.lower() in f.lower()
            
            if match_bulan and match_kode:
                hasil.append(f)

        if hasil:
            st.write(f"Ditemukan {len(hasil)} file:")
            for f in hasil:
                col_icon, col_name, col_btn = st.columns([1, 8, 2])
                col_icon.write("📄")
                display_name = f.split("_", 1)[-1] if "_" in f else f
                col_name.write(display_name)

                with open(os.path.join(folder, f), "rb") as pdf_file:
                    col_btn.download_button(
                        label="Buka/Unduh",
                        data=pdf_file,
                        file_name=display_name,
                        mime="application/pdf",
                        key=f 
                    )
        else:
            st.warning("⚠️ Tidak ada kwitansi yang ditemukan untuk kriteria ini.")
    else:
        st.info("Folder penyimpanan masih kosong.")

# HALAMAN PROFILE

elif st.session_state.page == "Profile":
    img_base64 = get_base64_of_bin_file("assets/logo_bpsdm_jatim.png")
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 80px; margin-right: 25px;">
            <div>
                <h2 style="margin: 0; color: #1e3a8a; font-size: 30px; font-weight: 800; line-height: 0;">
                    Profile Pengguna
                </h2>
                <p style="margin: 0; color: #64748b; font-size: 16px; font-weight: 500;">
                    Bidang Pengembangan Kompetensi Fungsional dan Sosial Kultural
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    with st.container(border=True):
        col_img, col_info = st.columns([1, 3])
        
        with col_img:
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                    <div style="width: 120px; height: 120px; background-color: #0B2A4A; border-radius: 50%; 
                                display: flex; justify-content: center; align-items: center; color: white; font-size: 50px;">
                        SK
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"""
                <div style="padding-left: 20px;">
                    <h3 style="margin-bottom: 0px; color: #0B2A4A;">Staf Keuangan</h3>
                    <p style="color: #64748b; font-size: 16px; margin-top: 5px;">BPSDM Provinsi Jawa Timur</p>
                    <hr style="margin: 15px 0;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 15px;">
                        <tr>
                            <td style="padding: 8px 0; color: #64748b; width: 30%;"><b>Unit Kerja</b></td>
                            <td style="padding: 8px 0; color: #0B2A4A;">: Bidang Pengembangan Kompetensi Fungsional & Sosial Kultural</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #64748b;"><b>Jabatan</b></td>
                            <td style="padding: 8px 0; color: #0B2A4A;">: Pengelola Keuangan</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #64748b;"><b>Status Akun</b></td>
                            <td style="padding: 8px 0;"><span style="background-color: #dcfce7; color: #166534; padding: 3px 10px; border-radius: 12px; font-size: 12px;">Aktif</span></td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Input Hari Ini", "12 Nota")
    with c2:
        st.metric("Terakhir Login", "08:15 WIB")
    with c3:
        total_data = len(df)
        st.metric("Total Database", f"{total_data} Transaksi")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Keluar Aplikasi", use_container_width=True):
        st.toast("Menghapus sesi...", icon="⏳")
