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
    page_title="Simulator SNBP - Master PTN & PDF Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎓 Simulator Rekomendasi PTN & Vokasi SNBP")
st.caption("Analisis Kelolosan SNBP Kurikulum Merdeka — Fitur Cetak Laporan PDF Resmi")
st.divider()

# ==========================================
# 2. FUNGSI GENERATOR PDF LAPORAN REKOMENDASI
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
    
    # Header Dokumen
    story.append(Paragraph("<b>BIMBINGAN BELAJAR NURUL FIKRI</b>", title_style))
    story.append(Paragraph("LAPORAN HASIL REKOMENDASI & ANALISIS KELOLOSAN SNBP", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=15))
    
    # Tabel Data Identitas & Hasil
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
    
    # Catatan & Rekomendasi Konselor
    story.append(Paragraph("<b>Rekomendasi & Catatan Aturan SNBP:</b>", ParagraphStyle('RecHeader', parent=bold_style, textColor=colors.HexColor('#1E3A8A'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph(catatan_snbp, normal_style))
    story.append(Spacer(1, 30))
    
    # Lembar Pengesahan / Tanda Tangan
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
# 3. MASTER DATA ITB & PTN
# ==========================================
DATA_ITB_FAKULTAS = {
    "STEI-K (Komputasi)": {"strata": "S1", "daya_tampung": 120, "porto": False},
    "STEI-R (Rekayasa)": {"strata": "S1", "daya_tampung": 150, "porto": False},
    "FTTM (Pertambangan & Perminyakan)": {"strata": "S1", "daya_tampung": 160, "porto": False},
    "FTMD (Mesin & Dirgantara)": {"strata": "S1", "daya_tampung": 140, "porto": False},
    "FTSL (Sipil & Lingkungan)": {"strata": "S1", "daya_tampung": 150, "porto": False},
    "FMIPA (Matematika & IPA)": {"strata": "S1", "daya_tampung": 190, "porto": False},
    "SITH (Ilmu & Tek. Hayati)": {"strata": "S1", "daya_tampung": 190, "porto": False},
    "FITB (Kebumian)": {"strata": "S1", "daya_tampung": 130, "porto": False},
    "FSRD (Seni Rupa & Desain)": {"strata": "S1", "daya_tampung": 110, "porto": True},
    "SBM (Bisnis & Manajemen)": {"strata": "S1", "daya_tampung": 84, "porto": False},
}

# ==========================================
# 4. SIDEBAR INPUT DATA SISWA
# ==========================================
st.sidebar.header("👤 Profil Siswa & Sekolah")
nama_siswa = st.sidebar.text_input("Nama Siswa", value="Ahmad Fikri")
sekolah_asal = st.sidebar.text_input("Nama Sekolah", value="SMAN 1 Depok")
jenjang_sekolah = st.sidebar.selectbox("Jenjang Sekolah", ["SMA/MA", "SMK"], index=0)
akreditasi_sekolah = st.sidebar.selectbox("Akreditasi Sekolah", ["A (Unggul)", "B (Baik)", "C (Cukup)"], index=0)
kkm_rapor = st.sidebar.number_input("Nilai KKM Rapor", 60.0, 90.0, 75.0, 0.5)
sebaran_alumni = st.sidebar.number_input("Jumlah Sebaran Alumni", 0, 100, 3, 1)
is_commuter = st.sidebar.checkbox("Preferensi Commuter (Tanpa Kos)", value=True)

# ==========================================
# 5. FORM TABS UTAMA
# ==========================================
tab1, tab2, tab3 = st.tabs(["📚 Nilai Rapor", "🎯 Target PTN", "🎨 Portofolio"])

with tab1:
    c1, c2, c3, c4, c5 = st.columns(5)
    sem1 = c1.number_input("Sem 1", 0.0, 100.0, 83.0, 0.5)
    sem2 = c2.number_input("Sem 2", 0.0, 100.0, 84.0, 0.5)
    sem3 = c3.number_input("Sem 3", 0.0, 100.0, 85.5, 0.5)
    sem4 = c4.number_input("Sem 4", 0.0, 100.0, 87.0, 0.5)
    sem5 = c5.number_input("Sem 5", 0.0, 100.0, 88.5, 0.5)
    rata_sem = (sem1 + sem2 + sem3 + sem4 + sem5) / 5.0
    
    col_m1, col_m2 = st.columns(2)
    n_mapel_1 = col_m1.number_input("Nilai Mapel Peminatan 1", 0.0, 100.0, 90.0, 0.5)
    n_mapel_2 = col_m2.number_input("Nilai Mapel Peminatan 2", 0.0, 100.0, 88.0, 0.5)

with tab2:
    provinsi_sekolah = st.selectbox("Provinsi Sekolah Asal", ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur"], index=0)
    is_itb = st.checkbox("Pilih Institut Teknologi Bandung (ITB)", value=True)
    if is_itb:
        ptn_target = "Institut Teknologi Bandung (ITB)"
        prodi_target = st.selectbox("Pilih Fakultas ITB", list(DATA_ITB_FAKULTAS.keys()))
        strata = "S1"
        daya_tampung = DATA_ITB_FAKULTAS[prodi_target]["daya_tampung"]
    else:
        ptn_target = st.text_input("Nama PTN", "Universitas Indonesia")
        prodi_target = st.text_input("Nama Prodi", "Teknik Informatika")
        strata = "S1"
        daya_tampung = 60

with tab3:
    butuh_porto = st.checkbox("Membutuhkan Portofolio?", value=False)
    skor_porto = st.number_input("Estimasi Skor Portofolio", 0.0, 100.0, 85.0, 1.0) if butuh_porto else 0.0

# ==========================================
# 6. EXECUTION ENGINE & PDF GENERATOR
# ==========================================
st.divider()

if st.button("🚀 Jalankan Analisis Kelolosan SNBP", type="primary", use_container_width=True):
    n_pendukung = (n_mapel_1 + n_mapel_2) / 2.0
    s_rapor = (0.50 * rata_sem) + (0.50 * n_pendukung)
    s_berkas = (0.50 * s_rapor) + (0.50 * skor_porto) if butuh_porto else s_rapor
    
    bobot_akreditasi = 25.0 if "A" in akreditasi_sekolah else 15.0
    margin_kkm = max(0.0, rata_sem - kkm_rapor)
    indeks_alumni = min(100.0, (sebaran_alumni * 15.0) + bobot_akreditasi + (margin_kkm * 1.5))
    
    s_total = (0.50 * s_berkas) + (0.35 * indeks_alumni) + (15.0)
    
    if s_total >= 85.0:
        status_zone = "🟢 SAFE ZONE (Sangat Aman)"
        st.success(f"**{status_zone}:** Peluang tinggi untuk {nama_siswa} di {prodi_target} ({ptn_target}).")
    elif s_total >= 75.0:
        status_zone = "🟡 RATIONAL ZONE (Prospektif)"
        st.warning(f"**{status_zone}:** Peluang cukup rasional. Siapkan Pilihan 2 jaring pengaman.")
    else:
        status_zone = "🔴 HIGH RISK (Risiko Tinggi)"
        st.error(f"**{status_zone}:** Skor belum memenuhi ambang aman. Disarankan pivot prodi/PTN.")

    catatan_snbp = f"Analisis dilakukan berdasarkan Kurikulum Merdeka. Nilai Rapor Rata-Rata: {rata_sem:.2f}. "
    if provinsi_sekolah == "DKI Jakarta" and is_commuter and "ITB" in ptn_target:
        catatan_snbp += "Sesuai aturan SNBP, karena Pilihan 1 berada di luar DKI Jakarta (Jawa Barat), Pilihan 2 WAJIB memilih PTN di DKI Jakarta (UNJ/UPNVJ)."

    # GENERATE PDF BYTES
    pdf_bytes = generate_pdf_report(
        nama_siswa, sekolah_asal, provinsi_sekolah, ptn_target, prodi_target, 
        strata, s_rapor, s_total, status_zone, catatan_snbp
    )

    st.divider()
    
    # TOMBOL DOWNLOAD PDF
    st.download_button(
        label="📄 Download Laporan Rekomendasi (PDF)",
        data=pdf_bytes,
        file_name=f"Laporan_SNBP_{nama_siswa.replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary"
    )
    st.caption("🖨️ *Setelah mengunduh file PDF, buka file tersebut dan tekan **Ctrl + P** (atau **Cmd + P** di Mac) untuk mencetak dokumen.*")
