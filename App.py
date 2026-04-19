"""
YouTube Niche Insight & Growth Tool
=====================================
أداة تحليل نيتشات يوتيوب باستخدام YouTube Data API v3 و Streamlit
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime, timedelta
import re
import json
import random

# ──────────────────────────────────────────────
# إعداد صفحة Streamlit
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Niche Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS مخصص لتصميم Dashboard احترافي
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* الخلفية العامة */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'DM Sans', sans-serif;
}

/* الشريط الجانبي */
section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e3a;
}
section[data-testid="stSidebar"] * {
    color: #c8c8e0 !important;
}

/* بطاقات المقاييس */
.metric-card {
    background: linear-gradient(135deg, #13131f 0%, #1a1a2e 100%);
    border: 1px solid #252545;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6c63ff, #ff6584);
}
.metric-label {
    font-size: 12px;
    color: #7878aa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
    font-family: 'DM Sans', sans-serif;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}
.metric-sub {
    font-size: 12px;
    color: #5a5a8a;
    margin-top: 4px;
}

/* عنوان رئيسي */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #6c63ff 0%, #ff6584 50%, #ffa600 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 8px;
}
.hero-sub {
    color: #5a5a8a;
    font-size: 15px;
    margin-bottom: 32px;
}

/* بطاقة النيتش */
.niche-badge {
    display: inline-block;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.35);
    color: #a89fff;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 3px;
    font-family: 'DM Sans', sans-serif;
}

/* بطاقة الفيديو */
.video-card {
    background: #13131f;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.video-card:hover {
    border-color: #6c63ff;
}
.video-title-text {
    font-size: 14px;
    font-weight: 600;
    color: #d8d8ee;
    margin-bottom: 6px;
    font-family: 'Syne', sans-serif;
}
.video-meta {
    font-size: 12px;
    color: #5a5a8a;
}
.video-views {
    color: #6c63ff;
    font-weight: 600;
}

/* تنبيهات */
.insight-box {
    background: rgba(108,99,255,0.08);
    border-left: 3px solid #6c63ff;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0;
    color: #b8b8d8;
    font-size: 14px;
}
.warning-box {
    background: rgba(255,101,132,0.08);
    border-left: 3px solid #ff6584;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0;
    color: #ffb8c8;
    font-size: 14px;
}
.success-box {
    background: rgba(0,200,150,0.08);
    border-left: 3px solid #00c896;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0;
    color: #88eedd;
    font-size: 14px;
}

/* أزرار */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #ff6584) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* فاصل */
.section-divider {
    border: none;
    border-top: 1px solid #1e1e3a;
    margin: 28px 0;
}

/* عنوان القسم */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #c8c8e8;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* بطاقة الـ AI */
.ai-card {
    background: linear-gradient(135deg, #0f0f1f 0%, #181830 100%);
    border: 1px solid #252550;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.ai-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #8878ff;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}
.ai-title-item {
    background: #1a1a30;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    color: #d0d0ee;
    font-size: 14px;
    border-left: 2px solid #6c63ff;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# دوال YouTube Data API
# ══════════════════════════════════════════════════════════════

def search_videos(api_key: str, keyword: str, max_results: int = 30) -> list:
    """
    البحث عن الفيديوهات باستخدام YouTube Data API v3
    يُرجع قائمة بـ video IDs المنشورة خلال آخر 30 يوماً
    """
    published_after = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": published_after,
        "maxResults": max_results,
        "key": api_key,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [item["id"]["videoId"] for item in data.get("items", [])]


def get_videos_details(api_key: str, video_ids: list) -> list:
    """
    جلب تفاصيل الفيديوهات (إحصائيات، محتوى، snippet)
    """
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": api_key,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("items", [])


def get_channel_info(api_key: str, channel_ids: list) -> dict:
    """
    جلب معلومات القنوات (عدد المشتركين) لحساب نسبة Views/Subs
    """
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics",
        "id": ",".join(set(channel_ids)),
        "key": api_key,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    return {item["id"]: int(item["statistics"].get("subscriberCount", 0)) for item in items}


def parse_duration(duration_str: str) -> int:
    """
    تحويل مدة ISO 8601 (مثل PT5M30S) إلى ثوانٍ
    """
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def analyze_title_tone(title: str) -> str:
    """
    تحليل نبرة العنوان: عاطفية، تعليمية، أو Clickbait
    """
    title_lower = title.lower()
    emotional_keywords = ["أفضل", "مذهل", "رهيب", "لا تصدق", "حصري", "سري",
                          "best", "amazing", "incredible", "shocking", "secret", "revealed", "you won't believe"]
    educational_keywords = ["كيف", "شرح", "تعلم", "دليل", "خطوات",
                            "how", "tutorial", "guide", "learn", "tips", "steps", "what is"]
    clickbait_keywords = ["!", "؟", "?", "#", "...", "🔥", "💥", "😱", "🤑"]

    emotional_score = sum(1 for kw in emotional_keywords if kw in title_lower)
    educational_score = sum(1 for kw in educational_keywords if kw in title_lower)
    clickbait_score = sum(1 for kw in clickbait_keywords if kw in title)

    if clickbait_score >= 3 or (emotional_score >= 2 and clickbait_score >= 1):
        return "🎭 Clickbait"
    elif educational_score >= 2:
        return "📚 تعليمي"
    elif emotional_score >= 1:
        return "❤️ عاطفي"
    else:
        return "📋 محايد"


# ══════════════════════════════════════════════════════════════
# دوال تحليل البيانات
# ══════════════════════════════════════════════════════════════

def build_dataframe(videos: list, channel_subs: dict) -> pd.DataFrame:
    """
    بناء DataFrame شامل من بيانات الفيديوهات
    """
    rows = []
    for v in videos:
        snippet = v.get("snippet", {})
        stats = v.get("statistics", {})
        content = v.get("contentDetails", {})

        channel_id = snippet.get("channelId", "")
        subs = channel_subs.get(channel_id, 0)
        views = int(stats.get("viewCount", 0))
        duration_sec = parse_duration(content.get("duration", "PT0S"))
        title = snippet.get("title", "")
        published_at = snippet.get("publishedAt", "")[:10]
        tags = snippet.get("tags", [])

        # نسبة المشاهدات إلى المشتركين (Views-to-Subscribers Ratio)
        vts_ratio = round(views / subs, 3) if subs > 0 else 0

        rows.append({
            "video_id": v.get("id", ""),
            "title": title,
            "channel": snippet.get("channelTitle", ""),
            "channel_id": channel_id,
            "published_at": published_at,
            "views": views,
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "subscribers": subs,
            "vts_ratio": vts_ratio,
            "duration_sec": duration_sec,
            "title_length": len(title),
            "tone": analyze_title_tone(title),
            "tags": tags,
            "tags_count": len(tags),
        })
    return pd.DataFrame(rows)


def extract_top_tags(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    استخراج الكلمات المفتاحية الأكثر تكراراً من كل الفيديوهات
    """
    all_tags = []
    for tags_list in df["tags"]:
        all_tags.extend([t.lower().strip() for t in tags_list])
    counter = Counter(all_tags)
    top = counter.most_common(top_n)
    return pd.DataFrame(top, columns=["tag", "count"])


