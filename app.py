import streamlit as st
import base64
import io
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="E-CV Kelompok UBSI", page_icon="🎓", layout="wide")

# ==========================================
# 1. INISIALISASI STATE & DATA
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user' not in st.session_state:
    st.session_state.user = None

data_anggota = [
    {
        "id": "gregorius",
        "nama": "Gregorius Waek", "role": "Product Manager & Fullstack Dev", "foto": "assets/gregorius.jpeg", "cv": "assets/cv.pdf", "email": "waekgregorius@gmail.com", "wa": "081234567890",
        "about": "Mahasiswa Sistem Informasi semester 7 di UBSI yang berfokus pada pengembangan web. Berperan sebagai Product Manager dan Fullstack Developer dalam proyek E-CV ini. Memiliki ketertarikan mendalam pada optimasi backend dan arsitektur sistem yang aman.",
        "skills": [
            {"name": "Laravel", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-original.svg"},
            {"name": "PHP", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg"},
            {"name": "MySQL", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg"},
            {"name": "Git", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg"}
        ],
        "experience": "Web Developer Intern | Majalah Hidup (2026 - Sekarang).\nMerancang dan membangun ulang website utama perusahaan menggunakan Laravel 12, mengimplementasikan CMS untuk redaksi, dan optimasi database.",
        "projects": "Full-stack Web App (Majalah HIDUP).\nMembangun sistem dari nol dengan fitur Admin Dashboard, E-Commerce, dan Smart Search Algorithm.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang).\nFokus pada rekayasa perangkat lunak dan pemrograman web."
    },
    {
        "id": "maria",
        "nama": "Maria Oktaviani Timung", "role": "UI/UX Designer", "foto": "assets/maria.jpeg", "cv": "assets/cv_maria.pdf", "email": "maria.oktaviani@gmail.com", "wa": "081234567891",
        "about": "Mahasiswa Sistem Informasi yang berfokus pada perancangan antarmuka (UI) dan pengalaman pengguna (UX). Bertanggung jawab atas design system E-CV ini agar ramah pengguna dan estetis.",
        "skills": [
            {"name": "Figma", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg"},
            {"name": "Adobe XD", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/xd/xd-plain.svg"}
        ],
        "experience": "Freelance UI/UX Designer (2024 - Sekarang).\nMendesain aplikasi mobile untuk UMKM lokal dengan pendekatan Design Thinking dan user testing.",
        "projects": "Redesign Aplikasi Mobile UMKM.\nMembuat wireframe hingga prototipe interaktif menggunakan Figma.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang).\nFokus pada interaksi manusia dan komputer."
    },
    {
        "id": "anggun",
        "nama": "Anggun Berliani", "role": "Front-End Developer (Inti)", "foto": "assets/anggun.jpeg", "cv": "assets/cv_anggun.pdf", "email": "anggun@gmail.com", "wa": "081234567892",
        "about": "Mahasiswa Sistem Informasi dengan ketelitian tinggi pada pengembangan antarmuka. Bertanggung jawab atas struktur halaman dan navigasi antar anggota pada E-CV ini.",
        "skills": [
            {"name": "HTML", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"},
            {"name": "React", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg"},
            {"name": "Tailwind", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg"}
        ],
        "experience": "Web Developer Intern | PT Teknologi Nusantara (2025).\nMembangun landing page responsif untuk berbagai event perusahaan.",
        "projects": "Landing Page Event Kampus.\nMembangun antarmuka interaktif menggunakan React JS dan Tailwind CSS.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    },
    {
        "id": "nela",
        "nama": "Nela Nyft", "role": "Front-End Developer (Konten)", "foto": "assets/nela.jpg", "cv": "assets/cv_nela.pdf", "email": "nela@gmail.com", "wa": "081234567893",
        "about": "Mahasiswa Sistem Informasi yang antusias dalam pengembangan aplikasi web. Bertanggung jawab atas komponen skills, experience, dan project cards pada E-CV ini.",
        "skills": [
            {"name": "Flutter", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg"},
            {"name": "Dart", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dart/dart-original.svg"}
        ],
        "experience": "Mobile Developer (Freelance) | 2023 - Sekarang.\nMembangun aplikasi mobile manajemen tugas mahasiswa menggunakan Flutter.",
        "projects": "Aplikasi Manajemen Tugas Mahasiswa.\nIntegrasi REST API dari backend ke aplikasi mobile Flutter.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    },
    {
        "id": "fauzi",
        "nama": "Fauzi Ramdani Koswara", "role": "QA & Deployment", "foto": "assets/fauzi.jpeg", "cv": "assets/cv_fauzi.pdf", "email": "fauzi@gmail.com", "wa": "081234567894",
        "about": "Mahasiswa Sistem Informasi yang berfokus pada kualitas perangkat lunak. Bertanggung jawab atas pengujian responsif dan deployment E-CV ini ke Streamlit Cloud.",
        "skills": [
            {"name": "Docker", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg"},
            {"name": "Node.js", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg"}
        ],
        "experience": "Backend & QA Intern | Startup Fintech XYZ (2025).\nMenguji API dan melakukan optimasi query database MySQL.",
        "projects": "Sistem Manajemen Inventaris.\nMembangun backend Node.js dan melakukan pengujian black-box.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    }
]

proyek_bersama = {
    "judul": "E-CV Kelompok Sistem Informasi UBSI",
    "deskripsi": "Sebuah aplikasi web portofolio interaktif yang menampilkan profil 5 anggota kelompok dalam satu tautan. Dibangun menggunakan Python dan Streamlit, dengan desain responsif (mobile-friendly) dan tema korporat gelap.",
    "teknologi": "Python, Streamlit, HTML, CSS, GitHub, Streamlit Cloud"
}

# ==========================================
# 2. FUNGSI PENAJAM FOTO & LOGO FOOTER
# ==========================================
def get_optimized_base64(image_path, size=(240, 240)):
    if not Path(image_path).exists(): return None
    try:
        img = Image.open(image_path)
        width, height = img.size
        min_dim = min(width, height)
        left, top = (width - min_dim) / 2, (height - min_dim) / 3 
        right, bottom = (width + min_dim) / 2, top + min_dim
        if bottom > height: bottom, top = height, height - min_dim
        img = img.crop((left, top, right, bottom)).resize(size, Image.Resampling.LANCZOS)
        if img.mode in ('RGBA', 'P'): img = img.convert('RGB')
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=95)
        return base64.b64encode(buffered.getvalue()).decode()
    except: return None

b64_logo = get_optimized_base64("assets/gregorius.jpeg", size=(80, 80))

# ==========================================
# 3. CSS TAMPILAN (TEMA DARK BLUE CORPORATE)
# ==========================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {{ background-color: #0b1120 !important; color: #f8fafc !important; }}
    .block-container {{ padding-top: 1rem !important; max-width: 1300px !important; }}
    #MainMenu {{visibility: hidden;}} header {{visibility: hidden;}}
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    /* GANTI LOGO PINK STREAMLIT JADI FOTO KAMU */
    footer[data-testid="stFooter"] a[href*="streamlit.io"] {{
        background-image: url("data:image/jpeg;base64,{b64_logo}") !important;
        background-size: cover !important; background-position: center !important;
        border-radius: 50% !important; width: 22px !important; height: 22px !important;
        display: inline-block !important; vertical-align: middle !important;
        border: 1px solid #3B82F6 !important;
    }}
    footer[data-testid="stFooter"] a[href*="streamlit.io"] img,
    footer[data-testid="stFooter"] a[href*="streamlit.io"] svg {{ display: none !important; }}
    footer[data-testid="stFooter"] {{ background-color: transparent !important; }}
    footer[data-testid="stFooter"] div, footer[data-testid="stFooter"] span, footer[data-testid="stFooter"] a {{
        color: #94a3b8 !important;
    }}

    /* HEADER BARU YANG LEBIH KEREN */
    .main-header {{ text-align: center; padding: 50px 0 30px 0; }}
    .header-badge {{
        display: inline-block;
        background: rgba(37, 99, 235, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(37, 99, 235, 0.3);
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }}
    .main-header h1 {{
        background: linear-gradient(135deg, #f8fafc 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0;
    }}
    .header-divider {{
        width: 150px; height: 4px; 
        background: linear-gradient(90deg, transparent, #3B82F6, transparent);
        margin: 15px auto 0 auto; border-radius: 2px;
    }}

    .section-title {{ font-size: 20px; font-weight: 700; color: #f8fafc !important; margin-top: 35px; margin-bottom: 15px; border-bottom: 2px solid rgba(255,255,255,0.05); padding-bottom: 10px; }}

    /* KARTU ATAS */
    div[data-testid="column"] {{ 
        background-color: #0f172a !important; border: 1px solid rgba(255, 255, 255, 0.05) !important; 
        border-radius: 12px !important; padding: 25px 20px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important; 
        display: flex !important; flex-direction: column !important; height: 100% !important; transition: all 0.3s ease;
    }}
    div[data-testid="column"]:hover {{ border-color: #3B82F6 !important; box-shadow: 0 4px 25px rgba(59, 130, 246, 0.1) !important; }}
    
    .profile-pic {{ width: 120px; height: 120px; margin: 0 auto; border-radius: 50%; border: 3px solid #1e293b; overflow: hidden; }}
    .profile-pic img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }}

    /* TOMBOL LIHAT PROFIL */
    .st-key-view_0 button, .st-key-view_1 button, .st-key-view_2 button, .st-key-view_3 button, .st-key-view_4 button {{ 
        background-color: #2563EB !important; color: #FFFFFF !important; border: none !important; 
        font-weight: 600 !important; width: 100% !important; padding: 10px 0 !important; 
        font-size: 12px !important; margin-top: 10px !important; border-radius: 6px !important; transition: 0.2s;
    }}
    .st-key-view_0 button:hover, .st-key-view_1 button:hover, .st-key-view_2 button:hover, .st-key-view_3 button:hover, .st-key-view_4 button:hover {{ background-color: #1E40AF !important; }}

    /* TOMBOL UNDUH CV */
    .stDownloadButton > button {{ 
        background-color: transparent !important; color: #f8fafc !important; border: 1px solid rgba(255,255,255,0.2) !important; 
        border-radius: 6px !important; font-weight: 600 !important; width: 100% !important; padding: 10px 0 !important; 
        font-size: 12px !important; margin-top: 10px !important; transition: 0.2s; 
    }}
    .stDownloadButton > button:hover {{ background-color: rgba(255,255,255,0.05) !important; color: #fff !important; }}

    /* TOMBOL KEMBALI */
    .st-key-back_btn button {{ 
        background-color: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255,255,255,0.2) !important; 
        border-radius: 6px !important; padding: 8px 20px !important; width: auto !important; font-size: 14px !important; font-weight: 500 !important;
    }}
    .st-key-back_btn button:hover {{ background-color: rgba(255,255,255,0.05) !important; color: #fff !important; border-color: #fff !important;}}

    /* KARTU BAWAH (HALAMAN PROFIL) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{ 
        background-color: #0f172a !important; border: 1px solid rgba(255,255,255,0.05) !important; 
        border-radius: 12px !important; padding: 40px !important; margin-bottom: 40px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important; 
    }}
    
    .profile-pic-detail {{ width: 180px; height: 180px; border-radius: 50%; border: 4px solid #1e293b; overflow: hidden; margin-top: 10px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);}}
    .profile-pic-detail img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }}
    
    .d-name {{ font-weight: 800; color: #f8fafc !important; font-size: 28px; margin-bottom: 5px; }}
    .d-role {{ color: #60A5FA !important; font-size: 16px; margin-bottom: 25px; font-weight: 600; }}
    .d-text {{ color: #94a3b8 !important; font-size: 15px; line-height: 1.8; margin-bottom: 15px; text-align: justify; white-space: pre-line; }}

    /* TIMELINE & SKILLS */
    .timeline-item {{ border-left: 2px solid #3B82F6; padding-left: 20px; margin-bottom: 20px; position: relative; }}
    .timeline-item::before {{ content: ''; position: absolute; left: -7px; top: 0; width: 12px; height: 12px; background: #0f172a; border: 2px solid #3B82F6; border-radius: 50%; }}
    .skill-card {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 8px; margin: 5px; }}
    .skill-card img {{ width: 20px; height: 20px; object-fit: contain; }}
    .skill-card span {{ color: #cbd5e1 !important; font-size: 13px; font-weight: 600; }}

    /* FOOTER CUSTOM */
    .custom-footer {{
        text-align: center; margin-top: 50px; padding-top: 25px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }}
    .custom-footer p {{ color: #64748b; font-size: 13px; margin: 5px 0; }}
    .custom-footer .credit {{ color: #94a3b8; font-weight: 500; }}

    /* LINK */
    a {{ color: #60A5FA !important; text-decoration: none !important; transition: 0.2s; font-weight: 500;}}
    a:hover {{ text-decoration: underline !important; color: #3B82F6 !important; }}

    @media (max-width: 768px) {{
        div[data-testid="stHorizontalBlock"] {{ flex-direction: column !important; gap: 20px !important; }}
        div[data-testid="column"] {{ width: 100% !important; min-width: 100% !important; }}
        .main-header h1 {{ font-size: 2.2rem; }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{ padding: 25px !important; }}
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. TAMPILAN BERANDA
# ==========================================
if st.session_state.page == 'home':
    # Header Baru dengan Badge & Gradient Text
    st.markdown("""
    <div class="main-header">
        <span class="header-badge">✨ E-CV Kelompok Digital Kreatif</span>
        <h1>SISTEM INFORMASI UBSI</h1>
        <div class="header-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5, gap="medium")
    for i, col in enumerate(cols):
        with col:
            d = data_anggota[i]
            b64 = get_optimized_base64(d["foto"], size=(240, 240))
            img_html = f'<div class="profile-pic"><img src="data:image/jpeg;base64,{b64}"></div>' if b64 else f'<div class="profile-pic" style="background:#1e293b; display:flex; align-items:center; justify-content:center; font-size:35px; font-weight:bold; color:#94a3b8;">{d["nama"][0]}</div>'

            html_content = f"""{img_html}
<div style="height: 45px; display: flex; justify-content: center; align-items: center; overflow: hidden; margin-top: 15px;">
<div style="font-weight: 700; font-size: 15px; text-align: center; color: #f8fafc;">{d['nama']}</div>
</div>
<div style="height: 25px; display: flex; justify-content: center; align-items: flex-start; margin-bottom: 15px;">
<div style="font-size: 12px; text-align: center; color: #60A5FA !important; font-weight: 600;">{d['role']}</div>
</div>
<div style="border-top: 1px solid rgba(255,255,255,0.05); margin: 10px 0 15px 0;"></div>
<div style="text-align: left;">
<div style="font-size: 11px; font-weight: 700; color: #64748b !important; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Kontak</div>
<a href="mailto:{d['email']}" style="display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 8px; color: #94a3b8 !important;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">Email</span>
</a>
<a href="https://wa.me/62{d['wa'][1:]}" style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #94a3b8 !important;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="#64748b"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
<span>WhatsApp</span>
</a>
</div>"""
            
            st.markdown(html_content, unsafe_allow_html=True)
            st.markdown('<div style="margin-top: auto;"></div>', unsafe_allow_html=True)
            
            if Path(d["cv"]).exists():
                with open(d["cv"], "rb") as pdf:
                    st.download_button(label="UNDUH CV", data=pdf, file_name=f"CV_{d['nama']}.pdf", mime="application/pdf", key=f"btn_{i}", use_container_width=True)
            else:
                st.button("UNDUH CV", key=f"btn_{i}", disabled=True, use_container_width=True)

            if st.button("LIHAT PROFIL", key=f"view_{i}", use_container_width=True):
                st.session_state.user = i
                st.session_state.page = 'profile'
                st.rerun()

    # Bagian Bawah Beranda
    st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.05); margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #f8fafc; margin-bottom: 30px; font-weight: 700;'>LEBIH DEKAT DENGAN KAMI</h2>", unsafe_allow_html=True)
    
    link_web = "https://gregorius-portfolio.streamlit.app/"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={link_web}"
    
    html_kartu_bawah = f"""<div style="display: flex; gap: 20px; align-items: stretch; margin-top: 20px;"><div style="flex: 1; min-height: 320px; background-color: #0f172a; border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; box-shadow: 0 4px 20px rgba(0,0,0,0.2);"><h3 style="color: #f8fafc; margin-top: 0; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; font-size: 18px;">🏛️ Tentang Kami</h3><p style="color: #94a3b8; font-size: 14px; line-height: 1.6; flex-grow: 1;">Kami adalah kelompok mahasiswa Sistem Informasi UBSI yang berdedikasi untuk menciptakan solusi digital yang inovatif, kreatif, dan fungsional.</p><p style="font-size: 12px; color: #60A5FA; margin-bottom: 0; font-weight: 700;">Mata Kuliah: Digital Kreatif</p></div><div style="flex: 1; min-height: 320px; background-color: #0f172a; border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; box-shadow: 0 4px 20px rgba(0,0,0,0.2);"><h3 style="color: #f8fafc; margin-top: 0; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; font-size: 18px;">🚀 Proyek Bersama</h3><p style="color: #94a3b8; font-size: 14px; line-height: 1.6; flex-grow: 1;">{proyek_bersama['deskripsi']}</p><div><span style="display: inline-block; background: rgba(37, 99, 235, 0.15); color: #60A5FA; padding: 4px 12px; border-radius: 6px; font-size: 11px; margin: 2px; border: 1px solid rgba(37, 99, 235, 0.3); font-weight: 600;">Python</span><span style="display: inline-block; background: rgba(37, 99, 235, 0.15); color: #60A5FA; padding: 4px 12px; border-radius: 6px; font-size: 11px; margin: 2px; border: 1px solid rgba(37, 99, 235, 0.3); font-weight: 600;">Streamlit</span><span style="display: inline-block; background: rgba(37, 99, 235, 0.15); color: #60A5FA; padding: 4px 12px; border-radius: 6px; font-size: 11px; margin: 2px; border: 1px solid rgba(37, 99, 235, 0.3); font-weight: 600;">GitHub</span></div></div><div style="flex: 1; min-height: 320px; background-color: #0f172a; border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.2);"><h3 style="color: #f8fafc; margin-top: 0; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; font-size: 18px;">📱 Scan Tautan</h3><p style="color: #94a3b8; font-size: 14px; line-height: 1.6; flex-grow: 1;">Buka portofolio ini di HP Anda dengan memindai QR Code di bawah ini.</p><div style="display: flex; justify-content: center; margin-top: 10px;"><img src="{qr_url}" style="width: 120px; height: 120px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); padding: 5px; background: white;"></div></div></div>"""
    st.markdown(html_kartu_bawah, unsafe_allow_html=True)
    
    # FOOTER BARU (HANYA COPYRIGHT)
    st.markdown("""
    <div class="custom-footer">
        <p class="credit">© 2026 Sistem Informasi UBSI - Digital Kreatif</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. TAMPILAN PROFIL (HALAMAN BARU)
# ==========================================
elif st.session_state.page == 'profile':
    user_index = st.session_state.user
    if user_index is not None:
        d = data_anggota[user_index]
        
        col_back, _, _ = st.columns([1.5, 4, 4])
        with col_back:
            if st.button("⬅️ Kembali", key="back_btn"):
                st.session_state.page = 'home'
                st.session_state.user = None
                st.rerun()

        with st.container(border=True):
            col_foto, col_teks = st.columns([1, 3.5], gap="large")
            
            with col_foto:
                b64 = get_optimized_base64(d["foto"], size=(240, 240))
                if b64:
                    st.markdown(f'<div class="profile-pic-detail"><img src="data:image/jpeg;base64,{b64}"></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="profile-pic-detail" style="background:#1e293b; display:flex; align-items:center; justify-content:center; font-size:45px; font-weight:bold; color:#64748b;">{d["nama"][0]}</div>', unsafe_allow_html=True)
            
            with col_teks:
                st.markdown(f'<div class="d-name">{d["nama"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="d-role">{d["role"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="section-title">ABOUT ME</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="d-text">{d["about"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="section-title">SKILLS</div>', unsafe_allow_html=True)
                skills_html = ""
                for skill in d["skills"]:
                    skills_html += f'<div class="skill-card"><img src="{skill["icon"]}"><span>{skill["name"]}</span></div>'
                st.markdown(skills_html, unsafe_allow_html=True)
                
                st.markdown(f'<div class="section-title">EXPERIENCE</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="timeline-item"><div class="d-text">{d["experience"]}</div></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="section-title">PROJECTS</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="d-text">{d["projects"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="section-title">EDUCATION</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="d-text">{d["education"]}</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="section-title">CONTACT</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="d-text">📧 Email: {d["email"]}<br>💬 WhatsApp: {d["wa"]}</div>', unsafe_allow_html=True)
    else:
        st.session_state.page = 'home'
        st.rerun()
