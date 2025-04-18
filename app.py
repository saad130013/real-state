import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# إعداد الصفحة
st.set_page_config(
    page_title="Real Estate Insights | تحليلات العقار",
    layout="wide"
)

# تحميل البيانات
url = 'https://drive.google.com/uc?id=1e8yBrvhfAP5ArPhgnTszizT21gQeGVg7'
df = pd.read_csv(url)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna()

st.title("📊 Real Estate Full Insights Dashboard | لوحة تحليلات كاملة للعقار")

# 1. الاتجاه الزمني لكل نوع عقار
st.subheader("📈 الاتجاه الزمني لكل نوع عقار")
fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=df, x="Year", y="Real estate price index", hue="Item", ax=ax1)
ax1.set_title("تغير مؤشر الأسعار حسب نوع العقار بمرور الوقت")
ax1.set_ylabel("مؤشر السعر (ريال)")
st.pyplot(fig1)

# 2. أعلى وأقل مؤشر سعر لكل نوع
st.subheader("📊 أعلى وأقل مؤشر سعر لكل نوع")
idx_max = df.groupby("Item")["Real estate price index"].idxmax()
idx_min = df.groupby("Item")["Real estate price index"].idxmin()
df_max = df.loc[idx_max].set_index("Item")
df_min = df.loc[idx_min].set_index("Item")
st.write("🔺 أعلى مؤشر:", df_max["Real estate price index"].sort_values(ascending=False).astype(str) + " ريال")
st.write("🔻 أقل مؤشر:", df_min["Real estate price index"].sort_values().astype(str) + " ريال")

# 3. المتوسط العام لمؤشر كل نوع
st.subheader("🧮 المتوسط العام لمؤشر كل نوع")
avg_df = df.groupby("Item")["Real estate price index"].mean().sort_values(ascending=False)
st.dataframe(avg_df.round(2).astype(str) + " ريال")

# 4. النوع الأكثر استقرارًا أو تقلبًا
st.subheader("🥇 النوع الأكثر استقرارًا أو تقلبًا")
std_df = df.groupby("Item")["Real estate price index"].std().sort_values()
st.write("أكثر الأنواع استقرارًا:")
st.dataframe(std_df.head(5).round(2).astype(str) + " ريال")
st.write("أكثر الأنواع تقلبًا:")
st.dataframe(std_df.tail(5).round(2).astype(str) + " ريال")

# 5. مقارنة الأنواع في سنة معينة
st.subheader("📅 مقارنة الأنواع في سنة معينة")
year_selected = st.slider("اختر سنة", int(df["Year"].min()), int(df["Year"].max()), 2020)
year_df = df[df["Year"] == year_selected].sort_values("Real estate price index", ascending=False)
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.barplot(data=year_df, y="Item", x="Real estate price index", ax=ax2)
ax2.set_title(f"مقارنة أنواع العقارات في سنة {year_selected}")
ax2.set_xlabel("مؤشر السعر (ريال)")
st.pyplot(fig2)

# 6. التنبؤ بالسعر في 2026 و 2027
st.subheader("🔮 التنبؤ بمؤشر السعر للسنوات القادمة")
selected_item = st.selectbox("اختر نوع العقار للتنبؤ:", sorted(df["Item"].unique()))
item_df = df[df["Item"] == selected_item]
X = item_df[["Year"]]
y = item_df["Real estate price index"]
model = LinearRegression()
model.fit(X, y)

future_years = [2026, 2027]
future_X = pd.DataFrame({"Year": future_years})
predictions = model.predict(future_X)

pred_df = pd.DataFrame({
    "السنة": future_years,
    "المؤشر المتوقع": [f"{val:.2f} ريال" for val in predictions]
})
st.write(f"🔮 المؤشرات المتوقعة لنوع {selected_item}:")
st.dataframe(pred_df)