def calculate_niche_score(df: pd.DataFrame) -> float:
    """
    حساب نقاط سهولة اختراق النيتش (كلما ارتفع الـ VTS ratio = نيتش سهل)
    """
    avg_vts = df["vts_ratio"].mean()
    avg_views = df["views"].mean()
    # نقاط من 0 إلى 100
    score = min(100, (avg_vts * 10 + (avg_views / 100000)) * 5)
    return round(score, 1)


# ══════════════════════════════════════════════════════════════
# دوال توليد المحتوى بالذكاء الاصطناعي (Anthropic API)
# ══════════════════════════════════════════════════════════════

def generate_ai_titles(top_titles: list, keyword: str, anthropic_key: str | None = None) -> list:
    """
    توليد عناوين مقترحة باستخدام Anthropic API أو Fallback ذكي
    """
    if anthropic_key:
        try:
            headers = {
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            titles_sample = "\n".join(f"- {t}" for t in top_titles[:8])
            payload = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 600,
                "messages": [{
                    "role": "user",
                    "content": f"""أنت خبير في تحسين محتوى يوتيوب. بناءً على هذه العناوين الناجحة في نيتش '{keyword}':

{titles_sample}

اقترح 5 عناوين جديدة جذابة ومختلفة. اجعل كل عنوان على سطر منفصل. لا تضف أرقاماً أو شرحاً، فقط العناوين."""
                }]
            }
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=20
            )
            if resp.status_code == 200:
                text = resp.json()["content"][0]["text"]
                lines = [l.strip().lstrip("-• ") for l in text.strip().split("\n") if len(l.strip()) > 10]
                return lines[:5]
        except Exception:
            pass

    # Fallback: توليد عناوين بناءً على قوالب ذكية
    patterns = [
        f"كيف تنجح في {keyword} بدون خبرة سابقة",
        f"أسرار {keyword} التي لا يخبرك بها أحد",
        f"أفضل {keyword} في 2025: دليلك الشامل",
        f"{keyword} للمبتدئين: خطوة بخطوة",
        f"لماذا يفشل الجميع في {keyword}؟ الحقيقة الكاملة",
    ]
    return patterns


