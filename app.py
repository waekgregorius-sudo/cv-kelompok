import streamlit as st
import base64
import io
from PIL import Image
from pathlib import Path
import qrcode
import json
import zipfile
from data import DATA_ANGGOTA, load_guestbook, save_guestbook

st.set_page_config(page_title="E-CV Kelompok UBSI", page_icon="🎓", layout="wide")

LINK_WEB = "https://gregorius-portfolio.streamlit.app/"

# ==========================================
# STATE & FUNGSI
# ==========================================
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'lang' not in st.session_state: st.session_state.lang = 'id'
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user' not in st.session_state: st.session_state.user = None

@st.cache_data
def get_optimized_base64(image_path, size=(240, 240)):
    if not Path(image_path).exists(): return None
    try:
        img = Image.open(image_path)
        width, height = img.size
        min_dim = min(width, height)
        left, top = (width - min_dim) / 2, (height - min_dim) / 2
        right, bottom = left + min_dim, top + min_dim
        img = img.crop((left, top, right, bottom)).resize(size, Image.Resampling.LANCZOS)
        if img.mode in ('RGBA', 'P'): img = img.convert('RGB')
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=95)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        return None

@st.cache_data
def get_qr_base64(text, size=150):
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").resize((size, size), Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@st.cache_data
def create_zip_cv():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for member in DATA_ANGGOTA:
            if Path(member["cv"]).exists():
                zip_file.write(member["cv"], arcname=f"CV_{member['nama'].replace(' ', '_')}.pdf")
    return zip_buffer.getvalue()

# ==========================================
# CSS TAMPILAN
# ==========================================
bg_color = "#0b1120" if st.session_state.theme == 'dark' else "#f8fafc"
card_color = "#0f172a" if st.session_state.theme == 'dark' else "#ffffff"
text_color = "#f8fafc" if st.session_state.theme == 'dark' else "#1e293b"
subtext_color = "#94a3b8" if st.session_state.theme == 'dark' else "#64748b"
border_color = "rgba(255,255,255,0.1)" if st.session_state.theme == 'dark' else "rgba(0,0,0,0.1)"

