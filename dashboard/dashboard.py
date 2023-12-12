import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_monthly_orders(dataset):
  monthly_orders_dataset = dataset.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "price": "sum"})

  monthly_orders_dataset.index = monthly_orders_dataset.index.strftime('%Y-%m')
  monthly_orders_dataset = monthly_orders_dataset.reset_index()
  monthly_orders_dataset.rename(columns={
      "order_id": "order_count",
      "price": "revenue"
  }, inplace=True)

  return monthly_orders_dataset

def create_product_revenue(dataset) :
  product_revenue = all_dataset.groupby("product_category_name_english").price.sum().sort_values(ascending=False).reset_index()

  return product_revenue

def create_rfm_customer_city(dataset):
  rfm_dataset = all_dataset.groupby(by="customer_city", as_index=False).agg({
    "order_purchase_timestamp": "max", 
    "order_id": "nunique",
    "price": "sum" 
  })
  rfm_dataset.columns = ["customer_city", "max_order_timestamp", "frequency", "monetary"]
  
  rfm_dataset.drop("max_order_timestamp", axis=1, inplace=True)

  return rfm_dataset

all_dataset = pd.read_csv("all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_estimated_delivery_date"]
all_dataset.sort_values(by="order_purchase_timestamp", inplace=True)
all_dataset.reset_index(inplace=True)
 
for column in datetime_columns:
    all_dataset[column] = pd.to_datetime(all_dataset[column])


min_date = all_dataset["order_purchase_timestamp"].min()
max_date = all_dataset["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_dataset = all_dataset[(all_dataset["order_purchase_timestamp"] >= str(start_date)) & 
                (all_dataset["order_purchase_timestamp"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
monthly_orders_dataset = create_monthly_orders(main_dataset)
product_revenue= create_product_revenue(main_dataset)
rfm_dataset = create_rfm_customer_city(main_dataset)

# plot number of orders 
st.header('E-Commerce Dashboard :sparkles:')
st.subheader('Number of Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = monthly_orders_dataset.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = monthly_orders_dataset.revenue.sum()
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_dataset["order_purchase_timestamp"],
    monthly_orders_dataset["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)

st.pyplot(fig)

#plot product revenue
st.subheader("Produk dengan Pendapatan Tertinggi (2016-2018)")

plt.figure(figsize=(10, 5))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3"]

sns.barplot(x="price", y="product_category_name_english", data=product_revenue.head(10), palette=colors)

plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)

st.pyplot(fig)

#plot RFM customer_city
st.subheader('Best Customer Based on RFM Parameters (customer_city)')

col1, col2 = st.columns(2)

with col1:
    avg_frequency = round(rfm_dataset.frequency.mean(), 0)
    st.metric("Average Frequency", value=avg_frequency)
 
with col2:
    avg_monetory = rfm_dataset.monetary.mean()
    st.metric("Average Monetory", value=avg_monetory)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
 
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
 
sns.barplot(y="frequency", x="customer_city", data=rfm_dataset.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Frequency", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)
 
sns.barplot(y="monetary", x="customer_city", data=rfm_dataset.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Monetary", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
 

st.pyplot(fig)

st.caption('Copyright © Adelia Setiyaningrum 2023')