def generate_thumbnail_idea(keyword: str, top_title: str, anthropic_key: str | None = None) -> str:
    """
    توليد فكرة Thumbnail لزيادة الـ CTR
    """
    if anthropic_key:
        try:
            headers = {
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            payload = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 300,
                "messages": [{
                    "role": "user",
                    "content": f"""اقترح فكرة Thumbnail احترافي لفيديو يوتيوب بعنوان: '{top_title}' في نيتش '{keyword}'.

اذكر: العناصر البصرية، الألوان، النص على الصورة، وتعبير الوجه إن وُجد. كن محدداً وعملياً في 3-4 جمل فقط."""
                }]
            }
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=20
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"].strip()
        except Exception:
            pass

    # Fallback
    return (
        f"خلفية بلون داكن (أسود أو أزرق غامق) مع نص كبير وجريء بلون أصفر/أبيض يكتب أبرز فائدة. "
        f"أضف صورة شخص بتعبير مندهش أو مبتسم في الجانب الأيسر. "
        f"استخدم أيقونة أو رمز يمثل '{keyword}' في الركن. "
        f"أبقِ النص أقل من 6 كلمات لقراءة سريعة."
    )


# ══════════════════════════════════════════════════════════════
# دوال الرسوم البيانية
# ══════════════════════════════════════════════════════════════

PLOTLY_THEME = dict(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font=dict(family="DM Sans", color="#9898c0", size=12),
    margin=dict(t=40, b=40, l=40, r=20),
    xaxis=dict(gridcolor="#1e1e3a", linecolor="#1e1e3a"),
    yaxis=dict(gridcolor="#1e1e3a", linecolor="#1e1e3a"),
)


def chart_views_over_time(df: pd.DataFrame) -> go.Figure:
    """رسم بياني: المشاهدات بمرور الوقت"""
    df_sorted = df.sort_values("published_at")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted["published_at"],
        y=df_sorted["views"],
        mode="lines+markers",
        line=dict(color="#6c63ff", width=2),
        marker=dict(size=7, color="#ff6584", line=dict(width=1, color="#6c63ff")),
        fill="tozeroy",
        fillcolor="rgba(108,99,255,0.08)",
        hovertemplate="<b>%{text}</b><br>المشاهدات: %{y:,}<extra></extra>",
        text=df_sorted["channel"],
    ))
    fig.update_layout(
        title="📈 المشاهدات عبر الزمن",
        **PLOTLY_THEME,
        xaxis_title="تاريخ النشر",
        yaxis_title="المشاهدات",
    )
    return fig


