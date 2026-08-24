import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Simulator SNBP 38 Provinsi - Nurul Fikri",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎓 Simulator Rekomendasi PTN SNBP (38 Provinsi)")
st.caption(
    "Analisis Kelolosan SNBP Kurikulum Merdeka & Vokasi — PTN Resmi SNPMB"
)
st.divider()

# ==========================================
# 2. DATA MASTER MAPEL TKA (SMA/MA & SMK)
# ==========================================
MAPEL_TKA = {
    "SMA/MA": {
        "wajib": ["Matematika", "Bahasa Indonesia", "Bahasa Inggris"],
        "peminatan": [
            "Matematika Lanjut",
            "Fisika",
            "Kimia",
            "Biologi",
            "Pendidikan Jasmani, Olahraga dan Kesehatan (PJOK)",
            "Ekonomi",
            "Geografi",
            "Sosiologi",
            "Sejarah",
            "Antropologi",
            "Pendidikan Pancasila",
            "Pendidikan Kewarganegaraan (PKn)",
            "Seni Budaya",
            "Bahasa Indonesia Tingkat Lanjut",
            "Bahasa Inggris Tingkat Lanjut",
            "Bahasa Arab",
            "Bahasa Jerman",
            "Bahasa Prancis",
            "Bahasa Jepang",
            "Bahasa Korea",
            "Bahasa Mandarin",
        ],
    },
    "SMK": {
        "wajib": ["Matematika", "Bahasa Indonesia", "Bahasa Inggris"],
        "peminatan": [
            "Agribisnis perikanan",
            "Agribisnis tanaman",
            "Agribisnis ternak",
            "Agroteknologi pengolahan hasil pertanian",
            "Akuntansi dan keuangan lembaga",
            "Animasi",
            "Broadcasting dan perfilman",
            "Busana",
            "Desain dan produksi kriya",
            "Desain komunikasi visual",
            "Desain permodelan dan informasi bangunan",
            "Kecantikan dan spa",
            "Kehutanan",
            "Kimia analisis",
            "Konstruksi dan perawatan bangunan sipil",
            "Kuliner",
            "Layanan kesehatan",
            "Manajemen perkantoran dan layanan bisnis",
            "Nautika kapal niaga",
            "Nautika kapal penangkapan ikan",
            "Pekerjaan sosial",
            "Pemasaran",
            "Pengembangan perangkat lunak dan gim",
            "Perhotelan",
            "Produk atau projek kreatif dan kewirausahaan",
            "Seni pertunjukan",
            "Seni rupa",
            "Teknik elektronika",
            "Teknik energi terbarukan",
            "Teknik furnitur",
            "Teknik geologi pertambangan",
            "Teknik geospasial",
            "Teknik jaringan komputer dan telekomunikasi",
            "Teknik ketenagalistrikan",
            "Teknik kimia industri",
            "Teknik konstruksi dan perumahan",
            "Teknik konstruksi kapal",
            "Teknik laboratorium medik",
            "Teknik logistik",
            "Teknik mesin",
            "Teknik otomotif",
            "Teknik pengelasan dan fabrikasi logam",
            "Teknik perawatan gedung",
            "Teknik perminyakan",
            "Teknik pesawat udara",
            "Teknik tekstil",
            "Teknik kapal niaga",
            "Teknik kapal penangkap ikan",
            "Teknologi farmasi",
            "Usaha layanan pariwisata",
            "Usaha pertanian terpadu.",
        ],
    },
}

