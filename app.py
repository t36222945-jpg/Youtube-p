"""
🎯 رادار يوتيوب أوروبا — بحث تلقائي بدون كلمات مفتاحية
يستهدف: إسبانيا، فرنسا، ألمانيا، إيطاليا، البرتغال
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from googleapiclient.discovery import build
from datetime import datetime

# ──────────────────────────────────────────────
# إعداد الصفحة
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="رادار يوتيوب أوروبا",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS احترافي
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');

html, body, .stApp {
    background: #07070f;
    color: #e0e0f0;
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d1c !important;
    border-left: 1px solid #1a1a35;
}
section[data-testid="stSidebar"] * { color: #b0b0d0 !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0d0d20 0%, #12122a 100%);
    border: 1px solid #1e1e40;
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #ff4d4d, #ff9900, #ffdd00, #00c896, #4d79ff);
}
.hero-title {
    font-size: 36px;
    font-weight: 800;
    background: linear-gradient(135deg, #ff9900, #ffdd00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}
.hero-sub {
    color: #5a5a8a;
    font-size: 15px;
}

/* بطاقة دولة */
.country-card {
    background: #0f0f22;
    border: 1px solid #1e1e3a;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.2s;
}
.country-card:hover { border-color: #ff9900; }
.country-flag { font-size: 28px; }
.country-name { font-size: 14px; font-weight: 700; color: #d0d0f0; }
.country-lang { font-size: 11px; color: #4a4a7a; }

/* بطاقة فيديو */
.vid-card {
    background: #0f0f22;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 10px;
    border-left: 3px solid #ff9900;
}
.vid-rank {
    font-size: 11px;
    color: #ff9900;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.vid-title {
    font-size: 15px;
    font-weight: 700;
    color: #e0e0f8;
    margin-bottom: 8px;
    line-height: 1.4;
}
.vid-meta {
    font-size: 12px;
    color: #4a4a7a;
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}
.vid-ratio {
    font-size: 22px;
    font-weight: 800;
    color: #ffdd00;
}
.vid-ratio-label { font-size: 11px; color: #5a5a8a; }

/* بطاقة الفرصة الكبرى */
.top-card {
    background: linear-gradient(135deg, #1a1200 0%, #2a1e00 100%);
    border: 2px solid #ff9900;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 14px;
    position: relative;
}
.top-card::after {
    content: '🔥 أفضل فرصة';
    position: absolute;
    top: -12px; right: 20px;
    background: #ff9900;
    color: #000;
    font-size: 11px;
    font-weight: 800;
    padding: 3px 12px;
    border-radius: 20px;
}

/* مقياس */
.metric-box {
    background: #0f0f22;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
}
.metric-num {
    font-size: 30px;
    font-weight: 800;
    color: #ffdd00;
    font-family: 'Tajawal', sans-serif;
}
.metric-lbl {
    font-size: 12px;
    color: #4a4a7a;
    margin-top: 4px;
}

/* زر */
.stButton > button {
    background: linear-gradient(135deg, #ff9900, #ffdd00) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    padding: 12px 0 !important;
    width: 100% !important;
}

/* تنبيهات */
.info-box {
    background: rgba(77,121,255,0.08);
    border-left: 3px solid #4d79ff;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    color: #9090d8;
    font-size: 13px;
    margin: 10px 0;
}
.success-box {
    background: rgba(0,200,150,0.08);
    border-left: 3px solid #00c896;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    color: #80ddc8;
    font-size: 13px;
    margin: 10px 0;
}
.divider { border: none; border-top: 1px solid #1a1a35; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# إعدادات الدول والفئات
# ══════════════════════════════════════════════════════════════

# الدول المستهدفة مع علاماتها وأكواد المنطقة
COUNTRIES = {
    "🇪🇸 إسبانيا": {"code": "ES", "flag": "🇪🇸", "lang": "Español"},
    "🇲🇽 المكسيك": {"code": "MX", "flag": "🇲🇽", "lang": "Español (MX)"},
    "🇫🇷 فرنسا":   {"code": "FR", "flag": "🇫🇷", "lang": "Français"},
    "🇩🇪 ألمانيا": {"code": "DE", "flag": "🇩🇪", "lang": "Deutsch"},
    "🇮🇹 إيطاليا": {"code": "IT", "flag": "🇮🇹", "lang": "Italiano"},
    "🇧🇷 البرازيل": {"code": "BR", "flag": "🇧🇷", "lang": "Português"},
    "🇵🇱 بولندا":  {"code": "PL", "flag": "🇵🇱", "lang": "Polski"},
    "🇳🇱 هولندا":  {"code": "NL", "flag": "🇳🇱", "lang": "Nederlands"},
}

# الفئات المتاحة في YouTube (categoryId)
CATEGORIES = {
    "🎬 الترفيه":         "24",
    "🎮 الألعاب":         "20",
    "💻 التقنية":         "28",
    "📚 التعليم":         "27",
    "🎵 الموسيقى":        "10",
    "⚽ الرياضة":         "17",
    "🍳 الطبخ والأسلوب":  "26",
    "🎤 الكوميديا":       "23",
}


# ══════════════════════════════════════════════════════════════
# دوال جلب البيانات
# ══════════════════════════════════════════════════════════════

def fetch_trending(youtube, region_code: str, category_id: str, max_results: int = 15) -> list:
    """
    جلب فيديوهات Trending من YouTube لمنطقة وفئة محددة
    """
    try:
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            chart="mostPopular",
            regionCode=region_code,
            categoryId=category_id,
            maxResults=max_results,
            fields="items(id,snippet(title,channelTitle,channelId,publishedAt,thumbnails),statistics(viewCount,likeCount,commentCount))"
        ).execute()
        return response.get("items", [])
    except Exception:
        return []


def fetch_channel_subs(youtube, channel_id: str) -> int:
    """
    جلب عدد مشتركي قناة واحدة
    """
    try:
        resp = youtube.channels().list(
            part="statistics",
            id=channel_id,
            fields="items(statistics(subscriberCount))"
        ).execute()
        items = resp.get("items", [])
        if items:
            return int(items[0]["statistics"].get("subscriberCount", 1))
    except Exception:
        pass
    return 1


def run_radar(api_key: str, selected_countries: list, selected_categories: list, max_per_combo: int) -> pd.DataFrame:
    """
    الدالة الرئيسية: تمسح كل مجموعة (دولة × فئة) وتجمع النتائج
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    rows = []

    total = len(selected_countries) * len(selected_categories)
    progress = st.progress(0, text="⏳ جاري المسح التلقائي...")
    step = 0

    for country_name in selected_countries:
        country_info = COUNTRIES[country_name]
        region = country_info["code"]
        flag = country_info["flag"]

        for cat_name in selected_categories:
            cat_id = CATEGORIES[cat_name]

            videos = fetch_trending(youtube, region, cat_id, max_per_combo)

            for v in videos:
                vid_id   = v.get("id", "")
                snippet  = v.get("snippet", {})
                stats    = v.get("statistics", {})

                views    = int(stats.get("viewCount", 0))
                likes    = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))
                ch_id    = snippet.get("channelId", "")
                subs     = fetch_channel_subs(youtube, ch_id)

                # قوة الانتشار = نسبة المشاهدات إلى المشتركين
                ratio = round(views / subs, 2) if subs > 0 else 0

                # نسبة التفاعل (Engagement Rate)
                engagement = round((likes + comments) / views * 100, 2) if views > 0 else 0

                rows.append({
                    "الدولة":         f"{flag} {country_name.split(' ', 1)[1]}",
                    "الفئة":          cat_name,
                    "العنوان":        snippet.get("title", ""),
                    "القناة":         snippet.get("channelTitle", ""),
                    "المشاهدات":      views,
                    "الإعجابات":      likes,
                    "التعليقات":      comments,
                    "المشتركين":      subs,
                    "قوة الانتشار":   ratio,
                    "نسبة التفاعل %": engagement,
                    "تاريخ النشر":    snippet.get("publishedAt", "")[:10],
                    "الرابط":         f"https://youtube.com/watch?v={vid_id}",
                    "channel_id":     ch_id,
                })

            step += 1
            progress.progress(step / total, text=f"⏳ {flag} {cat_name} ...")

    progress.empty()
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════
# الشريط الجانبي
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🌍 رادار يوتيوب أوروبا")
    st.markdown("---")

    yt_key = st.text_input("🔑 YouTube API Key", type="password", placeholder="AIza...")

    st.markdown("---")
    st.markdown("**🌐 اختر الدول**")
    selected_countries = st.multiselect(
        label="الدول",
        options=list(COUNTRIES.keys()),
        default=["🇪🇸 إسبانيا", "🇫🇷 فرنسا", "🇩🇪 ألمانيا"],
        label_visibility="collapsed",
    )

    st.markdown("**📂 اختر الفئات**")
    selected_categories = st.multiselect(
        label="الفئات",
        options=list(CATEGORIES.keys()),
        default=["🎬 الترفيه", "🎮 الألعاب", "💻 التقنية"],
        label_visibility="collapsed",
    )

    max_per = st.slider("فيديو لكل مجموعة", 5, 20, 10)

    st.markdown("---")
    run_btn = st.button("🚀 تشغيل الرادار")

    st.markdown("""
    <div style='font-size:12px; color:#2a2a4a; margin-top:16px; line-height:1.8;'>
    <b style='color:#3a3a6a'>كيف يعمل؟</b><br>
    ✅ لا يحتاج كلمات مفتاحية<br>
    ✅ يمسح Trending كل دولة<br>
    ✅ يحسب قوة الانتشار تلقائياً<br>
    ✅ يكشف القنوات الصغيرة الناجحة
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# الصفحة الرئيسية
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-title">🌍 رادار يوتيوب أوروبا التلقائي</div>
    <div class="hero-sub">يمسح Trending أوروبا وأمريكا اللاتينية تلقائياً · لا كلمات مفتاحية · فقط بيانات حقيقية</div>
</div>
""", unsafe_allow_html=True)