def chart_vts_scatter(df: pd.DataFrame) -> go.Figure:
    """رسم بياني: العلاقة بين المشاهدات والمشتركين"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["subscribers"],
        y=df["views"],
        mode="markers",
        marker=dict(
            size=10,
            color=df["vts_ratio"],
            colorscale=[[0, "#252545"], [0.5, "#6c63ff"], [1, "#ff6584"]],
            showscale=True,
            colorbar=dict(title="VTS Ratio", tickfont=dict(color="#9898c0")),
            line=dict(width=0.5, color="#1e1e3a"),
        ),
        hovertemplate="<b>%{text}</b><br>مشتركون: %{x:,}<br>مشاهدات: %{y:,}<extra></extra>",
        text=df["channel"],
    ))
    fig.update_layout(
        title="🔍 المشاهدات مقابل المشتركين (كشف الفرص)",
        **PLOTLY_THEME,
        xaxis_title="عدد المشتركين",
        yaxis_title="عدد المشاهدات",
    )
    return fig


def chart_top_tags(tags_df: pd.DataFrame) -> go.Figure:
    """رسم بياني: أكثر الكلمات المفتاحية تكراراً"""
    tags_df = tags_df.head(15)
    fig = go.Figure(go.Bar(
        x=tags_df["count"],
        y=tags_df["tag"],
        orientation="h",
        marker=dict(
            color=tags_df["count"],
            colorscale=[[0, "#252545"], [1, "#6c63ff"]],
        ),
        hovertemplate="%{y}: %{x} مرة<extra></extra>",
    ))
    fig.update_layout(
        title="🏷️ أكثر الكلمات المفتاحية (Tags) تكراراً",
        **PLOTLY_THEME,
        yaxis=dict(autorange="reversed", gridcolor="#1e1e3a"),
        xaxis_title="التكرار",
    )
    return fig


def chart_tone_distribution(df: pd.DataFrame) -> go.Figure:
    """رسم بياني: توزيع نبرة العناوين"""
    tone_counts = df["tone"].value_counts().reset_index()
    tone_counts.columns = ["tone", "count"]
    colors = ["#6c63ff", "#ff6584", "#ffa600", "#00c896"]
    fig = go.Figure(go.Pie(
        labels=tone_counts["tone"],
        values=tone_counts["count"],
        hole=0.55,
        marker=dict(colors=colors[:len(tone_counts)], line=dict(color="#0a0a0f", width=2)),
        hovertemplate="%{label}: %{value} فيديو<extra></extra>",
    ))
    fig.update_layout(
        title="🎭 توزيع نبرة العناوين",
        **PLOTLY_THEME,
        legend=dict(font=dict(color="#9898c0")),
    )
    return fig


def chart_title_length(df: pd.DataFrame) -> go.Figure:
    """رسم بياني: توزيع طول العناوين"""
    fig = go.Figure(go.Histogram(
        x=df["title_length"],
        nbinsx=20,
        marker=dict(color="#6c63ff", line=dict(color="#0a0a0f", width=1)),
        hovertemplate="طول %{x}: %{y} فيديو<extra></extra>",
    ))
    fig.update_layout(
        title="📏 توزيع طول العناوين (بالأحرف)",
        **PLOTLY_THEME,
        xaxis_title="عدد الأحرف",
        yaxis_title="عدد الفيديوهات",
    )
    return fig


# ══════════════════════════════════════════════════════════════
# الشريط الجانبي (Sidebar)
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🎯 YouTube Niche Analyzer")
    st.markdown("---")

    # مفاتيح API (password mode للأمان)
    yt_api_key = st.text_input(
        "🔑 YouTube API Key",
        type="password",
        placeholder="AIza...",
        help="احصل عليه من Google Cloud Console → YouTube Data API v3"
    )

    anthropic_key = st.text_input(
        "🤖 Anthropic API Key (اختياري)",
        type="password",
        placeholder="sk-ant-...",
        help="لتفعيل توليد العناوين والـ Thumbnail بالذكاء الاصطناعي"
    )

    st.markdown("---")

    # إعدادات البحث
    keyword = st.text_input(
        "🔍 الكلمة المفتاحية",
        placeholder="مثال: تعلم Python، كيف تربح من الإنترنت",
    )

    max_results = st.slider("عدد الفيديوهات للتحليل", min_value=10, max_value=50, value=25, step=5)

    st.markdown("---")

    analyze_btn = st.button("🚀 ابدأ التحليل")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#3a3a5a; line-height:1.8;'>
    <b style='color:#4a4a7a'>كيف يعمل؟</b><br>
    1. أدخل مفتاح YouTube API<br>
    2. اكتب الكلمة المفتاحية<br>
    3. اضغط تحليل واستمتع بالنتائج<br><br>
    <b style='color:#4a4a7a'>Anthropic Key</b> اختياري لتحسين الـ AI
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# الصفحة الرئيسية
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="hero-title">YouTube Niche Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">اكتشف الفرص الذهبية في نيتشات يوتيوب بالبيانات الحقيقية والذكاء الاصطناعي</div>', unsafe_allow_html=True)

# ── حالة الترحيب (قبل البحث) ──────────────────────────
if not analyze_btn or not keyword or not yt_api_key:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Viral Potential</div>
            <div class="metric-value">🔥</div>
            <div class="metric-sub">تحليل أكثر الفيديوهات انتشاراً</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Niche Difficulty</div>
            <div class="metric-value">📊</div>
            <div class="metric-sub">نسبة Views/Subscribers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AI Content Tools</div>
            <div class="metric-value">🤖</div>
            <div class="metric-sub">مولد عناوين وأفكار Thumbnail</div>
        </div>""", unsafe_allow_html=True)

    if not yt_api_key:
        st.markdown('<div class="insight-box">👈 أدخل <b>YouTube API Key</b> من الشريط الجانبي للبدء</div>', unsafe_allow_html=True)
    elif not keyword:
        st.markdown('<div class="insight-box">✍️ اكتب <b>الكلمة المفتاحية</b> التي تريد تحليل نيتشها</div>', unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════
# تنفيذ التحليل
# ══════════════════════════════════════════════════════════════

with st.spinner(f"🔄 جارٍ تحليل نيتش «{keyword}»..."):
    try:
        # 1. البحث عن الفيديوهات
        video_ids = search_videos(yt_api_key, keyword, max_results)
        if not video_ids:
            st.markdown('<div class="warning-box">⚠️ لم يتم العثور على فيديوهات. جرّب كلمة مفتاحية مختلفة.</div>', unsafe_allow_html=True)
            st.stop()

        # 2. جلب التفاصيل
        videos = get_videos_details(yt_api_key, video_ids)

        # 3. جلب بيانات القنوات
        channel_ids = [v["snippet"]["channelId"] for v in videos]
        channel_subs = get_channel_info(yt_api_key, channel_ids)

        # 4. بناء DataFrame
        df = build_dataframe(videos, channel_subs)
        df = df[df["views"] > 0].reset_index(drop=True)

        if df.empty:
            st.markdown('<div class="warning-box">⚠️ البيانات المسترجعة غير كافية للتحليل.</div>', unsafe_allow_html=True)
            st.stop()

        # 5. استخراج Tags
        tags_df = extract_top_tags(df)

        # 6. حساب نقاط النيتش
        niche_score = calculate_niche_score(df)

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "?"
        if status == 403:
            st.markdown('<div class="warning-box">❌ <b>مفتاح API غير صالح أو منتهي الصلاحية.</b> تأكد من تفعيل YouTube Data API v3.</div>', unsafe_allow_html=True)
        elif status == 400:
            st.markdown('<div class="warning-box">❌ <b>طلب غير صحيح.</b> تحقق من صيغة الكلمة المفتاحية.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">❌ خطأ HTTP {status}: {str(e)}</div>', unsafe_allow_html=True)
        st.stop()
    except Exception as e:
        st.markdown(f'<div class="warning-box">❌ خطأ غير متوقع: {str(e)}</div>', unsafe_allow_html=True)
        st.stop()


# ══════════════════════════════════════════════════════════════
# عرض النتائج
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="success-box">✅ تم تحليل <b>{}</b> فيديو بنجاح لنيتش «{}»</div>'.format(len(df), keyword), unsafe_allow_html=True)

# ── المقاييس الرئيسية ──────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 المقاييس الرئيسية</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">متوسط المشاهدات</div>
        <div class="metric-value">{df['views'].mean():,.0f}</div>
        <div class="metric-sub">لآخر 30 يوم</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">أعلى مشاهدات</div>
        <div class="metric-value">{df['views'].max():,}</div>
        <div class="metric-sub">Viral Potential</div>
    </div>""", unsafe_allow_html=True)
with col3:
    avg_subs = df['subscribers'].mean()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">متوسط المشتركين</div>
        <div class="metric-value">{avg_subs:,.0f}</div>
        <div class="metric-sub">للقنوات المحللة</div>
    </div>""", unsafe_allow_html=True)
