import streamlit as st

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="Rekomendasi PTN SNBP - Nurul Fikri",
    page_icon="🎓",
    layout="wide"
)

# Title & Deskripsi
st.title("🎓 Simulator Rekomendasi PTN SNBP")
st.subheader("Kurikulum Merdeka — Rumpun S1 & Vokasi (D4/D3)")
st.caption("Aplikasi Analisis Kelolosan & Mitigasi Risiko Siswa - Nurul Fikri")
st.divider()

# 2. SIDEBAR: DATA SISWA & PREFERENSI LOKASI
st.sidebar.header("👤 Profile Siswa & Sekolah")
nama_siswa = st.sidebar.text_input("Nama Siswa", "Ahmad Fikri")
asal_provinsi = st.sidebar.selectbox(
    "Provinsi Sekolah Asal", 
    ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Lainnya"]
)

st.sidebar.divider()
st.sidebar.header("⚙️ Preferensi Khusus")
is_commuter = st.sidebar.checkbox(
    "Preferensi Commuter (Tidak Ingin Kos)", 
    value=True,
    help="Aktifkan jika siswa hanya ingin kuliah di PTN yang terjangkau transportasi harian."
)

# 3. AREA INPUT FORM UTAMA
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📚 1. Nilai Rapor & Peminatan")
    n_wajib = st.number_input(
        "Rata-Rata Nilai Mapel Wajib (Sem 1-5)", 
        min_value=0.0, max_value=100.0, value=85.0, step=0.5
    )
    
    st.markdown("**Mata Pelajaran Peminatan Utama:**")
    mapel_1 = st.selectbox(
        "Mapel Peminatan 1", 
        ["Matematika Lanjut", "Informatika", "Fisika", "Sosiologi", "Ekonomi", "Bahasa Inggris Lanjut", "Seni Rupa"]
    )
    n_mapel_1 = st.number_input(f"Nilai {mapel_1}", min_value=0.0, max_value=100.0, value=90.0, step=0.5)
    
    mapel_2 = st.selectbox(
        "Mapel Peminatan 2", 
        ["Informatika", "Matematika Lanjut", "Fisika", "Sosiologi", "Ekonomi", "Bahasa Inggris Lanjut", "Seni Rupa"]
    )
    n_mapel_2 = st.number_input(f"Nilai {mapel_2}", min_value=0.0, max_value=100.0, value=88.0, step=0.5)

with col_right:
    st.markdown("### 🎯 2. Target PTN & Indeks Sekolah")
    ptn_target = st.selectbox(
        "PTN Target (Pilihan 1)", 
        [
            "Universitas Indonesia (UI) - Jawa Barat", 
            "Universitas Negeri Jakarta (UNJ) - DKI Jakarta", 
            "UPN Veteran Jakarta (UPNVJ) - DKI Jakarta", 
            "Institut Teknologi Bandung (ITB) - Jawa Barat", 
            "Politeknik Negeri Jakarta (PNJ) - Jawa Barat",
            "IPB University (SV IPB) - Jawa Barat"
        ]
    )
    prodi_target = st.text_input("Nama Prodi / Fakultas", "Teknik Informatika / STEI-K")
    
    st.markdown("**Variabel Indeks Sekolah:**")
    indeks_alumni = st.slider("Indeks Alumni Sekolah di PTN ini (0-100)", 0, 100, 75)
    keketatan = st.slider("Indeks Keketatan Prodi Target (0-100)", 0, 100, 70)

# 4. BOTON DAN LOGIKA KALKULASI SCORING
st.divider()
if st.button("🚀 Jalankan Analisis Kelolosan", type="primary", use_container_width=True):
    
    # Formula Rata-Rata Rapor (50% Umum + 50% Pendukung)
    n_seluruh = (n_wajib + n_mapel_1 + n_mapel_2) / 3
    n_pendukung = (n_mapel_1 + n_mapel_2) / 2
    s_rapor = (0.50 * n_seluruh) + (0.50 * n_pendukung)
    
    # Formula Skor Total SNBP (50% Rapor + 35% Alumni + 15% Keketatan)
    s_total = (0.50 * s_rapor) + (0.35 * indeks_alumni) + (0.15 * keketatan)
    
    # Display Metrik Hasil Perhitungan
    st.markdown("### 📊 Ringkasan Skor Kelayakan")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rata Umum Rapor", f"{n_seluruh:.2f}")
    m2.metric("Rata Mapel Pendukung", f"{n_pendukung:.2f}")
    m3.metric("Skor Rapor (S_rapor)", f"{s_rapor:.2f}")
    m4.metric("SKOR TOTAL (S_total)", f"{s_total:.2f}")
    
    st.divider()
    
    # Penentuan Risk Zone Status
    if s_total >= 85.0:
        st.success(f"🟢 **SAFE ZONE (Sangat Aman):** Peluang kelolosan tinggi untuk **{nama_siswa}** pada prodi **{prodi_target}** di **{ptn_target}**.")
    elif s_total >= 75.0:
        st.warning(f"🟡 **RATIONAL ZONE (Prospektif):** Peluang rasional. Pastikan Pilihan 2 disiapkan jaring pengaman (Safe Zone se-provinsi / Vokasi).")
    else:
        st.error(f"🔴 **HIGH RISK (Risiko Tinggi):** Skor total belum memenuhi ambang aman. Disarankan melakukan *pivot* prodi/PTN atau beralih ke jenjang Vokasi (D4/D3).")

    # Peringatan Khusus Aturan Commuter & Aturan Provinsi DKI Jakarta
    if asal_provinsi == "DKI Jakarta" and is_commuter:
        if "UI" in ptn_target or "PNJ" in ptn_target or "ITB" in ptn_target:
            st.info(
                "💡 **Catatan Aturan SNBP untuk Siswa DKI Jakarta:**\n"
                f"PTN pilihan Anda ({ptn_target}) secara administratif berlokasi di **luar Provinsi DKI Jakarta**.\n\n"
                " Sesuai aturan SNBP, jika Anda mengambil 2 pilihan, maka **Pilihan 2 WAJIB memilih PTN di DKI Jakarta** (misal: UNJ atau UPNVJ)."
            )