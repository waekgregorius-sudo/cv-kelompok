import streamlit as st
import base64
import io
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="Group Portfolio - UBSI", page_icon="💻", layout="wide")

# ==========================================
# FUNGSI PENAJAM FOTO (ANTI BLUR)
# ==========================================
def get_optimized_base64(image_path, size=(240, 240)):
    if not Path(image_path).exists():
        return None
    try:
        img = Image.open(image_path)
        
        # 1. Potong jadi persegi (fokus agak ke atas buat wajah)
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 3 
        right = (width + min_dim) / 2
        bottom = top + min_dim
        
        if bottom > height:
            bottom = height
            top = height - min_dim
            
        img = img.crop((left, top, right, bottom))
        
        # 2. Perkecil pakai algoritma LANCZOS (paling tajam)
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        # 3. Simpan ke base64
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=95)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        return None

# ==========================================
# DATA 5 ANGGOTA
# ==========================================
data_anggota = [
    {
        "nama": "Gregorius Waek", 
        "role": "Fullstack Dev", 
        "email": "waekgregorius@gmail.com", 
        "wa": "081234567890", 
        "foto": "assets/gregorius.jpeg", 
        "cv": "assets/cv.pdf",
        "about": "Mahasiswa Sistem Informasi semester 7 di Universitas Bina Sarana Informatika (UBSI) yang berfokus pada pengembangan web. Saat ini saya sedang mengasah kemampuan backend dan arsitektur database melalui program magang di Majalah Hidup, di mana saya membangun sistem aplikasi web dari nol menggunakan Laravel. Saya senang membangun sistem yang kompleks, aman, dan memberikan solusi nyata bagi pengguna.",
        "pengalaman": """<b>Web Developer Intern</b> | Majalah Hidup (2026 - Sekarang)
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Merancang dan membangun ulang website utama perusahaan (Redesign) secara end-to-end menggunakan Laravel 12 dan MySQL.</li>
<li>Berperan sebagai Fullstack Developer dalam membangun sistem CMS (Content Management System) untuk redaksi.</li>
<li>Mengembangkan sistem E-Commerce (Keranjang & Checkout) serta integrasi pelacakan pengunjung (Traffic Tracking).</li>
</ul>
<b>Proyek Utama: Full-stack Web App (Majalah HIDUP)</b>
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li><b>Tech Stack:</b> Laravel 12, MySQL, Bootstrap, Vanilla JS.</li>
<li>Membangun sistem dari nol dengan fitur Admin Dashboard, E-Commerce, Smart Search Algorithm, dan keamanan multi-guard auth.</li>
</ul>
<b>Pendidikan</b>
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>S1 Sistem Informasi | Universitas Bina Sarana Informatika (UBSI), Kramat 98 (2023 - Sekarang).</li>
</ul>
<b>Keahlian (Skills)</b>
<ul style="margin-top: 8px; margin-bottom: 0px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Laravel, PHP, MySQL, HTML, CSS, JavaScript, Bootstrap, Tailwind CSS, Git, VS Code, Laragon.</li>
</ul>"""
    },
    {
        "nama": "Maria Oktaviani Timung", 
        "role": "UI/UX Designer", 
        "email": "maria.oktaviani@gmail.com", 
        "wa": "081234567891", 
        "foto": "assets/maria.jpeg", 
        "cv": "assets/cv_maria.pdf",
        "about": "Mahasiswa Sistem Informasi yang berfokus pada perancangan antarmuka (UI) dan pengalaman pengguna (UX). Memiliki ketertarikan besar dalam menciptakan desain yang estetis, fungsional, dan mudah digunakan. Berpengalaman menggunakan Figma untuk membuat wireframe, prototipe, dan user testing.",
        "pengalaman": """<b>Freelance UI/UX Designer</b> | 2024 - Sekarang
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Mendesain aplikasi mobile untuk UMKM lokal dengan pendekatan Design Thinking.</li>
<li>Membangun landing page untuk berbagai event kampus dan organisasi mahasiswa.</li>
</ul>
<b>Asisten Laboratorium Desain</b> | Universitas Bina Sarana Informatika (2025)
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Membantu mahasiswa dalam memahami dasar-dasar desain antarmuka menggunakan Figma.</li>
</ul>
<b>Keahlian (Skills)</b>
<ul style="margin-top: 8px; margin-bottom: 0px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Figma, Adobe XD, UI Design, UX Research, Wireframing, Prototyping.</li>
</ul>"""
    },
    {
        "nama": "Anggun Berliani", 
        "role": "Quality Assurance", 
        "email": "anggun@gmail.com", 
        "wa": "081234567892", 
        "foto": "assets/anggun.jpeg", 
        "cv": "assets/cv_anggun.pdf",
        "about": "Mahasiswa Sistem Informasi dengan ketelitian tinggi pada pengujian perangkat lunak. Berfokus pada manual testing dan otomasi untuk memastikan aplikasi berjalan bebas dari bug. Terbiasa bekerja dalam tim Agile.",
        "pengalaman": """<b>QA Intern</b> | PT Teknologi Nusantara (2025)
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Melakukan manual testing pada aplikasi web internal perusahaan.</li>
<li>Membuat laporan bug (bug report) yang detail dan terstruktur untuk tim developer.</li>
</ul>
<b>Keahlian (Skills)</b>
<ul style="margin-top: 8px; margin-bottom: 0px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Manual Testing, Selenium, Katalon Studio, Jira, Software Development Life Cycle (SDLC).</li>
</ul>"""
    },
    {
        "nama": "Nela Nyft", 
        "role": "Mobile Developer", 
        "email": "nela@gmail.com", 
        "wa": "081234567893", 
        "foto": "assets/nela.jpg", 
        "cv": "assets/cv_nela.pdf",
        "about": "Mahasiswa Sistem Informasi yang antusias dalam pengembangan aplikasi mobile lintas platform. Senang mengeksplorasi fitur-fitur baru pada framework Flutter untuk menciptakan aplikasi yang ringan dan responsif.",
        "pengalaman": """<b>Mobile Developer (Freelance)</b> | 2023 - Sekarang
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Membangun aplikasi mobile untuk manajemen tugas mahasiswa menggunakan Flutter dan Firebase.</li>
<li>Melakukan integrasi REST API dari backend ke aplikasi mobile.</li>
</ul>
<b>Keahlian (Skills)</b>
<ul style="margin-top: 8px; margin-bottom: 0px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Flutter, Dart, Firebase, REST API, Android Studio, Git.</li>
</ul>"""
    },
    {
        "nama": "Fauzi Ramdani Koswara", 
        "role": "Backend Dev", 
        "email": "fauzi@gmail.com", 
        "wa": "081234567894", 
        "foto": "assets/fauzi.jpeg", 
        "cv": "assets/cv_fauzi.pdf",
        "about": "Mahasiswa Sistem Informasi yang berfokus pada arsitektur server dan pengelolaan database. Memiliki minat besar dalam membangun API yang aman, cepat, dan mudah di-maintain oleh tim frontend.",
        "pengalaman": """<b>Backend Intern</b> | Startup Fintech XYZ (2025)
<ul style="margin-top: 8px; margin-bottom: 20px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Membantu pengembangan REST API menggunakan Node.js dan Express.js.</li>
<li>Melakukan optimasi query pada database MySQL untuk mempercepat waktu respons server.</li>
</ul>
<b>Keahlian (Skills)</b>
<ul style="margin-top: 8px; margin-bottom: 0px; padding-left: 20px; color: #FFFFFF !important; line-height: 1.6;">
<li>Node.js, Express.js, PHP, MySQL, MongoDB, Postman, Docker (Dasar).</li>
</ul>"""
    }
]