with col4:
    avg_vts = df['vts_ratio'].mean()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">VTS Ratio</div>
        <div class="metric-value">{avg_vts:.2f}x</div>
        <div class="metric-sub">Views ÷ Subscribers</div>
    </div>""", unsafe_allow_html=True)
with col5:
    score_color = "#00c896" if niche_score > 60 else "#ffa600" if niche_score > 30 else "#ff6584"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">سهولة الاختراق</div>
        <div class="metric-value" style="color:{score_color}">{niche_score}/100</div>
        <div class="metric-sub">{"سهل 🟢" if niche_score > 60 else "متوسط 🟡" if niche_score > 30 else "صعب 🔴"}</div>
    </div>""", unsafe_allow_html=True)

# ── الرسوم البيانية ─────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 التحليل البياني</div>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)
with col_left:
    st.plotly_chart(chart_views_over_time(df), use_container_width=True)
with col_right:
    st.plotly_chart(chart_vts_scatter(df), use_container_width=True)

col_left2, col_right2 = st.columns(2)
with col_left2:
    if not tags_df.empty:
        st.plotly_chart(chart_top_tags(tags_df), use_container_width=True)
    else:
        st.markdown('<div class="insight-box">ℹ️ لا توجد Tags كافية في هذه الفيديوهات</div>', unsafe_allow_html=True)
