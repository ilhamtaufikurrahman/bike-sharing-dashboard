import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling CSS untuk tampilan modern dan bersih
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border-left: 5px solid #2563EB;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.85rem;
        color: #6B7280;
        border-top: 1px solid #E5E7EB;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi memuat data dengan caching
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    main_data_path = os.path.join(current_dir, 'main_data.csv')
    hourly_data_path = os.path.join(current_dir, 'hourly_data.csv')
    
    # Fallback paths jika dijalankan dari root direktori
    if not os.path.exists(main_data_path):
        main_data_path = 'submission/dashboard/main_data.csv'
        hourly_data_path = 'submission/dashboard/hourly_data.csv'
    
    day_df = pd.read_csv(main_data_path)
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    hour_df = pd.read_csv(hourly_data_path)
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# ================= SIDEBAR =================
st.sidebar.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.title("🚲 Filter Dashboard")

# Filter Rentang Tanggal
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()

date_range = st.sidebar.date_input(
    label="Pilih Rentang Tanggal:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter Musim
all_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim (Season):",
    options=all_seasons,
    default=all_seasons
)

# Filter Kondisi Cuaca
all_weathers = ['Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Rain']
selected_weathers = st.sidebar.multiselect(
    label="Pilih Kondisi Cuaca:",
    options=all_weathers,
    default=all_weathers
)

# Filter Tipe Hari
day_type_option = st.sidebar.radio(
    label="Tipe Hari:",
    options=["Semua Hari", "Hari Kerja (Workingday)", "Akhir Pekan / Libur (Weekend/Holiday)"],
    index=0
)

# Terapkan filter ke dataframe
filtered_day = day_df[
    (day_df['dteday'].dt.date >= start_date) &
    (day_df['dteday'].dt.date <= end_date) &
    (day_df['season_label'].isin(selected_seasons)) &
    (day_df['weather_label'].isin(selected_weathers))
]

filtered_hour = hour_df[
    (hour_df['dteday'].dt.date >= start_date) &
    (hour_df['dteday'].dt.date <= end_date) &
    (hour_df['season_label'].isin(selected_seasons)) &
    (hour_df['weather_label'].isin(selected_weathers))
]

if day_type_option == "Hari Kerja (Workingday)":
    filtered_day = filtered_day[filtered_day['workingday'] == 1]
    filtered_hour = filtered_hour[filtered_hour['workingday'] == 1]
elif day_type_option == "Akhir Pekan / Libur (Weekend/Holiday)":
    filtered_day = filtered_day[filtered_day['workingday'] == 0]
    filtered_hour = filtered_hour[filtered_hour['workingday'] == 0]

# Informasi Author di Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Author:** Ilham Taufikurrahman")
st.sidebar.markdown("**Email:** ilhamt35@gmail.com")
st.sidebar.markdown("**Dicoding ID:** `ilhamtaufikurrahman`")

# ================= HEADER UTAMA =================
st.markdown('<div class="main-title">🚲 Bike Sharing Rental Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analisis Pola Penggunaan Sepeda, Dinamika Cuaca, dan Segmentasi Mobilitas (2011–2012)</div>', unsafe_allow_html=True)

# ================= KPI METRICS =================
col1, col2, col3, col4 = st.columns(4)

total_rentals = filtered_day['cnt'].sum() if not filtered_day.empty else 0
total_registered = filtered_day['registered'].sum() if not filtered_day.empty else 0
total_casual = filtered_day['casual'].sum() if not filtered_day.empty else 0
avg_daily = filtered_day['cnt'].mean() if not filtered_day.empty else 0

with col1:
    st.metric("Total Penyewaan (cnt)", f"{total_rentals:,} unit")
with col2:
    st.metric("Pengguna Terdaftar (Registered)", f"{total_registered:,} unit", delta=f"{(total_registered/total_rentals*100):.1f}%" if total_rentals > 0 else None)
with col3:
    st.metric("Pengguna Kasual (Casual)", f"{total_casual:,} unit", delta=f"{(total_casual/total_rentals*100):.1f}%" if total_rentals > 0 else None)
with col4:
    st.metric("Rata-Rata Sewa Harian", f"{int(avg_daily):,} unit/hari")

st.markdown("---")

