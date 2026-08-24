import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Simulator SNBP - Master PTN & ITB Special Engine",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎓 Simulator Rekomendasi PTN & Vokasi SNBP")
st.caption(
    "Analisis Kelolosan SNBP Kurikulum Merdeka — Terintegrasi Data Strata, Daya Tampung, & Sistem Fakultas ITB"
)
st.divider()

# ==========================================
# 2. MASTER DATA KHUSUS ITB (FAKULTAS/SEKOLAH S1)
# ==========================================
DATA_ITB_FAKULTAS = {
    "STEI-K (Sekolah Teknik Elektro dan Informatika - Komputasi)": {
        "strata": "S1",
        "daya_tampung": 120,
        "rumpun": "Teknologi & Komputer",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Informatika",
        "porto": False,
    },
    "STEI-R (Sekolah Teknik Elektro dan Informatika - Rekayasa)": {
        "strata": "S1",
        "daya_tampung": 150,
        "rumpun": "Teknologi & Elektro",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Fisika",
        "porto": False,
    },
    "FTTM (Fakultas Teknik Pertambangan dan Perminyakan)": {
        "strata": "S1",
        "daya_tampung": 160,
        "rumpun": "Kebumian & Energi",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Fisika",
        "porto": False,
    },
    "FTMD (Fakultas Teknik Mesin dan Dirgantara)": {
        "strata": "S1",
        "daya_tampung": 140,
        "rumpun": "Manufaktur & Dirgantara",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Fisika",
        "porto": False,
    },
    "FTSL (Fakultas Teknik Sipil dan Lingkungan)": {
        "strata": "S1",
        "daya_tampung": 150,
        "rumpun": "Infrastruktur & Lingkungan",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Fisika",
        "porto": False,
    },
    "FMIPA-M (Fakultas MIPA - Matematika)": {
        "strata": "S1",
        "daya_tampung": 80,
        "rumpun": "Sains & Aktuaria",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Matematika",
        "porto": False,
    },
    "FMIPA-A (Fakultas MIPA - Sains Alam)": {
        "strata": "S1",
        "daya_tampung": 110,
        "rumpun": "Fisika & Kimia",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Fisika",
        "porto": False,
    },
    "SITH-R (Sekolah Ilmu dan Teknologi Hayati - Rekayasa)": {
        "strata": "S1",
        "daya_tampung": 120,
        "rumpun": "Bioteknologi & Pertanian",
        "mapel_1": "Biologi",
        "mapel_2": "Kimia",
        "porto": False,
    },
    "SITH-S (Sekolah Ilmu dan Teknologi Hayati - Sains)": {
        "strata": "S1",
        "daya_tampung": 70,
        "rumpun": "Biologi Murni",
        "mapel_1": "Biologi",
        "mapel_2": "Kimia",
        "porto": False,
    },
    "FITB (Fakultas Ilmu dan Teknologi Kebumian)": {
        "strata": "S1",
        "daya_tampung": 130,
        "rumpun": "Geodesi & Oseanografi",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Fisika",
        "porto": False,
    },
    "FSRD (Fakultas Seni Rupa dan Desain)": {
        "strata": "S1",
        "daya_tampung": 110,
        "rumpun": "Seni & DKV",
        "mapel_1": "Seni Budaya",
        "mapel_2": "Informatika",
        "porto": True,
    },
    "SBM (Sekolah Bisnis dan Manajemen)": {
        "strata": "S1",
        "daya_tampung": 84,
        "rumpun": "Manajemen & Bisnis",
        "mapel_1": "Ekonomi",
        "mapel_2": "Matematika Lanjut",
        "porto": False,
    },
    "SAPPK (Sekolah Arsitektur, Perencanaan & Pengembangan Kebijakan)": {
        "strata": "S1",
        "daya_tampung": 90,
        "rumpun": "Arsitektur & PWK",
        "mapel_1": "Matematika Lanjut",
        "mapel_2": "Sosiologi",
        "porto": False,
    },
}

# ==========================================
# 3. LOADER & GENERATOR CSV MASTER PTN SELURUH INDONESIA
# ==========================================
CSV_FILE_PATH = "master_ptn_prodi.csv"

