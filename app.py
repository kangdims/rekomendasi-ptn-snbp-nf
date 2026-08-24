import io
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Import ReportLab untuk Pembuatan File PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Simulator SNBP - Master PTN & Automatic Lookup Engine",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🎓 Simulator Rekomendasi PTN & Vokasi SNBP")
st.caption("Analisis Kelolosan SNBP Kurikulum Merdeka — Auto-Lookup PTN, Prodi, Mapel Pendukung, & Daya Tampung")
st.divider()

# ==========================================
# 2. PROFIL SISWA & DATA SEKOLAH (HORIZONTAL)
# ==========================================
st.subheader("👤 Profil Siswa, Data Sekolah & Preferensi")

col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    nama_siswa = st.text_input("Nama Siswa", value="Ahmad Fikri")
    sekolah_asal = st.text_input("Nama Sekolah", value="SMAN 1 Depok")

with col_p2:
    jenjang_sekolah = st.selectbox("Jenjang Sekolah", ["SMA/MA", "SMK"], index=0)
    provinsi_sekolah = st.selectbox(
        "Provinsi Sekolah Asal",
        ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Banten", "Lainnya"],
        index=0,
    )

with col_p3:
    akreditasi_sekolah = st.selectbox("Akreditasi Sekolah", ["A (Unggul)", "B (Baik)", "C (Cukup)"], index=0)
    kkm_rapor = st.number_input("Nilai KKM Rapor", 60.0, 90.0, 75.0, 0.5)

with col_p4:
    sebaran_alumni = st.number_input("Jumlah Sebaran Alumni (3 Thn)", 0, 100, 3, 1)
    is_commuter = st.checkbox("Preferensi Commuter (Tanpa Kos)", value=True)

st.divider()

