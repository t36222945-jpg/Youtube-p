"""
تطبيق رادار اكتشاف الفرص التلقائي
Auto-Niche Discovery Radar Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openai
from datetime import datetime, timedelta
from collections import Counter

# ============================================================================
# الإعدادات
# ============================================================================

st.set_page_config(
    page_title="🎯 رادار اكتشاف الفرص",
    page_icon="🎯",
    layout="wide"
)

# CSS للثيم الفاخر
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #FFD700;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    .opportunity-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #2a2f4a 100%);
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# الدوال المساعدة
# ============================================================================

@st.cache_resource
def init_youtube_api(api_key):
    """تهيئة YouTube API"""
    try:
        return build('youtube', 'v3', developerKey=api_key)
    except Exception as e:
        st.error(f"خطأ: {e}")
        return None

@st.cache_data(ttl=3600)
def get_trending_videos(youtube, category_id, max_results=50):
    """الحصول على الفيديوهات الرائجة"""
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode="US",
            categoryId=category_id,
            maxResults=min(max_results, 50),
            fields="items(id,snippet(title,publishedAt,channelId,tags),statistics(viewCount,likeCount,commentCount))"
        )
        response = request.execute()
        return response.get('items', [])
    except HttpError as e:
        st.error(f"خطأ API: {e}")
        return []

def get_channel_info(youtube, channel_id):
    """الحصول على معلومات القناة"""
    try:
        request = youtube.channels().list(
            part="statistics,snippet",
            id=channel_id,
            fields="items(statistics(subscriberCount),snippet(title))"
        )
        response = request.execute()
        if response.get('items'):
            stats = response['items'][0]['statistics']
            return {
                'subscribers': int(stats.get('subscriberCount', 0)),
                'channelName': response['items'][0]['snippet'].get('title', 'Unknown')
            }
    except:
        pass
    return {'subscribers': 0, 'channelName': 'Unknown'}

def filter_recent_videos(videos, days=7):
    """تصفية الفيديوهات من آخر 7 أيام"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    filtered = []
    
    for video in videos:
        try:
            published_at = datetime.fromisoformat(
                video['snippet']['publishedAt'].replace('Z', '+00:00')
            )
            if published_at > cutoff_date:
                filtered.append(video)
        except:
            pass
    
    return filtered

def calculate_opportunity_score(views, subscribers):
    """حساب نقاط الفرصة"""
    if subscribers == 0:
        return 20
    
    ratio = views / max(subscribers, 1)
    
    if ratio > 1000:
        return 95
    elif ratio > 500:
        return 85
    elif ratio > 100:
        return 75
    elif ratio > 50:
        return 60
    elif ratio > 10:
        return 40
    else:
        return 20

def identify_rising_niches(youtube, category_ids, num_niches=5):
    """تحديد النيتشات الصاعدة"""
    niche_data = {}
    category_names = {
        '25': 'العلوم والتكنولوجيا',
        '27': 'التعليم',
        '26': 'الطريقة والأسلوب',
        '24': 'الترفيه',
        '28': 'الطبيعة والعلوم'
    }
    
    for category_id in category_ids:
        videos = get_trending_videos(youtube, category_id, max_results=30)
        recent_videos = filter_recent_videos(videos, days=7)
        
        if recent_videos:
            total_views = sum(int(v['statistics'].get('viewCount', 0)) for v in recent_videos)
            avg_views = total_views / len(recent_videos)
            growth_rate = avg_views / (len(recent_videos) + 1)
            
            niche_data[category_id] = {
                'name': category_names.get(category_id, f'نيتش {category_id}'),
                'growth_rate': growth_rate,
                'avg_views': avg_views,
                'video_count': len(recent_videos),
                'total_views': total_views
            }
    
    sorted_niches = sorted(
        niche_data.items(),
        key=lambda x: x[1]['growth_rate'],
        reverse=True
    )
    
    return sorted_niches[:num_niches]