# ================= TAB NAVIGASI =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tren Waktu & Overview",
    "⛅ Pengaruh Musim & Cuaca (Q1)",
    "⏰ Pola Jam: Kasual vs Terdaftar (Q2)",
    "🎯 Segmentasi & Clustering",
    "💡 Kesimpulan & Rekomendasi"
])

# ================= TAB 1: TREN WAKTU =================
with tab1:
    st.subheader("Tren Perkembangan Penyewaan Sepeda Harian")
    if filtered_day.empty:
        st.warning("Tidak ada data untuk rentang filter yang dipilih.")
    else:
        fig_trend, ax_trend = plt.subplots(figsize=(14, 5))
        ax_trend.plot(filtered_day['dteday'], filtered_day['cnt'], color='#2563EB', linewidth=1.5, label='Total Peminjaman (cnt)')
        ax_trend.plot(filtered_day['dteday'], filtered_day['registered'], color='#059669', linewidth=1.2, alpha=0.8, label='Registered Users')
        ax_trend.plot(filtered_day['dteday'], filtered_day['casual'], color='#D97706', linewidth=1.2, alpha=0.8, label='Casual Users')
        
        # 7-day rolling mean
        if len(filtered_day) >= 7:
            rolling_7 = filtered_day.set_index('dteday')['cnt'].rolling(7).mean()
            ax_trend.plot(rolling_7.index, rolling_7.values, color='#DC2626', linewidth=2.2, linestyle='--', label='7-Day Moving Average')
        
        ax_trend.set_title("Fluktuasi Harian Jumlah Sewa Sepeda (2011–2012)", fontsize=13, fontweight='bold', pad=10)
        ax_trend.set_xlabel("Tanggal", fontsize=11)
        ax_trend.set_ylabel("Jumlah Sewa Harian (unit)", fontsize=11)
        ax_trend.legend(loc='upper left', frameon=True)
        ax_trend.grid(True, linestyle=':', alpha=0.6)
        st.pyplot(fig_trend)

        st.info("💡 **Insight Tren:** Terlihat tren kenaikan yang sangat kuat dari 2011 ke 2012 dengan pola siklus musiman yang berulang: volume memuncak pada pertengahan hingga akhir tahun (musim panas dan gugur) dan menurun di awal tahun.")

# ================= TAB 2: MUSIM & CUACA (Q1) =================
with tab2:
    st.subheader("Pertanyaan 1: Pengaruh Musim dan Kondisi Cuaca terhadap Volume Peminjaman")
    st.markdown("""
    **Pertanyaan Analisis:**  
    *Bagaimana pengaruh perubahan musim (season) dan kondisi cuaca (weathersit) terhadap rata-rata jumlah penyewaan sepeda harian (cnt) sepanjang periode 2011–2012, serta pada musim dan kondisi cuaca apa penyewaan mencapai titik tertinggi dan terendah?*
    """)
    
    col_q1_a, col_q1_b = st.columns(2)
    
    with col_q1_a:
        st.markdown("#### Rata-Rata Sewa Harian Berdasarkan Musim")
        season_avg = filtered_day.groupby('season_label', observed=False)['cnt'].mean().reindex(['Spring', 'Summer', 'Fall', 'Winter']).reset_index()
        
        fig_s, ax_s = plt.subplots(figsize=(7, 5))
        palette_s = ['#94A3B8', '#FBBF24', '#16A34A', '#60A5FA']
        bars_s = ax_s.bar(season_avg['season_label'], season_avg['cnt'], color=palette_s, edgecolor='black', width=0.55)
        ax_s.set_ylabel("Rata-Rata Sewa Harian (unit)", fontsize=10, fontweight='bold')
        ax_s.set_ylim(0, max(season_avg['cnt'].max() * 1.2, 1000))
        for bar in bars_s:
            yval = bar.get_height()
            if not np.isnan(yval):
                ax_s.text(bar.get_x() + bar.get_width()/2, yval + 100, f"{int(yval):,} unit", ha='center', va='bottom', fontweight='bold', fontsize=9)
        st.pyplot(fig_s)
        
    with col_q1_b:
        st.markdown("#### Rata-Rata Sewa Harian Berdasarkan Cuaca")
        weather_avg = filtered_day.groupby('weather_label', observed=False)['cnt'].mean().reindex(['Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Rain']).dropna().reset_index()
        
        fig_w, ax_w = plt.subplots(figsize=(7, 5))
        palette_w = ['#38BDF8', '#94A3B8', '#EF4444']
        bars_w = ax_w.bar(weather_avg['weather_label'], weather_avg['cnt'], color=palette_w, edgecolor='black', width=0.55)
        ax_w.set_ylabel("Rata-Rata Sewa Harian (unit)", fontsize=10, fontweight='bold')
        ax_w.set_ylim(0, max(weather_avg['cnt'].max() * 1.2, 1000))
        for bar in bars_w:
            yval = bar.get_height()
            if not np.isnan(yval):
                ax_w.text(bar.get_x() + bar.get_width()/2, yval + 100, f"{int(yval):,} unit", ha='center', va='bottom', fontweight='bold', fontsize=9)
        st.pyplot(fig_w)

    st.success("""
    📌 **Temuan Kunci Pertanyaan 1:**
    - **Puncak Musim:** **Musim Gugur (Fall)** adalah musim paling populer dengan rata-rata tertinggi (~5.644 unit/hari), diikuti Musim Panas (Summer: ~4.992 unit/hari).
    - **Titik Terendah:** **Musim Semi (Spring)** berada di posisi paling rendah (~2.604 unit/hari) akibat suhu awal tahun yang masih dingin di Washington DC.
    - **Dampak Cuaca:** Cuaca cerah (*Clear*) menghasilkan peminjaman tertinggi (~4.877 unit/hari). Saat kondisi hujan atau bersalju (*Light Snow/Rain*), peminjaman anjlok hingga 63% menjadi hanya ~1.803 unit/hari.
    """)

