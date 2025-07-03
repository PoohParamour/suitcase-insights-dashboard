import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import unicodedata
from io import StringIO

# Set page config
st.set_page_config(
    page_title="Suitcase Insights Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Thai fonts and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Sarabun', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 50%, #667eea 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.25);
        margin: 15px 0;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(31, 38, 135, 0.6);
    }
    
    .metric-card h2 {
        font-size: 2.5em;
        margin: 10px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        font-weight: bold;
    }
    
    .metric-card h3 {
        font-size: 1.3em;
        margin-bottom: 10px;
        opacity: 0.95;
        font-weight: 600;
    }
    
    .metric-card p {
        font-size: 0.9em;
        opacity: 0.9;
        margin-top: 5px;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(116, 185, 255, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .insight-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(116, 185, 255, 0.6);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(253, 203, 110, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .warning-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(253, 203, 110, 0.6);
    }
    
    .success-box {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0, 184, 148, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .success-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 184, 148, 0.6);
    }
    
    .insight-box h4, .warning-box h4, .success-box h4 {
        margin-bottom: 15px;
        font-size: 1.3em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .insight-box p, .warning-box p, .success-box p {
        font-size: 1.1em;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    .sidebar .sidebar-content {
        font-family: 'Sarabun', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 1rem;
    }
    
    /* Sidebar background - much darker */
    .css-1d391kg {
        background-color: rgba(20, 25, 35, 1.0) !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.3);
    }
    
    .sidebar .sidebar-content {
        background-color: rgba(20, 25, 35, 1.0) !important;
        color: white !important;
    }
    
    .css-1cypcdb {
        background-color: rgba(20, 25, 35, 1.0) !important;
    }
    
    .css-17eq0hr {
        background-color: rgba(20, 25, 35, 1.0) !important;
        color: white !important;
    }
    
    /* Main sidebar container */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 25, 35, 1.0) !important;
        border-right: 2px solid rgba(100, 120, 150, 0.3);
    }
    
    [data-testid="stSidebar"] > div {
        background-color: rgba(20, 25, 35, 1.0) !important;
    }
    
    /* Sidebar elements styling */
    [data-testid="stSidebar"] .element-container {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(40, 50, 65, 0.9) !important;
        border: 2px solid rgba(78, 205, 196, 0.6) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]:hover {
        border-color: rgba(78, 205, 196, 1.0) !important;
        box-shadow: 0 0 15px rgba(78, 205, 196, 0.4) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        color: white !important;
        font-weight: 500 !important;
        background-color: rgba(40, 50, 65, 0.9) !important;
    }
    
    /* Dropdown menu styling */
    [data-testid="stSidebar"] .stSelectbox div[role="listbox"] {
        background-color: rgba(20, 25, 35, 0.98) !important;
        border: 2px solid rgba(78, 205, 196, 0.6) !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[role="option"] {
        background-color: rgba(40, 50, 65, 0.9) !important;
        color: white !important;
        border-bottom: 1px solid rgba(78, 205, 196, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[role="option"]:hover {
        background-color: rgba(78, 205, 196, 0.3) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[role="option"][aria-selected="true"] {
        background-color: rgba(78, 205, 196, 0.5) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #E8F4F8 !important;
        font-size: 0.95em !important;
        line-height: 1.5 !important;
        background-color: rgba(78, 205, 196, 0.15) !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        border-left: 3px solid #4ECDC4 !important;
        margin: 8px 0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #4ECDC4 !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #4ECDC4 !important;
        text-shadow: 0 0 15px rgba(78, 205, 196, 0.5);
        text-align: center !important;
        padding: 20px 0 !important;
        border-bottom: 2px solid rgba(78, 205, 196, 0.3) !important;
        margin-bottom: 20px !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #45B7D1 !important;
        margin-top: 20px !important;
        text-shadow: 0 0 8px rgba(69, 183, 209, 0.4);
    }
    
    [data-testid="stSidebar"] .metric {
        background-color: rgba(78, 205, 196, 0.2) !important;
        border: 2px solid rgba(78, 205, 196, 0.5) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .metric-value {
        color: #4ECDC4 !important;
        font-weight: 800 !important;
        font-size: 1.8em !important;
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.6) !important;
    }
    
    [data-testid="stSidebar"] .metric-label {
        color: #E8F4F8 !important;
        font-weight: 600 !important;
        font-size: 1em !important;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(40, 50, 65, 0.9) !important;
        border-radius: 10px;
        color: white !important;
    }
    
    /* Global dropdown styling */
    div[data-baseweb="popover"] {
        background-color: rgba(20, 25, 35, 0.98) !important;
        border: 2px solid rgba(78, 205, 196, 0.6) !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
    
    div[data-baseweb="menu"] {
        background-color: rgba(20, 25, 35, 0.98) !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="menu"] li {
        background-color: rgba(40, 50, 65, 0.9) !important;
        color: white !important;
        border-bottom: 1px solid rgba(78, 205, 196, 0.2) !important;
    }
    
    div[data-baseweb="menu"] li:hover {
        background-color: rgba(78, 205, 196, 0.3) !important;
        color: white !important;
    }
    
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    h1, h2, h3 {
        color: #2d3436;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .plotly-graph-div {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }
    
    /* Fix any remaining white backgrounds */
    [data-testid="stSidebar"] * {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] > div {
        background-color: rgba(40, 50, 65, 0.9) !important;
    }
    
    /* Force dropdown elements to use dark theme */
    .stSelectbox [data-baseweb="select"] {
        background-color: rgba(40, 50, 65, 0.9) !important;
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] * {
        background-color: rgba(40, 50, 65, 0.9) !important;
        color: white !important;
    }
    
    /* Universal fix for white backgrounds in sidebar */
    [data-testid="stSidebar"] .st-emotion-cache-1ww9g20,
    [data-testid="stSidebar"] .st-emotion-cache-1y4p8pa,
    [data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
        background-color: rgba(40, 50, 65, 0.9) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Load and process data
@st.cache_data
def load_data():
    """Load and process the survey data"""
    try:
        df = pd.read_csv("data/data_renamefinal.csv")
        
        # Clean data similar to notebook
        df = df.dropna(subset=["gender", "age", "monthly_income"]).reset_index(drop=True)
        df["age"] = df["age"].astype(int)
        
                # Income midpoint calculation
        def income_to_midpoint(x):
            if pd.isna(x):
                return np.nan
            nums = list(map(int, re.findall(r"\d+", str(x).replace(",", ""))))
            return np.mean(nums) if nums else np.nan

        df["income_mid"] = df["monthly_income"].apply(income_to_midpoint)
        
        # Price range processing
        def price_range_to_midpoint(x):
            if pd.isna(x):
                return np.nan
            nums = list(map(int, re.findall(r"\d+", str(x).replace(",", ""))))
            if len(nums) >= 2:
                return np.mean(nums)
            elif len(nums) == 1:
                return nums[0]
            else:
                return np.nan
        
        if 'preferred_price_range ' in df.columns:
            df["price_midpoint"] = df["preferred_price_range "].apply(price_range_to_midpoint)
        elif 'preferred_price_range' in df.columns:
            df["price_midpoint"] = df["preferred_price_range"].apply(price_range_to_midpoint)
        
        # Fill missing values for Likert scale columns
        likert_cols = [c for c in df.columns if re.match(r"(factor|price|channel|promo)_", c)]
        for col in likert_cols:
            df[col] = df[col].fillna(df[col].median())
        
        # Create age and income groups
        df["age_group"] = pd.cut(
            df["age"], bins=[0,17,24,34,44,150],
            labels=["<18","18-24","25-34","35-44","45+"]
        )
        df["income_group"] = pd.cut(
            df["income_mid"], bins=[0,15000,30000,50000,1e9],
            labels=["<15k","15-30k","30-50k","50k+"]
        )
        
        # Remove rows with NaN income_group (high income groups with no data)
        df = df.dropna(subset=['income_group']).reset_index(drop=True)
        
        return df
        
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ข้อมูล กรุณาตรวจสอบ path ของไฟล์")
        return None

# Data processing functions
def normalize_th(text):
    """Normalize Thai text"""
    if pd.isna(text):
        return text
    text = unicodedata.normalize("NFKC", str(text))
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

def explode_multiselect(series, sep_pattern=r"[;,/|]", clean_func=None):
    """Explode multi-select columns"""
    exploded = (
        series.fillna("")
              .astype(str)
              .str.replace(r"[\[\]\']", "", regex=True)
              .str.replace(sep_pattern, ",", regex=True)
              .str.split(",")
              .explode()
              .str.strip()
              .replace("", pd.NA)
              .dropna()
    )
    if clean_func:
        exploded = exploded.apply(clean_func)
    return exploded.to_frame(name="value")

def main():
    st.title("Suitcase Insights Dashboard")
    st.markdown("### การวิเคราะห์ข้อมูลการสำรวจพฤติกรรมผู้บริโภคกระเป๋าเดินทาง")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "เลือกหน้าที่ต้องการดู",
        ["ภาพรวม", "ข้อมูลประชากรศาสตร์", "ปัจจัยการตัดสินใจ", 
         "ความต้องการผลิตภัณฑ์", "ความอ่อนไหวต่อราคา", "ช่องทางการขาย",
         "การตลาด", "Brand Awareness", "Brand Image & Barriers",
         "Customer Personas"]
    )
    
    # Display metrics in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ข้อมูลพื้นฐาน")
    
    # Enhanced metrics with better styling
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.2), rgba(69, 183, 209, 0.2)); 
                padding: 15px; border-radius: 12px; margin: 10px 0; 
                border: 2px solid rgba(78, 205, 196, 0.4);
                box-shadow: 0 4px 15px rgba(78, 205, 196, 0.2);">
        <h4 style="color: #4ECDC4; margin-bottom: 10px; text-align: center;">ผู้เข้าร่วม</h4>
        <h2 style="color: #E8F4F8; text-align: center; margin: 0; 
                   text-shadow: 0 0 10px rgba(78, 205, 196, 0.6);">{len(df)} คน</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(69, 183, 209, 0.2), rgba(102, 126, 234, 0.2)); 
                padding: 15px; border-radius: 12px; margin: 10px 0; 
                border: 2px solid rgba(69, 183, 209, 0.4);
                box-shadow: 0 4px 15px rgba(69, 183, 209, 0.2);">
        <h4 style="color: #45B7D1; margin-bottom: 10px; text-align: center;">จำนวนคำถาม</h4>
        <h2 style="color: #E8F4F8; text-align: center; margin: 0; 
                   text-shadow: 0 0 10px rgba(69, 183, 209, 0.6);">{len(df.columns)} ข้อ</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Gender distribution with enhanced styling
    gender_dist = df['gender'].value_counts()
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255, 107, 157, 0.2), rgba(78, 205, 196, 0.2)); 
                padding: 15px; border-radius: 12px; margin: 10px 0; 
                border: 2px solid rgba(255, 107, 157, 0.4);
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.2);">
        <h4 style="color: #FF6B9D; margin-bottom: 10px; text-align: center;">การกระจายเพศ</h4>
        <p style="color: #E8F4F8; text-align: center; margin: 5px 0; font-size: 1.1em;">
            <strong style="color: #FF6B9D;">หญิง:</strong> {gender_dist.get('หญิง', 0)} คน<br>
            <strong style="color: #4ECDC4;">ชาย:</strong> {gender_dist.get('ชาย', 0)} คน
        </p>
        {f'<p style="color: #E8F4F8; text-align: center; margin: 5px 0; font-size: 1.1em;"><strong style="color: #45B7D1;">LGBTQ+:</strong> {gender_dist.get("LGBTQ+", 0)} คน</p>' if 'LGBTQ+' in gender_dist.index else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Age range with enhanced styling
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)); 
                padding: 15px; border-radius: 12px; margin: 10px 0; 
                border: 2px solid rgba(102, 126, 234, 0.4);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);">
        <h4 style="color: #667eea; margin-bottom: 10px; text-align: center;">ช่วงอายุ</h4>
        <h3 style="color: #E8F4F8; text-align: center; margin: 0; 
                   text-shadow: 0 0 8px rgba(102, 126, 234, 0.6);">{df['age'].min()}-{df['age'].max()} ปี</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content based on selected page
    if page == "ภาพรวม":
        show_overview(df)
    elif page == "ข้อมูลประชากรศาสตร์":
        show_demographics(df)
    elif page == "ปัจจัยการตัดสินใจ":
        show_factors(df)
    elif page == "ความต้องการผลิตภัณฑ์":
        show_products(df)
    elif page == "ความอ่อนไหวต่อราคา":
        show_pricing(df)
    elif page == "ช่องทางการขาย":
        show_channels(df)
    elif page == "การตลาด":
        show_marketing(df)
    elif page == "Brand Awareness":
        show_brand_awareness(df)
    elif page == "Brand Image & Barriers":
        show_brand_image(df)
    elif page == "Customer Personas":
        show_personas(df)