def generate_title_with_ai(openai_key, niche, trending_titles):
    """توليد عناوين بالذكاء الاصطناعي"""
    if not openai_key:
        return "أضف OpenAI API Key"
    
    try:
        openai.api_key = openai_key
        titles_context = "\n".join(trending_titles[:5])
        
        prompt = f"""
        أنت متخصص في إنشاء عناوين YouTube جاذبة.
        النيتش: {niche}
        الأمثلة: {titles_context}
        
        أنشئ 3 عناوين مقترحة احترافية (50-70 حرف).
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"خطأ: {str(e)}"

def generate_script_outline(openai_key, title, niche):
    """توليد خطة الفيديو"""
    if not openai_key:
        return "أضف OpenAI API Key"
    
    try:
        openai.api_key = openai_key
        
        prompt = f"""
        أنت كاتب سيناريو YouTube متخصص.
        العنوان: {title}
        النيتش: {niche}
        
        أنشئ خطة فيديو مختصرة:
        1. المقدمة (5-10 ث)
        2. المشكلة (10-15 ث)
        3. الحل (30-60 ث)
        4. الأمثلة (20-30 ث)
        5. الخاتمة (5-10 ث)
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"خطأ: {str(e)}"

# ============================================================================
# الواجهة الرئيسية
# ============================================================================

# الشريط الجانبي
with st.sidebar:
    st.markdown("## ⚙️ الإعدادات")
    
    youtube_api_key = st.text_input("🔑 YouTube API Key:", type="password")
    openai_api_key = st.text_input("🤖 OpenAI API Key:", type="password")
    
    st.divider()
    st.success("رادار اكتشاف الفرص التلقائي")

# الرأس
st.markdown('<div class="main-header">🎯 رادار اكتشاف الفرص التلقائي</div>', unsafe_allow_html=True)
st.markdown("<center style='color: #b0b0b0;'>Auto-Niche Discovery Radar</center>", unsafe_allow_html=True)
st.divider()

if not youtube_api_key:
    st.error("❌ أضف YouTube API Key")
    st.stop()

youtube = init_youtube_api(youtube_api_key)
if youtube is None:
    st.stop()

# الأزرار
col1, col2, col3 = st.columns(3)

with col1:
    explore_button = st.button("🚀 استكشاف الفرص الآن", use_container_width=True)

with col2:
    rising_button = st.button("📈 النيتشات الصاعدة", use_container_width=True)

with col3:
    generate_button = st.button("✨ توليد محتوى ذكي", use_container_width=True)

st.divider()

# ============================================================================
# الميزة 1: استكشاف الفرص
# ============================================================================