with col_right2:
    st.plotly_chart(chart_tone_distribution(df), use_container_width=True)

st.plotly_chart(chart_title_length(df), use_container_width=True)

# ── تحليل الكلمات المفتاحية ──────────────────────────────────
if not tags_df.empty:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏷️ أهم الكلمات المفتاحية (Tags)</div>', unsafe_allow_html=True)
    tags_html = "".join(f'<span class="niche-badge">{row["tag"]} ({row["count"]})</span>' for _, row in tags_df.head(20).iterrows())
    st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)

# ── أفضل الفيديوهات ─────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏆 أعلى 10 فيديوهات أداءً</div>', unsafe_allow_html=True)

top10 = df.nlargest(10, "views")
for _, row in top10.iterrows():
    yt_url = f"https://youtube.com/watch?v={row['video_id']}"
    st.markdown(f"""
    <div class="video-card">
        <div class="video-title-text">
            <a href="{yt_url}" target="_blank" style="color:#c8c8e8; text-decoration:none;">
                {row['title']}
            </a>
        </div>
        <div class="video-meta">
            📺 {row['channel']} &nbsp;|&nbsp;
            <span class="video-views">👁️ {row['views']:,}</span> &nbsp;|&nbsp;
            📅 {row['published_at']} &nbsp;|&nbsp;
            🎭 {row['tone']} &nbsp;|&nbsp;
            VTS: {row['vts_ratio']}x
        </div>
    </div>""", unsafe_allow_html=True)

# ── أدوات الذكاء الاصطناعي ─────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🤖 أدوات الذكاء الاصطناعي</div>', unsafe_allow_html=True)

if not anthropic_key:
    st.markdown('<div class="insight-box">💡 أضف <b>Anthropic API Key</b> في الشريط الجانبي للحصول على عناوين وأفكار Thumbnail أكثر دقة وإبداعاً</div>', unsafe_allow_html=True)

top_titles = top10["title"].tolist()
best_title = top_titles[0] if top_titles else keyword

col_ai1, col_ai2 = st.columns(2)

with col_ai1:
    with st.spinner("🧠 جارٍ توليد العناوين..."):
        ai_titles = generate_ai_titles(top_titles, keyword, anthropic_key or None)

    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-card-title">✨ عناوين مقترحة بالذكاء الاصطناعي</div>
        {''.join(f'<div class="ai-title-item">{t}</div>' for t in ai_titles)}
    </div>""", unsafe_allow_html=True)

with col_ai2:
    with st.spinner("🎨 جارٍ توليد فكرة الـ Thumbnail..."):
        thumb_idea = generate_thumbnail_idea(keyword, best_title, anthropic_key or None)

    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-card-title">🖼️ فكرة Thumbnail لأعلى CTR</div>
        <div style="color:#c0c0e0; font-size:14px; line-height:1.7;">{thumb_idea}</div>
        <div style="margin-top:12px; font-size:12px; color:#4a4a7a;">
            📌 مبني على: "{best_title[:60]}..."
        </div>
    </div>""", unsafe_allow_html=True)

# ── تصدير البيانات ─────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💾 تصدير البيانات</div>', unsafe_allow_html=True)

export_df = df.drop(columns=["tags", "channel_id"], errors="ignore")
csv_data = export_df.to_csv(index=False, encoding="utf-8-sig")

col_dl1, col_dl2 = st.columns([1, 3])
with col_dl1:
    st.download_button(
        label="⬇️ تحميل CSV",
        data=csv_data,
        file_name=f"niche_{keyword.replace(' ','_')}.csv",
        mime="text/csv",
    )

# ── Footer ──────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:40px 0 20px; color:#2a2a4a; font-size:12px; font-family:DM Sans;'>
    YouTube Niche Analyzer • بيانات حقيقية • تحليل ذكي
</div>
""", unsafe_allow_html=True)