def show_overview(df):
    """Show overview page"""
    st.header("ภาพรวมผลการสำรวจ")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3> ผู้เข้าร่วม</h3>
            <h2>{}</h2>
            <p>คน</p>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        avg_age = df['age'].mean()
        st.markdown("""
        <div class="metric-card">
            <h3> อายุเฉลี่ย</h3>
            <h2>{:.1f}</h2>
            <p>ปี</p>
        </div>
        """.format(avg_age), unsafe_allow_html=True)
    
    with col3:
        gender_counts = df['gender'].value_counts()
        female_count = gender_counts.get('หญิง', 0)
        st.markdown("""
        <div class="metric-card">
            <h3> เพศหญิง</h3>
            <h2>{}</h2>
            <p>คน ({:.1f}%)</p>
        </div>
        """.format(female_count, (female_count/len(df)*100)), unsafe_allow_html=True)
    
    with col4:
        student_pct = (df['occupation'] == 'นักเรียน/นักศึกษา').mean() * 100
        st.markdown("""
        <div class="metric-card">
            <h3> นักเรียน/นักศึกษา</h3>
            <h2>{:.1f}%</h2>
            <p>ของผู้ตอบ</p>
        </div>
        """.format(student_pct), unsafe_allow_html=True)
    
    # Gender breakdown section
    st.markdown("---")
    st.subheader(" การกระจายตามเพศ")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        gender_counts = df['gender'].value_counts()
        
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="สัดส่วนเพศของผู้ตอบแบบสำรวจ",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1']
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        st.markdown("**จำนวนตามเพศ:**")
        for gender, count in gender_counts.items():
            percentage = (count / len(df)) * 100
            st.markdown(f"- **{gender}**: {count} คน ({percentage:.1f}%)")
    
    # Key insights
    st.markdown("---")
    st.subheader(" ข้อค้นพบสำคัญ")
    
    # Factor analysis
    factor_cols = [c for c in df.columns if c.startswith("factor_")]
    if factor_cols:
        factor_means = df[factor_cols].mean().sort_values(ascending=False)
        top_factor = factor_means.index[0].replace("factor_", "").replace("_", " ")
        
        st.markdown(f"""
        <div class="insight-box">
            <h4> ปัจจัยสำคัญที่สุด</h4>
            <p><strong>{top_factor}</strong> ได้คะแนนเฉลี่ย {factor_means.iloc[0]:.2f} จาก 5</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Price sensitivity
    if 'preferred_price_range' in df.columns:
        popular_price = df['preferred_price_range'].mode().iloc[0] if not df['preferred_price_range'].mode().empty else "ไม่ระบุ"
        st.markdown(f"""
        <div class="insight-box">
            <h4> ช่วงราคาที่นิยม</h4>
            <p><strong>{popular_price}</strong> เป็นช่วงราคาที่ผู้ตอบแบบสำรวจเลือกมากที่สุด</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Travel frequency
    if 'luggage_frequency' in df.columns:
        popular_freq = df['luggage_frequency'].mode().iloc[0] if not df['luggage_frequency'].mode().empty else "ไม่ระบุ"
        st.markdown(f"""
        <div class="insight-box">
            <h4> ความถี่ในการเดินทาง</h4>
            <p><strong>{popular_freq}</strong> เป็นความถี่ที่พบมากที่สุด</p>
        </div>
        """, unsafe_allow_html=True)

def show_demographics(df):
    """Show demographics analysis"""
    st.header(" ข้อมูลประชากรศาสตร์")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        st.subheader(" การกระจายตามเพศ")
        gender_counts = df['gender'].value_counts()
        
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="สัดส่วนเพศของผู้ตอบแบบสำรวจ",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)
        
        # Gender details table
        st.markdown("**รายละเอียดการกระจายตามเพศ:**")
        gender_df = pd.DataFrame({
            'เพศ': gender_counts.index,
            'จำนวน (คน)': gender_counts.values,
            'สัดส่วน (%)': [f"{(count/len(df)*100):.1f}%" for count in gender_counts.values]
        })
        st.dataframe(gender_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Age distribution
        st.subheader(" การกระจายตามอายุ")
        age_counts = df['age_group'].value_counts().sort_index()
        
        fig_age = px.bar(
            x=age_counts.index,
            y=age_counts.values,
            title="จำนวนผู้ตอบแบบสำรวจตามช่วงอายุ",
            labels={'x': 'ช่วงอายุ', 'y': 'จำนวนคน'},
            color=age_counts.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    # Income and occupation
    col3, col4 = st.columns(2)
    
    with col3:
        # Income distribution
        st.subheader(" การกระจายตามรายได้")
        income_counts = df['income_group'].value_counts().sort_index()
        
        fig_income = px.bar(
            x=income_counts.index,
            y=income_counts.values,
            title="จำนวนผู้ตอบแบบสำรวจตามช่วงรายได้",
            labels={'x': 'ช่วงรายได้ (บาท)', 'y': 'จำนวนคน'},
            color=income_counts.values,
            color_continuous_scale='plasma'
        )
        st.plotly_chart(fig_income, use_container_width=True)
    
    with col4:
        # Occupation distribution
        st.subheader("การกระจายตามอาชีพ")
        occupation_counts = df['occupation'].value_counts().head(10)
        
        fig_occupation = px.bar(
            x=occupation_counts.values,
            y=occupation_counts.index,
            orientation='h',
            title="อาชีพของผู้ตอบแบบสำรวจ (Top 10)",
            labels={'x': 'จำนวนคน', 'y': 'อาชีพ'},
            color=occupation_counts.values,
            color_continuous_scale='turbo'
        )
        st.plotly_chart(fig_occupation, use_container_width=True)

def show_factors(df):
    """Show importance factors analysis"""
    st.header(" ปัจจัยการตัดสินใจซื้อกระเป๋าเดินทาง")
    
    factor_cols = [c for c in df.columns if c.startswith("factor_")]
    
    if not factor_cols:
        st.warning("ไม่พบข้อมูลปัจจัยการตัดสินใจ")
        return
    
    # Overall importance ranking
    st.subheader(" ลำดับความสำคัญของปัจจัยโดยรวม")
    
    factor_means = df[factor_cols].mean().sort_values(ascending=False)
    factor_names = [col.replace("factor_", "").replace("_", " ").title() for col in factor_means.index]
    
    fig_factors = px.bar(
        x=factor_means.values,
        y=factor_names,
        orientation='h',
        title="คะแนนเฉลี่ยความสำคัญของปัจจัยต่างๆ (1-5)",
        labels={'x': 'คะแนนเฉลี่ย', 'y': 'ปัจจัย'},
        color=factor_means.values,
        color_continuous_scale='RdYlGn'
    )
    fig_factors.update_layout(height=600)
    st.plotly_chart(fig_factors, use_container_width=True)
    
    # Factors by demographics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" ปัจจัยความสำคัญตามเพศ")
        gender_factors = df.groupby('gender')[factor_cols].mean()
        
        fig_gender_factors = px.imshow(
            gender_factors.T,
            title="Heatmap: ความสำคัญของปัจจัยตามเพศ",
            labels=dict(x="เพศ", y="ปัจจัย", color="คะแนนเฉลี่ย"),
            aspect="auto",
            color_continuous_scale='RdYlBu_r'
        )
        st.plotly_chart(fig_gender_factors, use_container_width=True)
    
    with col2:
        st.subheader(" ปัจจัยความสำคัญตามรายได้")
        if 'income_group' in df.columns:
            income_factors = df.groupby('income_group', observed=False)[factor_cols].mean()
            
            fig_income_factors = px.imshow(
                income_factors.T,
                title="Heatmap: ความสำคัญของปัจจัยตามรายได้",
                labels=dict(x="กลุ่มรายได้", y="ปัจจัย", color="คะแนนเฉลี่ย"),
                aspect="auto",
                color_continuous_scale='RdYlBu_r'
            )
            st.plotly_chart(fig_income_factors, use_container_width=True)

def show_products(df):
    """Show product preferences analysis"""
    st.header(" ความต้องการด้านผลิตภัณฑ์")
    
    col1, col2 = st.columns(2)
    
    # Style preferences
    if 'preferred_styles' in df.columns:
        with col1:
            st.subheader(" สไตล์/สีที่ต้องการ")
            
            style_long = explode_multiselect(df['preferred_styles'], clean_func=normalize_th)
            style_counts = style_long['value'].value_counts().head(10)
            
            fig_styles = px.bar(
                x=style_counts.values,
                y=style_counts.index,
                orientation='h',
                title="สไตล์/สีที่ได้รับความนิยม (Top 10)",
                labels={'x': 'จำนวนครั้งที่เลือก', 'y': 'สไตล์/สี'},
                color=style_counts.values,
                color_continuous_scale='sunset'
            )
            st.plotly_chart(fig_styles, use_container_width=True)
    
    # Bag types
    if 'used_bag_types' in df.columns:
        with col2:
            st.subheader(" ประเภทกระเป๋าที่ใช้")
            
            bag_long = explode_multiselect(df['used_bag_types'], clean_func=normalize_th)
            bag_counts = bag_long['value'].value_counts().head(8)
            
            fig_bags = px.pie(
                values=bag_counts.values,
                names=bag_counts.index,
                title="ประเภทกระเป๋าที่ใช้บ่อย",
                color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            )
            st.plotly_chart(fig_bags, use_container_width=True)
    
    # Size preferences
    if 'luggage_size_short_trip' in df.columns:
        st.subheader(" ขนาดกระเป๋าที่ต้องการ")
        
        size_counts = df['luggage_size_short_trip'].value_counts()
        
        fig_sizes = px.bar(
            x=size_counts.index,
            y=size_counts.values,
            title="ขนาดกระเป๋าที่นิยมสำหรับการเดินทางระยะสั้น",
            labels={'x': 'ขนาด (นิ้ว)', 'y': 'จำนวนคน'},
            color=size_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_sizes, use_container_width=True)

def show_pricing(df):
    """Show price sensitivity analysis"""
    st.header(" ความอ่อนไหวต่อราคา")
    
    # Price range preferences
    price_col = 'preferred_price_range ' if 'preferred_price_range ' in df.columns else 'preferred_price_range'
    if price_col in df.columns:
        st.subheader(" ช่วงราคาที่ต้องการ")
        
        price_counts = df[price_col].value_counts()
        
        fig_price = px.bar(
            x=price_counts.index,
            y=price_counts.values,
            title="ช่วงราคาที่ผู้บริโภคต้องการ",
            labels={'x': 'ช่วงราคา', 'y': 'จำนวนคน'}
        )
        fig_price.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_price, use_container_width=True)
    
    # Price factors analysis (Likert scale factors only)
    price_factor_cols = [c for c in df.columns if c.startswith("price_") and c not in ['price_midpoint', 'price_min', 'price_max', 'price_mid']]
    
    if price_factor_cols:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" ปัจจัยด้านราคา")
            
            price_means = df[price_factor_cols].mean().sort_values(ascending=False)
            
            # Create Thai names for price factors
            factor_name_mapping = {
                'price_within_budget': 'อยู่ในงบประมาณ',
                'price_value_for_quality': 'คุ้มค่าต่อคุณภาพ', 
                'price_vs_competitor': 'เทียบกับคู่แข่ง',
                'price_image_boost': 'เพิ่มภาพลักษณ์'
            }
            
            price_names = [factor_name_mapping.get(col, col.replace("price_", "").replace("_", " ").title()) for col in price_means.index]
            
            fig_price_factors = px.bar(
                x=price_means.values,
                y=price_names,
                orientation='h',
                title="ความสำคัญของปัจจัยด้านราคา (คะแนน 1-5)",
                labels={'x': 'คะแนนเฉลี่ย', 'y': 'ปัจจัยด้านราคา'},
                color=price_means.values,
                color_continuous_scale='Blues'
            )
            fig_price_factors.update_layout(
                xaxis=dict(range=[1, 5]),  # Set range for Likert scale
                height=400
            )
            st.plotly_chart(fig_price_factors, use_container_width=True)
        
        with col2:
            st.subheader(" ราคา vs รายได้")
            
            price_col = 'preferred_price_range ' if 'preferred_price_range ' in df.columns else 'preferred_price_range'
            if 'income_group' in df.columns and price_col in df.columns:
                # Clean data first - remove NaN income groups
                clean_df = df.dropna(subset=['income_group', price_col])
                
                if len(clean_df) > 0:
                    # Cross-tabulation
                    price_income = pd.crosstab(clean_df['income_group'], clean_df[price_col])
                    
                    # Only proceed if we have data
                    if not price_income.empty and price_income.sum().sum() > 0:
                        fig_price_income = px.imshow(
                            price_income.values,
                            x=price_income.columns,
                            y=price_income.index,
                            title="ความสัมพันธ์ระหว่างรายได้กับช่วงราคาที่ต้องการ",
                            labels=dict(x="ช่วงราคา", y="กลุ่มรายได้", color="จำนวนคน"),
                            color_continuous_scale='Blues'
                        )
                        fig_price_income.update_layout(
                            xaxis={'side': 'bottom'},
                            height=400
                        )
                        st.plotly_chart(fig_price_income, use_container_width=True)
                        
                        # Add summary table
                        st.markdown("**ตารางสรุป:**")
                        summary_df = price_income.reset_index()
                        st.dataframe(summary_df, use_container_width=True)
                    else:
                        # Alternative visualization using existing price_midpoint column
                        st.markdown("**การวิเคราะห์ราคาเฉลี่ยที่ต้องการตามรายได้**")
                        
                        # Use the price_midpoint column that was created during data loading
                        if 'price_midpoint' in clean_df.columns:
                            # Remove NaN price midpoints
                            price_df = clean_df.dropna(subset=['price_midpoint'])
                            
                            if len(price_df) > 0:
                                # Calculate statistics by income group
                                income_stats = price_df.groupby('income_group').agg({
                                    'price_midpoint': ['mean', 'median', 'count'],
                                    price_col: lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'ไม่มีข้อมูล'
                                }).round(0)
                                
                                # Flatten column names
                                income_stats.columns = ['ราคาเฉลี่ย', 'ราคากลาง', 'จำนวนคน', 'ช่วงราคาที่นิยม']
                                
                                # Create bar chart
                                fig_price_avg = px.bar(
                                    x=income_stats.index,
                                    y=income_stats['ราคาเฉลี่ย'],
                                    title="ราคาเฉลี่ยที่ต้องการตามกลุ่มรายได้",
                                    labels={'x': 'กลุ่มรายได้', 'y': 'ราคาเฉลี่ย (บาท)'},
                                    color=income_stats['ราคาเฉลี่ย'],
                                    color_continuous_scale='Viridis',
                                    text=income_stats['ราคาเฉลี่ย']
                                )
                                fig_price_avg.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                                fig_price_avg.update_layout(height=400)
                                st.plotly_chart(fig_price_avg, use_container_width=True)
                                
                                # Display summary table
                                st.markdown("**ตารางสรุป:**")
                                display_stats = income_stats.copy()
                                display_stats['ราคาเฉลี่ย'] = display_stats['ราคาเฉลี่ย'].apply(lambda x: f"{x:,.0f} บาท")
                                display_stats['ราคากลาง'] = display_stats['ราคากลาง'].apply(lambda x: f"{x:,.0f} บาท")
                                st.dataframe(display_stats, use_container_width=True)
                            else:
                                st.warning("ไม่มีข้อมูลราคาที่สามารถประมวลผลได้")
                        else:
                            st.warning("ไม่พบข้อมูลราคา - กรุณาตรวจสอบการโหลดข้อมูล")
                else:
                    st.warning("ไม่มีข้อมูลเพียงพอสำหรับการวิเคราะห์ราคา vs รายได้")

