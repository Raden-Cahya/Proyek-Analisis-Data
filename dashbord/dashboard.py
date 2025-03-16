import streamlit as st
import pandas as pd
import plotly.express as px

orders_df = pd.read_csv("data/orders_dataset.csv")
payments_df = pd.read_csv("data/order_payments_dataset.csv")

orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

merged_df = pd.merge(orders_df[['order_id', 'order_purchase_timestamp']], payments_df, on='order_id')

orders_df['month_year'] = orders_df['order_purchase_timestamp'].dt.to_period("M")

st.sidebar.title("📊 E-Commerce Dashboard")
option = st.sidebar.selectbox("🔍 Pilih Analisis:", ["Metode Pembayaran", "Pola Penjualan Bulanan"])

if option == "Metode Pembayaran":
    st.title("💳 Distribusi Metode Pembayaran")

    start_date = st.sidebar.date_input("📅 Pilih Tanggal Mulai", merged_df['order_purchase_timestamp'].min().date())
    end_date = st.sidebar.date_input("📅 Pilih Tanggal Akhir", merged_df['order_purchase_timestamp'].max().date())

    selected_payment = st.sidebar.multiselect(
        "🏦 Pilih Metode Pembayaran:",
        payments_df['payment_type'].unique(),
        default=payments_df['payment_type'].unique()
    )

    filtered_payments_df = merged_df[
        (merged_df['order_purchase_timestamp'].dt.date >= start_date) & 
        (merged_df['order_purchase_timestamp'].dt.date <= end_date) & 
        (merged_df['payment_type'].isin(selected_payment))
    ]

    payment_counts = filtered_payments_df['payment_type'].value_counts(normalize=True) * 100

    fig = px.bar(
        payment_counts,
        x=payment_counts.index,
        y=payment_counts.values,
        title="📊 Distribusi Metode Pembayaran",
        labels={'x': 'Metode Pembayaran', 'y': 'Persentase (%)'},
        text_auto='.2f',
        color=payment_counts.index
    )

    fig.update_layout(
        plot_bgcolor="white",  
        paper_bgcolor="white", 
        legend=dict(
            title=dict(text="Metode Pembayaran", font=dict(color="black")),  
            font=dict(color="black")  
        ),
        xaxis=dict(
            showgrid=True, 
            gridcolor="lightgray",
            tickfont=dict(color="black"),
            title=dict(text="Metode Pembayaran", font=dict(color="black"))
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor="lightgray",
            tickfont=dict(color="black"),
            title=dict(text="Persentase (%)", font=dict(color="black"))
        ),
        title_font=dict(color="black"),
        font=dict(color="black"),
    )

    st.plotly_chart(fig)

elif option == "Pola Penjualan Bulanan":
    st.title("📈 Pola Penjualan Bulanan")

    start_date = st.sidebar.date_input("📅 Pilih Tanggal Mulai", orders_df['order_purchase_timestamp'].min().date())
    end_date = st.sidebar.date_input("📅 Pilih Tanggal Akhir", orders_df['order_purchase_timestamp'].max().date())

    filtered_orders = orders_df[
        (orders_df['order_purchase_timestamp'].dt.date >= start_date) & 
        (orders_df['order_purchase_timestamp'].dt.date <= end_date)
    ]

    monthly_orders = filtered_orders.groupby('month_year')['order_id'].count().reset_index()
    monthly_orders['month_year'] = monthly_orders['month_year'].astype(str)

    fig = px.line(
        monthly_orders,
        x='month_year',
        y='order_id',
        title="📊 Tren Penjualan Bulanan",
        markers=True
    )

    fig.update_layout(
        plot_bgcolor="white",  
        paper_bgcolor="white",  
        xaxis=dict(
            showgrid=True, 
            gridcolor="lightgray",
            tickfont=dict(color="black"),
            title=dict(text="Bulan-Tahun", font=dict(color="black"))
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor="lightgray",
            tickfont=dict(color="black"),
            title=dict(text="Jumlah Pesanan", font=dict(color="black"))
        ),
        title_font=dict(color="black"),
        font=dict(color="black"),
    )

    st.plotly_chart(fig)
