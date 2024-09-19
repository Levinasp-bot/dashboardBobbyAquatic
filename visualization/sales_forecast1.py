import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk menampilkan dashboard prediksi
def show_dashboard(daily_profit, hw_forecast_future, forecast_horizon=365):
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
            last_date = daily_profit.index[-1]
            forecast_dates = pd.date_range(start=last_date, periods=forecast_horizon + 1)[1:]
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