# ==========================================
# 3. DATA MASTER PROVINSI, PTN, PRODI, STRATA & DAYA TAMPUNG
# ==========================================
DATA_MASTER_PTN_PRODI = {
    "Jawa Barat": {
        "Institut Teknologi Bandung (ITB)": {
            "STEI-K (Komputasi)": {"strata": "S1", "daya_tampung": 120, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "STEI-R (Rekayasa)": {"strata": "S1", "daya_tampung": 150, "mapel_1": "Matematika Lanjut", "mapel_2": "Fisika", "porto": False},
            "FTTM (Pertambangan & Perminyakan)": {"strata": "S1", "daya_tampung": 160, "mapel_1": "Matematika Lanjut", "mapel_2": "Fisika", "porto": False},
            "FTMD (Mesin & Dirgantara)": {"strata": "S1", "daya_tampung": 140, "mapel_1": "Matematika Lanjut", "mapel_2": "Fisika", "porto": False},
            "FTSL (Sipil & Lingkungan)": {"strata": "S1", "daya_tampung": 150, "mapel_1": "Matematika Lanjut", "mapel_2": "Fisika", "porto": False},
            "FSRD (Seni Rupa & Desain)": {"strata": "S1", "daya_tampung": 110, "mapel_1": "Seni Budaya", "mapel_2": "Informatika", "porto": True},
            "SBM (Bisnis & Manajemen)": {"strata": "S1", "daya_tampung": 84, "mapel_1": "Ekonomi", "mapel_2": "Matematika Lanjut", "porto": False},
        },
        "Universitas Indonesia (UI)": {
            "Teknik Informatika": {"strata": "S1", "daya_tampung": 60, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "Sistem Informasi": {"strata": "S1", "daya_tampung": 50, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "Manajemen": {"strata": "S1", "daya_tampung": 90, "mapel_1": "Ekonomi", "mapel_2": "Matematika Lanjut", "porto": False},
            "Ilmu Hukum": {"strata": "S1", "daya_tampung": 110, "mapel_1": "Sosiologi", "mapel_2": "Pendidikan Pancasila", "porto": False},
        },
        "Universitas Padjadjaran (UNPAD)": {
            "Teknik Informatika": {"strata": "S1", "daya_tampung": 40, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "Kedokteran": {"strata": "S1", "daya_tampung": 70, "mapel_1": "Biologi", "mapel_2": "Kimia", "porto": False},
            "Ilmu Komunikasi": {"strata": "S1", "daya_tampung": 65, "mapel_1": "Sosiologi", "mapel_2": "Bahasa Indonesia Tingkat Lanjut", "porto": False},
        },
        "Politeknik Negeri Jakarta (PNJ)": {
            "D4 Teknik Informatika": {"strata": "D4", "daya_tampung": 48, "mapel_1": "Informatika", "mapel_2": "Matematika Lanjut", "porto": False},
            "D3 Teknik Elektronika": {"strata": "D3", "daya_tampung": 32, "mapel_1": "Fisika", "mapel_2": "Matematika Lanjut", "porto": False},
            "D4 Desain Grafis": {"strata": "D4", "daya_tampung": 36, "mapel_1": "Seni Budaya", "mapel_2": "Informatika", "porto": True},
        },
        "IPB University": {
            "D4 Teknologi Rekayasa Komputer (SV)": {"strata": "D4", "daya_tampung": 80, "mapel_1": "Informatika", "mapel_2": "Matematika Lanjut", "porto": False},
            "S1 Kedokteran Hewan": {"strata": "S1", "daya_tampung": 60, "mapel_1": "Biologi", "mapel_2": "Kimia", "porto": False},
        }
    },
    "DKI Jakarta": {
        "Universitas Negeri Jakarta (UNJ)": {
            "Pendidikan Ilmu Komputer": {"strata": "S1", "daya_tampung": 45, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "Desain Komunikasi Visual": {"strata": "S1", "daya_tampung": 35, "mapel_1": "Seni Budaya", "mapel_2": "Informatika", "porto": True},
            "Pendidikan Jasmani & Kesehatan": {"strata": "S1", "daya_tampung": 50, "mapel_1": "Pendidikan Jasmani, Olahraga dan Kesehatan (PJOK)", "mapel_2": "Biologi", "porto": True},
        },
        "UPN Veteran Jakarta (UPNVJ)": {
            "S1 Informatika": {"strata": "S1", "daya_tampung": 72, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "S1 Kedokteran": {"strata": "S1", "daya_tampung": 50, "mapel_1": "Biologi", "mapel_2": "Kimia", "porto": False},
            "D4 Sistem Informasi": {"strata": "D4", "daya_tampung": 40, "mapel_1": "Informatika", "mapel_2": "Matematika Lanjut", "porto": False},
        }
    },
    "DI Yogyakarta": {
        "Universitas Gadjah Mada (UGM)": {
            "Teknologi Informasi": {"strata": "S1", "daya_tampung": 55, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "Kedokteran": {"strata": "S1", "daya_tampung": 53, "mapel_1": "Biologi", "mapel_2": "Kimia", "porto": False},
            "Manajemen & Kebijakan Publik": {"strata": "S1", "daya_tampung": 40, "mapel_1": "Sosiologi", "mapel_2": "Ekonomi", "porto": False},
        }
    },
    "Jawa Timur": {
        "Institut Teknologi Sepuluh Nopember (ITS)": {
            "Teknik Informatika": {"strata": "S1", "daya_tampung": 90, "mapel_1": "Matematika Lanjut", "mapel_2": "Informatika", "porto": False},
            "Teknik Sipil": {"strata": "S1", "daya_tampung": 60, "mapel_1": "Matematika Lanjut", "mapel_2": "Fisika", "porto": False},
        },
        "Universitas Airlangga (UNAIR)": {
            "Kedokteran": {"strata": "S1", "daya_tampung": 75, "mapel_1": "Biologi", "mapel_2": "Kimia", "porto": False},
            "Farmasi": {"strata": "S1", "daya_tampung": 70, "mapel_1": "Kimia", "mapel_2": "Biologi", "porto": False},
        }
    }
}

MAPEL_TKA_LIST = [
    "Matematika Lanjut", "Fisika", "Kimia", "Biologi",
    "Pendidikan Jasmani, Olahraga dan Kesehatan (PJOK)", "Ekonomi", "Geografi",
    "Sosiologi", "Sejarah", "Antropologi", "Pendidikan Pancasila", "Pendidikan Kewarganegaraan (PKn)",
    "Seni Budaya", "Bahasa Indonesia Tingkat Lanjut", "Bahasa Inggris Tingkat Lanjut"
]

# ==========================================
# 4. FUNGSI GENERATOR PDF LAPORAN
# ==========================================
def generate_pdf_report(nama_siswa, sekolah, provinsi_sekolah, ptn_target, prodi_target, strata, s_rapor, s_total, status_zone, catatan_snbp):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=4,
        alignment=1
    )
    
    sub_style = ParagraphStyle(
        'SubStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#4B5563'),
        alignment=1,
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle('Norm', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14)
    bold_style = ParagraphStyle('Bld', parent=normal_style, fontName='Helvetica-Bold')
    
    story = []
    story.append(Paragraph("<b>BIMBINGAN BELAJAR NURUL FIKRI</b>", title_style))
    story.append(Paragraph("LAPORAN HASIL REKOMENDASI & ANALISIS KELOLOSAN SNBP", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=15))
    
    table_data = [
        [Paragraph("<b>Nama Siswa</b>", bold_style), Paragraph(nama_siswa, normal_style)],
        [Paragraph("<b>Sekolah Asal</b>", bold_style), Paragraph(f"{sekolah} ({provinsi_sekolah})", normal_style)],
        [Paragraph("<b>PTN Target</b>", bold_style), Paragraph(ptn_target, normal_style)],
        [Paragraph("<b>Prodi / Fakultas</b>", bold_style), Paragraph(f"{prodi_target} ({strata})", normal_style)],
        [Paragraph("<b>Skor Berkas Rapor (S_rapor)</b>", bold_style), Paragraph(f"{s_rapor:.2f}", normal_style)],
        [Paragraph("<b>Skor Kelayakan Total (S_total)</b>", bold_style), Paragraph(f"<b>{s_total:.2f}</b>", normal_style)],
        [Paragraph("<b>Status Kelolosan</b>", bold_style), Paragraph(f"<b>{status_zone}</b>", normal_style)],
    ]
    
    t = Table(table_data, colWidths=[160, 360])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Rekomendasi & Catatan Aturan SNBP:</b>", ParagraphStyle('RecHeader', parent=bold_style, textColor=colors.HexColor('#1E3A8A'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph(catatan_snbp, normal_style))
    story.append(Spacer(1, 30))
    
    ttd_data = [
        [Paragraph("", normal_style), Paragraph("Konselor Bimbingan SNBP", bold_style)],
        [Paragraph("", normal_style), Spacer(1, 40)],
        [Paragraph("", normal_style), Paragraph("( ________________________ )", bold_style)]
    ]
    t_ttd = Table(ttd_data, colWidths=[300, 220])
    t_ttd.setStyle(TableStyle([('ALIGN', (1, 0), (1, -1), 'CENTER')]))
    story.append(t_ttd)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ==========================================
# 5. FORM TABS UTAMA
# ==========================================
tab1, tab2 = st.tabs(["🎯 Pemilihan PTN Target & Auto-Lookup", "📚 Nilai Rapor, TKA & Portofolio"])

# --- TAB 1: CASCADING AUTO-LOOKUP TARGET PTN & PRODI ---
with tab1:
    st.markdown("### Pemilihan PTN Target Berdasarkan Provinsi")
    st.caption("Sistem akan menyaring nama PTN, Program Studi, Strata, Daya Tampung, dan Mapel Peminatan secara otomatis.")

    col_target_1, col_target_2, col_target_3 = st.columns(3)

    with col_target_1:
        # 1. Pilih Provinsi Target
        provinsi_ptn_options = list(DATA_MASTER_PTN_PRODI.keys())
        selected_prov_ptn = st.selectbox("1. Pilih Provinsi PTN Target", provinsi_ptn_options, index=0)

    with col_target_2:
        # 2. Filter Nama PTN di Provinsi Tersebut
        ptn_in_prov_options = list(DATA_MASTER_PTN_PRODI[selected_prov_ptn].keys())
        selected_ptn = st.selectbox("2. Pilih Nama PTN", ptn_in_prov_options, index=0)

    with col_target_3:
        # 3. Filter Nama Prodi di PTN Tersebut
        prodi_in_ptn_options = list(DATA_MASTER_PTN_PRODI[selected_prov_ptn][selected_ptn].keys())
        selected_prodi = st.selectbox("3. Pilih Program Studi / Fakultas", prodi_in_ptn_options, index=0)

    # Ekstraksi Detail Otomatis
    detail_prodi = DATA_MASTER_PTN_PRODI[selected_prov_ptn][selected_ptn][selected_prodi]
    selected_strata = detail_prodi["strata"]
    selected_daya_tampung = detail_prodi["daya_tampung"]
    required_mapel_1 = detail_prodi["mapel_1"]
    required_mapel_2 = detail_prodi["mapel_2"]
    auto_porto_req = detail_prodi["porto"]

    st.divider()

    # Display Informasi Detail Hasil Auto-Lookup
    st.markdown("#### 📋 Info Kuota & Persyaratan Resmi SNBP")
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)

    info_col1.metric("Jenjang / Strata", selected_strata)
    info_col2.metric("Daya Tampung SNBP", f"{selected_daya_tampung} Kursi")
    info_col3.metric("Mapel Peminatan Utama 1", required_mapel_1)
    info_col4.metric("Mapel Peminatan Utama 2", required_mapel_2)

    if auto_porto_req:
        st.warning("🎨 **Status Portofolio:** Program Studi ini **WAJIB** melampirkan Portofolio Karya/Praktik.")
    else:
        st.info("ℹ️ **Status Portofolio:** Program Studi ini **TIDAK** memerlukan portofolio tambahan.")

# --- TAB 2: NILAI RAPOR, TKA, DAN PORTOFOLIO ---
with tab2:
    st.markdown("### 1. Input Nilai Rapor Semester 1 s/d 5")
    c1, c2, c3, c4, c5 = st.columns(5)
    sem1 = c1.number_input("Semester 1", 0.0, 100.0, 83.0, 0.5)
    sem2 = c2.number_input("Semester 2", 0.0, 100.0, 84.0, 0.5)
    sem3 = c3.number_input("Semester 3", 0.0, 100.0, 85.5, 0.5)
    sem4 = c4.number_input("Semester 4", 0.0, 100.0, 87.0, 0.5)
    sem5 = c5.number_input("Semester 5", 0.0, 100.0, 88.5, 0.5)
    rata_sem = (sem1 + sem2 + sem3 + sem4 + sem5) / 5.0

    st.info(f"📈 **Rata-Rata Rapor Umum (Sem 1-5):** `{rata_sem:.2f}`")

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
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # SECTION 2: MAPEL TKA (OTOMATIS TERSINKRON DENGAN SYARAT PRODI)
    st.markdown("### 2. Nilai Mata Pelajaran Peminatan / TKA Siswa")
    st.caption(f"Mapel yang direkomendasikan untuk **{selected_prodi}**: **{required_mapel_1}** & **{required_mapel_2}**.")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        # Default disesuaikan dengan mapel syarat prodi
        idx_m1 = MAPEL_TKA_LIST.index(required_mapel_1) if required_mapel_1 in MAPEL_TKA_LIST else 0
        mapel_1 = st.selectbox("Mapel Peminatan 1", MAPEL_TKA_LIST, index=idx_m1)
        n_mapel_1 = st.number_input(f"Nilai Rata-Rata {mapel_1}", 0.0, 100.0, 90.0, 0.5)

    with col_m2:
        idx_m2 = MAPEL_TKA_LIST.index(required_mapel_2) if required_mapel_2 in MAPEL_TKA_LIST else 1
        mapel_2 = st.selectbox("Mapel Peminatan 2", MAPEL_TKA_LIST, index=idx_m2)
        n_mapel_2 = st.number_input(f"Nilai Rata-Rata {mapel_2}", 0.0, 100.0, 88.0, 0.5)

    st.divider()

    # SECTION 3: INTEGRASI PORTOFOLIO
    st.markdown("### 3. Integrasi Portofolio Karya (Khusus Seni & Olahraga)")
    butuh_porto = st.checkbox(
        "Prodi Target Mensyaratkan Portofolio?",
        value=auto_porto_req
    )

    skor_porto = 0.0
    if butuh_porto:
        col_po1, col_po2 = st.columns(2)
        with col_po1:
            uploaded_file = st.file_uploader(
                "Unggah File Portofolio (PDF / ZIP / MP4 / JPG / PNG)",
                type=["pdf", "zip", "mp4", "jpg", "png"],
                help="Unggah draf karya atau video praktik untuk ditinjau konselor.",
            )
            if uploaded_file is not None:
                st.success(f"✅ Berkas `{uploaded_file.name}` berhasil diunggah!")

        with col_po2:
            skor_porto = st.number_input(
                "Estimasi Skor Evaluasi Portofolio (0 s/d 100)",
                min_value=0.0, max_value=100.0, value=85.0, step=1.0
            )

# ==========================================
# 6. EXECUTION ENGINE & PDF GENERATOR
# ==========================================
st.divider()

if st.button("🚀 Jalankan Analisis Kelolosan SNBP", type="primary", use_container_width=True):
    n_pendukung = (n_mapel_1 + n_mapel_2) / 2.0
    s_rapor = (0.50 * rata_sem) + (0.50 * n_pendukung)
    s_berkas = (0.50 * s_rapor) + (0.50 * skor_porto) if butuh_porto else s_rapor
    
    bobot_akreditasi = 25.0 if "A" in akreditasi_sekolah else (15.0 if "B" in akreditasi_sekolah else 5.0)
    margin_kkm = max(0.0, rata_sem - kkm_rapor)
    indeks_alumni = min(100.0, (sebaran_alumni * 15.0) + bobot_akreditasi + (margin_kkm * 1.5))
    
    # Perhitungan keketatan dinamis dari daya tampung
    keketatan_score = min(90.0, max(50.0, selected_daya_tampung * 0.6))
    s_total = (0.50 * s_berkas) + (0.35 * indeks_alumni) + (0.15 * keketatan_score)
    
    st.markdown("### 📊 Ringkasan Skor Kelayakan SNBP")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Rata Rapor Sem 1-5", f"{rata_sem:.2f}")
    res2.metric("Rata Mapel Pendukung", f"{n_pendukung:.2f}")
    res3.metric("Skor Berkas Akhir", f"{s_berkas:.2f}")
    res4.metric("SKOR TOTAL (S_total)", f"{s_total:.2f}")
    
    st.divider()
    
    if s_total >= 85.0:
        status_zone = "🟢 SAFE ZONE (Sangat Aman)"
        st.success(f"**{status_zone}:** Peluang kelolosan sangat tinggi untuk **{nama_siswa}** pada **{selected_prodi} ({selected_strata})** di **{selected_ptn}**.")
    elif s_total >= 75.0:
        status_zone = "🟡 RATIONAL ZONE (Prospektif)"
        st.warning(f"**{status_zone}:** Peluang cukup rasional. Pastikan Pilihan 2 disiapkan jaring pengaman se-provinsi.")
    else:
        status_zone = "🔴 HIGH RISK (Risiko Tinggi)"
        st.error(f"**{status_zone}:** Skor total di bawah ambang aman. Disarankan *pivot* prodi atau beralih ke Vokasi.")

    catatan_snbp = f"Analisis Kurikulum Merdeka. Rata-Rata Rapor: {rata_sem:.2f}. Mapel Pendukung Utama: {required_mapel_1} & {required_mapel_2}. "
    if provinsi_sekolah == "DKI Jakarta" and is_commuter and selected_prov_ptn != "DKI Jakarta":
        catatan_snbp += "Sesuai aturan SNBP, karena Pilihan 1 di luar DKI Jakarta, Pilihan 2 WAJIB memilih PTN di DKI Jakarta (UNJ/UPNVJ)."

    # GENERATE PDF BYTES
    pdf_bytes = generate_pdf_report(
        nama_siswa, sekolah_asal, provinsi_sekolah, selected_ptn, selected_prodi, 
        selected_strata, s_rapor, s_total, status_zone, catatan_snbp
    )

    st.divider()
    
    # TOMBOL DOWNLOAD PDF LAPORAN
    st.download_button(
        label="📄 Download Laporan Rekomendasi (PDF)",
        data=pdf_bytes,
        file_name=f"Laporan_SNBP_{nama_siswa.replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary"
    )
    st.caption("🖨️ *Buka file PDF yang terunduh dan tekan **Ctrl + P** (atau **Cmd + P** di Mac) untuk mencetak Laporan Rekomendasi.*")