def init_master_csv():
    """Membuat CSV Sampel Master PTN jika belum ada"""
    if not os.path.exists(CSV_FILE_PATH):
        sample_data = [
            # UI
            {"provinsi": "Jawa Barat", "nama_ptn": "Universitas Indonesia (UI)", "nama_prodi": "Teknik Informatika", "strata": "S1", "daya_tampung": 60, "requires_portfolio": False},
            {"provinsi": "Jawa Barat", "nama_ptn": "Universitas Indonesia (UI)", "nama_prodi": "Sistem Informasi", "strata": "S1", "daya_tampung": 50, "requires_portfolio": False},
            {"provinsi": "Jawa Barat", "nama_ptn": "Universitas Indonesia (UI)", "nama_prodi": "Manajemen", "strata": "S1", "daya_tampung": 90, "requires_portfolio": False},
            # UGM
            {"provinsi": "DI Yogyakarta", "nama_ptn": "Universitas Gadjah Mada (UGM)", "nama_prodi": "Teknologi Informasi", "strata": "S1", "daya_tampung": 55, "requires_portfolio": False},
            {"provinsi": "DI Yogyakarta", "nama_ptn": "Universitas Gadjah Mada (UGM)", "nama_prodi": "Manajemen & Kebijakan Publik", "strata": "S1", "daya_tampung": 40, "requires_portfolio": False},
            # UNJ (DKI Jakarta)
            {"provinsi": "DKI Jakarta", "nama_ptn": "Universitas Negeri Jakarta (UNJ)", "nama_prodi": "Pendidikan Ilmu Komputer", "strata": "S1", "daya_tampung": 45, "requires_portfolio": False},
            {"provinsi": "DKI Jakarta", "nama_ptn": "Universitas Negeri Jakarta (UNJ)", "nama_prodi": "Desain Komunikasi Visual", "strata": "S1", "daya_tampung": 35, "requires_portfolio": True},
            # UPNVJ
            {"provinsi": "DKI Jakarta", "nama_ptn": "UPN Veteran Jakarta (UPNVJ)", "nama_prodi": "S1 Informatika", "strata": "S1", "daya_tampung": 72, "requires_portfolio": False},
            {"provinsi": "DKI Jakarta", "nama_ptn": "UPN Veteran Jakarta (UPNVJ)", "nama_prodi": "D4 Sistem Informasi", "strata": "D4", "daya_tampung": 40, "requires_portfolio": False},
            # PNJ (Vokasi)
            {"provinsi": "Jawa Barat", "nama_ptn": "Politeknik Negeri Jakarta (PNJ)", "nama_prodi": "D4 Teknik Informatika", "strata": "D4", "daya_tampung": 48, "requires_portfolio": False},
            {"provinsi": "Jawa Barat", "nama_ptn": "Politeknik Negeri Jakarta (PNJ)", "nama_prodi": "D3 Teknik Elektronika", "strata": "D3", "daya_tampung": 32, "requires_portfolio": False},
            # SV IPB
            {"provinsi": "Jawa Barat", "nama_ptn": "IPB University", "nama_prodi": "D4 Teknologi Rekayasa Komputer", "strata": "D4", "daya_tampung": 80, "requires_portfolio": False},
            # ITS & UNAIR
            {"provinsi": "Jawa Timur", "nama_ptn": "Institut Teknologi Sepuluh Nopember (ITS)", "nama_prodi": "Teknik Informatika", "strata": "S1", "daya_tampung": 90, "requires_portfolio": False},
            {"provinsi": "Jawa Timur", "nama_ptn": "Universitas Airlangga (UNAIR)", "nama_prodi": "Kedokteran", "strata": "S1", "daya_tampung": 75, "requires_portfolio": False},
        ]
        df = pd.DataFrame(sample_data)
        df.to_csv(CSV_FILE_PATH, index=False)

@st.cache_data
def load_ptn_database():
    init_master_csv()
    return pd.read_csv(CSV_FILE_PATH)

df_master_ptn = load_ptn_database()

# MAPEL TKA DICTIONARY
MAPEL_TKA_LIST = [
    "Matematika Lanjut", "Fisika", "Kimia", "Biologi", 
    "Pendidikan Jasmani, Olahraga dan Kesehatan (PJOK)", "Ekonomi", 
    "Geografi", "Sosiologi", "Sejarah", "Antropologi", "Pendidikan Pancasila", 
    "Seni Budaya", "Bahasa Indonesia Tingkat Lanjut", "Bahasa Inggris Tingkat Lanjut"
]

# ==========================================
# 4. SIDEBAR: PROFIL SEKOLAH & ALUMNI
# ==========================================
st.sidebar.header("🏫 Data Sekolah & Alumni")

