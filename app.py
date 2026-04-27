import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sistem Penilaian Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "mahasiswa" not in st.session_state:
    st.session_state.mahasiswa = []
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# ─────────────────────────────────────────────
# AKUN (username: (password, role))
# ─────────────────────────────────────────────
USERS = {
    "admin":      ("admin123",  "admin"),
    "2313010642": ("samhan642", "mahasiswa"),  # Ahmad Samhan
    "2313010623": ("khoris623", "mahasiswa"),  # Khoris Najda
    "2313010636": ("bagas636",  "mahasiswa"),  # Bagas Dzaki
}

# Mapping NIM → Nama lengkap
NAMA_MAHASISWA = {
    "2313010642": "Ahmad Samhan",
    "2313010623": "Khoris Najda",
    "2313010636": "Bagas Dzaki",
}

# ─────────────────────────────────────────────
# RULE-BASED SYSTEM  →  IF–THEN
# ─────────────────────────────────────────────
def hitung_nilai_akhir(kehadiran, tugas, uts, uas):
    return round((kehadiran * 0.10) + (tugas * 0.20) + (uts * 0.30) + (uas * 0.40), 2)

def rule_grade(na):
    if na >= 85:   return "A", "Sangat Memuaskan", "🟢"
    elif na >= 75: return "B", "Memuaskan",        "🟢"
    elif na >= 65: return "C", "Cukup",            "🟡"
    elif na >= 55: return "D", "Kurang",           "🔴"
    else:          return "E", "Tidak Lulus",      "🔴"

def rule_status(na):
    return "LULUS" if na >= 55 else "TIDAK LULUS"