# ================= TAB 3: POLA JAM (Q2) =================
with tab3:
    st.subheader("Pertanyaan 2: Pola Jam Peminjaman Pengguna Kasual vs Terdaftar")
    st.markdown("""
    **Pertanyaan Analisis:**  
    *Bagaimana perbedaan pola distribusi peminjaman sepeda per jam (hourly rental pattern) antara pengguna kasual (casual users) dan pengguna terdaftar (registered users) pada hari kerja dibandingkan akhir pekan/libur sepanjang 2011–2012?*
    """)
    
    col_q2_a, col_q2_b = st.columns(2)
    
    hourly_work = filtered_hour[filtered_hour['workingday'] == 1].groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()
    hourly_nonwork = filtered_hour[filtered_hour['workingday'] == 0].groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()
    
    with col_q2_a:
        st.markdown("#### Hari Kerja (Working Days)")
        fig_hw, ax_hw = plt.subplots(figsize=(8, 5))
        ax_hw.plot(hourly_work['hr'], hourly_work['registered'], marker='o', color='#1D4ED8', linewidth=2.2, label='Registered')
        ax_hw.plot(hourly_work['hr'], hourly_work['casual'], marker='s', color='#EA580C', linewidth=2.2, linestyle='--', label='Casual')
        ax_hw.set_title("Pola Jam Kerja: Puncak Komuter Bimodal", fontsize=11, fontweight='bold')
        ax_hw.set_xlabel("Jam (0-23)")
        ax_hw.set_ylabel("Rata-Rata Sewa per Jam (unit)")
        ax_hw.set_xticks(range(0, 24, 2))
        ax_hw.grid(True, linestyle=':', alpha=0.6)
        ax_hw.axvspan(7, 9, color='#BFDBFE', alpha=0.35, label='Jam Berangkat (07-09)')
        ax_hw.axvspan(16, 19, color='#FED7AA', alpha=0.35, label='Jam Pulang (16-19)')
        ax_hw.legend(loc='upper right', frameon=True)
        st.pyplot(fig_hw)
        
    with col_q2_b:
        st.markdown("#### Akhir Pekan & Hari Libur (Non-Working Days)")
        fig_hn, ax_hn = plt.subplots(figsize=(8, 5))
        ax_hn.plot(hourly_nonwork['hr'], hourly_nonwork['registered'], marker='o', color='#1D4ED8', linewidth=2.2, label='Registered')
        ax_hn.plot(hourly_nonwork['hr'], hourly_nonwork['casual'], marker='s', color='#EA580C', linewidth=2.2, linestyle='--', label='Casual')
        ax_hn.set_title("Pola Akhir Pekan: Puncak Rekreasi Siang", fontsize=11, fontweight='bold')
        ax_hn.set_xlabel("Jam (0-23)")
        ax_hn.set_ylabel("Rata-Rata Sewa per Jam (unit)")
        ax_hn.set_xticks(range(0, 24, 2))
        ax_hn.grid(True, linestyle=':', alpha=0.6)
        ax_hn.axvspan(11, 16, color='#BBF7D0', alpha=0.35, label='Puncak Rekreasi (11-16)')
        ax_hn.legend(loc='upper right', frameon=True)
        st.pyplot(fig_hn)

    st.success("""
    📌 **Temuan Kunci Pertanyaan 2:**
    - **Pola Komuter Hari Kerja:** Pengguna terdaftar (*Registered*) mendominasi lalu lintas peminjaman dengan dua lonjakan tajam pada jam 08:00 (berangkat kantor, ~368 unit) dan jam 17:00–18:00 (pulang kantor, ~460–490 unit).
    - **Pola Rekreasi Akhir Pekan:** Pengguna kasual (*Casual*) meningkat tajam di akhir pekan dengan pola kurva tunggal memuncak pada jam 11:00 hingga 16:00 (>100 unit/jam), didorong oleh aktivitas santai dan wisata keluarga.
    """)

