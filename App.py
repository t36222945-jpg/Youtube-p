import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# --- الإعدادات الأساسية ---
st.set_page_config(page_title="رادار اليوتيوب الذكي", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FFD700; color: black; font-weight: bold; }
    .card { padding: 20px; border-radius: 15px; border: 1px solid #FFD700; background-color: #1e1e1e; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 رادار اكتشاف الفرص التلقائي")
st.write("يبحث في أكثر الأقسام ربحاً (التقنية، التعليم، الأسلوب) ليجد فيديوهات تفوقت على حجم قنواتها.")

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🔑 إعدادات الوصول")
    yt_key = st.text_input("YouTube API Key:", type="password")
    days_filter = st.slider("البحث في آخر (أيام):", 1, 30, 7)
    st.divider()
    st.info("هذا التطبيق يبحث تلقائياً دون الحاجة لكلمات مفتاحية.")

# --- الدوال البرمجية ---
def get_trending_insights(api_key, days):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        # الأقسام: 25 (تقنية)، 27 (تعليم)، 26 (أسلوب حياة)
        categories = ['25', '27', '26']
        all_vids = []

        for cat in categories:
            request = youtube.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode="US", # يمكنك تغييرها لـ EG أو SA
                categoryId=cat,
                maxResults=10
            )
            response = request.execute()

            for item in response.get('items', []):
                # جلب بيانات القناة للمقارنة
                ch_id = item['snippet']['channelId']
                ch_request = youtube.channels().list(part="statistics", id=ch_id)
                ch_response = ch_request.execute()
                
                subs = int(ch_response['items'][0]['statistics'].get('subscriberCount', 1))
                views = int(item['statistics'].get('viewCount', 0))
                
                # حساب النسبة (قوة الانتشار)
                ratio = views / subs if subs > 0 else 0
                
                all_vids.append({
                    'العنوان': item['snippet']['title'],
                    'القناة': item['snippet']['channelTitle'],
                    'المشاهدات': views,
                    'المشتركين': subs,
                    'قوة الانتشار': round(ratio, 2),
                    'الرابط': f"https://youtube.com/watch?v={item['id']}"
                })
        return pd.DataFrame(all_vids)
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        return pd.DataFrame()

# --- واجهة التشغيل ---
if st.button("🚀 ابدأ الرادار التلقائي"):
    if not yt_key:
        st.error("يرجى إدخال YouTube API Key أولاً!")
    else:
        with st.spinner("⏳ جاري مسح الخوارزمية واكتشاف الكنوز..."):
            df = get_trending_insights(yt_key, days_filter)
            
            if not df.empty:
                # ترتيب حسب قوة الانتشار (الفرصة)
                df = df.sort_values(by='قوة الانتشار', ascending=False)
                
                st.success(f"✅ تم اكتشاف {len(df)} فرصة محتملة!")
                
                # عرض أفضل 3 فرص بوضوح
                top_3 = df.head(3)
                cols = st.columns(3)
                for i, (index, row) in enumerate(top_3.iterrows()):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="card">
                            <h4>🔥 فرصة #{i+1}</h4>
                            <p>{row['العنوان'][:50]}...</p>
                            <h2 style="color:#FFD700;">{row['قوة الانتشار']}x</h2>
                            <p>المشاهدات أعلى من المشتركين</p>
                        </div>
                        """, unsafe_allow_html=True)

                # الجدول الكامل
                st.subheader("📊 تقرير البيانات الكامل")
                st.dataframe(df, use_container_width=True)
                
                # رسم بياني
                fig = px.scatter(df, x="المشتركين", y="المشاهدات", size="قوة الانتشار", 
                                 hover_name="العنوان", title="تحليل (المشاهدات مقابل حجم القناة)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("لم نتمكن من جلب البيانات، تأكد من صحة الـ API Key.")
