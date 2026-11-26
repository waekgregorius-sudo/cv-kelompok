import json
import os

DATA_ANGGOTA = [
    {
        "id": "gregorius",
        "nama": "Gregorius Waek", "role": "Product Manager & Fullstack Dev", "foto": "assets/gregorius.jpeg", "cv": "assets/cv.pdf", "email": "waekgregorius@gmail.com", "wa": "081234567890",
        "skills": ["Laravel", "PHP", "MySQL", "Git"],
        "about": "Mahasiswa Sistem Informasi semester 7 di UBSI yang berfokus pada pengembangan web. Berperan sebagai Product Manager dan Fullstack Developer dalam proyek E-CV ini.",
        "experience": "Web Developer Intern | Majalah Hidup (2026 - Sekarang).\nMerancang dan membangun ulang website utama perusahaan menggunakan Laravel 12.",
        "projects": "Full-stack Web App (Majalah HIDUP).\nMembangun sistem dari nol dengan fitur Admin Dashboard.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    },
    {
        "id": "maria",
        "nama": "Maria Oktaviani Timung", "role": "UI/UX Designer", "foto": "assets/maria.jpeg", "cv": "assets/cv_maria.pdf", "email": "maria.oktaviani@gmail.com", "wa": "081234567891",
        "skills": ["Figma", "Adobe XD", "Design Thinking"],
        "about": "Mahasiswa Sistem Informasi yang berfokus pada perancangan antarmuka (UI) dan pengalaman pengguna (UX). Bertanggung jawab atas design system E-CV ini.",
        "experience": "Freelance UI/UX Designer (2024 - Sekarang).\nMendesain aplikasi mobile untuk UMKM lokal.",
        "projects": "Redesign Aplikasi Mobile UMKM.\nMembuat wireframe hingga prototipe interaktif menggunakan Figma.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    },
    {
        "id": "anggun",
        "nama": "Anggun Berliani", "role": "Front-End Developer (Inti)", "foto": "assets/anggun.jpeg", "cv": "assets/cv_anggun.pdf", "email": "anggun@gmail.com", "wa": "081234567892",
        "skills": ["HTML", "React", "Tailwind"],
        "about": "Mahasiswa Sistem Informasi dengan ketelitian tinggi pada pengembangan antarmuka. Bertanggung jawab atas struktur halaman dan navigasi.",
        "experience": "Web Developer Intern | PT Teknologi Nusantara (2025).",
        "projects": "Landing Page Event Kampus.\nMembangun antarmuka interaktif menggunakan React JS.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    },
    {
        "id": "nela",
        "nama": "Nela Nyft", "role": "Front-End Developer (Konten)", "foto": "assets/nela.jpg", "cv": "assets/cv_nela.pdf", "email": "nela@gmail.com", "wa": "081234567893",
        "skills": ["Flutter", "Dart"],
        "about": "Mahasiswa Sistem Informasi yang antusias dalam pengembangan aplikasi web. Bertanggung jawab atas komponen skills dan project cards.",
        "experience": "Mobile Developer (Freelance) | 2023 - Sekarang.",
        "projects": "Aplikasi Manajemen Tugas Mahasiswa.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    },
    {
        "id": "fauzi",
        "nama": "Fauzi Ramdani Koswara", "role": "QA & Deployment", "foto": "assets/fauzi.jpeg", "cv": "assets/cv_fauzi.pdf", "email": "fauzi@gmail.com", "wa": "081234567894",
        "skills": ["Docker", "Node.js", "Testing"],
        "about": "Mahasiswa Sistem Informasi yang berfokus pada kualitas perangkat lunak. Bertanggung jawab atas pengujian responsif dan deployment.",
        "experience": "Backend & QA Intern | Startup Fintech XYZ (2025).",
        "projects": "Sistem Manajemen Inventaris.",
        "education": "S1 Sistem Informasi | UBSI Kramat 98 (2023 - Sekarang)."
    }
]

GUESTBOOK_FILE = "buku_tamu.json"

def load_guestbook():
    if os.path.exists(GUESTBOOK_FILE):
        with open(GUESTBOOK_FILE, "r") as f:
            return json.load(f)
    return []

def save_guestbook(pesan):
    data = load_guestbook()
    data.append(pesan)
    with open(GUESTBOOK_FILE, "w") as f:
        json.dump(data, f, indent=4)
