import streamlit as st
import pandas as pd
import plotly.express as px

orders_df = pd.read_csv("data/orders_dataset.csv")
payments_df = pd.read_csv("data/order_payments_dataset.csv")

orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

st.sidebar.title("E-Commerce Dashboard")
option = st.sidebar.selectbox("Pilih Analisis:", ["Metode Pembayaran", "Pola Penjualan Bulanan"])

start_date = st.sidebar.date_input("Tanggal Mulai", orders_df['order_purchase_timestamp'].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", orders_df['order_purchase_timestamp'].max().date())

filtered_orders_df = orders_df[
    (orders_df['order_purchase_timestamp'].dt.date >= start_date) &
    (orders_df['order_purchase_timestamp'].dt.date <= end_date)
]

if option == "Metode Pembayaran":
    st.title("Distribusi Metode Pembayaran")
    
    selected_payment = st.sidebar.multiselect(
        "Pilih Metode Pembayaran:",
        payments_df['payment_type'].unique(),
        default=payments_df['payment_type'].unique()
    )

    filtered_payments_df = payments_df[payments_df['payment_type'].isin(selected_payment)]
    
    payment_counts = filtered_payments_df['payment_type'].value_counts(normalize=True) * 100

    fig = px.bar(
        payment_counts,
        x=payment_counts.index,
        y=payment_counts.values,
        title="Distribusi Metode Pembayaran",
        labels={'x': 'Metode Pembayaran', 'y': 'Persentase (%)'},
        text_auto='.2f',
        color=payment_counts.index
    )
    st.plotly_chart(fig)

elif option == "Pola Penjualan Bulanan":
    st.title("Pola Penjualan Bulanan")

    filtered_orders_df['month_year'] = filtered_orders_df['order_purchase_timestamp'].dt.to_period("M")
    selected_year = st.sidebar.slider(
        "Pilih Tahun:",
        min_value=int(filtered_orders_df['order_purchase_timestamp'].dt.year.min()),
        max_value=int(filtered_orders_df['order_purchase_timestamp'].dt.year.max()),
        value=int(filtered_orders_df['order_purchase_timestamp'].dt.year.max())
    )

    monthly_orders = filtered_orders_df.groupby('month_year')['order_id'].count().reset_index()
    monthly_orders['month_year'] = monthly_orders['month_year'].astype(str)
    monthly_orders_filtered = monthly_orders[monthly_orders['month_year'].str.startswith(str(selected_year))]

    fig = px.line(
        monthly_orders_filtered,
        x='month_year',
        y='order_id',
        title=f"Pola Penjualan Bulanan - {selected_year}",
        markers=True
    )
    fig.update_traces(line=dict(color='blue', width=2), marker=dict(size=8))
    fig.update_layout(xaxis_tickangle=-45, xaxis_title="Bulan-Tahun", yaxis_title="Jumlah Pesanan")

    st.plotly_chart(fig)