def show_channels(df):
    """Show sales channels analysis"""
    st.header(" ช่องทางการขาย")
    
    # Platform usage
    if 'most_used_platform' in df.columns:
        st.subheader(" แพลตฟอร์มที่ใช้มากที่สุด")
        
        platform_counts = df['most_used_platform'].value_counts().head(10)
        
        fig_platforms = px.pie(
            values=platform_counts.values,
            names=platform_counts.index,
            title="แพลตฟอร์มที่ผู้บริโภคใช้มากที่สุด",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF7675', '#A29BFE']
        )
        st.plotly_chart(fig_platforms, use_container_width=True)
    
    # Purchase channels
    if 'purchase_channels' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛒 ช่องทางการซื้อ")
            
            channel_long = explode_multiselect(df['purchase_channels'], clean_func=normalize_th)
            channel_counts = channel_long['value'].value_counts().head(10)
            
            fig_channels = px.bar(
                x=channel_counts.values,
                y=channel_counts.index,
                orientation='h',
                title="ช่องทางการซื้อที่นิยม",
                labels={'x': 'จำนวนครั้งที่เลือก', 'y': 'ช่องทางการซื้อ'}
            )
            st.plotly_chart(fig_channels, use_container_width=True)
        
        with col2:
            # Channel preferences by age
            st.subheader(" ช่องทางการซื้อตามอายุ")
            
            if 'age_group' in df.columns:
                # สร้าง cross-tabulation แบบง่าย
                age_channel_data = []
                for age_grp in df['age_group'].cat.categories:
                    age_subset = df[df['age_group'] == age_grp]
                    if len(age_subset) > 0:
                        # เอาช่องทางที่นิยมที่สุดในแต่ละกลุ่มอายุ
                        top_channels = age_subset['most_used_platform'].value_counts().head(3)
                        for channel, count in top_channels.items():
                            age_channel_data.append({
                                'age_group': age_grp,
                                'channel': channel,
                                'count': count
                            })
                
                if age_channel_data:
                    age_channel_df = pd.DataFrame(age_channel_data)
                    
                    fig_age_channel = px.bar(
                        age_channel_df,
                        x='age_group',
                        y='count',
                        color='channel',
                        title="ช่องทางที่นิยมตามกลุ่มอายุ",
                        labels={'x': 'กลุ่มอายุ', 'y': 'จำนวนคน', 'color': 'ช่องทาง'}
                    )
                    st.plotly_chart(fig_age_channel, use_container_width=True)

