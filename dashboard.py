import os
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk menggabungkan semua file .xlsm dari folder yang dipilih
def load_all_excel_files(folder_path, sheet_name):
    dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith('.xlsm'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# Load data dari semua file Excel di folder
folder_path = "./DATA/Bobby Aquatic 1"
sheet_name = 'Penjualan'
penjualan_data = load_all_excel_files(folder_path, sheet_name)

# Mengambil hanya kolom tanggal dan laba dari data penjualan
daily_profit = penjualan_data[['TANGGAL', 'LABA']].copy()
daily_profit['TANGGAL'] = pd.to_datetime(daily_profit['TANGGAL'])

# Agregasi laba per hari (sum laba per tanggal)
daily_profit = daily_profit.groupby('TANGGAL').sum()

# Menghapus duplikasi indeks
daily_profit = daily_profit[~daily_profit.index.duplicated(keep='first')]

# Menetapkan frekuensi pada indeks waktu jika belum ada
daily_profit = daily_profit.asfreq('D', fill_value=0)  # Asumsi data harian dan isi yang kosong dengan 0

# Membagi data menjadi training dan testing (90% training, 10% testing)
train_size = int(len(daily_profit) * 0.9)
train, test = daily_profit[:train_size], daily_profit[train_size:]

best_mae = float('inf')
best_forecast = None

# Tentukan periode musiman yang sesuai (misalnya, 7 hari untuk mingguan atau 365 hari untuk tahunan)
seasonal_periods = 365  # Misalnya, 365 hari untuk musiman tahunan

try:
    # Menentukan model Holt-Winters pada data training
    hw_model = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=seasonal_periods).fit()
    
    # Prediksi untuk data testing
    hw_forecast_test = hw_model.forecast(len(test))
    
    # Perhitungan MAE untuk data test
    mae_test = mean_absolute_error(test, hw_forecast_test)
    
    best_mae = mae_test
    best_forecast = hw_forecast_test
except Exception as e:
    print(f"An error occurred: {e}")

# Prediksi 365 hari ke depan dengan model terbaik
forecast_horizon = 365
hw_forecast_future = hw_model.forecast(forecast_horizon)

# Membuat tanggal untuk prediksi masa depan
last_date = daily_profit.index[-1]
forecast_dates = pd.date_range(start=last_date, periods=forecast_horizon + 1)[1:]

# Streamlit - Visualisasi Dashboard
st.title("Dashboard Prediksi Laba Bobby Aquatic")

# Filter data berdasarkan tahun
st.subheader("Filter berdasarkan Tahun")
selected_years = st.multiselect("Pilih Tahun", daily_profit.index.year.unique())

if selected_years:
    # Plot Data Historis dan Prediksi Masa Depan
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot data historis berdasarkan tahun yang dipilih
    for year in selected_years:
        filtered_data = daily_profit[daily_profit.index.year == year]
        filtered_data['LABA'].plot(ax=ax, label=f'Data Historis {year}', color='blue')

    # Plot prediksi masa depan hanya jika tahun terbaru dipilih
    if max(selected_years) == daily_profit.index.year.max():
        pd.Series(hw_forecast_future, index=forecast_dates).plot(ax=ax, label='Prediksi Masa Depan', linestyle='--', color='purple')
        chart_title = f'Data Historis dan Prediksi Laba - Tahun {", ".join(map(str, selected_years))}'
    else:
        chart_title = f'Data Historis Laba - Tahun {", ".join(map(str, selected_years))}'

    ax.set_title(chart_title)
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Laba')
    ax.legend()
    st.pyplot(fig)
else:
    st.write("Silakan pilih minimal satu tahun untuk melihat data historis.")