if explore_button:
    st.subheader("🔍 الفرص الرائجة")
    
    category_ids = ['25', '27', '26', '24']
    category_names_map = {
        '25': 'العلوم والتكنولوجيا',
        '27': 'التعليم',
        '26': 'الطريقة والأسلوب',
        '24': 'الترفيه'
    }
    
    all_opportunities = []
    
    with st.spinner("⏳ جاري البحث..."):
        for category_id in category_ids:
            videos = get_trending_videos(youtube, category_id, max_results=50)
            recent_videos = filter_recent_videos(videos, days=7)
            
            for video in recent_videos:
                try:
                    channel_id = video['snippet']['channelId']
                    channel_info = get_channel_info(youtube, channel_id)
                    
                    views = int(video['statistics'].get('viewCount', 0))
                    subscribers = channel_info['subscribers']
                    
                    opportunity_score = calculate_opportunity_score(views, subscribers)
                    
                    if opportunity_score >= 60:
                        all_opportunities.append({
                            'title': video['snippet']['title'][:80],
                            'views': views,
                            'subscribers': subscribers,
                            'channel': channel_info['channelName'],
                            'category': category_names_map[category_id],
                            'score': opportunity_score,
                            'likes': int(video['statistics'].get('likeCount', 0)),
                            'comments': int(video['statistics'].get('commentCount', 0))
                        })
                except:
                    pass
    
    opportunities_df = pd.DataFrame(all_opportunities)
    opportunities_df = opportunities_df.sort_values('score', ascending=False)
    
    if not opportunities_df.empty:
        st.success(f"✅ تم اكتشاف {len(opportunities_df)} فرصة!")
        
        for idx, (_, opp) in enumerate(opportunities_df.head(10).iterrows(), 1):
            st.markdown(f"""
                <div class="opportunity-card">
                <h3>#{idx} | {opp['title']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎯 الفرصة", f"{opp['score']:.0f}/100")
            with col2:
                st.metric("👁️ المشاهدات", f"{opp['views']:,}")
            with col3:
                st.metric("👥 المشتركين", f"{opp['subscribers']:,}")
            with col4:
                ratio = opp['views'] / max(opp['subscribers'], 1)
                st.metric("📊 النسبة", f"{ratio:.1f}x")
            
            st.write(f"**القناة:** {opp['channel']} | **النيتش:** {opp['category']}")
            st.divider()
        
        # رسم بياني
        fig = px.bar(
            opportunities_df.head(10),
            x='title',
            y='score',
            color='score',
            title='أفضل 10 فرص',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(plot_bgcolor='#0a0e27', paper_bgcolor='#0a0e27', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# الميزة 2: النيتشات الصاعدة
# ============================================================================

if rising_button:
    st.subheader("📈 أفضل 5 نيتشات صاعدة")
    
    category_ids = ['25', '27', '26', '24', '28']
    
    with st.spinner("⏳ جاري التحليل..."):
        rising_niches = identify_rising_niches(youtube, category_ids, num_niches=5)
    
    if rising_niches:
        st.success("✅ تم التحديد!")
        
        for idx, (cat_id, niche_data) in enumerate(rising_niches, 1):
            st.markdown(f"""
                <div class="opportunity-card">
                <h2>#{idx} | {niche_data['name']}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 النمو", f"{niche_data['growth_rate']:.2f}k")
            with col2:
                st.metric("📈 متوسط", f"{niche_data['avg_views']:,.0f}")
            with col3:
                st.metric("🎬 الفيديوهات", f"{niche_data['video_count']}")
            
            st.divider()

# ============================================================================
# الميزة 3: توليد المحتوى
# ============================================================================

if generate_button:
    st.subheader("✨ توليد محتوى ذكي")
    
    if not openai_api_key:
        st.warning("⚠️ أضف OpenAI API Key")
    else:
        niche_options = ['العلوم والتكنولوجيا', 'التعليم', 'الطريقة والأسلوب', 'الترفيه']
        selected_niche = st.selectbox("اختر النيتش:", niche_options)
        
        category_id = {'العلوم والتكنولوجيا': '25', 'التعليم': '27', 'الطريقة والأسلوب': '26', 'الترفيه': '24'}.get(selected_niche, '25')
        
        with st.spinner("⏳ جاري الحصول على أمثلة..."):
            sample_videos = get_trending_videos(youtube, category_id, max_results=10)
            sample_titles = [v['snippet']['title'] for v in sample_videos]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 عناوين مقترحة")
            if st.button("توليد عناوين"):
                with st.spinner("🤖 جاري..."):
                    titles = generate_title_with_ai(openai_api_key, selected_niche, sample_titles)
                    st.markdown(titles)
        
        with col2:
            st.markdown("### 📝 خطة الفيديو")
            if st.button("توليد الخطة"):
                sample_title = sample_titles[0] if sample_titles else f"فيديو عن {selected_niche}"
                with st.spinner("🤖 جاري..."):
                    script = generate_script_outline(openai_api_key, sample_title, selected_niche)
                    st.markdown(script)

st.divider()
st.markdown("### 📊 معلومات مفيدة")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("💡 ابحث عن مشاهدات > 100x المشتركين")
with col2:
    st.success("🎯 النسبة > 100x = فرصة ذهبية")
with col3:
    st.warning("⚠️ حدث البيانات كل ساعة")