# ================= TAB 4: ADVANCED ANALYSIS =================
with tab4:
    st.subheader("🎯 Analisis Lanjutan: Segmentasi Suhu & Klaster Jam Operasional")
    st.markdown("""
    Penerapan teknik analisis lanjutan (*Clustering & Binning*) tanpa *machine learning* untuk segmentasi bisnis:
    1. **Temperature Binning:** Pengelompokan kenyamanan suhu manusia (`Cold < 12°C`, `Mild 12–20°C`, `Warm 20–28°C`, `Hot > 28°C`).
    2. **Operational Time Clustering:** Pengelompokan fungsional mobilitas harian (`Off-Peak`, `Morning Rush`, `Mid-Day`, `Evening Rush`, `Night`).
    """)
    
    col_cl1, col_cl2 = st.columns(2)
    
    with col_cl1:
        st.markdown("#### Segmentasi Rata-Rata Sewa per Klaster Suhu")
        temp_order = ['Cold (<12C)', 'Mild (12-20C)', 'Warm (20-28C)', 'Hot (>28C)']
        temp_agg = filtered_day.groupby('temp_cluster', observed=False)['cnt'].mean().reindex(temp_order).dropna().reset_index()
        
        fig_tc, ax_tc = plt.subplots(figsize=(7, 5))
        pal_tc = ['#60A5FA', '#34D399', '#FBBF24', '#F87171']
        bars_tc = ax_tc.bar(temp_agg['temp_cluster'], temp_agg['cnt'], color=pal_tc, edgecolor='black', width=0.55)
        ax_tc.set_ylabel("Rata-Rata Sewa Harian (unit)", fontsize=10, fontweight='bold')
        ax_tc.set_ylim(0, max(temp_agg['cnt'].max() * 1.2, 1000))
        for bar in bars_tc:
            yval = bar.get_height()
            if not np.isnan(yval):
                ax_tc.text(bar.get_x() + bar.get_width()/2, yval + 100, f"{int(yval):,} unit", ha='center', va='bottom', fontweight='bold', fontsize=9)
        st.pyplot(fig_tc)
        
    with col_cl2:
        st.markdown("#### Proporsi Kontribusi Klaster Jam Mobilitas")
        time_order = ['Off-Peak / Midnight', 'Morning Rush Hour', 'Mid-Day Leisure', 'Evening Rush Hour', 'Night Hours']
        time_agg = filtered_hour.groupby('time_cluster', observed=False)['cnt'].sum().reindex(time_order).dropna().reset_index()
        time_agg['Pct'] = (time_agg['cnt'] / time_agg['cnt'].sum()) * 100
        
        fig_tm, ax_tm = plt.subplots(figsize=(7, 5))
        pal_tm = ['#9CA3AF', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']
        bars_tm = ax_tm.bar(time_agg['time_cluster'], time_agg['Pct'], color=pal_tm, edgecolor='black', width=0.55)
        ax_tm.set_ylabel("Kontribusi (%)", fontsize=10, fontweight='bold')
        ax_tm.set_ylim(0, max(time_agg['Pct'].max() * 1.25, 40))
        plt.setp(ax_tm.get_xticklabels(), rotation=25, ha='right')
        for bar in bars_tm:
            yval = bar.get_height()
            if not np.isnan(yval):
                ax_tm.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=9)
        st.pyplot(fig_tm)

    st.info("💡 **Insight Segmentasi:** Suhu optimal *Warm (20–28°C)* melipatgandakan sewa harian (+121%) dibanding cuaca dingin. Sementara itu, jam sibuk pagi dan sore (*Rush Hours*) menggerakkan lebih dari 55% perputaran unit sepeda harian.")

