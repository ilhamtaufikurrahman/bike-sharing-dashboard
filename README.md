# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan submission akhir untuk kelas **Belajar Fundamental Analisis Data** di **Dicoding Indonesia**. Proyek ini mencakup analisis eksplorasi data (*Exploratory Data Analysis / EDA*), pembersihan data, visualisasi data, analisis segmentasi lanjutan (*clustering & binning*), serta pengembangan dashboard interaktif menggunakan **Streamlit**.

---

## 📌 Identitas Pengembang
- **Nama:** Ilham Taufikurrahman
- **Email:** ilhamt35@gmail.com
- **ID Dicoding:** ilhamtaufikurrahman

---

## 📂 Struktur Direktori Proyek

Sesuai dengan ketentuan submission Dicoding:
```text
submission
├── dashboard/
│   ├── dashboard.py         # Skrip aplikasi dashboard Streamlit
│   ├── hourly_data.csv      # Dataset granular per jam yang telah dibersihkan
│   └── main_data.csv        # Dataset harian utama yang telah dibersihkan
├── data/
│   ├── day.csv              # Raw dataset harian (Bike Sharing)
│   ├── hour.csv             # Raw dataset per jam (Bike Sharing)
│   └── Readme.txt           # Dokumentasi asli dataset
├── notebook.ipynb           # Jupyter Notebook analisis lengkap (telah dieksekusi)
├── README.md                # Panduan proyek & cara menjalankan
├── requirements.txt         # Daftar dependensi library Python
└── url.txt                  # Tautan URL dashboard di Streamlit Cloud
```

---

## 🎯 Pertanyaan Bisnis yang Dijawab

1. **Pertanyaan 1 (Pengaruh Musim & Cuaca terhadap Volume Peminjaman):**  
   *Bagaimana pengaruh perubahan musim (season) dan kondisi cuaca (weathersit) terhadap rata-rata jumlah penyewaan sepeda harian (cnt) sepanjang periode 2011–2012, serta pada musim dan kondisi cuaca apa penyewaan mencapai volume tertinggi dan terendah?*
2. **Pertanyaan 2 (Pola Jam Sibuk Pengguna Kasual vs Terdaftar):**  
   *Bagaimana perbedaan pola distribusi peminjaman sepeda per jam (hourly rental pattern) antara pengguna kasual (casual users) dan pengguna terdaftar (registered users) pada hari kerja (working days) dibandingkan akhir pekan/libur (weekends/holidays) sepanjang 2011–2012?*
3. **Analisis Lanjutan (Clustering & Binning):**  
   *Bagaimana hasil segmentasi permintaan penyewaan sepeda berdasarkan klaster kenyamanan suhu (Temperature Binning: Cold, Mild, Warm, Hot) dan klaster jam operasional mobilitas perkotaan (Off-Peak, Morning Rush, Mid-Day Leisure, Evening Rush, Night)?*

---

## ⚙️ Cara Menjalankan Dashboard Streamlit di Lingkungan Lokal

### 1. Prasyarat (*Prerequisites*)
Pastikan Anda telah menginstal **Python** (versi 3.8 ke atas) pada sistem Anda.

### 2. Kloning atau Ekstrak Berkas Proyek
Buka terminal / Command Prompt / PowerShell, lalu masuk ke folder `submission`:
```bash
cd submission
```

### 3. Buat dan Aktifkan Virtual Environment (Disarankan)
- **Windows (Command Prompt / PowerShell):**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Instal Dependensi
Jalankan perintah berikut untuk menginstal pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi Dashboard
Jalankan Streamlit dengan perintah:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard secara otomatis akan terbuka di peramban web (*browser*) Anda pada alamat:
`http://localhost:8501`

---

## 📊 Cara Menjalankan Jupyter Notebook

Untuk meninjau proses analisis data langkah demi langkah:
1. Pastikan Jupyter Notebook atau JupyterLab telah terpasang:
   ```bash
   pip install jupyter
   ```
2. Buka notebook:
   ```bash
   jupyter notebook notebook.ipynb
   ```
3. Seluruh sel kode telah dieksekusi dengan rapi (*executed with live visualizations and summary tables*). Anda juga dapat memilih menu **Kernel -> Restart & Run All** untuk mengeksekusi ulang.

---

## 🌐 Deploy ke Streamlit Cloud

Tautan dashboard yang telah di-deploy secara publik dapat diakses melalui:
- **URL Dashboard:** Cek berkas `url.txt` atau kunjungi tautan yang tertera di dalamnya.
