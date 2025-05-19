import streamlit as st

# ========================
# Tambahkan background & gaya teks
# ========================
def set_background_with_overlay(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        * {{
            color: black !important;
        }}
        h1, h2, h3, h4 {{
            color: black !important;
        }}
        table, th, td {{
            color: black !important;
            border: 1px solid black !important;
        }}
        .streamlit-expanderHeader, .stTextInput, .stNumberInput, .stSelectbox {{
            color: black !important;
        }}
        .stButton button {{
            background-color: #4CAF50;
            color: white !important;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        }}
        .stButton button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

background_url = "https://i.pinimg.com/736x/01/6c/d4/016cd4f6c8f71d37c06cd72de6e8dbbe.jpg"
set_background_with_overlay(background_url)

# ========================
# Inisialisasi halaman
# ========================
if 'halaman' not in st.session_state:
    st.session_state.halaman = 'form'

# ========================
# Fungsi perhitungan
# ========================
def hitung_kalori(berat, tinggi, usia, jenis_kelamin, aktivitas):
    if jenis_kelamin == "Laki-laki":
        bmr = 66 + (13.7 * berat) + (5 * tinggi) - (6.8 * usia)
    else:
        bmr = 655 + (9.6 * berat) + (1.8 * tinggi) - (4.7 * usia)

    faktor = {"Rendah": 1.2, "Sedang": 1.55, "Tinggi": 1.9}
    kalori = bmr * faktor[aktivitas]
    return round(kalori)

def hitung_makronutrien(kalori):
    protein_gram = round((kalori * 0.15) / 4)
    lemak_gram = round((kalori * 0.25) / 9)
    karbo_gram = round((kalori * 0.60) / 4)
    return protein_gram, lemak_gram, karbo_gram

# ========================
# Halaman 1: Form
# ========================
if st.session_state.halaman == 'form':
    st.title("🍎 Aplikasi Asupan Gizi & Nutrisi Sehat")
    st.header("🔍 Masukkan Data Pribadimu")

    with st.form(key='form_data'):
        nama = st.text_input("Nama")
        usia = st.number_input("Usia (tahun)", min_value=1, max_value=100)
        berat = st.number_input("Berat Badan (kg)", min_value=1.0)
        tinggi = st.number_input("Tinggi Badan (cm)", min_value=30.0)
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        aktivitas = st.selectbox("Tingkat Aktivitas Fisik", ["Rendah", "Sedang", "Tinggi"])
        lanjut = st.form_submit_button("Lanjutkan ke Hasil")

    if lanjut:
        st.session_state.update({
            'nama': nama,
            'usia': usia,
            'berat': berat,
            'tinggi': tinggi,
            'jenis_kelamin': jenis_kelamin,
            'aktivitas': aktivitas,
            'halaman': 'hasil'
        })
        st.rerun()

# ========================
# Halaman 2: Hasil
# ========================
elif st.session_state.halaman == 'hasil':
    st.title("📊 Hasil Asupan Gizi Harianmu")

    kebutuhan_kalori = hitung_kalori(
        st.session_state.berat,
        st.session_state.tinggi,
        st.session_state.usia,
        st.session_state.jenis_kelamin,
        st.session_state.aktivitas
    )
    protein, lemak, karbo = hitung_makronutrien(kebutuhan_kalori)

    st.success(f"Halo {st.session_state.nama}, berikut kebutuhan harianmu:")
    st.write(f"🔥 Kalori: {kebutuhan_kalori} kkal")
    st.write(f"🥩 Protein: {protein} gram")
    st.write(f"🥑 Lemak: {lemak} gram")
    st.write(f"🍚 Karbohidrat: {karbo} gram")

    st.caption("📚 Sumber perhitungan: Harris, J. A., & Benedict, F. G. (1919). A biometric study of human basal metabolism. Washington, DC: Carnegie Institution of Washington.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Kembali ke Form"):
            st.session_state.halaman = 'form'
            st.rerun()

    with col2:
        if st.button("Lanjutkan ke Rekomendasi Gizi Usia"):
            st.session_state.halaman = 'rekomendasi'
            st.rerun()

# ========================
# Halaman 3: Rekomendasi Gizi + Makanan
# ========================
elif st.session_state.halaman == 'rekomendasi':
    st.title("📘 Rekomendasi Gizi dan Pola Makan Sehat")

    st.subheader("🥗 Makanan Sehat vs 🍔 Tidak Sehat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ✅ Makanan Sehat")
        st.markdown("""
        - Sayuran dan buah segar  
        - Makanan yang direbus, dikukus, atau dipanggang  
        - Sumber protein tanpa lemak (ikan, ayam tanpa kulit, tahu, tempe)  
        - Sumber karbohidrat kompleks (beras merah, roti gandum)  
        - Camilan sehat seperti kacang panggang, yoghurt rendah lemak  
        """)
    with col2:
        st.markdown("#### 🚫 Makanan Tidak Sehat")
        st.markdown("""
        - Makanan yang digoreng dengan banyak minyak  
        - Makanan cepat saji dan olahan tinggi lemak jenuh/trans  
        - Minuman manis seperti soda dan sirup  
        - Camilan tinggi gula dan garam (keripik, permen, kue kemasan)  
        - Daging olahan (sosis, nugget)  
        """)

    st.caption("📚 Sumber: [Nestlé Indonesia – Makanan Sehat & Tidak Sehat](https://www.nestle.co.id/kisah/makanan-sehat-dan-tidak-sehat)")

    st.markdown("### 📘 Berdasarkan PMK No. 28 Tahun 2019")

    st.markdown("""
    | Kelompok Umur | Energi (kkal) | Protein (g) | Lemak (g) | Karbohidrat (g) |
    |:--------------|:-------------:|:-----------:|:---------:|:---------------:|
    | 1–3 tahun     | 1350          | 20          | 45        | 215             |
    | 4–6 tahun     | 1400          | 25          | 50        | 220             |
    | 7–9 tahun     | 1650          | 40          | 55        | 250             |
    | Laki-laki ||||| 
    | 10–12 tahun   | 2000          | 50          | 65        | 300             |
    | 13–15 tahun   | 2400          | 70          | 80        | 350             |
    | 16–18 tahun   | 2650          | 75          | 85        | 400             |
    | 19–29 tahun   | 2650          | 65          | 75        | 430             |
    | 30–49 tahun   | 2550          | 65          | 70        | 415             |
    | 50–64 tahun   | 2150          | 60          | 60        | 340             |
    | 65–80 tahun   | 1800          | 60          | 50        | 275             |
    | >80 tahun     | 1600          | 64          | 45        | 250             |
    | Perempuan ||||| 
    | 10–12 tahun   | 1900          | 55          | 60        | 280             |
    | 13–15 tahun   | 2050          | 65          | 70        | 300             |
    | 16–18 tahun   | 2100          | 65          | 70        | 300             |
    | 19–29 tahun   | 2250          | 60          | 65        | 360             |
    | 30–49 tahun   | 2150          | 60          | 60        | 340             |
    | 50–64 tahun   | 1800          | 50          | 50        | 280             |
    | 65–80 tahun   | 1550          | 58          | 45        | 230             |
    | >80 tahun     | 1400          | 58          | 40        | 200             |
    """)

    st.caption("📚 Sumber: [PMK No. 28 Tahun 2019](http://hukor.kemkes.go.id/uploads/produk_hukum/PMK_No__28_Th_2019_ttg_Angka_Kecukupan_Gizi_Yang_Dianjurkan_Untuk_Masyarakat_Indonesia.pdf)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Kembali ke Hasil"):
            st.session_state.halaman = 'hasil'
            st.rerun()

    with col2:
        if st.button("🔄 Hitung Ulang dari Awal"):
            st.session_state.halaman = 'form'
            st.rerun()