# ================= TAB 5: KESIMPULAN & REKOMENDASI =================
with tab5:
    st.subheader("💡 Kesimpulan & Rekomendasi Rencana Aksi (Action Items)")
    
    st.markdown("""
    ### 🎯 Ringkasan Kesimpulan Analisis:
    1. **Faktor Lingkungan Sangat Menentukan:** Permintaan sewa memuncak di Musim Gugur (Fall: ~5.644 unit/hari) dan merosot tajam pada cuaca buruk/hujan (turun 63%).
    2. **Segmentasi Pengguna Berbeda Karakteristik:**
       - Pengguna terdaftar (*Registered*) memfungsikan sepeda sebagai transportasi komuter harian jam sibuk (08:00 dan 17:00-18:00).
       - Pengguna kasual (*Casual*) memfungsikan sepeda untuk rekreasi akhir pekan pada siang hari (11:00-16:00).
    3. **Efisiensi Armada Terpusat pada Jam Sibuk:** Dua klaster jam komuter pagi & sore menyerap 55.7% total rental.
    """)
    
    st.markdown("### 🚀 Rekomendasi Action Items yang Dapat Diterapkan Bisnis:")
    
    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        st.markdown("""
        **1. Strategi Rebalancing Armada Dinamis (Smart Fleet Rebalancing)**  
        - *Tindakan:* Distribusikan ulang unit sepeda ke stasiun perumahan sebelum pukul 07:30 pagi, dan relokasi ke stasiun pusat perkantoran sebelum pukul 16:30 sore pada hari kerja.
        - *Dampak:* Mencegah stasiun kosong pada jam sibuk dan meningkatkan ketersediaan unit sepeda komuter.
        
        **2. Kampanye Konversi Pengguna Kasual (Casual-to-Member Conversion)**  
        - *Tindakan:* Tampilkan penawaran khusus diskon membership tahunan pada aplikasi bagi pengguna kasual yang menyewa di akhir pekan (jam 11:00–16:00).
        - *Dampak:* Meningkatkan retensi pelanggan dan recurring subscription revenue.
        """)
        
    with col_rec2:
        st.markdown("""
        **3. Penjadwalan Pemeliharaan Berkala Musiman (Seasonal Maintenance)**  
        - *Tindakan:* Lakukan servis besar (*overhaul*) armada pada bulan Januari–Februari (musim sepi / off-season).
        - *Dampak:* Memastikan kesiapan 100% armada saat memasuki musim puncak di Musim Panas dan Gugur tanpa mengganggu pendapatan.
        
        **4. Insentif Cuaca Dinamis (Weather-Based Dynamic Incentives)**  
        - *Tindakan:* Integrasikan prakiraan cuaca pada aplikasi untuk menawarkan promo diskon tarif saat cuaca mendung sejuk guna memicu penggunaan sebelum hujan.
        - *Dampak:* Memaksimalkan utilitas sepeda di kondisi cuaca marjinal.
        """)

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    Proyek Analisis Data - Belajar Fundamental Analisis Data | Dicoding Indonesia<br>
    Dikembangkan oleh <b>Ilham Taufikurrahman</b> (ID Dicoding: <code>ilhamtaufikurrahman</code>) &copy; 2026
</div>
""", unsafe_allow_html=True)