# ==========================================
# CSS TAMPILAN
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #3D0A0A !important; color: #FFFFFF !important; }
    .block-container { padding-top: 2rem !important; max-width: 1300px !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    /* PAKSA SEMUA LINK JADI PUTIH/EMAS */
    a, a:visited, a:link, a:active, 
    a span, a div, a p, 
    [data-testid="stMarkdownContainer"] a,
    [data-testid="stMarkdownContainer"] a * {
        color: #FFFFFF !important; 
        text-decoration: none !important;
    }
    a:hover, a:hover *, 
    [data-testid="stMarkdownContainer"] a:hover,
    [data-testid="stMarkdownContainer"] a:hover * {
        color: #FFD700 !important;
    }

    /* CSS BAGIAN ATAS (5 KOTAK) */
    div[data-testid="column"] {
        background-color: #6B1414 !important; 
        border: 2px solid #FFD700 !important; 
        border-radius: 16px !important;
        padding: 25px 15px !important; 
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.6) !important;
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
    }

    .icon-svg { width: 14px; height: 14px; flex-shrink: 0; }
    
    /* FOTO ATAS */
    .profile-pic { 
        width: 120px; height: 120px; margin: 0 auto; border-radius: 50%; 
        border: 3px solid #FFD700; overflow: hidden; 
    }
    .profile-pic img { 
        width: 100%; height: 100%; 
        object-fit: cover; 
    }
    
    .stDownloadButton > button, .stButton > button {
        background-color: #C9A227 !important; color: #3D0A0A !important; 
        border-radius: 8px !important; font-weight: 700 !important; border: none !important; 
        width: 100% !important; padding: 10px 0 !important; font-size: 12px !important;
        margin-top: 15px !important;
    }

    /* CSS BAGIAN BAWAH (DETAIL PROFIL) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #6B1414 !important; 
        border: 2px solid #FFD700 !important; 
        border-radius: 16px !important;
        padding: 30px !important; 
        margin-bottom: 30px !important;
    }
    
    /* FOTO BAWAH */
    .profile-pic-detail { 
        width: 120px; height: 120px; border-radius: 50%; 
        border: 3px solid #FFD700; overflow: hidden; margin-top: 10px;
    }
    .profile-pic-detail img { 
        width: 100%; height: 100%; 
        object-fit: cover; 
    }
    
    .d-name { font-weight: 700; color: #FFD700 !important; font-size: 24px; margin-bottom: 5px; }
    .d-role { color: #E2E8F0 !important; font-size: 15px; margin-bottom: 25px; font-weight: 600; }
    .d-title { font-weight: 700; color: #FFFFFF !important; font-size: 17px; margin-bottom: 10px; margin-top: 15px; }
    .d-text { color: #FFFFFF !important; font-size: 14px; line-height: 1.8; margin-bottom: 20px; text-align: justify; }

    /* ========================================== */
    /* TAMBAHAN CSS KHUSUS UNTUK LAYAR HP (MOBILE) */
    /* ========================================== */
    @media (max-width: 768px) {
        /* 1. Ubah layout 5 kolom jadi 1 kolom ke bawah */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 15px !important;
        }
        
        /* 2. Pastikan kotak mengisi layar penuh di HP */
        div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            margin-bottom: 10px !important;
            padding: 20px 15px !important;
        }

        /* 3. Sesuaikan ukuran font agar tidak terlalu besar di HP */
        .d-name { font-size: 20px !important; }
        .d-role { font-size: 13px !important; margin-bottom: 15px !important; }
        .d-title { font-size: 15px !important; }
        .d-text { font-size: 13px !important; text-align: left !important; }

        /* 4. Sesuaikan ukuran foto di HP */
        .profile-pic { width: 100px !important; height: 100px !important; }
        .profile-pic-detail { margin: 0 auto 15px auto !important; }

        /* 5. Kurangi padding kotak bawah agar layar tidak sempit */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            padding: 15px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header 
st.markdown("<h2 style='text-align: center; color: #FFD700 !important; margin-bottom: 40px;'>Sistem Informasi UBSI</h2>", unsafe_allow_html=True)

# ==========================================
# 1. BAGIAN ATAS: 5 KOTAK
# ==========================================
cols = st.columns(5, gap="medium")

for i, col in enumerate(cols):
    with col:
        d = data_anggota[i]
        
        # Panggil fungsi penajam
        b64 = get_optimized_base64(d["foto"], size=(240, 240))
        
        if b64:
            img_html = f'<div class="profile-pic"><img src="data:image/jpeg;base64,{b64}"></div>'
        else:
            img_html = f'<div class="profile-pic" style="background:#C9A227; display:flex; align-items:center; justify-content:center; font-size:35px; font-weight:bold; color:#3D0A0A;">{d["nama"][0]}</div>'

        html_content = f"""<div style="height: 130px; display: flex; justify-content: center; align-items: flex-start;">{img_html}</div>
<div style="height: 45px; display: flex; justify-content: center; align-items: center; overflow: hidden; margin-top: 10px;">
<div style="font-weight: 700; font-size: 14px; line-height: 1.2; text-align: center;">{d['nama']}</div>
</div>
<div style="height: 30px; display: flex; justify-content: center; align-items: flex-start; margin-bottom: 10px;">
<div style="font-size: 12px; text-align: center; color: #E2E8F0 !important;">{d['role']}</div>
</div>
<div style="border-top: 1px solid rgba(255,255,255,0.2); margin: 10px 0 15px 0;"></div>
<div style="text-align: left;">
<div style="font-size: 12px; font-weight: 700; color: #FFD700 !important; margin-bottom: 12px;">📬 Kontak</div>
<a href="mailto:{d['email']}" style="display: flex; align-items: center; gap: 8px; font-size: 11px; margin-bottom: 10px;">
<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="#FFD700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{d['email']}</span>
</a>
<a href="https://wa.me/62{d['wa'][1:]}" style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
<svg class="icon-svg" viewBox="0 0 24 24" fill="#FFD700"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
<span>WhatsApp</span>
</a>
</div>"""
        
        st.markdown(html_content, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: auto;"></div>', unsafe_allow_html=True)
        
        if Path(d["cv"]).exists():
            with open(d["cv"], "rb") as pdf:
                st.download_button(label="📄 Download CV", data=pdf, file_name=f"CV_{d['nama']}.pdf", mime="application/pdf", key=f"btn_{i}", use_container_width=True)
        else:
            st.button("📄 Download CV", key=f"btn_{i}", disabled=True, use_container_width=True)

# Garis pemisah
st.markdown("<hr style='border: 2px solid #FFD700; margin: 50px 0;'>", unsafe_allow_html=True)

# ==========================================
# 2. BAGIAN BAWAH: PENJELASAN DETAIL
# ==========================================
st.markdown("<h2 style='text-align: center; color: #FFD700 !important; margin-bottom: 40px;'>Profil Lengkap Anggota</h2>", unsafe_allow_html=True)

for i, d in enumerate(data_anggota):
    with st.container(border=True):
        col_foto, col_teks = st.columns([1, 3], gap="large")
        
        with col_foto:
            b64 = get_optimized_base64(d["foto"], size=(240, 240))
            if b64:
                st.markdown(f'<div class="profile-pic-detail"><img src="data:image/jpeg;base64,{b64}"></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="profile-pic-detail" style="background:#C9A227; display:flex; align-items:center; justify-content:center; font-size:45px; font-weight:bold; color:#3D0A0A;">{d["nama"][0]}</div>', unsafe_allow_html=True)
        
        with col_teks:
            st.markdown(f'<div class="d-name">{d["nama"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="d-role">{d["role"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="d-title">👨‍💻 About Me</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="d-text">{d["about"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="d-title">💼 Pengalaman, Pendidikan & Keahlian</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="d-text">{d["pengalaman"]}</div>', unsafe_allow_html=True)