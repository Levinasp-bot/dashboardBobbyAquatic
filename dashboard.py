from sales_forecast1 import load_all_excel_files, forecast_profit, show_dashboard

# Load data dari semua file Excel di folder
folder_path = "./data/Bobby Aquatic 1"
sheet_name = 'Penjualan'
penjualan_data = load_all_excel_files(folder_path, sheet_name)

# Lakukan analisis prediksi laba
daily_profit, hw_forecast_future, hw_model = forecast_profit(penjualan_data)

# Tampilkan dashboard
show_dashboard(daily_profit, hw_forecast_future)