jenjang_sekolah = st.sidebar.selectbox("Jenjang Sekolah", ["SMA/MA", "SMK"], index=0)
akreditasi_sekolah = st.sidebar.selectbox("Akreditasi Sekolah", ["A (Unggul)", "B (Baik)", "C (Cukup)"], index=0)
kkm_rapor = st.sidebar.number_input("Nilai KKM Rapor Sekolah", 60.0, 90.0, 75.0, 0.5)
sebaran_alumni = st.sidebar.number_input("Jumlah Sebaran Alumni di PTN Target (3 Thn Terakhir)", 0, 100, 3, 1)

st.sidebar.divider()
is_commuter = st.sidebar.checkbox("Preferensi Commuter (Tanpa Kos)", value=True)

# ==========================================
# 5. FORM TABS UTAMA
# ==========================================
tab1, tab2, tab3 = st.tabs(["📚 Nilai Rapor & TKA", "🎯 Target PTN / ITB", "🎨 Portofolio Karya"])

# --- TAB 1: NILAI RAPOR SEM 1-5 ---
with tab1:
    st.subheader("Input Rata-Rata Nilai Rapor Semester 1 s/d 5")
    c1, c2, c3, c4, c5 = st.columns(5)
    sem1 = c1.number_input("Semester 1", 0.0, 100.0, 83.0, 0.5)
    sem2 = c2.number_input("Semester 2", 0.0, 100.0, 84.0, 0.5)
    sem3 = c3.number_input("Semester 3", 0.0, 100.0, 85.5, 0.5)
    sem4 = c4.number_input("Semester 4", 0.0, 100.0, 87.0, 0.5)
    sem5 = c5.number_input("Semester 5", 0.0, 100.0, 88.5, 0.5)

    rata_sem_1_5 = (sem1 + sem2 + sem3 + sem4 + sem5) / 5.0
    st.info(f"📈 **Rata-Rata Rapor Umum (Sem 1-5):** `{rata_sem_1_5:.2f}`")

    # Chart Plotly
    sem_labels = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5"]
    sem_values = [sem1, sem2, sem3, sem4, sem5]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sem_labels, y=sem_values, mode="lines+markers+text", text=[f"{v:.1f}" for v in sem_values], textposition="top center", line=dict(color="#1E3A8A", width=3, shape="spline"), marker=dict(size=10, color="#FBBF24")))
    fig.update_layout(title="<b>Grafik Tren Kenaikan Nilai Rapor (Semester 1–5)</b>", yaxis=dict(range=[max(0, min(sem_values)-5), 100]), height=300, margin=dict(l=20, r=20, t=40, b=20), template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Mata Pelajaran TKA / Peminatan Utama")
    col_m1, col_m2 = st.columns(2)
    mapel_1 = col_m1.selectbox("Mapel Peminatan 1", MAPEL_TKA_LIST, index=0)
    n_mapel_1 = col_m1.number_input(f"Nilai {mapel_1}", 0.0, 100.0, 90.0, 0.5)
    mapel_2 = col_m2.selectbox("Mapel Peminatan 2", MAPEL_TKA_LIST, index=1)
    n_mapel_2 = col_m2.number_input(f"Nilai {mapel_2}", 0.0, 100.0, 88.0, 0.5)

# --- TAB 2: PILIHAN PTN / ITB ENGINE ---
with tab2:
    st.subheader("Pemilihan PTN, Strata, & Daya Tampung")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        provinsi_sekolah = st.selectbox("1. Provinsi Sekolah Asal Siswa", ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Lainnya"], index=0)
        
        # Opsi Pilihan PTN (Memisahkan Jalur Khusus ITB dengan PTN Umum)
        is_itb_mode = st.checkbox("🎯 Pilih Institut Teknologi Bandung (ITB)", value=True)
        
    with col_p2:
        if is_itb_mode:
            st.success("🏛️ **Sistem Seleksi Khusus ITB Terdeteksi**")
            itb_unit_selected = st.selectbox("2. Pilih Fakultas / Sekolah ITB (TPB)", list(DATA_ITB_FAKULTAS.keys()))
            
            # Detail Otomatis ITB
            itb_info = DATA_ITB_FAKULTAS[itb_unit_selected]
            selected_ptn_name = "Institut Teknologi Bandung (ITB)"
            selected_prodi_name = itb_unit_selected
            selected_strata = itb_info["strata"]
            selected_daya_tampung = itb_info["daya_tampung"]
            auto_porto_req = itb_info["porto"]
            
            st.markdown(f"""
            * **Jenjang/Strata:** `{selected_strata}` (TPB 1 Tahun)
            * **Daya Tampung SNBP:** `{selected_daya_tampung} Kursi`
            * **Mapel Pendukung Utama:** `{itb_info['mapel_1']}` & `{itb_info['mapel_2']}`
            """)
            st.caption("ℹ️ *Penjurusan ke prodi spesifik dilakukan pada tahun ke-2 berdasarkan IPK TPB.*")
            
        else:
            # Mode PTN Umum (Dari Master CSV)
            ptn_list = df_master_ptn["nama_ptn"].unique()
            selected_ptn_name = st.selectbox("2. Pilih PTN Target", ptn_list)
            
            df_prodi_filtered = df_master_ptn[df_master_ptn["nama_ptn"] == selected_ptn_name]
            selected_prodi_name = st.selectbox("3. Pilih Program Studi", df_prodi_filtered["nama_prodi"].unique())
            
            prodi_row = df_prodi_filtered[df_prodi_filtered["nama_prodi"] == selected_prodi_name].iloc[0]
            selected_strata = prodi_row["strata"]
            selected_daya_tampung = prodi_row["daya_tampung"]
            auto_porto_req = prodi_row["requires_portfolio"]
            
            st.markdown(f"""
            * **Jenjang/Strata:** `{selected_strata}`
            * **Daya Tampung SNBP:** `{selected_daya_tampung} Kursi`
            """)

# --- TAB 3: PORTOFOLIO ---
with tab3:
    st.subheader("Upload & Penilaian Portofolio")
    butuh_portofolio = st.checkbox("Prodi Target Mensyaratkan Portofolio?", value=auto_porto_req)
    skor_portofolio = 0.0
    if butuh_portofolio:
        st.file_uploader("Unggah File Portofolio (PDF/ZIP/MP4)", type=["pdf", "zip", "mp4", "png"])
        skor_portofolio = st.number_input("Estimasi Skor Evaluasi Portofolio (0-100)", 0.0, 100.0, 85.0, 1.0)

# ==========================================
# 6. EXECUTION ENGINE
# ==========================================
st.divider()

if st.button("🚀 Jalankan Analisis Kelolosan SNBP", type="primary", use_container_width=True):
    n_pendukung = (n_mapel_1 + n_mapel_2) / 2.0
    s_rapor = (0.50 * rata_sem_1_5) + (0.50 * n_pendukung)
    s_berkas = (0.50 * s_rapor) + (0.50 * skor_portofolio) if butuh_portofolio else s_rapor
    
    bobot_akreditasi = 25.0 if "A" in akreditasi_sekolah else (15.0 if "B" in akreditasi_sekolah else 5.0)
    margin_kkm = max(0.0, rata_sem_1_5 - kkm_rapor)
    indeks_alumni = min(100.0, (sebaran_alumni * 15.0) + bobot_akreditasi + (margin_kkm * 1.5))
    
    # Keketatan dinamis berdasarkan Daya Tampung
    keketatan_score = min(90.0, max(50.0, selected_daya_tampung * 0.6))
    
    s_total = (0.50 * s_berkas) + (0.35 * indeks_alumni) + (0.15 * keketatan_score)
    
    st.markdown("### 📊 Ringkasan Skor Kelayakan SNBP")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Rata Rapor Sem 1-5", f"{rata_sem_1_5:.2f}")
    res2.metric("Rata Mapel Pendukung", f"{n_pendukung:.2f}")
    res3.metric("Daya Tampung", f"{selected_daya_tampung} Kursi")
    res4.metric("SKOR TOTAL (S_total)", f"{s_total:.2f}")
    
    st.divider()
    
    if s_total >= 85.0:
        st.success(f"🟢 **SAFE ZONE (Sangat Aman):** Peluang kelolosan tinggi pada **{selected_prodi_name} ({selected_strata})** di **{selected_ptn_name}**.")
    elif s_total >= 75.0:
        st.warning(f"🟡 **RATIONAL ZONE (Prospektif):** Peluang rasional. Pastikan Pilihan 2 disiapkan jaring pengaman se-provinsi / Vokasi.")
    else:
        st.error(f"🔴 **HIGH RISK (Risiko Tinggi):** Skor total di bawah ambang batas aman. Disarankan pivot ke prodi lain atau jenjang Vokasi.")

    # Validasi Commuter DKI Jakarta
    if provinsi_sekolah == "DKI Jakarta" and is_commuter and "Jawa Barat" in selected_ptn_name or "ITB" in selected_ptn_name or "UI" in selected_ptn_name:
        st.info("💡 **Aturan Provinsi SNBP:** Karena PTN pilihan Anda berada di luar DKI Jakarta (misal: ITB/UI/PNJ), maka Pilihan 2 **WAJIB** memilih PTN yang berlokasi di DKI Jakarta (UNJ atau UPNVJ).")
