import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from accessmlmodel import main
from productsearch import reslst

# Simulating API response for product prices
def fetch_prices():
    # Simulated prices from Amazon and Flipkart ** ₹30,999
    data = [
        {"name": "Samsung Galaxy A35 5G", "amazon_price":int(reslst[1][1:3]+reslst[1][4:]) , "flipkart_price": int(reslst[3][4:6]+reslst[3][7:])},
        {"name": "Apple iPhone 15 Pro", "amazon_price": random.randint(120000, 125000), "flipkart_price": random.randint(118000, 123000)},
        {"name": "Samsung Galaxy M15 5G Prime", "amazon_price": random.randint(15000, 17000), "flipkart_price": random.randint(14500, 16500)}
    ]
    return data


# Fetch product data
product_data = fetch_prices()

# Create a DataFrame
df = pd.DataFrame(product_data)
df['lowest_price'] = df[['amazon_price', 'flipkart_price']].min(axis=1)
df['app_price'] = main()

# Streamlit app
st.title("Product Price Comparison App")
st.write("This app displays product details and compares prices from Amazon, Flipkart, and our platform.")

# Display product details
for index, row in df.iterrows():
    st.subheader(row['name'])
    st.write(f"Amazon Price: ₹{row['amazon_price']}")
    st.write(f"Flipkart Price: ₹{row['flipkart_price']}")
    st.write(f"Our Price : ₹{row['app_price']}")
    st.markdown("---")

# Plot prices
st.subheader("Price Comparison Chart")
fig, ax = plt.subplots()
x = df['name']
ax.bar(x, df['amazon_price'], label='Amazon', alpha=0.7)
ax.bar(x, df['flipkart_price'], label='Flipkart', alpha=0.7, bottom=df['amazon_price'])
ax.bar(x, df['app_price'], label='Our Price', alpha=0.9, color='green')
ax.set_ylabel("Prices (₹)")
ax.legend()

# Display the plot
st.pyplot(fig)

# Footer
st.write("Prices fetched are simulated for demonstration purposes.")