# ==========================================
# 3. DATA MASTER 38 PROVINSI & PTN SNPMB
# ==========================================
DATA_PTN_38_PROVINSI = {
    "Aceh": [
        "Universitas Syiah Kuala (USK)",
        "Universitas Malikussaleh (UNIMAL)",
        "Universitas Teuku Umar (UTU)",
        "Universitas Samudra (UNSAM)",
        "ISBI Aceh",
        "Politeknik Negeri Lhokseumawe",
        "UIN Ar-Raniry",
    ],
    "Sumatera Utara": [
        "Universitas Sumatera Utara (USU)",
        "Universitas Negeri Medan (UNIMED)",
        "Politeknik Negeri Medan",
        "UIN Sumatera Utara",
    ],
    "Sumatera Barat": [
        "Universitas Andalas (UNAND)",
        "Universitas Negeri Padang (UNP)",
        "ISI Padangpanjang",
        "Politeknik Negeri Padang",
        "Politeknik Pertanian Negeri Payakumbuh",
        "UIN Imam Bonjol",
    ],
    "Riau": [
        "Universitas Riau (UNRI)",
        "UIN Sultan Syarif Kasim (UIN Suska)",
        "Politeknik Negeri Bengkalis",
    ],
    "Kepulauan Riau": [
        "Universitas Maritim Raja Ali Haji (UMRAH)",
        "Politeknik Negeri Batam",
    ],
    "Jambi": ["Universitas Jambi (UNJA)", "UIN Sulthan Thaha Saifuddin"],
    "Sumatera Selatan": [
        "Universitas Sriwijaya (UNSRI)",
        "Politeknik Negeri Sriwijaya",
        "UIN Raden Fatah",
    ],
    "Bangka Belitung": [
        "Universitas Bangka Belitung (UBB)",
        "Politeknik Manufaktur Negeri Bangka Belitung",
    ],
    "Bengkulu": ["Universitas Bengkulu (UNIB)", "UIN Fatmawati Sukarno"],
    "Lampung": [
        "Universitas Lampung (UNILA)",
        "Institut Teknologi Sumatera (ITERA)",
        "Politeknik Negeri Lampung",
        "UIN Raden Intan",
    ],
    "DKI Jakarta": [
        "Universitas Negeri Jakarta (UNJ)",
        "UPN Veteran Jakarta (UPNVJ)",
        "UIN Syarif Hidayatullah Jakarta",
    ],
    "Jawa Barat": [
        "Universitas Indonesia (UI)",
        "Institut Teknologi Bandung (ITB)",
        "Universitas Padjadjaran (UNPAD)",
        "IPB University (SV & S1)",
        "ISBI Bandung",
        "Politeknik Negeri Bandung (POLBAN)",
        "Politeknik Negeri Subang",
        "Politeknik Negeri Indramayu",
        "UIN Sunan Gunung Djati",
    ],
    "Jawa Tengah": [
        "Universitas Diponegoro (UNDIP)",
        "Universitas Sebelas Maret (UNS)",
        "Universitas Negeri Semarang (UNNES)",
        "Universitas Jenderal Soedirman (UNSOED)",
        "ISI Surakarta",
        "Politeknik Negeri Semarang (POLINES)",
        "Politeknik Negeri Cilacap",
        "UIN Walisongo",
        "UIN Raden Mas Said",
    ],
    "DI Yogyakarta": [
        "Universitas Gadjah Mada (UGM)",
        "Universitas Negeri Yogyakarta (UNY)",
        "UPN Veteran Yogyakarta (UPNYK)",
        "ISI Yogyakarta",
        "UIN Sunan Kalijaga",
    ],
    "Jawa Timur": [
        "Universitas Airlangga (UNAIR)",
        "Institut Teknologi Sepuluh Nopember (ITS)",
        "Universitas Brawijaya (UB)",
        "Universitas Negeri Malang (UM)",
        "Universitas Jember (UNEJ)",
        "UPN Veteran Jawa Timur",
        "Universitas Trunojoyo Madura (UTM)",
        "Politeknik Negeri Malang (POLINEMA)",
        "Politeknik Negeri Jember (POLIJE)",
        "Politeknik Perkapalan Negeri Surabaya (PPNS)",
        "Politeknik Elektronika Negeri Surabaya (PENS)",
        "UIN Sunan Ampel",
        "UIN Maulana Malik Ibrahim",
    ],
    "Banten": ["Universitas Sultan Ageng Tirtayasa (UNTIRTA)", "UIN SMH Banten"],
    "Bali": [
        "Universitas Udayana (UNUD)",
        "Universitas Pendidikan Ganesha (UNDIKSHA)",
        "ISI Denpasar",
        "Politeknik Negeri Bali",
    ],
    "Nusa Tenggara Barat": [
        "Universitas Mataram (UNRAM)",
        "UIN Mataram",
    ],
    "Nusa Tenggara Timur": [
        "Universitas Nusa Cendana (UNDANA)",
        "Politeknik Negeri Kupang",
        "Politeknik Pertanian Negeri Kupang",
    ],
    "Kalimantan Barat": [
        "Universitas Tanjungpura (UNTAN)",
        "Politeknik Negeri Pontianak",
        "Politeknik Negeri Sambas",
        "Politeknik Negeri Ketapang",
    ],
    "Kalimantan Tengah": [
        "Universitas Palangka Raya (UPR)",
        "IAIN Palangka Raya",
    ],
    "Kalimantan Selatan": [
        "Universitas Lambung Mangkurat (ULM)",
        "Politeknik Negeri Banjarmasin",
        "Politeknik Negeri Tanah Laut",
    ],
    "Kalimantan Timur": [
        "Universitas Mulawarman (UNMUL)",
        "Institut Teknologi Kalimantan (ITK)",
        "Politeknik Negeri Samarinda",
        "Politeknik Pertanian Negeri Samarinda",
    ],
    "Kalimantan Utara": ["Universitas Borneo Tarakan (UBT)"],
    "Sulawesi Utara": [
        "Universitas Sam Ratulangi (UNSRAT)",
        "Universitas Negeri Manado (UNIMA)",
        "Politeknik Negeri Manado",
        "Politeknik Negeri Nusa Utara",
    ],
    "Sulawesi Tengah": ["Universitas Tadulako (UNTAD)", "UIN Datokarama"],
    "Sulawesi Selatan": [
        "Universitas Hasanuddin (UNHAS)",
        "Universitas Negeri Makassar (UNM)",
        "Politeknik Negeri Ujung Pandang",
        "Politeknik Pertanian Negeri Pangkajene Kepulauan",
        "UIN Alauddin",
    ],
    "Sulawesi Tenggara": ["Universitas Halu Oleo (UHO)", "IAIN Kendari"],
    "Gorontalo": ["Universitas Negeri Gorontalo (UNG)"],
    "Sulawesi Barat": ["Universitas Sulawesi Barat (UNSULBAR)"],
    "Maluku": [
        "Universitas Pattimura (UNPATTI)",
        "Politeknik Negeri Ambon",
        "Politeknik Perikanan Negeri Tual",
    ],
    "Maluku Utara": ["Universitas Khairun (UNKHAIR)"],
    "Papua": ["Universitas Cenderawasih (UNCEN)", "ISBI Tanah Papua"],
    "Papua Barat": [
        "Universitas Papua (UNIPA)",
        "Politeknik Negeri Fakfak",
    ],
    "Papua Barat Daya": [
        "Universitas Papua (Kampus Sorong)",
        "IAIN Sorong",
    ],
    "Papua Tengah": ["Universitas Cenderawasih (PDD Nabire)"],
    "Papua Pegunungan": ["Universitas Cenderawasih (PDD Jayawijaya)"],
    "Papua Selatan": ["Universitas Musamus Merauke (UNMUS)"],
}

