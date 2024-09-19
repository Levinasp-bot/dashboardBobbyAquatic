import os
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error

# Fungsi untuk menggabungkan semua file .xlsm dari folder yang dipilih
def load_all_excel_files(folder_path, sheet_name):
    dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith('.xlsm'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# Fungsi untuk melakukan analisis prediksi
def forecast_profit(data, seasonal_periods=365, forecast_horizon=365):
    # Mengambil hanya kolom tanggal dan laba dari data penjualan
    daily_profit = data[['TANGGAL', 'LABA']].copy()
    daily_profit['TANGGAL'] = pd.to_datetime(daily_profit['TANGGAL'])

    # Agregasi laba per hari
    daily_profit = daily_profit.groupby('TANGGAL').sum()

    # Menghapus duplikasi indeks
    daily_profit = daily_profit[~daily_profit.index.duplicated(keep='first')]

    # Menetapkan frekuensi pada indeks waktu
    daily_profit = daily_profit.asfreq('D', fill_value=0)

    # Membagi data menjadi training dan testing
    train_size = int(len(daily_profit) * 0.9)
    train, test = daily_profit[:train_size], daily_profit[train_size:]

    best_mae = float('inf')
    best_forecast = None

    try:
        # Menentukan model Holt-Winters pada data training
        hw_model = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=seasonal_periods).fit()
        
        # Prediksi untuk data testing
        hw_forecast_test = hw_model.forecast(len(test))
        
        # Perhitungan MAE
        mae_test = mean_absolute_error(test, hw_forecast_test)
        
        best_mae = mae_test
        best_forecast = hw_forecast_test
    except Exception as e:
        print(f"An error occurred: {e}")

    # Prediksi 365 hari ke depan dengan model terbaik
    hw_forecast_future = hw_model.forecast(forecast_horizon)
    
    return daily_profit, hw_forecast_future, hw_model
