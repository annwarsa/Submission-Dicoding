import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

all_df = pd.read_csv("all_data.csv")

def review(df):
    review_scores = all_df.groupby('product_category_name_english')['review_score'].mean().reset_index()
    sorted_review_scores = review_scores.sort_values(by='review_score', ascending=False)
    return sorted_review_scores

def product_sales(df):
    product_sales = all_df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_product_sales = product_sales.sort_values(by='product_id', ascending=False)
    return sorted_product_sales

def payment(df):
    payment_frequency = all_df['payment_type'].value_counts()
    return payment_frequency

def yearly_income(df):
    yearly_income_df = all_df.resample(rule='Y', on='order_approved_at').agg({
        "price": "sum"
    })
    yearly_income_df = yearly_income_df.reset_index()
    yearly_income_df.rename(columns={
        "price": "total_income"
    }, inplace=True)
    yearly_income_df['order_approved_at'] = yearly_income_df['order_approved_at'].dt.year

    return yearly_income_df

def purchase(df):
    city_purchase_counts = all_df['customer_city'].value_counts().head(5)
    state_purchase_counts = all_df['customer_state'].value_counts().head(5)

    return city_purchase_counts, state_purchase_counts

def rfm(df):
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
    recent_date = all_df["order_purchase_timestamp"].max()
    recency = (recent_date - all_df.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days
    frequency = all_df.groupby('customer_id')['order_id'].count()
    monetary = all_df.groupby('customer_id')['price'].sum()

    rfm_df = pd.DataFrame({
        'customer_id': recency.index,
        'recency': recency.values,
        'frequency': frequency.values,
        'monetary': monetary.values
    })
    
    return rfm_df

datetime_cols = [
    "order_approved_at", 
    "order_delivered_carrier_date", 
    "order_delivered_customer_date", 
    "order_estimated_delivery_date", 
    "order_purchase_timestamp", 
    "shipping_limit_date"
]

all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])


min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()


## Sidebar
with st.sidebar:
    #Menambahkan logo
    st.image("dicoding_logo.jpeg")

    #Mengambil start and end date dari input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & (all_df["order_approved_at"] <= str(end_date))] 

## Memanggil function
sorted_review_scores = review(main_df)
sorted_product_sales = product_sales(main_df)
payment_frequency = payment(main_df)
yearly_income_df = yearly_income(main_df)
city_purchase_counts, state_purchase_counts = purchase(main_df) 

rfm_df = rfm(main_df)

#Header
st.header("Data Analisis E-commerce :sparkles:")

#Product Review#
st.subheader("Produk dengan Review Tertinggi dan Terendah")

col1, col2 = st.columns(2)

with col1:
   highest_total = sorted_review_scores[sorted_review_scores['product_category_name_english'] == 'cds_dvds_musicals']['review_score'].values[0]
   st.metric("Total cds_dvds_musicals review", highest_total)

with col2:
    lowest_total = sorted_review_scores[sorted_review_scores['product_category_name_english'] == 'security_and_services']['review_score'].values[0]
    st.metric("Total cds_dvds_musicals review", lowest_total)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="review_score", y="product_category_name_english", data=sorted_review_scores.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk dengan Review Tertinggi", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(x="review_score", y="product_category_name_english", data=sorted_review_scores.sort_values(by="review_score", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk dengan Review Terendah", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)


# Penjualan Product #
st.subheader("Product dengan Penjualan Tertinggi dan Terendah")

col1, col2 = st.columns(2)

with col1:
    highest_revenue = sorted_product_sales[sorted_product_sales['product_category_name_english'] == 'bed_bath_table']['product_id'].values[0]
    st.metric("Total penjualan bed_bath_table", highest_revenue)

with col2:
    lowest_revenue = sorted_product_sales[sorted_product_sales['product_category_name_english'] == 'security_and_services']['product_id'].values[0]
    st.metric("Total penjualan security_and_service", lowest_revenue)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", data=sorted_product_sales.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk dengan Penjualan Terbanyak", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(x="product_id", y="product_category_name_english", data=sorted_product_sales.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk dengan Penjualan Terendah", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# Pembayaran #
st.subheader("Pembayaran yang sering digunakan")

plt.figure(figsize=(10, 8))
plt.pie(payment_frequency, labels=None, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
plt.title('Pembayaran yang sering digunakan')
plt.axis('equal')  
plt.legend(payment_frequency.index, title="Payment Method", loc="upper right")

st.pyplot(plt)


#Pendapatan Pertahun#
st.subheader("Pendapatan E-commerce Pertahun")

col1, col2, col3 = st.columns(3)

with col1:
    revenue_2016 = yearly_income_df[yearly_income_df['order_approved_at'] == 2016]['total_income'].values[0]
    st.metric("Pendapatan tahun 2016", revenue_2016)

with col2:
    revenue_2017 = yearly_income_df[yearly_income_df['order_approved_at'] == 2017]['total_income'].values[0]
    st.metric("Pendapatan tahun 2017", revenue_2017)

with col3:
    revenue_2018 = yearly_income_df[yearly_income_df['order_approved_at'] == 2018]['total_income'].values[0]
    st.metric("Pendapatan tahun 2018", revenue_2018)

plt.figure(figsize=(10, 6))
plt.bar(
    yearly_income_df["order_approved_at"],
    yearly_income_df["total_income"],
    color="#72BCD4"
)
plt.title("Pendapatan E-commerce per Tahun")
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)

st.pyplot(plt)

#Wilayah Pembeli#
st.subheader("Wilayah dengan Pembeli Terbanyak")

col1, col2 = st.columns(2)

with col1:
    total_pembeli = city_purchase_counts['sao paulo']
    st.metric("Total pembeli di city sao paulo", total_pembeli)
with col2:
    total_pembeli = state_purchase_counts['SP']
    st.metric("Total pembeli di state SP", total_pembeli)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

ax[0].pie(city_purchase_counts, labels=None, autopct='%1.1f%%', startangle=140)
ax[0].set_title('Top 5 City dengan pembelian Terbanyak')
ax[0].axis('equal') 
ax[0].legend(city_purchase_counts.index, title="City", loc="upper right")

ax[1].pie(state_purchase_counts, labels=None, autopct='%1.1f%%', startangle=140)
ax[1].set_title('Top 5 States dengan pembelian Terbanyak')
ax[1].axis('equal') 
ax[1].legend(state_purchase_counts.index, title="State", loc="upper right")

st.pyplot(fig)

# RFM #
st.subheader("Customer Terbaik berdasrkan RFM parameter")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Rata-rata Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Rata-rata Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale="pt_BR") 
    st.metric("Rata-rata Monetary", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id")
ax[0].set_title("By Recency (hari)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)
ax[0].set_xticks([])

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id")
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
ax[1].set_xticks([])

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id")
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
ax[2].set_xticks([])

st.pyplot(fig)


st.caption('Copyright (c) Syaiful Anwar 2024')