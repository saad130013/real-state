
from pytrends.request import TrendReq
import pandas as pd

# إعداد الاتصال
pytrends = TrendReq(hl='en-US', tz=360)

# الكلمات المفتاحية المهمة (تقدر تغيرها)
keywords = ['AI', 'Bitcoin', 'ChatGPT', 'Saudi Arabia', 'Apple']

# بناء الطلب
pytrends.build_payload(keywords, timeframe='now 1-d', geo='')

# جلب بيانات الترند خلال آخر 24 ساعة
df = pytrends.interest_over_time()

# التحقق من وجود بيانات
if not df.empty:
    # حذف عمود isPartial إذا موجود
    if 'isPartial' in df.columns:
        df = df.drop(columns=['isPartial'])

    # حفظ النتائج في ملف CSV
    df.to_csv('daily_global_trends.csv')
    print("✅ تم حفظ الترندات في: daily_global_trends.csv")
else:
    print("❌ لم يتم العثور على بيانات، جرّب كلمات مفتاحية أخرى.")
