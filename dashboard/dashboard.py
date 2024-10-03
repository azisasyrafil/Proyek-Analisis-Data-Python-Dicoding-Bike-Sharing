import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Masukan dan Mendefinisikan DataFrame
all_bike_df = pd.read_csv("dashboard/all_data.csv")

label_musim = {
    1: 'Cerah',
    2: 'Berkabut',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
all_bike_df['label_musim'] = all_bike_df['weathersit_day'].map(label_musim)

datetime_columns = ["dteday"]

for column in datetime_columns:
    all_bike_df[column] = pd.to_datetime(all_bike_df[column])

min_date = all_bike_df["dteday"].min()
max_date = all_bike_df["dteday"].max()

with st.sidebar:
    # Logo perusahaan
    
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_bike_df[(all_bike_df["dteday"] >= str(start_date)) & 
                (all_bike_df["dteday"] <= str(end_date))]

st.header('Eksplorasi Data Analis Menggunakan Bike Data Set :bicyclist::fire:')

st.subheader('Jumlah Pengguna Harian Teregistrasi dan Pengguna Kasual')
col1, col2 = st.columns(2)
with col1 :
    total_registered = main_df.registered_hour.sum()
    st.metric("Total Pengguna Teregistrasi", value=total_registered)
with col2 :
    total_casual = main_df.casual_hour.sum()
    st.metric("Total Pengguna Kasual", value=total_casual )


# Grafik 1
avg_weather = all_bike_df.groupby('label_musim')['cnt_day'].mean().reset_index().sort_values("cnt_day")
total_rentals = avg_weather['cnt_day'].sum()
labels = avg_weather['label_musim']
sizes = avg_weather['cnt_day']

colors = ['lightblue', 'grey', 'yellow']  

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct=lambda pct: '{:.1f}%'.format(pct), startangle=90, colors=colors)  # Menambahkan parameter colors
plt.title('Rata-Rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=12, fontweight='bold')
plt.ylabel('')
plt.text(0, 1.2, f"Total Jumlah Rental Sepeda: {round(total_rentals, 1)}", ha='center')
print(f"Total number of bike rentals: {total_rentals}")

st.pyplot(plt)

# Grafik 2
avg_holiday = all_bike_df.groupby('holiday_day')['cnt_day'].mean().reset_index().sort_values("holiday_day")

plt.figure(figsize=(8, 5))


sns.barplot(x='holiday_day', y='cnt_day', data=avg_holiday, palette=['green', 'red'])


plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Jenis Hari', fontsize=12, fontweight='bold')
plt.xlabel('Jenis Hari', fontsize=12, fontweight='bold')
plt.ylabel('Rata-rata Penyewaan', fontsize=12, fontweight='bold')

# Memastikan urutan label x-axis benar
plt.xticks([0, 1], ['Hari Biasa', 'Hari Libur'])  

# Menambahkan nilai di atas setiap bar dengan data yang benar
for i, row in avg_holiday.iterrows():
    plt.text(i, row['cnt_day'] + 0.5, round(row['cnt_day'], 2), 
             ha='center', va='bottom', fontsize=10, fontweight='bold')

st.pyplot(plt)

# Grafik 3
import numpy as np

# Menghitung rata-rata penyewaan per jam
rental_jam = all_bike_df.groupby('hr')['cnt_hour'].mean()
plt.figure(figsize=(10, 10))

# Menentukan nilai maksimum dan minimum
max_value = rental_jam.max()
min_value = rental_jam.min()

# Mengatur warna berdasarkan nilai
colors = np.where(rental_jam == max_value, 'green', np.where(rental_jam == min_value, 'red', 'lightblue'))

# Membuat bar chart
plt.bar(rental_jam.index, rental_jam.values, color=colors)

# Menambahkan nilai tertinggi dan terendah di atas bar
for i, value in enumerate(rental_jam):
    if value == max_value:
        plt.text(i, value + 0.5, f'{value:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='green')
    elif value == min_value:
        plt.text(i, value + 0.5, f'{value:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='red')
    else:
        plt.text(i, value + 0.5, f'{value:.2f}', ha='center', va='bottom', fontsize=9)

# Menambahkan judul dan label
plt.title('Rata - Rata Penyewaan per Jam dalam Hari', fontsize=12, fontweight='bold')
plt.xlabel('Jam', fontsize=12, fontweight='bold')
plt.ylabel('Rata - Rata Penyewaan', fontsize=12, fontweight='bold')

st.pyplot(plt)


st.caption('Copyright (c) Asyrafil N Azis 2024')