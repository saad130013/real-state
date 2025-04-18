import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Real Estate Price Dashboard",
    layout="centered"
)

st.title("📊 Real Estate Price Index Dashboard")

# Load the CSV file from Google Drive
url = 'https://drive.google.com/uc?id=1e8yBrvhfAP5ArPhgnTszizT21gQeGVg7'
df = pd.read_csv(url)

# Clean data
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna()

# Sidebar filters
items = sorted(df['Item'].unique())
selected_item = st.sidebar.selectbox("Select Real Estate Type", items)

# Filter based on selection
filtered_df = df[df['Item'] == selected_item]

# Line plot
st.subheader(f"📈 Price Index Over Time: {selected_item}")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x='Year', y='Real estate price index', marker='o', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Price Index")
ax.set_title(f"{selected_item} Price Trend")
ax.grid(True)
st.pyplot(fig)

# Show stats
st.markdown("### 📌 Key Statistics")
max_row = filtered_df.loc[filtered_df['Real estate price index'].idxmax()]
min_row = filtered_df.loc[filtered_df['Real estate price index'].idxmin()]

st.write("📈 **Highest Price Index**")
st.write(max_row)

st.write("📉 **Lowest Price Index**")
st.write(min_row)