def show_marketing(df):
    """Show marketing preferences analysis"""
    st.header(" Marketing Preferences")
    
    # Promotion preferences
    promo_cols = [c for c in df.columns if c.startswith("promo_")]
    
    if promo_cols:
        st.subheader(" ประสิทธิภาพของโปรโมชั่นแต่ละประเภท")
        
        # Calculate average scores for each promotion type
        promo_means = df[promo_cols].mean().sort_values(ascending=False)
        promo_names = [col.replace("promo_", "").replace("_", " ").title() for col in promo_means.index]
        
        # Create insights based on scores
        col1, col2 = st.columns(2)
        
        with col1:
            fig_promo = px.bar(
                x=promo_means.values,
                y=promo_names,
                orientation='h',
                title="คะแนนเฉลี่ยประสิทธิภาพโปรโมชั่น (1-5)",
                labels={'x': 'คะแนนเฉลี่ย', 'y': 'ประเภทโปรโมชั่น'},
                color=promo_means.values,
                color_continuous_scale='RdYlGn'
            )
            fig_promo.update_layout(height=400)
            st.plotly_chart(fig_promo, use_container_width=True)
        
        with col2:
            # Key insights
            top_promo = promo_names[0]
            top_score = promo_means.iloc[0]
            worst_promo = promo_names[-1]  
            worst_score = promo_means.iloc[-1]
            
            st.markdown(f"""
            <div class="insight-box">
                <h4> โปรโมชั่นที่ได้ผลที่สุด</h4>
                <p><strong>{top_promo}</strong><br>คะแนนเฉลี่ย: {top_score:.2f}/5</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="warning-box">
                <h4> โปรโมชั่นที่ได้ผลต่ำสุด</h4>
                <p><strong>{worst_promo}</strong><br>คะแนนเฉลี่ย: {worst_score:.2f}/5</p>
                <small>ควรพิจารณาปรับกลยุทธ์หรือลดการลงทุน</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Presenter preferences
    if 'preferred_presenter' in df.columns:
        st.subheader(" พรีเซนเตอร์ที่ต้องการ")
        
        presenter_counts = df['preferred_presenter'].value_counts().head(10)
        presenter_counts = presenter_counts[presenter_counts.index != '-']  # Remove empty values
        
        if len(presenter_counts) > 0:
            fig_presenter = px.bar(
                x=presenter_counts.values,
                y=presenter_counts.index,
                orientation='h',
                title="พรีเซนเตอร์ที่ได้รับความนิยม",
                labels={'x': 'จำนวนครั้งที่เลือก', 'y': 'พรีเซนเตอร์'}
            )
            st.plotly_chart(fig_presenter, use_container_width=True)

def show_brand_awareness(df):
    """Show T.Partner brand awareness analysis"""
    st.header(" Brand Awareness - T.Partner")
    
    # Brand recognition level
    if 'know_tpartner' in df.columns:
        st.subheader(" ระดับการรู้จักแบรนด์ T.Partner")
        
        awareness_counts = df['know_tpartner'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_awareness = px.pie(
                values=awareness_counts.values,
                names=awareness_counts.index,
                title="สัดส่วนการรู้จักแบรนด์ T.Partner"
            )
            st.plotly_chart(fig_awareness, use_container_width=True)
        
        with col2:
            # Calculate key metrics
            total_respondents = len(df)
            know_brand = (df['know_tpartner'] == 'รู้จัก และรู้ว่าเป็นแบรนด์กระเป๋าเดินทาง').sum()
            seen_before = (df['know_tpartner'] == 'เคยเห็นผ่านตา แต่ไม่แน่ใจว่าแบรนด์ทำอะไร').sum()
            never_heard = (df['know_tpartner'] == 'ไม่รู้จักมาก่อนเลย').sum()
            
            st.markdown(f"""
            <div class="metric-card">
                <h4> Brand Recognition Metrics</h4>
                <p><strong>รู้จักแบรนด์:</strong> {know_brand} คน ({know_brand/total_respondents*100:.1f}%)</p>
                <p><strong>เคยเห็นผ่านตา:</strong> {seen_before} คน ({seen_before/total_respondents*100:.1f}%)</p>
                <p><strong>ไม่รู้จักเลย:</strong> {never_heard} คน ({never_heard/total_respondents*100:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)
    
    # First channel awareness
    if 'tpartner_first_channel' in df.columns:
        st.subheader("📡 ช่องทางที่รู้จักแบรนด์ครั้งแรก")
        
        # Filter out non-responses
        first_channel_data = df[df['tpartner_first_channel'].notna() & 
                                (df['tpartner_first_channel'] != '') & 
                                (df['tpartner_first_channel'] != '-')]
        
        if len(first_channel_data) > 0:
            channel_counts = first_channel_data['tpartner_first_channel'].value_counts().head(10)
            
            fig_channels = px.bar(
                x=channel_counts.index,
                y=channel_counts.values,
                title="ช่องทางที่ทำให้รู้จักแบรนด์ T.Partner ครั้งแรก",
                labels={'x': 'ช่องทาง', 'y': 'จำนวนคน'}
            )
            fig_channels.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_channels, use_container_width=True)
            
            # Key insight
            top_channel = channel_counts.index[0]
            top_count = channel_counts.iloc[0]
            total_responses = len(first_channel_data)
            
            st.markdown(f"""
            <div class="insight-box">
                <h4> ช่องทางหลักในการสร้าง Brand Awareness</h4>
                <p><strong>{top_channel}</strong> เป็นช่องทางที่ทำให้คนรู้จักแบรนด์มากที่สุด</p>
                <p>คิดเป็น {top_count} คนจาก {total_responses} คนที่ตอบ ({top_count/total_responses*100:.1f}%)</p>
                <p><small> ควรเพิ่มการลงทุนในช่องทางนี้เพื่อเพิ่ม brand awareness</small></p>
            </div>
            """, unsafe_allow_html=True)

def show_brand_image(df):
    """Show brand image and barriers to purchase analysis"""
    st.header(" Brand Image & Barriers to Purchase")
    
    # Brand positioning perception
    if 'tpartner_positioning' in df.columns:
        st.subheader(" การรับรู้ positioning ของแบรนด์")
        
        positioning_data = df[df['tpartner_positioning'].notna() & 
                             (df['tpartner_positioning'] != '') & 
                             (df['tpartner_positioning'] != '-')]
        
        if len(positioning_data) > 0:
            positioning_counts = positioning_data['tpartner_positioning'].value_counts().head(8)
            
            fig_positioning = px.bar(
                x=positioning_counts.values,
                y=positioning_counts.index,
                orientation='h',
                title="การรับรู้ positioning ของ T.Partner",
                labels={'x': 'จำนวนคน', 'y': 'Positioning'}
            )
            st.plotly_chart(fig_positioning, use_container_width=True)
    
    # First impression analysis
    col1, col2 = st.columns(2)
    
    with col1:
        if 'first_impression' in df.columns:
            st.subheader(" First Impression")
            
            impression_data = df[df['first_impression'].notna() & 
                               (df['first_impression'] != '') & 
                               (df['first_impression'] != '-')]
            
            if len(impression_data) > 0:
                # Simple sentiment analysis based on keywords
                positive_keywords = ['ดี', 'สวย', 'น่าสนใจ', 'ชอบ', 'ทันสมัย', 'หรู', 'คุณภาพ']
                neutral_keywords = ['เรียบ', 'ธรรมดา', 'ปกติ', 'กลางๆ']
                negative_keywords = ['ไม่', 'แพง', 'เก่า', 'น่าเบื่อ']
                
                def classify_sentiment(text):
                    if pd.isna(text):
                        return 'ไม่ระบุ'
                    text = str(text).lower()
                    
                    positive_score = sum(1 for word in positive_keywords if word in text)
                    negative_score = sum(1 for word in negative_keywords if word in text)
                    
                    if positive_score > negative_score:
                        return 'เชิงบวก'
                    elif negative_score > positive_score:
                        return 'เชิงลบ'
                    else:
                        return 'กลางๆ'
                
                impression_data = impression_data.copy()
                impression_data['sentiment'] = impression_data['first_impression'].apply(classify_sentiment)
                sentiment_counts = impression_data['sentiment'].value_counts()
                
                fig_sentiment = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="อารมณ์ของ First Impression",
                    color_discrete_map={
                        'เชิงบวก': '#28a745',
                        'กลางๆ': '#ffc107', 
                        'เชิงลบ': '#dc3545'
                    }
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        if 'considered_tpartner' in df.columns:
            st.subheader(" เคยพิจารณาซื้อ T.Partner หรือไม่")
            
            considered_counts = df['considered_tpartner'].value_counts()
            
            fig_considered = px.pie(
                values=considered_counts.values,
                names=considered_counts.index,
                title="การพิจารณาซื้อแบรนด์ T.Partner"
            )
            st.plotly_chart(fig_considered, use_container_width=True)
    
    # Barriers to purchase
    if 'reason_not_chosen' in df.columns:
        st.subheader(" เหตุผลที่ยังไม่ซื้อ / Barriers to Purchase")
        
        barrier_data = df[df['reason_not_chosen'].notna() & 
                         (df['reason_not_chosen'] != '') & 
                         (df['reason_not_chosen'] != '-')]
        
        if len(barrier_data) > 0:
            # Count common barriers
            barrier_counts = barrier_data['reason_not_chosen'].value_counts().head(10)
            
            fig_barriers = px.bar(
                x=barrier_counts.values,
                y=barrier_counts.index,
                orientation='h',
                title="เหตุผลที่ยังไม่ได้เลือกซื้อ T.Partner",
                labels={'x': 'จำนวนคน', 'y': 'เหตุผล'},
                color=barrier_counts.values,
                color_continuous_scale='Reds'
            )
            fig_barriers.update_layout(height=500)
            st.plotly_chart(fig_barriers, use_container_width=True)
            
            # Key insights
            top_barrier = barrier_counts.index[0]
            top_barrier_count = barrier_counts.iloc[0]
            total_barriers = len(barrier_data)
            
            st.markdown(f"""
            <div class="warning-box">
                <h4> อุปสรรคหลักในการซื้อ</h4>
                <p><strong>"{top_barrier}"</strong></p>
                <p>{top_barrier_count} คนจาก {total_barriers} คนที่ให้เหตุผล ({top_barrier_count/total_barriers*100:.1f}%)</p>
                <p><small> นี่คือประเด็นที่แบรนด์ควรแก้ไขเป็นอันดับแรก</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Actionable insights
            st.subheader(" ข้อเสนอแนะเชิงกลยุทธ์")
            
            # Analyze barriers and provide recommendations
            price_related = barrier_data['reason_not_chosen'].str.contains('แพง|ราคา|คุ้ม', case=False, na=False).sum()
            quality_related = barrier_data['reason_not_chosen'].str.contains('คุณภาพ|ทน|รีวิว', case=False, na=False).sum()
            availability_related = barrier_data['reason_not_chosen'].str.contains('หา|ซื้อ|ไม่รู้', case=False, na=False).sum()
            
            col3, col4, col5 = st.columns(3)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4> Price-related Issues</h4>
                    <h2>{price_related}</h2>
                    <p>คน ({price_related/total_barriers*100:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4> Quality-related Issues</h4>
                    <h2>{quality_related}</h2>
                    <p>คน ({quality_related/total_barriers*100:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <h4> Availability Issues</h4>
                    <h2>{availability_related}</h2>
                    <p>คน ({availability_related/total_barriers*100:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)

def show_personas(df):
    """Show comprehensive persona analysis combining behavior, beliefs, channels, and price"""
    st.header(" Customer Personas - การวิเคราะห์กลุ่มลูกค้าเชิงลึก")
    
    st.markdown("""
    <div class="insight-box">
        <h4> การสร้าง Persona แบบ 360 องศา</h4>
        <p>การรวมวิเคราะห์ <strong>พฤติกรรม + ความเชื่อ + เหตุผล + ช่องทาง + ราคา</strong> เพื่อเข้าใจลูกค้าอย่างลึกซึ้ง</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare data for clustering
    feature_cols = []
    
    # 1. Demographics (encoded)
    demo_cols = ['gender', 'age', 'monthly_income']
    
    # 2. Behavioral factors
    behavior_cols = [c for c in df.columns if c in ['luggage_frequency', 'buy_frequency']]
    
    # 3. Value/Belief factors (Likert scales)
    factor_cols = [c for c in df.columns if c.startswith('factor_')]
    
    # 4. Price sensitivity (Likert scales)
    price_cols = [c for c in df.columns if c.startswith('price_') and c not in ['price_midpoint', 'price_min', 'price_max', 'price_mid']]
    
    # 5. Channel preferences (Likert scales)
    channel_cols = [c for c in df.columns if c.startswith('channel_')]
    
    # 6. Marketing preferences (Likert scales)
    promo_cols = [c for c in df.columns if c.startswith('promo_')]
    
    # Create persona analysis
    st.subheader(" การวิเคราะห์แบบกลุ่ม (Cluster Analysis)")
    
    # Prepare numerical data for clustering
    cluster_data = df[factor_cols + price_cols + channel_cols + promo_cols].copy()
    
    # Simple clustering based on key behavioral patterns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Persona แบบ Value-Based")
        
        # Create value-based personas
        df_analysis = df.copy()
        
        # Calculate key scores
        df_analysis['quality_focus'] = df_analysis[['factor_durability', 'factor_warranty', 'price_value_for_quality']].mean(axis=1)
        df_analysis['price_sensitive'] = df_analysis[['price_within_budget', 'promo_discount']].mean(axis=1)
        df_analysis['brand_conscious'] = df_analysis[['factor_brand_trust', 'price_image_boost']].mean(axis=1)
        df_analysis['convenience_focus'] = df_analysis[['channel_fast_shipping', 'channel_easy_to_find']].mean(axis=1)
        
        # Create persona categories
        def categorize_persona(row):
            if row['quality_focus'] >= 4.5 and row['price_sensitive'] <= 3.5:
                return "Premium Quality Seeker"
            elif row['price_sensitive'] >= 4.5 and row['quality_focus'] >= 4.0:
                return "Value Hunter"
            elif row['brand_conscious'] >= 4.0:
                return "Brand Loyalist" 
            elif row['convenience_focus'] >= 4.5:
                return "Convenience Lover"
            else:
                return "Practical Buyer"
        
        df_analysis['persona_type'] = df_analysis.apply(categorize_persona, axis=1)
        
        # Show persona distribution
        persona_counts = df_analysis['persona_type'].value_counts()
        
        fig_personas = px.pie(
            values=persona_counts.values,
            names=persona_counts.index,
            title="การกระจายตัวของ Persona",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
        st.plotly_chart(fig_personas, use_container_width=True)
    
    with col2:
        st.subheader(" Persona แบบ Price vs Quality")
        
        # Price vs Quality Matrix
        fig_matrix = px.scatter(
            df_analysis,
            x='price_sensitive',
            y='quality_focus',
            color='persona_type',
            size='brand_conscious',
            title="Price Sensitivity vs Quality Focus Matrix",
            labels={
                'price_sensitive': 'ความอ่อนไหวต่อราคา',
                'quality_focus': 'มุ่งเน้นคุณภาพ'
            },
            hover_data=['convenience_focus']
        )
        fig_matrix.update_layout(height=400)
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Detailed Persona Profiles
    st.subheader(" รายละเอียด Persona แต่ละกลุ่ม")
    
    for persona_name in persona_counts.index:
        with st.expander(f"👤 {persona_name} ({persona_counts[persona_name]} คน - {persona_counts[persona_name]/len(df)*100:.1f}%)"):
            persona_df = df_analysis[df_analysis['persona_type'] == persona_name]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("** Demographics**")
                gender_dist = persona_df['gender'].value_counts()
                st.write(f"• เพศหลัก: {gender_dist.index[0]} ({gender_dist.iloc[0]} คน)")
                
                avg_age = persona_df['age'].mean()
                st.write(f"• อายุเฉลี่ย: {avg_age:.0f} ปี")
                
                top_income = persona_df['monthly_income'].mode().iloc[0] if len(persona_df) > 0 else "ไม่ระบุ"
                st.write(f"• รายได้หลัก: {top_income}")
                
                st.markdown("**🛒 พฤติกรรม**")
                if 'luggage_frequency' in persona_df.columns:
                    top_freq = persona_df['luggage_frequency'].mode().iloc[0] if len(persona_df) > 0 else "ไม่ระบุ"
                    st.write(f"• ความถี่ใช้งาน: {top_freq}")
                
                if 'most_used_platform' in persona_df.columns:
                    top_platform = persona_df['most_used_platform'].mode().iloc[0] if len(persona_df) > 0 else "ไม่ระบุ"
                    st.write(f"• แพลตฟอร์มหลัก: {top_platform}")
            
            with col2:
                st.markdown("** ความเชื่อ & ค่านิยม**")
                factor_scores = persona_df[factor_cols].mean().sort_values(ascending=False)
                st.write("ปัจจัยสำคัญ Top 3:")
                for i, (factor, score) in enumerate(factor_scores.head(3).items()):
                    factor_name = factor.replace('factor_', '').replace('_', ' ').title()
                    st.write(f"{i+1}. {factor_name}: {score:.1f}/5")
                
                st.markdown("** ความอ่อนไหวต่อราคา**")
                price_scores = persona_df[price_cols].mean().sort_values(ascending=False)
                for factor, score in price_scores.head(2).items():
                    factor_name = factor.replace('price_', '').replace('_', ' ').title()
                    st.write(f"• {factor_name}: {score:.1f}/5")
            
            with col3:
                st.markdown("** ช่องทางที่ต้องการ**")
                channel_scores = persona_df[channel_cols].mean().sort_values(ascending=False)
                for factor, score in channel_scores.head(3).items():
                    factor_name = factor.replace('channel_', '').replace('_', ' ').title()
                    st.write(f"• {factor_name}: {score:.1f}/5")
                
                st.markdown("** การตลาดที่ได้ผล**")
                promo_scores = persona_df[promo_cols].mean().sort_values(ascending=False)
                for factor, score in promo_scores.head(2).items():
                    factor_name = factor.replace('promo_', '').replace('_', ' ').title()
                    st.write(f"• {factor_name}: {score:.1f}/5")
    
    # Marketing Strategy Recommendations
    st.subheader(" กลยุทธ์การตลาดเฉพาะกลุ่ม")
    
    strategy_mapping = {
        "Premium Quality Seeker": {
            "strategy": "เน้นคุณภาพพรีเมี่ยม",
            "messaging": "ความทนทาน, การรับประกัน, คุณภาพระดับโลก", 
            "channels": "ร้านค้าอย่างเป็นทางการ, เว็บไซต์แบรนด์",
            "promotion": "Bundle premium, ข้อมูลเชิงลึกเรื่องคุณภาพ"
        },
        "Value Hunter": {
            "strategy": "เน้นความคุ้มค่า",
            "messaging": "คุณภาพดีในราคาที่เหมาะสม, เปรียบเทียบกับคู่แข่ง",
            "channels": "E-commerce, ส่วนลดออนไลน์",
            "promotion": "Flash sale, ส่วนลดพิเศษ, Bundle deal"
        },
        "Brand Loyalist": {
            "strategy": "เสริมสร้างภาพลักษณ์แบรนด์",
            "messaging": "ประวัติแบรนด์, เอกลักษณ์, สถานะทางสังคม",
            "channels": "Social media, Influencer, Event",
            "promotion": "Exclusive member, Limited edition"
        },
        "Convenience Lover": {
            "strategy": "เน้นความสะดวกสบาย",
            "messaging": "ง่าย, รวดเร็ว, หาซื้อง่าย",
            "channels": "App, Fast delivery, One-click purchase",
            "promotion": "Free shipping, Same-day delivery"
        },
        "Practical Buyer": {
            "strategy": "เน้นการใช้งานจริง",
            "messaging": "ใช้งานได้จริง, ตอบโจทย์ชีวิต, ไม่ซับซ้อน",
            "channels": "รีวิวจากผู้ใช้จริง, Tutorial, Demo",
            "promotion": "Trial period, การรับประกันการใช้งาน"
        }
    }
    
    for persona_name, count in persona_counts.items():
        if persona_name in strategy_mapping:
            strategy = strategy_mapping[persona_name]
            
            st.markdown(f"""
            <div class="metric-card">
                <h4> {persona_name} Strategy</h4>
                <p><strong> กลยุทธ์หลัก:</strong> {strategy['strategy']}</p>
                <p><strong> Message:</strong> {strategy['messaging']}</p>
                <p><strong> Channels:</strong> {strategy['channels']}</p>
                <p><strong> Promotion:</strong> {strategy['promotion']}</p>
                <p><small> Target Size: {count} คน ({count/len(df)*100:.1f}% ของตลาด)</small></p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 