import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# إعداد الصفحة
st.set_page_config(
    page_title="Real Estate Dashboard | لوحة مؤشرات العقار",
    layout="centered"
)

# اختيار اللغة
language = st.sidebar.radio("Language | اللغة", ["English", "العربية"])

# تحميل البيانات
url = 'https://drive.google.com/uc?id=1e8yBrvhfAP5ArPhgnTszizT21gQeGVg7'
df = pd.read_csv(url)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna()

items = sorted(df['Item'].unique())
selected_item = st.sidebar.selectbox("Select Real Estate Type | اختر نوع العقار", items)

filtered_df = df[df['Item'] == selected_item]
max_row = filtered_df.loc[filtered_df['Real estate price index'].idxmax()]
min_row = filtered_df.loc[filtered_df['Real estate price index'].idxmin()]

# نموذج التنبؤ
X = filtered_df[['Year']]
y = filtered_df['Real estate price index']
model = LinearRegression()
model.fit(X, y)
next_year = X['Year'].max() + 1
predicted_value = model.predict([[next_year]])[0]

# الألوان والخطوط (تحسين شكل)
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12})

# المحتوى حسب اللغة
if language == "English":
    st.title("📊 Real Estate Price Index Dashboard")
    st.subheader(f"📈 Price Index Over Time: {selected_item}")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=filtered_df, x='Year', y='Real estate price index', marker='o', ax=ax, color="#1f77b4")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price Index")
    ax.set_title(f"{selected_item} Price Trend")
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("### 🤖 AI Prediction")
    st.success(f"Predicted price index for {next_year}: **{predicted_value:.2f}**")

    st.markdown("### 📌 Key Statistics")
    st.markdown("#### 🔺 Highest Price Index")
    st.write(max_row)
    st.markdown("#### 🔻 Lowest Price Index")
    st.write(min_row)

else:
    st.title("📊 لوحة مؤشرات أسعار العقارات")
    st.subheader(f"📈 تغير مؤشر السعر بمرور الوقت: {selected_item}")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=filtered_df, x='Year', y='Real estate price index', marker='o', ax=ax, color="#1f77b4")
    ax.set_xlabel("السنة")
    ax.set_ylabel("مؤشر السعر")
    ax.set_title(f"توجهات أسعار {selected_item}")
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("### 🤖 التنبؤ بالذكاء الاصطناعي")
    st.success(f"القيمة المتوقعة لمؤشر السعر في سنة {next_year}: **{predicted_value:.2f}**")

    st.markdown("### 📌 الإحصائيات الرئيسية")
    st.markdown("#### 🔺 أعلى مؤشر سعر")
    st.write(max_row)
    st.markdown("#### 🔻 أقل مؤشر سعر")
    st.write(min_row)