st.markdown(f"""
<style>
    /* GLOBAL */
    .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    .block-container {{ padding-top: 1rem !important; max-width: 1300px !important; }}
    #MainMenu, header, footer {{visibility: hidden;}}
    
    /* HEADER UTAMA */
    .main-header {{ text-align: center; padding: 20px 0 30px 0; }}
    .main-header h1 {{ background: linear-gradient(135deg, {text_color} 0%, #60A5FA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 800; letter-spacing: 2px; }}

    /* PAKSA SEMUA TOMBOL JADI BIRU & PUTIH */
    .stButton > button, .stDownloadButton > button {{
        background-color: #2563EB !important; 
        color: #ffffff !important; 
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background-color: #1E40AF !important;
        border-color: #60A5FA !important;
    }}

    /* AREA FORM (BUKU TAMU) */
    div[data-testid="stForm"] {{
        background-color: {card_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }}
    
    /* PAKSA SEMUA TEKS (LABEL & PLACEHOLDER) DI DALAM FORM JADI PUTIH */
    div[data-testid="stForm"] label p {{
        color: {text_color} !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stForm"] input::placeholder {{
        color: {subtext_color} !important;
        opacity: 1 !important;
    }}
    div[data-testid="stForm"] input {{
        color: {text_color} !important;
        background-color: {bg_color} !important;
        border: 1px solid {border_color} !important;
    }}

    /* TOMBOL KIRIM PESAN DI DALAM FORM */
    div[data-testid="stForm"] button {{
        background-color: #2563EB !important;
        color: #ffffff !important;
        border: 1px solid #3B82F6 !important;
        width: 100% !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stForm"] button:hover {{
        background-color: #1E40AF !important;
    }}
    div[data-testid="stForm"] button p {{
        color: #ffffff !important; /* Paksa teks tombol jadi putih */
    }}

    /* KOTAK PENCARIAN (HOME) */
    input {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Selectbox */
    div[data-baseweb="select"] > div {{
        background-color: {card_color} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}

    /* KARTU PROFIL */
    div[data-testid="stVerticalBlockBorderWrapper"] {{ 
        background-color: {card_color} !important; 
        border: 1px solid {border_color} !important; 
        border-radius: 12px !important; 
        padding: 20px !important; 
        height: 100% !important;
    }}
    .profile-pic {{ width: 120px; height: 120px; margin: 0 auto; border-radius: 50%; border: 3px solid #3B82F6; overflow: hidden; }}
    .profile-pic img {{ width: 100%; height: 100%; object-fit: cover; }}
    
    /* SKILL BADGES */
    .skill-badge {{ display: inline-flex; align-items: center; background: rgba(37, 99, 235, 0.15); color: {text_color}; padding: 6px 12px; border-radius: 8px; font-size: 13px; margin: 5px; font-weight: 600; border: 1px solid rgba(37, 99, 235, 0.3); gap: 8px; }}
    .skill-badge img {{ width: 20px; height: 20px; object-fit: contain; }}

    /* KARTU BAWAH */
    .bottom-cards-container {{ display: flex; gap: 20px; align-items: stretch; margin-top: 20px; flex-wrap: wrap; }}
    .bottom-card {{ 
        flex: 1 1 280px; background-color: {card_color}; border: 1px solid {border_color}; 
        border-radius: 12px; padding: 30px; display: flex; flex-direction: column; box-sizing: border-box;
    }}
    .bottom-card h3 {{ color: {text_color} !important; border-bottom: 1px solid {border_color}; padding-bottom: 12px; }}
    .bottom-card p {{ color: {subtext_color} !important; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# TOMBOL ATAS
# ==========================================
teks = {
    'id': {'cari': "Cari nama anggota...", 'filter': "Filter Skill", 'semua': "Semua Skill", 'buku_tamu': "📖 Buku Tamu & Testimoni", 'kirim': "Kirim Pesan", 'nama': "Nama Anda", 'pesan': "Pesan/Testimoni"},
    'en': {'cari': "Search member name...", 'filter': "Filter Skill", 'semua': "All Skills", 'buku_tamu': "📖 Guestbook & Testimonial", 'kirim': "Send Message", 'nama': "Your Name", 'pesan': "Message/Testimonial"}
}
t = teks[st.session_state.lang]

col_opt1, col_opt2, col_opt3, _ = st.columns([1.5, 1, 1.5, 6])
with col_opt1:
    if st.button("🌙 Dark" if st.session_state.theme == 'dark' else "☀️ Light", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
with col_opt2:
    if st.button("🇬🇧 EN" if st.session_state.lang == 'id' else "🇮🇩 ID", use_container_width=True):
        st.session_state.lang = 'en' if st.session_state.lang == 'id' else 'id'
        st.rerun()
with col_opt3:
    zip_data = create_zip_cv()
    st.download_button(label="📥 ZIP CV", data=zip_data, file_name="Semua_CV_ECV.zip", mime="application/zip", use_container_width=True)

# ==========================================
# HALAMAN HOME
# ==========================================
if st.session_state.page == 'home':
    st.markdown('<div class="main-header"><h1>SISTEM INFORMASI UBSI</h1></div>', unsafe_allow_html=True)

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input(t['cari'], placeholder=t['cari'], label_visibility="collapsed")
    with col_filter:
        all_skills = list(set([skill for member in DATA_ANGGOTA for skill in member["skills"]]))
        selected_skill = st.selectbox(t['filter'], [t['semua']] + all_skills, label_visibility="collapsed")

    filtered_anggota = DATA_ANGGOTA
    if search_query: filtered_anggota = [d for d in filtered_anggota if search_query.lower() in d["nama"].lower()]
    if selected_skill != t['semua']: filtered_anggota = [d for d in filtered_anggota if selected_skill in d["skills"]]

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered_anggota:
        st.warning("Data tidak ditemukan." if st.session_state.lang == 'id' else "Data not found.")
    else:
        cols = st.columns(len(filtered_anggota) if len(filtered_anggota) < 5 else 5, gap="medium")
        for i, col in enumerate(cols):
            with col:
                with st.container(border=True):
                    d = filtered_anggota[i]
                    b64 = get_optimized_base64(d["foto"], size=(240, 240))
                    img_html = f'<div class="profile-pic"><img src="data:image/jpeg;base64,{b64}"></div>' if b64 else f'<div class="profile-pic" style="background:#1e293b; display:flex; align-items:center; justify-content:center; font-size:35px; font-weight:bold;">{d["nama"][0]}</div>'

                    st.markdown(f"""{img_html}
                    <div style="text-align: center; margin-top: 15px;">
                        <div style="font-weight: 700; font-size: 16px; color: {text_color}; min-height: 40px; display: flex; align-items: center; justify-content: center;">{d['nama']}</div>
                        <div style="font-size: 12px; color: #60A5FA; font-weight: 600; margin-bottom: 20px; min-height: 30px;">{d['role']}</div>
                        <div style="text-align: left; margin-bottom: 15px; border-top: 1px solid {border_color}; padding-top: 15px;">
                            <a href="mailto:{d['email']}" style="display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 8px; color: {subtext_color} !important; text-decoration: none;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                                <span>Email</span>
                            </a>
                            <a href="https://wa.me/62{d['wa'][1:]}" style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: {subtext_color} !important; text-decoration: none;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="#64748b"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                                <span>WhatsApp</span>
                            </a>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    if Path(d["cv"]).exists():
                        with open(d["cv"], "rb") as pdf:
                            st.download_button(label="📄 Unduh CV", data=pdf, file_name=f"CV_{d['nama']}.pdf", mime="application/pdf", key=f"btn_{d['id']}", use_container_width=True)
                    
                    if st.button("LIHAT PROFIL" if st.session_state.lang == 'id' else "VIEW PROFILE", key=f"view_{d['id']}", use_container_width=True):
                        st.session_state.user = d["id"]
                        st.session_state.page = 'profile'
                        st.rerun()

    st.markdown("---")
    
    # BUKU TAMU
    st.markdown(f"### {t['buku_tamu']}")
    with st.form("form_buku_tamu", clear_on_submit=True):
        col_nama, col_pesan = st.columns([1, 2])
        with col_nama: gb_nama = st.text_input(t['nama'])
        with col_pesan: gb_pesan = st.text_input(t['pesan'])
        submit_gb = st.form_submit_button(t['kirim'])
        if submit_gb and gb_nama and gb_pesan:
            save_guestbook({"nama": gb_nama, "pesan": gb_pesan})
            st.success("Tersimpan!" if st.session_state.lang == 'id' else "Saved!")
            st.rerun()

    pesan_tamu = load_guestbook()
    if pesan_tamu:
        for p in reversed(pesan_tamu):
            st.markdown(f'<div style="background: {card_color}; border-left: 4px solid #3B82F6; padding: 15px; margin-bottom: 10px; border-radius: 5px;"><div style="color: #3B82F6; font-weight: bold; margin-bottom: 5px;">💬 {p["nama"]}</div><div style="color: {subtext_color}; font-size: 14px;">{p["pesan"]}</div></div>', unsafe_allow_html=True)

    # KARTU BAWAH
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: {text_color}; margin-bottom: 30px; font-weight: 700;'>LEBIH DEKAT DENGAN KAMI</h2>", unsafe_allow_html=True)
    
    qr_b64 = get_qr_base64(LINK_WEB, size=150)
    qr_url = f"data:image/png;base64,{qr_b64}"
    
    html_kartu_bawah = f"""<div class="bottom-cards-container">
        <div class="bottom-card"><h3>🏛️ Tentang Kami</h3><p>Kami adalah kelompok mahasiswa Sistem Informasi UBSI yang berdedikasi untuk menciptakan solusi digital yang inovatif, kreatif, dan fungsional.</p><p style="font-size: 12px; color: #60A5FA; margin-bottom: 0; font-weight: 700;">Mata Kuliah: Digital Kreatif</p></div>
        <div class="bottom-card"><h3>🚀 Proyek Bersama</h3><p>Sebuah aplikasi web portofolio interaktif yang menampilkan profil 5 anggota kelompok dalam satu tautan. Dibangun menggunakan Python dan Streamlit, dengan desain responsif (mobile-friendly) dan tema korporat gelap.</p></div>
        <div class="bottom-card" style="text-align: center;"><h3>📱 Scan Tautan</h3><p>Buka portofolio ini di HP Anda dengan memindai QR Code di bawah ini.</p><div style="display: flex; justify-content: center; margin-top: 10px;"><a href="{LINK_WEB}" target="_blank"><img src="{qr_url}" style="width: 120px; height: 120px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); padding: 5px; background: white;"></a></div></div>
    </div>"""
    st.markdown(html_kartu_bawah, unsafe_allow_html=True)

    # FOOTER
    st.markdown(f'<div style="text-align: center; margin-top: 50px; padding-top: 25px; border-top: 1px solid {border_color};"><p style="color: {subtext_color}; font-size: 13px;">© 2026 Sistem Informasi UBSI - Digital Kreatif</p></div>', unsafe_allow_html=True)

# ==========================================
# HALAMAN PROFIL
# ==========================================
elif st.session_state.page == 'profile':
    user_id = st.session_state.user
    user_index = next((i for i, x in enumerate(DATA_ANGGOTA) if x["id"] == user_id), None)
    
    if user_index is not None:
        d = DATA_ANGGOTA[user_index]
        if st.button("⬅️ Kembali" if st.session_state.lang == 'id' else "⬅️ Back", key="back_btn"):
            st.session_state.page = 'home'
            st.session_state.user = None
            st.rerun()

        with st.container(border=True):
            b64 = get_optimized_base64(d["foto"], size=(240, 240))
            if b64: 
                st.markdown(f'<div style="text-align: center;"><div class="profile-pic" style="width: 180px; height: 180px; border-width: 5px; margin: 0 auto;"><img src="data:image/jpeg;base64,{b64}"></div></div>', unsafe_allow_html=True)
            
            st.markdown(f"<h1 style='text-align: center; color: {text_color}; margin-bottom: 0; margin-top: 15px;'>{d['nama']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #60A5FA; margin-top: 5px;'>{d['role']}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"<hr style='border: 1px solid {border_color}; margin: 20px 0;'>", unsafe_allow_html=True)

            st.markdown(f"<h4 style='color: {text_color};'>About Me</h4>", unsafe_allow_html=True)
            st.write(d["about"])
            
            st.markdown(f"<h4 style='color: {text_color};'>Skills & Technologies</h4>", unsafe_allow_html=True)
            
            icons = {
                "Laravel": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-original.svg",
                "PHP": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg",
                "MySQL": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
                "Git": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
                "Figma": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg",
                "Adobe XD": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/xd/xd-plain.svg",
                "Design Thinking": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/trello/trello-plain.svg",
                "HTML": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
                "React": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
                "Tailwind": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg",
                "Flutter": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg",
                "Dart": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dart/dart-original.svg",
                "Docker": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
                "Node.js": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg",
                "Testing": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jest/jest-plain.svg"
            }

            skills_html = ""
            for s in d["skills"]:
                icon_url = icons.get(s, "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/devicon/devicon-original.svg")
                skills_html += f'<div class="skill-badge"><img src="{icon_url}"><span>{s}</span></div>'
            
            st.markdown(skills_html, unsafe_allow_html=True)

            st.markdown(f"<h4 style='color: {text_color}; margin-top: 20px;'>Experience</h4>", unsafe_allow_html=True)
            st.write(d["experience"])

            st.markdown(f"<h4 style='color: {text_color}; margin-top: 20px;'>Projects</h4>", unsafe_allow_html=True)
            st.write(d["projects"])

            st.markdown(f"<h4 style='color: {text_color}; margin-top: 20px;'>Education</h4>", unsafe_allow_html=True)
            st.write(d["education"])

    else:
        st.session_state.page = 'home'
        st.rerun()