# ─────────────────────────────────────────────
# HALAMAN LOGIN
# ─────────────────────────────────────────────
def halaman_login():
    st.markdown("""
        <div style='text-align:center;padding:50px 0 20px 0;'>
            <h1 style='color:#4B3DE3;'>🎓 Sistem Penilaian Mahasiswa</h1>
            <p style='color:#888;font-size:15px;'>Rule-Based System – STMIK AMIKOM Surakarta</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.container(border=True):
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True, type="primary"):
                if username in USERS and USERS[username][0] == password:
                    st.session_state.logged_in = True
                    st.session_state.username  = username
                    st.session_state.role      = USERS[username][1]
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")

            st.divider()
            st.caption("**Akun Login:**")
            st.caption("👑 Admin        → `admin` / `admin123`")
            st.caption("🎓 Ahmad Samhan → `2313010642` / `samhan642`")
            st.caption("🎓 Khoris Najda → `2313010623` / `khoris623`")
            st.caption("🎓 Bagas Dzaki  → `2313010636` / `bagas636`")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎓 Sistem Penilaian")
        st.divider()

        role_label = "👑 Admin" if st.session_state.role == "admin" else "🎓 Mahasiswa"
        st.markdown(f"**{role_label}**")
        st.markdown(f"Halo, **{st.session_state.username}**!")
        st.divider()

        if st.session_state.role == "admin":
            menu = st.radio("Menu", [
                "🏠 Dashboard",
                "➕ Tambah Nilai",
                "📊 Data Mahasiswa",
                "ℹ️ Tentang Sistem",
            ])
        else:
            menu = st.radio("Menu", [
                "🏠 Dashboard",
                "📋 Nilai Saya",
                "ℹ️ Tentang Sistem",
            ])

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username  = ""
            st.session_state.role      = ""
            st.session_state.edit_index = None
            st.rerun()

    return menu

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
def halaman_dashboard():
    st.title("🏠 Dashboard")
    st.caption("Sistem Cerdas – Rule-Based System | IF–THEN")
    st.divider()

    data  = st.session_state.mahasiswa
    total = len(data)
    lulus = sum(1 for m in data if rule_status(m["nilai_akhir"]) == "LULUS")
    rata  = round(sum(m["nilai_akhir"] for m in data) / total, 2) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Data",    total)
    c2.metric("Lulus",         lulus)
    c3.metric("Tidak Lulus",   total - lulus)
    c4.metric("Rata-rata Nilai", rata)

    st.divider()
    st.subheader("📌 Tabel Aturan IF–THEN")
    rules = {
        "Kondisi (IF Nilai Akhir)": ["≥ 85", "75 – 84", "65 – 74", "55 – 64", "< 55"],
        "Grade (THEN)":             ["A", "B", "C", "D", "E"],
        "Keterangan":               ["Sangat Memuaskan", "Memuaskan", "Cukup", "Kurang", "Tidak Lulus"],
        "Status":                   ["✅ Lulus", "✅ Lulus", "✅ Lulus", "❌ Tidak Lulus", "❌ Tidak Lulus"],
    }
    st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("⚖️ Bobot Penilaian")
    bobot = {
        "Komponen": ["Kehadiran", "Tugas", "UTS", "UAS"],
        "Bobot":    ["10%", "20%", "30%", "40%"],
        "Formula":  ["× 0.10", "× 0.20", "× 0.30", "× 0.40"],
    }
    st.dataframe(pd.DataFrame(bobot), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# TAMBAH / EDIT NILAI  (ADMIN ONLY)
# ─────────────────────────────────────────────
def halaman_tambah():
    # Validasi: reset edit_index jika index sudah tidak valid (data dihapus)
    if st.session_state.edit_index is not None:
        if st.session_state.edit_index >= len(st.session_state.mahasiswa):
            st.session_state.edit_index = None

    edit_mode = st.session_state.edit_index is not None
    st.title("✏️ Edit Data Mahasiswa" if edit_mode else "➕ Tambah Data Mahasiswa")

    existing = {}
    if edit_mode:
        existing = st.session_state.mahasiswa[st.session_state.edit_index]

    with st.form("form_nilai", clear_on_submit=not edit_mode):
        col1, col2 = st.columns(2)
        with col1:
            nim    = st.text_input("NIM *",            value=existing.get("nim", ""))
            nama   = st.text_input("Nama Mahasiswa *", value=existing.get("nama", ""))
            matkul = st.text_input("Mata Kuliah",      value=existing.get("matkul", "Sistem Cerdas"))
        with col2:
            kehadiran = st.slider("Nilai Kehadiran (bobot 10%)", 0, 100, int(existing.get("kehadiran", 80)))
            tugas     = st.slider("Nilai Tugas     (bobot 20%)", 0, 100, int(existing.get("tugas", 75)))
            uts       = st.slider("Nilai UTS       (bobot 30%)", 0, 100, int(existing.get("uts", 70)))
            uas       = st.slider("Nilai UAS       (bobot 40%)", 0, 100, int(existing.get("uas", 70)))

        cs, cc = st.columns(2)
        submitted = cs.form_submit_button("💾 Simpan", use_container_width=True, type="primary")
        cancelled = cc.form_submit_button("✖ Batal",  use_container_width=True)

    if cancelled and edit_mode:
        st.session_state.edit_index = None
        st.rerun()

    if submitted:
        if not nim.strip() or not nama.strip():
            st.error("NIM dan Nama wajib diisi!")
            return

        na               = hitung_nilai_akhir(kehadiran, tugas, uts, uas)
        grade, ket, icon = rule_grade(na)
        status           = rule_status(na)

        record = dict(
            nim=nim.strip(), nama=nama.strip(), matkul=matkul,
            kehadiran=kehadiran, tugas=tugas, uts=uts, uas=uas,
            nilai_akhir=na, grade=grade, keterangan=ket, status=status
        )

        if edit_mode:
            st.session_state.mahasiswa[st.session_state.edit_index] = record
            st.session_state.edit_index = None
            st.success("✅ Data berhasil diperbarui!")
        else:
            st.session_state.mahasiswa.append(record)
            st.success("✅ Data berhasil ditambahkan!")

        st.divider()
        st.subheader("📋 Hasil Rule-Based System")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Nilai Akhir", na)
        r2.metric("Grade",       f"{icon} {grade}")
        r3.metric("Keterangan",  ket)
        r4.metric("Status",      status)

        st.info(
            f"**IF** nilai_akhir = **{na}**  \n"
            f"**THEN** Grade = **{grade}** ({ket})  \n"
            f"**THEN** Status = **{status}**"
        )

# ─────────────────────────────────────────────
# DATA MAHASISWA  (ADMIN ONLY)
# ─────────────────────────────────────────────
def halaman_data():
    st.title("📊 Data Mahasiswa")
    data = st.session_state.mahasiswa

    if not data:
        st.info("Belum ada data. Silakan tambah melalui menu ➕ Tambah Nilai.")
        return

    search = st.text_input("🔍 Cari NIM / Nama")
    filtered_idx = [
        i for i, m in enumerate(data)
        if not search
        or search.lower() in m["nama"].lower()
        or search.lower() in m["nim"].lower()
    ]

    if not filtered_idx:
        st.warning("Data tidak ditemukan.")
        return

    rows = [data[i] for i in filtered_idx]
    df   = pd.DataFrame(rows)[[
        "nim","nama","matkul","kehadiran","tugas","uts","uas","nilai_akhir","grade","keterangan","status"
    ]]
    df.columns = ["NIM","Nama","Mata Kuliah","Kehadiran","Tugas","UTS","UAS",
                  "Nilai Akhir","Grade","Keterangan","Status"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("⚙️ Kelola Data")
    for i in filtered_idx:
        m = data[i]
        with st.expander(f"{m['nim']} – {m['nama']}  |  Grade: {m['grade']}  |  {m['status']}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**Mata Kuliah:** {m['matkul']}")
                st.write(f"**Kehadiran:** {m['kehadiran']}  |  **Tugas:** {m['tugas']}  |  **UTS:** {m['uts']}  |  **UAS:** {m['uas']}")
                st.write(f"**Nilai Akhir:** {m['nilai_akhir']}  →  **{m['grade']}** – {m['keterangan']}  |  {m['status']}")
            with c2:
                if st.button("✏️ Edit",  key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.rerun()
                if st.button("🗑️ Hapus", key=f"hapus_{i}"):
                    st.session_state.mahasiswa.pop(i)
                    st.session_state.edit_index = None  # reset agar tidak IndexError
                    st.success("Data dihapus.")
                    st.rerun()

    st.divider()
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "data_nilai.csv", "text/csv")

# ─────────────────────────────────────────────
# NILAI SAYA  (MAHASISWA ONLY)
# ─────────────────────────────────────────────
def halaman_nilai_saya():
    st.title("📋 Nilai Saya")
    username = st.session_state.username  # berisi NIM mahasiswa
    nama_tampil = NAMA_MAHASISWA.get(username, username)
    data     = st.session_state.mahasiswa

    st.markdown(f"### 👤 {nama_tampil}  |  NIM: `{username}`")
    st.divider()

    # Cocokkan berdasarkan NIM login
    milik = [m for m in data if m["nim"] == username]

    if not milik:
        st.info(
            f"Belum ada data nilai untuk NIM **{username}** ({nama_tampil}).  \n"
            "Hubungi admin untuk input nilai."
        )
        return

    for m in milik:
        with st.container(border=True):
            st.subheader(f"📚 {m['matkul']}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Kehadiran", m["kehadiran"])
            c2.metric("Tugas",     m["tugas"])
            c3.metric("UTS",       m["uts"])
            c4.metric("UAS",       m["uas"])

            st.divider()
            n1, n2, n3 = st.columns(3)
            n1.metric("Nilai Akhir", m["nilai_akhir"])
            n2.metric("Grade",       m["grade"])
            n3.metric("Status",      m["status"])

            st.info(
                f"**Keterangan:** {m['keterangan']}  \n"
                f"**IF** nilai_akhir = **{m['nilai_akhir']}**  →  "
                f"**THEN** Grade = **{m['grade']}**, Status = **{m['status']}**"
            )

# ─────────────────────────────────────────────
# TENTANG SISTEM
# ─────────────────────────────────────────────
def halaman_tentang():
    st.title("ℹ️ Tentang Sistem")
    st.markdown("""
    ### 🤖 Rule-Based System – Sistem Cerdas
    Aplikasi ini dibuat untuk **Praktikum ke-3** mata kuliah **Sistem Cerdas**
    di **STMIK AMIKOM Surakarta**.

    ---
    #### 📐 Konsep Dasar
    > *Sistem bekerja berdasarkan aturan logika **IF kondisi THEN hasil***

    #### 🔗 Aturan IF–THEN
    | Rule | Kondisi | Hasil |
    |------|---------|-------|
    | R1 | IF nilai_akhir ≥ 85   | THEN Grade A – Sangat Memuaskan |
    | R2 | IF 75 ≤ nilai < 85    | THEN Grade B – Memuaskan |
    | R3 | IF 65 ≤ nilai < 75    | THEN Grade C – Cukup |
    | R4 | IF 55 ≤ nilai < 65    | THEN Grade D – Kurang |
    | R5 | IF nilai < 55         | THEN Grade E – Tidak Lulus |
    | R6 | IF nilai_akhir ≥ 55   | THEN Status = LULUS |
    | R7 | IF nilai_akhir < 55   | THEN Status = TIDAK LULUS |

    #### 📊 Formula Nilai Akhir
    ```
    Nilai Akhir = (Kehadiran×10%) + (Tugas×20%) + (UTS×30%) + (UAS×40%)
    ```

    #### 👥 Hak Akses
    | Role | Hak Akses |
    |------|-----------|
    | 👑 Admin | Dashboard · Tambah · Edit · Hapus data semua mahasiswa |
    | 🎓 Mahasiswa | Dashboard · Lihat nilai milik sendiri saja |

    ---
    **Teknologi:** Python + Streamlit
    """)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    halaman_login()
else:
    menu = render_sidebar()

    if menu == "🏠 Dashboard":
        halaman_dashboard()

    elif menu == "➕ Tambah Nilai":
        if st.session_state.role == "admin":
            halaman_tambah()
        else:
            st.error("⛔ Akses ditolak.")

    elif menu == "📊 Data Mahasiswa":
        if st.session_state.role == "admin":
            halaman_data()
        else:
            st.error("⛔ Akses ditolak.")

    elif menu == "📋 Nilai Saya":
        if st.session_state.role == "mahasiswa":
            halaman_nilai_saya()
        else:
            st.error("⛔ Akses ditolak.")

    elif menu == "ℹ️ Tentang Sistem":
        halaman_tentang()