# قبل التشغيل
if not run_btn:
    st.markdown('<div class="info-box">👈 اضبط الإعدادات من الشريط الجانبي ثم اضغط <b>تشغيل الرادار</b></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (name, info) in zip([c1, c2, c3, c4], list(COUNTRIES.items())[:4]):
        with col:
            st.markdown(f"""
            <div class="country-card">
                <div class="country-flag">{info['flag']}</div>
                <div class="country-name">{name.split(' ', 1)[1]}</div>
                <div class="country-lang">{info['lang']}</div>
            </div>""", unsafe_allow_html=True)
    st.stop()

# التحقق من المدخلات
if not yt_key:
    st.error("❌ أدخل YouTube API Key من الشريط الجانبي")
    st.stop()
if not selected_countries or not selected_categories:
    st.warning("⚠️ اختر دولة واحدة وفئة واحدة على الأقل")
    st.stop()


# ══════════════════════════════════════════════════════════════
# تشغيل الرادار
# ══════════════════════════════════════════════════════════════

try:
    df = run_radar(yt_key, selected_countries, selected_categories, max_per)
except Exception as e:
    if "quota" in str(e).lower():
        st.error("❌ انتهت حصة الـ API اليومية. حاول غداً أو استخدم مفتاحاً آخر.")
    elif "forbidden" in str(e).lower() or "403" in str(e):
        st.error("❌ مفتاح API غير صالح أو لا يملك صلاحية YouTube Data API v3")
    else:
        st.error(f"❌ خطأ: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ لم يتم جلب أي بيانات. جرب دولاً أو فئات مختلفة.")
    st.stop()

# ترتيب حسب قوة الانتشار
df = df.sort_values("قوة الانتشار", ascending=False).reset_index(drop=True)

st.markdown(f'<div class="success-box">✅ تم اكتشاف <b>{len(df)}</b> فيديو من <b>{len(selected_countries)}</b> دولة و <b>{len(selected_categories)}</b> فئة</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── أرقام ملخصة ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-box"><div class="metric-num">{len(df)}</div><div class="metric-lbl">فيديو محلَّل</div></div>', unsafe_allow_html=True)
with c2:
    top_ratio = df["قوة الانتشار"].max()
    st.markdown(f'<div class="metric-box"><div class="metric-num">{top_ratio}x</div><div class="metric-lbl">أعلى قوة انتشار</div></div>', unsafe_allow_html=True)
with c3:
    avg_views = int(df["المشاهدات"].mean())
    st.markdown(f'<div class="metric-box"><div class="metric-num">{avg_views:,}</div><div class="metric-lbl">متوسط المشاهدات</div></div>', unsafe_allow_html=True)
with c4:
    avg_eng = round(df["نسبة التفاعل %"].mean(), 2)
    st.markdown(f'<div class="metric-box"><div class="metric-num">{avg_eng}%</div><div class="metric-lbl">متوسط التفاعل</div></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── أفضل 3 فرص ───────────────────────────────────────────────
st.markdown("### 🏆 أفضل 3 فرص اكتُشفت")

top3 = df.head(3)
cols = st.columns(3)
for i, (_, row) in enumerate(top3.iterrows()):
    with cols[i]:
        border = "2px solid #ff9900" if i == 0 else "1px solid #1e1e3a"
        badge = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        st.markdown(f"""
        <div style="background:#0f0f22; border:{border}; border-radius:14px; padding:20px; text-align:center; position:relative;">
            <div style="font-size:28px; margin-bottom:8px;">{badge}</div>
            <div style="font-size:13px; font-weight:700; color:#d8d8f0; margin-bottom:12px; line-height:1.4; min-height:48px;">
                {row['العنوان'][:60]}{'...' if len(row['العنوان']) > 60 else ''}
            </div>
            <div class="vid-ratio">{row['قوة الانتشار']}x</div>
            <div class="vid-ratio-label">قوة الانتشار</div>
            <div style="margin-top:10px; font-size:12px; color:#4a4a7a;">
                {row['الدولة']} · {row['الفئة']}<br>
                📺 {row['القناة']}<br>
                👁️ {row['المشاهدات']:,}
            </div>
            <a href="{row['الرابط']}" target="_blank" style="display:block; margin-top:12px; background:#ff9900; color:#000; border-radius:8px; padding:6px; font-size:12px; font-weight:800; text-decoration:none;">▶ شاهد الفيديو</a>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── الرسوم البيانية ───────────────────────────────────────────
st.markdown("### 📊 التحليل البياني")

PLOT_LAYOUT = dict(
    paper_bgcolor="#07070f",
    plot_bgcolor="#07070f",
    font=dict(family="Tajawal", color="#8080b0", size=12),
    margin=dict(t=50, b=40, l=40, r=20),
)

tab1, tab2, tab3 = st.tabs(["🔥 قوة الانتشار", "🌍 مقارنة الدول", "📂 مقارنة الفئات"])

with tab1:
    top20 = df.head(20)
    fig1 = go.Figure(go.Bar(
        x=top20["قوة الانتشار"],
        y=top20["القناة"],
        orientation="h",
        marker=dict(
            color=top20["قوة الانتشار"],
            colorscale=[[0, "#1a1a35"], [0.5, "#ff9900"], [1, "#ffdd00"]],
        ),
        hovertemplate="<b>%{text}</b><br>قوة الانتشار: %{x}x<extra></extra>",
        text=top20["العنوان"].str[:40],
    ))
    fig1.update_layout(
        title="أعلى 20 فيديو بقوة انتشار",
        yaxis=dict(autorange="reversed", gridcolor="#1a1a35"),
        xaxis=dict(gridcolor="#1a1a35", title="قوة الانتشار (x)"),
        **PLOT_LAYOUT,
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    by_country = df.groupby("الدولة").agg(
        متوسط_الانتشار=("قوة الانتشار", "mean"),
        عدد_الفيديوهات=("العنوان", "count"),
        متوسط_المشاهدات=("المشاهدات", "mean"),
    ).reset_index().sort_values("متوسط_الانتشار", ascending=False)

    fig2 = px.bar(
        by_country, x="الدولة", y="متوسط_الانتشار",
        color="متوسط_المشاهدات",
        color_continuous_scale=[[0, "#1a1a35"], [1, "#ff9900"]],
        title="متوسط قوة الانتشار حسب الدولة",
        hover_data=["عدد_الفيديوهات", "متوسط_المشاهدات"],
    )
    fig2.update_layout(**PLOT_LAYOUT, xaxis=dict(gridcolor="#1a1a35"), yaxis=dict(gridcolor="#1a1a35"))
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    by_cat = df.groupby("الفئة").agg(
        متوسط_الانتشار=("قوة الانتشار", "mean"),
        عدد_الفيديوهات=("العنوان", "count"),
    ).reset_index().sort_values("متوسط_الانتشار", ascending=False)

    fig3 = px.pie(
        by_cat, names="الفئة", values="متوسط_الانتشار",
        hole=0.5,
        color_discrete_sequence=["#ff9900", "#ffdd00", "#ff4d4d", "#00c896", "#4d79ff", "#cc44ff", "#ff6699", "#00aaff"],
        title="توزيع قوة الانتشار حسب الفئة",
    )
    fig3.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)

# Scatter: المشاهدات vs المشتركين
st.markdown("### 🔍 الكنوز المخفية (قنوات صغيرة بمشاهدات ضخمة)")
fig4 = px.scatter(
    df,
    x="المشتركين", y="المشاهدات",
    size="قوة الانتشار",
    color="الدولة",
    hover_name="العنوان",
    hover_data={"القناة": True, "قوة الانتشار": True, "الدولة": False},
    title="المشاهدات مقابل حجم القناة — كل فقاعة = فيديو",
    size_max=40,
)
fig4.update_layout(
    **PLOT_LAYOUT,
    xaxis=dict(gridcolor="#1a1a35", title="عدد المشتركين"),
    yaxis=dict(gridcolor="#1a1a35", title="عدد المشاهدات"),
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── الجدول الكامل ─────────────────────────────────────────────
st.markdown("### 📋 قائمة الفيديوهات الكاملة")

display_df = df[["الدولة", "الفئة", "العنوان", "القناة", "المشاهدات",
                  "المشتركين", "قوة الانتشار", "نسبة التفاعل %", "تاريخ النشر", "الرابط"]].copy()

st.dataframe(
    display_df,
    use_container_width=True,
    column_config={
        "الرابط": st.column_config.LinkColumn("🔗 الرابط", display_text="▶ فتح"),
        "قوة الانتشار": st.column_config.NumberColumn(format="%.2fx"),
        "المشاهدات": st.column_config.NumberColumn(format="%d"),
        "المشتركين": st.column_config.NumberColumn(format="%d"),
    },
    hide_index=True,
)

# تصدير CSV
csv = display_df.to_csv(index=False, encoding="utf-8-sig")
st.download_button(
    "⬇️ تحميل النتائج CSV",
    data=csv,
    file_name=f"youtube_radar_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv",
)

st.markdown("""
<div style='text-align:center; padding:32px 0 12px; color:#1e1e3a; font-size:12px;'>
    🌍 رادار يوتيوب أوروبا · بيانات حقيقية · تحليل تلقائي بالكامل
</div>
""", unsafe_allow_html=True)