# ==========================================
# 4. SIDEBAR: PROFIL SEKOLAH & ALUMNI
# ==========================================
st.sidebar.header("🏫 Data Sekolah & Alumni")

jenjang_sekolah = st.sidebar.selectbox("Jenjang Sekolah", ["SMA/MA", "SMK"], index=0)

akreditasi_sekolah = st.sidebar.selectbox(
    "Akreditasi Sekolah", ["A (Unggul)", "B (Baik)", "C (Cukup)"], index=0
)
kkm_rapor = st.sidebar.number_input(
    "Nilai KKM Rapor Sekolah",
    min_value=60.0,
    max_value=90.0,
    value=75.0,
    step=0.5,
)
sebaran_alumni = st.sidebar.number_input(
    "Jumlah Sebaran Alumni di PTN Target (3 Thn Terakhir)",
    min_value=0,
    max_value=100,
    value=3,
    step=1,
)

st.sidebar.divider()
is_commuter = st.sidebar.checkbox(
    "Preferensi Commuter (Tanpa Kos)", value=True
)

# ==========================================
# 5. AREA FORM UTAMA (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(
    ["📚 Nilai Rapor & TKA", "🎯 Target PTN 38 Provinsi", "🎨 Portofolio Karya"]
)

# --- TAB 1: INPUT NILAI RAPOR SEMESTER 1 - 5 & MAPEL TKA ---
with tab1:
    st.subheader("Input Rata-Rata Nilai Rapor Semester 1 s/d 5")
    st.caption("Masukkan nilai rata-rata pengetahuan untuk seluruh mata pelajaran per semester.")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        sem1 = st.number_input("Semester 1", min_value=0.0, max_value=100.0, value=83.0, step=0.5)
    with c2:
        sem2 = st.number_input("Semester 2", min_value=0.0, max_value=100.0, value=84.0, step=0.5)
    with c3:
        sem3 = st.number_input("Semester 3", min_value=0.0, max_value=100.0, value=85.5, step=0.5)
    with c4:
        sem4 = st.number_input("Semester 4", min_value=0.0, max_value=100.0, value=87.0, step=0.5)
    with c5:
        sem5 = st.number_input("Semester 5", min_value=0.0, max_value=100.0, value=88.5, step=0.5)

    rata_sem_1_5 = (sem1 + sem2 + sem3 + sem4 + sem5) / 5.0
    st.info(f"📈 **Rata-Rata Rapor Umum (Sem 1-5):** `{rata_sem_1_5:.2f}`")

    # Visualisasi Plotly Tren Nilai Rapor
    sem_labels = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5"]
    sem_values = [sem1, sem2, sem3, sem4, sem5]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=sem_labels,
            y=sem_values,
            mode="lines+markers+text",
            text=[f"{v:.1f}" for v in sem_values],
            textposition="top center",
            line=dict(color="#1E3A8A", width=3, shape="spline"),
            marker=dict(size=10, color="#FBBF24", line=dict(width=2, color="#1E3A8A")),
            name="Nilai Rapor",
        )
    )
    min_y = max(0, min(sem_values) - 5)
    fig.update_layout(
        title="<b>Grafik Tren Kenaikan Nilai Rapor (Semester 1–5)</b>",
        xaxis_title="Semester",
        yaxis_title="Rata-Rata Nilai",
        yaxis=dict(range=[min_y, 100]),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader(f"Mata Pelajaran TKA / Peminatan ({jenjang_sekolah})")
    st.caption("Daftar mata pelajaran disesuaikan otomatis dengan jenjang yang dipilih pada sidebar.")

    daftar_peminatan = MAPEL_TKA[jenjang_sekolah]["peminatan"]

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        mapel_1 = st.selectbox("Mapel Peminatan 1", daftar_peminatan, index=0)
        n_mapel_1 = st.number_input(
            f"Nilai Rata-Rata {mapel_1}",
            min_value=0.0,
            max_value=100.0,
            value=90.0,
            step=0.5,
        )
    with col_m2:
        idx_default_2 = 1 if len(daftar_peminatan) > 1 else 0
        mapel_2 = st.selectbox("Mapel Peminatan 2", daftar_peminatan, index=idx_default_2)
        n_mapel_2 = st.number_input(
            f"Nilai Rata-Rata {mapel_2}",
            min_value=0.0,
            max_value=100.0,
            value=88.0,
            step=0.5,
        )

# --- TAB 2: PILIH PROVINSI & PTN TARGET ---
with tab2:
    st.subheader("Pemilihan PTN & Prodi Berdasarkan Provinsi SNPMB")

    col_prov, col_ptn = st.columns(2)
    with col_prov:
        provinsi_sekolah = st.selectbox(
            "1. Provinsi Sekolah Asal Siswa",
            list(DATA_PTN_38_PROVINSI.keys()),
            index=10,  # Default DKI Jakarta
        )
        provinsi_ptn_target = st.selectbox(
            "2. Provinsi PTN Target",
            list(DATA_PTN_38_PROVINSI.keys()),
            index=11,  # Default Jawa Barat
        )

    with col_ptn:
        daftar_ptn_tersedia = DATA_PTN_38_PROVINSI[provinsi_ptn_target]
        ptn_terpilih = st.selectbox("3. Pilih PTN Target", daftar_ptn_tersedia)
        prodi_terpilih = st.text_input(
            "4. Nama Program Studi Target", value="Teknik Informatika"
        )
        jenjang_prodi = st.radio(
            "Jenjang Studi", ["S1 (Akademik)", "D4 (Sarjana Terapan)", "D3 (Diploma)"], horizontal=True
        )

# --- TAB 3: UPLOAD PORTOFOLIO ---
with tab3:
    st.subheader("Upload & Penilaian Portofolio (Khusus Seni & Olahraga)")
    butuh_portofolio = st.checkbox(
        "Prodi Target Mensyaratkan Portofolio? (DKV, Seni Rupa, Olahraga, Musik, Tari, dll.)"
    )

    skor_portofolio = 0.0
    if butuh_portofolio:
        kategori_porto = st.selectbox(
            "Kategori Portofolio",
            [
                "Seni Rupa, Desain, dan Kriya (DKV/Seni Murni)",
                "Olahraga & Pendidikan Jasmani",
                "Tari",
                "Musik",
                "Teater & Seni Pertunjukan",
                "Fotografi",
                "Etnomusikologi",
            ],
        )

        uploaded_file = st.file_uploader(
            "Unggah File Portofolio (PDF / ZIP / MP4)",
            type=["pdf", "zip", "mp4", "jpg", "png"],
            help="Unggah draf karya atau video praktik untuk review konselor/mentor.",
        )

        if uploaded_file is not None:
            st.success(
                f"✅ Berkas `{uploaded_file.name}` berhasil diunggah! Berkas akan ditinjau oleh mentor spesialis."
            )

        skor_portofolio = st.number_input(
            "Estimasi Skor Evaluasi Portofolio (0 s/d 100)",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=1.0,
        )

# ==========================================
# 6. EXECUTION ENGINE & KALKULASI SKOR
# ==========================================
st.divider()

if st.button("🚀 Jalankan Analisis Kelolosan SNBP", type="primary", use_container_width=True):

    # 1. Perhitungan Mapel Pendukung & Skor Rapor (50% Rata Umum + 50% Pendukung)
    n_pendukung = (n_mapel_1 + n_mapel_2) / 2.0
    s_rapor = (0.50 * rata_sem_1_5) + (0.50 * n_pendukung)

    # 2. Koreksi Margin KKM
    margin_kkm = max(0.0, rata_sem_1_5 - kkm_rapor)

    # 3. Kalkulasi Skor Berkas (Jika ada Portofolio: 50% Rapor : 50% Porto)
    if butuh_portofolio:
        s_berkas = (0.50 * s_rapor) + (0.50 * skor_portofolio)
    else:
        s_berkas = s_rapor

    # 4. Formulasi Indeks Alumni
    bobot_akreditasi = (
        25.0 if "A" in akreditasi_sekolah else (15.0 if "B" in akreditasi_sekolah else 5.0)
    )
    indeks_alumni = min(100.0, (sebaran_alumni * 15.0) + bobot_akreditasi + (margin_kkm * 1.5))

    # 5. Keketatan Score
    keketatan_score = 75.0

    # 6. SKOR TOTAL AKHIR
    s_total = (0.50 * s_berkas) + (0.35 * indeks_alumni) + (0.15 * keketatan_score)

    # Output Metric Cards
    st.markdown("### 📊 Ringkasan Skor Kelayakan SNBP")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Rata Rapor Sem 1-5", f"{rata_sem_1_5:.2f}")
    res2.metric("Rata Mapel Pendukung", f"{n_pendukung:.2f}")
    res3.metric("Skor Berkas Akhir", f"{s_berkas:.2f}")
    res4.metric("SKOR TOTAL (S_total)", f"{s_total:.2f}")

    st.divider()

    # Dynamic Risk Category
    if s_total >= 85.0:
        st.success(
            f"🟢 **SAFE ZONE (Sangat Aman):** Peluang kelolosan tinggi untuk prodi **{prodi_terpilih} ({jenjang_prodi})** di **{ptn_terpilih}**."
        )
    elif s_total >= 75.0:
        st.warning(
            f"🟡 **RATIONAL ZONE (Prospektif):** Peluang cukup rasional. Pastikan Pilihan 2 disiapkan jaring pengaman D4/D3 se-provinsi."
        )
    else:
        st.error(
            f"🔴 **HIGH RISK (Risiko Tinggi):** Skor total di bawah ambang batas aman. Disarankan melakukan *pivot* prodi atau beralih ke jenjang Vokasi."
        )

    # Validasi Aturan Lokasi Provinsi SNBP
    if provinsi_sekolah == "DKI Jakarta" and is_commuter:
        if provinsi_ptn_target != "DKI Jakarta":
            st.info(
                f"💡 **Peringatan Aturan Provinsi SNBP:**\n"
                f"PTN Target Anda ({ptn_terpilih}) berlokasi di **{provinsi_ptn_target}**. Sesuai aturan resmi SNBP, karena sekolah Anda berada di **DKI Jakarta**, "
                f"maka Pilihan 2 **WAJIB** memilih PTN yang berlokasi di **DKI Jakarta** (UNJ atau UPNVJ)."
            )
