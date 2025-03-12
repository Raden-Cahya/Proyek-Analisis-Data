import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

orders_df = pd.read_csv("data", "orders_dataset.csv")
payments_df = pd.read_csv("data", "order_payments_dataset.csv")
items_df = pd.read_csv("data", "order_items_dataset.csv")

st.sidebar.title("E-Commerce Dashboard")
option = st.sidebar.selectbox("Pilih Analisis:", ["Metode Pembayaran", "Pola Penjualan Bulanan"])

if option == "Metode Pembayaran":
    st.title("Distribusi Metode Pembayaran")
    
    payment_counts = payments_df['payment_type'].value_counts(normalize=True) * 100
    
    fig, ax = plt.subplots()
    sns.barplot(x=payment_counts.index, y=payment_counts.values, palette='viridis', ax=ax)
    ax.set_xlabel("Metode Pembayaran")
    ax.set_ylabel("Persentase (%)")
    ax.set_title("Distribusi Metode Pembayaran")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif option == "Pola Penjualan Bulanan":
    st.title("Pola Penjualan Bulanan")
    
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['month_year'] = orders_df['order_purchase_timestamp'].dt.to_period("M")
    monthly_orders = orders_df.groupby('month_year')['order_id'].count().reset_index()
    monthly_orders['month_year'] = monthly_orders['month_year'].astype(str)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month_year', y='order_id', data=monthly_orders, marker='o', color='b', linestyle='-', ax=ax)
    ax.set_xlabel("Bulan-Tahun")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Pola Penjualan Bulanan")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    st.pyplot(fig)
