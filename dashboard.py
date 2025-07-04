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
import base64
import tempfile
import os
from datetime import datetime
import io
from urllib.parse import quote

# PDF Export dependencies
try:
    from weasyprint import HTML, CSS
    from jinja2 import Template
    PDF_AVAILABLE = True
    print("PDF libraries loaded successfully!")
except ImportError as e:
    PDF_AVAILABLE = False
    print(f"PDF libraries not available: {e}")

# Debug: Print PDF availability
print(f"PDF_AVAILABLE: {PDF_AVAILABLE}")

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

# PDF Export Functions
def create_pdf_template():
    """Create HTML template for PDF export"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');
            
            body {
                font-family: 'Sarabun', sans-serif;
                line-height: 1.5;
                margin: 20px;
                background-color: #f8f9fa;
                color: #2c3e50;
            }
            
            .header {
                text-align: center;
                padding: 20px 0;
                border-bottom: 3px solid #4ECDC4;
                margin-bottom: 20px;
            }
            
            .header h1 {
                color: #2c3e50;
                font-size: 2.2em;
                margin-bottom: 8px;
                font-weight: 700;
            }
            
            .header p {
                color: #7f8c8d;
                font-size: 1.2em;
                margin: 0;
            }
            
            .content {
                background-color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            
            h2 {
                color: #2c3e50;
                border-bottom: 2px solid #4ECDC4;
                padding-bottom: 8px;
                margin-top: 25px;
                margin-bottom: 15px;
                font-weight: 600;
                font-size: 1.5em;
            }
            
            h3 {
                color: #34495e;
                margin-top: 20px;
                margin-bottom: 12px;
                font-weight: 500;
                font-size: 1.2em;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 50%, #667eea 100%);
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                color: white;
                margin: 10px 0;
                box-shadow: 0 6px 20px rgba(31, 38, 135, 0.3);
                display: inline-block;
                min-width: 150px;
            }
            
            .metric-card h3 {
                font-size: 1.1em;
                margin-bottom: 10px;
                color: white;
            }
            
            .metric-card h2 {
                font-size: 1.8em;
                margin: 8px 0;
                color: white;
                border: none;
                padding: 0;
            }
            
            .metric-card p {
                font-size: 0.9em;
                margin-top: 5px;
                opacity: 0.9;
            }
            
            .insight-box {
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(116, 185, 255, 0.3);
            }
            
            .insight-box h4 {
                margin-bottom: 15px;
                font-size: 1.2em;
                color: white;
            }
            
            .insight-box p {
                font-size: 1em;
                line-height: 1.6;
                margin-bottom: 0;
            }
            
            .warning-box {
                background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);
            }
            
            .success-box {
                background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                overflow: hidden;
                font-size: 0.9em;
            }
            
            th, td {
                padding: 8px 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            
            th {
                background: linear-gradient(135deg, #4ECDC4, #45B7D1);
                color: white;
                font-weight: 600;
            }
            
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            
            tr:hover {
                background-color: #e8f4f8;
            }
            
            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #e9ecef;
                color: #7f8c8d;
                font-size: 0.9em;
            }
            
            .page-break {
                page-break-before: always;
            }
            
            ul, ol {
                padding-left: 20px;
            }
            
            li {
                margin-bottom: 5px;
            }
            
            .highlight {
                background-color: #fff3cd;
                padding: 10px;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
                margin: 15px 0;
            }
            
            .persona-section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                border: 1px solid #e9ecef;
            }
            
            .persona-details {
                display: flex;
                gap: 20px;
                margin-top: 15px;
            }
            
            .persona-column {
                flex: 1;
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
            
            .strategy-box {
                background: linear-gradient(135deg, #fff3e0, #ffeaa7);
                padding: 20px;
                border-radius: 12px;
                margin: 15px 0;
                border-left: 5px solid #ffa726;
            }
            
            /* Landscape-specific styles */
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            
            .chart-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 15px 0;
            }
            
            .chart-container img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            
            .two-column {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }
            
            .three-column {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 15px;
                margin: 20px 0;
            }
            
            @media print {
                body {
                    margin: 15px;
                }
                .content {
                    box-shadow: none;
                    border: 1px solid #ddd;
                }
                .persona-details {
                    display: block;
                }
                .persona-column {
                    margin-bottom: 15px;
                }
                .metrics-grid {
                    grid-template-columns: repeat(4, 1fr);
                }
                .two-column {
                    grid-template-columns: 1fr 1fr;
                }
                .three-column {
                    grid-template-columns: 1fr 1fr 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{ title }}</h1>
            <p>{{ subtitle }}</p>
            <p>วันที่สร้างรายงาน: {{ date }}</p>
        </div>
        
        <div class="content">
            {{ content }}
        </div>
        
        <div class="footer">
            <p>รายงานนี้สร้างจาก Suitcase Insights Dashboard</p>
            <p>© {{ current_year }} - วิเคราะห์ข้อมูลการสำรวจพฤติกรรมผู้บริโภคกระเป๋าเดินทาง</p>
        </div>
    </body>
    </html>
    """
    return Template(html_template)

def get_page_content_as_html(page_name, df):
    """Get current page content as HTML"""
    # Capture current page content based on the selected page
    content_html = ""
    
    if page_name == "ภาพรวม":
        content_html = generate_overview_html(df)
    elif page_name == "ข้อมูลประชากรศาสตร์":
        content_html = generate_demographics_html(df)
    elif page_name == "ปัจจัยการตัดสินใจ":
        content_html = generate_factors_html(df)
    elif page_name == "ความต้องการผลิตภัณฑ์":
        content_html = generate_products_html(df)
    elif page_name == "ความอ่อนไหวต่อราคา":
        content_html = generate_pricing_html(df)
    elif page_name == "ช่องทางการขาย":
        content_html = generate_channels_html(df)
    elif page_name == "การตลาด":
        content_html = generate_marketing_html(df)
    elif page_name == "Brand Awareness":
        content_html = generate_brand_awareness_html(df)
    elif page_name == "Brand Image & Barriers":
        content_html = generate_brand_image_html(df)
    elif page_name == "Customer Personas":
        content_html = generate_personas_html(df)
    
    return content_html

def plotly_to_base64(fig):
    """Convert Plotly figure to base64 image"""
    try:
        import plotly.io as pio
        
        # Set template and ensure consistent styling
        pio.templates.default = "plotly_white"
        
        # Update layout to ensure proper margins and text visibility
        fig.update_layout(
            margin=dict(l=80, r=50, t=80, b=120),  # Increased margins
            font=dict(size=12, color='#2c3e50'),  # Ensure font color
            title=dict(
                font=dict(size=16, color='#2c3e50'),
                x=0.5,  # Center title
                y=0.95
            ),
            xaxis=dict(
                title_font=dict(size=14, color='#2c3e50'),
                tickfont=dict(size=11, color='#2c3e50'),
                title_standoff=25,  # Space between axis and title
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            ),
            yaxis=dict(
                title_font=dict(size=14, color='#2c3e50'),
                tickfont=dict(size=11, color='#2c3e50'),
                title_standoff=25,
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Special handling for horizontal bar charts
        if hasattr(fig.data[0], 'orientation') and fig.data[0].orientation == 'h':
            fig.update_layout(
                margin=dict(l=150, r=50, t=80, b=80),  # More left margin for y-axis labels
                yaxis=dict(
                    title_font=dict(size=14, color='#2c3e50'),
                    tickfont=dict(size=10, color='#2c3e50'),
                    title_standoff=25,
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                )
            )
        
        # Special handling for pie charts
        if fig.data[0].type == 'pie':
            fig.update_layout(
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(color='#2c3e50')
                ),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            # Ensure pie chart colors are preserved and visible
            default_colors = ['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FF9F43', '#A8E6CF', '#FFB6C1', '#87CEEB']
            fig.update_traces(
                marker=dict(
                    colors=default_colors[:len(fig.data[0].values)],
                    line=dict(color='white', width=2)  # Add white border to pie slices
                ),
                textfont=dict(color='white', size=12, family='Arial Black')  # Ensure text is visible
            )
        
        # Special handling for bar charts to ensure colors are preserved
        elif fig.data[0].type in ['bar', 'scatter']:
            # Ensure bar chart colors are preserved
            default_bar_colors = ['#4ECDC4', '#FF6B9D', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FF9F43', '#A8E6CF']
            if hasattr(fig.data[0], 'marker') and not hasattr(fig.data[0].marker, 'color'):
                fig.update_traces(
                    marker=dict(
                        color=default_bar_colors[0],  # Primary color for single series
                        line=dict(color='white', width=1)
                    )
                )
            
        # Special handling for heatmaps
        elif hasattr(fig.data[0], 'type') and fig.data[0].type == 'heatmap':
            fig.update_traces(
                colorscale='RdYlBu_r',
                showscale=True
            )
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title_font=dict(color='#2c3e50'),
                    tickfont=dict(color='#2c3e50')
                )
            )
        
        # Convert to image with high quality settings
        img_bytes = pio.to_image(
            fig, 
            format="png", 
            width=900, 
            height=600, 
            scale=2,
            engine="kaleido"  # Use kaleido engine for better color reproduction
        )
        img_base64 = base64.b64encode(img_bytes).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        print(f"Error converting plotly to image: {e}")
        return None

def generate_overview_html(df):
    """Generate HTML content for overview page"""
    avg_age = df['age'].mean()
    gender_counts = df['gender'].value_counts()
    female_count = gender_counts.get('หญิง', 0)
    female_pct = (female_count/len(df)*100) if len(df) > 0 else 0
    student_pct = (df['occupation'] == 'นักเรียน/นักศึกษา').mean() * 100 if 'occupation' in df.columns else 0
    
    # Create gender pie chart
    gender_chart_html = ""
    try:
        import plotly.express as px
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="สัดส่วนเพศของผู้ตอบแบบสำรวจ",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1']
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        fig_gender.update_layout(
            font=dict(size=14),
            title=dict(font=dict(size=18))
        )
        
        gender_img = plotly_to_base64(fig_gender)
        if gender_img:
            gender_chart_html = f'<div class="chart-container"><img src="{gender_img}" alt="Gender Distribution Chart"></div>'
    except Exception as e:
        print(f"Error creating gender chart: {e}")
    
    # Factor analysis
    factor_insight = ""
    factor_cols = [c for c in df.columns if c.startswith("factor_")]
    if factor_cols:
        factor_means = df[factor_cols].mean().sort_values(ascending=False)
        top_factor = factor_means.index[0].replace("factor_", "").replace("_", " ")
        factor_insight = f"""
        <div class="insight-box">
            <h4>ปัจจัยสำคัญที่สุด</h4>
            <p><strong>{top_factor}</strong> ได้คะแนนเฉลี่ย {factor_means.iloc[0]:.2f} จาก 5</p>
        </div>
        """
    
    # Price preference
    price_insight = ""
    price_col = 'preferred_price_range ' if 'preferred_price_range ' in df.columns else 'preferred_price_range'
    if price_col in df.columns:
        popular_price = df[price_col].mode().iloc[0] if not df[price_col].mode().empty else "ไม่ระบุ"
        price_insight = f"""
        <div class="insight-box">
            <h4>ช่วงราคาที่นิยม</h4>
            <p><strong>{popular_price}</strong> เป็นช่วงราคาที่ผู้ตอบแบบสำรวจเลือกมากที่สุด</p>
        </div>
        """
    
    html_content = f"""
    <h2>ภาพรวมผลการสำรวจ</h2>
    
    <div class="metrics-grid">
        <div class="metric-card">
            <h3>ผู้เข้าร่วม</h3>
            <h2>{len(df)}</h2>
            <p>คน</p>
        </div>
        
        <div class="metric-card">
            <h3>อายุเฉลี่ย</h3>
            <h2>{avg_age:.1f}</h2>
            <p>ปี</p>
        </div>
        
        <div class="metric-card">
            <h3>เพศหญิง</h3>
            <h2>{female_count}</h2>
            <p>คน ({female_pct:.1f}%)</p>
        </div>
        
        <div class="metric-card">
            <h3>นักเรียน/นักศึกษา</h3>
            <h2>{student_pct:.1f}%</h2>
            <p>ของผู้ตอบ</p>
        </div>
    </div>
    
    <h3>การกระจายตามเพศ</h3>
    <table>
        <thead>
            <tr>
                <th>เพศ</th>
                <th>จำนวน (คน)</th>
                <th>สัดส่วน (%)</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for gender, count in gender_counts.items():
        percentage = (count / len(df)) * 100
        html_content += f"""
            <tr>
                <td>{gender}</td>
                <td>{count}</td>
                <td>{percentage:.1f}%</td>
            </tr>
        """
    
    html_content += f"""
        </tbody>
    </table>
    
    {gender_chart_html}
    
    <h3>ข้อค้นพบสำคัญ</h3>
    {factor_insight}
    {price_insight}
    """
    
    return html_content

def generate_demographics_html(df):
    """Generate HTML content for demographics page"""
    # Gender breakdown
    gender_counts = df['gender'].value_counts()
    
    # Age breakdown
    age_counts = df['age_group'].value_counts().sort_index() if 'age_group' in df.columns else pd.Series()
    
    # Income breakdown
    income_counts = df['income_group'].value_counts().sort_index() if 'income_group' in df.columns else pd.Series()
    
    # Occupation breakdown
    occupation_counts = df['occupation'].value_counts().head(10) if 'occupation' in df.columns else pd.Series()
    
    # Create charts
    charts_html = ""
    
    # Gender pie chart
    try:
        import plotly.express as px
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="การกระจายตามเพศ",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        fig_gender.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
        
        gender_img = plotly_to_base64(fig_gender)
        if gender_img:
            charts_html += f'<div class="chart-container"><img src="{gender_img}" alt="Gender Chart"></div>'
    except Exception as e:
        print(f"Error creating gender chart: {e}")
    
    # Age bar chart
    if not age_counts.empty:
        try:
            fig_age = px.bar(
                x=age_counts.index,
                y=age_counts.values,
                title="การกระจายตามอายุ",
                labels={'x': 'ช่วงอายุ', 'y': 'จำนวนคน'},
                color=age_counts.values,
                color_continuous_scale='Viridis'
            )
            fig_age.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            
            age_img = plotly_to_base64(fig_age)
            if age_img:
                charts_html += f'<div class="chart-container"><img src="{age_img}" alt="Age Chart"></div>'
        except Exception as e:
            print(f"Error creating age chart: {e}")
    
    # Income bar chart
    if not income_counts.empty:
        try:
            fig_income = px.bar(
                x=income_counts.index,
                y=income_counts.values,
                title="การกระจายตามรายได้",
                labels={'x': 'ช่วงรายได้ (บาท)', 'y': 'จำนวนคน'},
                color=income_counts.values,
                color_continuous_scale='plasma'
            )
            fig_income.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            
            income_img = plotly_to_base64(fig_income)
            if income_img:
                charts_html += f'<div class="chart-container"><img src="{income_img}" alt="Income Chart"></div>'
        except Exception as e:
            print(f"Error creating income chart: {e}")
    
    # Occupation horizontal bar chart
    if not occupation_counts.empty:
        try:
            fig_occupation = px.bar(
                x=occupation_counts.values,
                y=occupation_counts.index,
                orientation='h',
                title="การกระจายตามอาชีพ (Top 10)",
                labels={'x': 'จำนวนคน', 'y': 'อาชีพ'},
                color=occupation_counts.values,
                color_continuous_scale='turbo'
            )
            fig_occupation.update_layout(font=dict(size=14), title=dict(font=dict(size=18)), height=600)
            
            occupation_img = plotly_to_base64(fig_occupation)
            if occupation_img:
                charts_html += f'<div class="chart-container"><img src="{occupation_img}" alt="Occupation Chart"></div>'
        except Exception as e:
            print(f"Error creating occupation chart: {e}")
    
    html_content = f"""
    <h2>ข้อมูลประชากรศาสตร์</h2>
    
    <div class="two-column">
        <div>
            <h3>การกระจายตามเพศ</h3>
            <table>
                <thead>
                    <tr>
                        <th>เพศ</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for gender, count in gender_counts.items():
        percentage = (count / len(df)) * 100
        html_content += f"""
                    <tr>
                        <td>{gender}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>
    """
    
    if not age_counts.empty:
        html_content += f"""
        <div>
            <h3>การกระจายตามอายุ</h3>
            <table>
                <thead>
                    <tr>
                        <th>ช่วงอายุ</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for age_group, count in age_counts.items():
            percentage = (count / len(df)) * 100
            html_content += f"""
                    <tr>
                        <td>{age_group}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </div>
    </div>
        """
    
    if not income_counts.empty:
        html_content += f"""
    <div class="two-column">
        <div>
            <h3>การกระจายตามรายได้</h3>
            <table>
                <thead>
                    <tr>
                        <th>ช่วงรายได้ (บาท)</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for income_group, count in income_counts.items():
            percentage = (count / len(df)) * 100
            html_content += f"""
                    <tr>
                        <td>{income_group}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </div>
        """
    
    if not occupation_counts.empty:
        html_content += f"""
        <div>
            <h3>การกระจายตามอาชีพ (Top 10)</h3>
            <table>
                <thead>
                    <tr>
                        <th>อาชีพ</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for occupation, count in occupation_counts.items():
            percentage = (count / len(df)) * 100
            html_content += f"""
                    <tr>
                        <td>{occupation}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </div>
    </div>
        """
    
    # Add charts section
    html_content += f"""
    <div class="page-break"></div>
    <h2>กราฟแสดงการกระจายข้อมูล</h2>
    {charts_html}
    """
    
    return html_content

def generate_factors_html(df):
    """Generate HTML content for factors page"""
    factor_cols = [c for c in df.columns if c.startswith("factor_")]
    
    if not factor_cols:
        return "<h2>ไม่พบข้อมูลปัจจัยการตัดสินใจ</h2>"
    
    factor_means = df[factor_cols].mean().sort_values(ascending=False)
    
    # Create charts
    charts_html = ""
    
    # Main factors bar chart
    try:
        import plotly.express as px
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
        fig_factors.update_layout(height=600, font=dict(size=14), title=dict(font=dict(size=18)))
        
        factors_img = plotly_to_base64(fig_factors)
        if factors_img:
            charts_html += f'<div class="chart-container"><img src="{factors_img}" alt="Factors Chart"></div>'
    except Exception as e:
        print(f"Error creating factors chart: {e}")
    
    # Factors by gender heatmap
    try:
        gender_factors = df.groupby('gender')[factor_cols].mean()
        
        fig_gender_factors = px.imshow(
            gender_factors.T,
            title="Heatmap: ความสำคัญของปัจจัยตามเพศ",
            labels=dict(x="เพศ", y="ปัจจัย", color="คะแนนเฉลี่ย"),
            aspect="auto",
            color_continuous_scale='RdYlBu_r',
            text_auto=True
        )
        fig_gender_factors.update_traces(texttemplate="%{z:.2f}", textfont_size=12)
        fig_gender_factors.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
        
        gender_factors_img = plotly_to_base64(fig_gender_factors)
        if gender_factors_img:
            charts_html += f'<div class="chart-container"><img src="{gender_factors_img}" alt="Gender Factors Heatmap"></div>'
    except Exception as e:
        print(f"Error creating gender factors heatmap: {e}")
    
    # Factors by income heatmap
    if 'income_group' in df.columns:
        try:
            income_factors = df.groupby('income_group', observed=False)[factor_cols].mean()
            
            fig_income_factors = px.imshow(
                income_factors.T,
                title="Heatmap: ความสำคัญของปัจจัยตามรายได้",
                labels=dict(x="กลุ่มรายได้", y="ปัจจัย", color="คะแนนเฉลี่ย"),
                aspect="auto",
                color_continuous_scale='RdYlBu_r',
                text_auto=True
            )
            fig_income_factors.update_traces(texttemplate="%{z:.2f}", textfont_size=12)
            fig_income_factors.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            
            income_factors_img = plotly_to_base64(fig_income_factors)
            if income_factors_img:
                charts_html += f'<div class="chart-container"><img src="{income_factors_img}" alt="Income Factors Heatmap"></div>'
        except Exception as e:
            print(f"Error creating income factors heatmap: {e}")
    

    
    html_content = f"""
    <h2>ปัจจัยการตัดสินใจซื้อกระเป๋าเดินทาง</h2>
    
    <h3>ลำดับความสำคัญของปัจจัยโดยรวม</h3>
    <table>
        <thead>
            <tr>
                <th>อันดับ</th>
                <th>ปัจจัย</th>
                <th>คะแนนเฉลี่ย</th>
                <th>ระดับความสำคัญ</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for i, (factor, score) in enumerate(factor_means.items(), 1):
        factor_name = factor.replace("factor_", "").replace("_", " ").title()
        
        # Determine importance level
        if score >= 4.5:
            importance = "สำคัญมาก"
        elif score >= 4.0:
            importance = "สำคัญ"
        elif score >= 3.5:
            importance = "ปานกลาง"
        elif score >= 3.0:
            importance = "น้อย"
        else:
            importance = "น้อยมาก"
        
        html_content += f"""
            <tr>
                <td>{i}</td>
                <td>{factor_name}</td>
                <td>{score:.2f}</td>
                <td>{importance}</td>
            </tr>
        """
    
    html_content += """
        </tbody>
    </table>
    """
    
    # Top 3 insights
    top_3_factors = factor_means.head(3)
    html_content += f"""
    <h3>ปัจจัยสำคัญ 3 อันดับแรก</h3>
    """
    
    for i, (factor, score) in enumerate(top_3_factors.items(), 1):
        factor_name = factor.replace("factor_", "").replace("_", " ").title()
        html_content += f"""
        <div class="insight-box">
            <h4>อันดับ {i}: {factor_name}</h4>
            <p>คะแนนเฉลี่ย: <strong>{score:.2f}</strong> จาก 5 คะแนน</p>
        </div>
        """
    
    # Add charts section
    html_content += f"""
    <div class="page-break"></div>
    <h2>กราฟการวิเคราะห์ปัจจัย</h2>
    {charts_html}
    """
    
    return html_content

def generate_products_html(df):
    """Generate HTML content for products page"""
    html_content = "<h2>ความต้องการด้านผลิตภัณฑ์</h2>"
    
    # Create charts
    charts_html = ""
    
    # Style preferences
    if 'preferred_styles' in df.columns:
        style_long = explode_multiselect(df['preferred_styles'], clean_func=normalize_th)
        style_counts = style_long['value'].value_counts().head(10)
        
        # Create style chart
        try:
            import plotly.express as px
            fig_styles = px.bar(
                x=style_counts.values,
                y=style_counts.index,
                orientation='h',
                title="สไตล์/สีที่ได้รับความนิยม (Top 10)",
                labels={'x': 'จำนวนครั้งที่เลือก', 'y': 'สไตล์/สี'},
                color=style_counts.values,
                color_continuous_scale='sunset'
            )
            fig_styles.update_layout(height=500, font=dict(size=14), title=dict(font=dict(size=18)))
            
            styles_img = plotly_to_base64(fig_styles)
            if styles_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{styles_img}" style="max-width: 100%; height: auto;" alt="Styles Chart"></div>'
        except Exception as e:
            print(f"Error creating styles chart: {e}")
        
        html_content += f"""
        <h3>สไตล์/สีที่ต้องการ (Top 10)</h3>
        <table>
            <thead>
                <tr>
                    <th>อันดับ</th>
                    <th>สไตล์/สี</th>
                    <th>จำนวนครั้งที่เลือก</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        total_responses = len(df)
        for i, (style, count) in enumerate(style_counts.items(), 1):
            percentage = (count / total_responses) * 100
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{style}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
    
    # Bag types
    if 'used_bag_types' in df.columns:
        bag_long = explode_multiselect(df['used_bag_types'], clean_func=normalize_th)
        bag_counts = bag_long['value'].value_counts().head(8)
        
        # Create bag types chart
        try:
            fig_bags = px.pie(
                values=bag_counts.values,
                names=bag_counts.index,
                title="ประเภทกระเป๋าที่ใช้บ่อย",
                color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            )
            fig_bags.update_traces(textposition='inside', textinfo='percent+label')
            fig_bags.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            
            bags_img = plotly_to_base64(fig_bags)
            if bags_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{bags_img}" style="max-width: 100%; height: auto;" alt="Bag Types Chart"></div>'
        except Exception as e:
            print(f"Error creating bag types chart: {e}")
        
        html_content += f"""
        <h3>ประเภทกระเป๋าที่ใช้</h3>
        <table>
            <thead>
                <tr>
                    <th>อันดับ</th>
                    <th>ประเภทกระเป๋า</th>
                    <th>จำนวนครั้งที่เลือก</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        total_responses = len(df)
        for i, (bag_type, count) in enumerate(bag_counts.items(), 1):
            percentage = (count / total_responses) * 100
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{bag_type}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
    
    # Size preferences
    if 'luggage_size_short_trip' in df.columns:
        size_counts = df['luggage_size_short_trip'].value_counts()
        
        # Create size chart
        try:
            fig_sizes = px.bar(
                x=size_counts.index,
                y=size_counts.values,
                title="ขนาดกระเป๋าที่นิยมสำหรับการเดินทางระยะสั้น",
                labels={'x': 'ขนาด (นิ้ว)', 'y': 'จำนวนคน'},
                color=size_counts.values,
                color_continuous_scale='Blues'
            )
            fig_sizes.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            
            sizes_img = plotly_to_base64(fig_sizes)
            if sizes_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{sizes_img}" style="max-width: 100%; height: auto;" alt="Sizes Chart"></div>'
        except Exception as e:
            print(f"Error creating sizes chart: {e}")
        
        html_content += f"""
        <h3>ขนาดกระเป๋าที่ต้องการสำหรับการเดินทางระยะสั้น</h3>
        <table>
            <thead>
                <tr>
                    <th>ขนาด (นิ้ว)</th>
                    <th>จำนวนคน</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for size, count in size_counts.items():
            percentage = (count / len(df)) * 100
            html_content += f"""
                <tr>
                    <td>{size}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
    
    # Add charts section
    html_content += f"""
    <div class="page-break"></div>
    <h2>กราฟความต้องการผลิตภัณฑ์</h2>
    {charts_html}
    """
    
    return html_content

def generate_pricing_html(df):
    """Generate HTML content for pricing page"""
    html_content = "<h2>ความอ่อนไหวต่อราคา</h2>"
    
    # Create charts
    charts_html = ""
    
    # Price range preferences
    price_col = 'preferred_price_range ' if 'preferred_price_range ' in df.columns else 'preferred_price_range'
    if price_col in df.columns:
        price_counts = df[price_col].value_counts()
        
        # Create price chart
        try:
            import plotly.express as px
            fig_price = px.bar(
                x=price_counts.index,
                y=price_counts.values,
                title="ช่วงราคาที่ผู้บริโภคต้องการ",
                labels={'x': 'ช่วงราคา', 'y': 'จำนวนคน'},
                color=price_counts.values,
                color_continuous_scale='viridis'
            )
            fig_price.update_layout(xaxis_tickangle=45, font=dict(size=14), title=dict(font=dict(size=18)))
            
            price_img = plotly_to_base64(fig_price)
            if price_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{price_img}" style="max-width: 100%; height: auto;" alt="Price Chart"></div>'
        except Exception as e:
            print(f"Error creating price chart: {e}")
        
        html_content += f"""
        <h3>ช่วงราคาที่ต้องการ</h3>
        <table>
            <thead>
                <tr>
                    <th>ช่วงราคา</th>
                    <th>จำนวนคน</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for price_range, count in price_counts.items():
            percentage = (count / len(df)) * 100
            html_content += f"""
                <tr>
                    <td>{price_range}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
        
        # Most popular price insight
        most_popular_price = price_counts.index[0]
        most_popular_count = price_counts.iloc[0]
        most_popular_pct = (most_popular_count / len(df)) * 100
        
        html_content += f"""
        <div class="insight-box">
            <h4>ช่วงราคาที่นิยมที่สุด</h4>
            <p><strong>{most_popular_price}</strong> - {most_popular_count} คน ({most_popular_pct:.1f}%)</p>
        </div>
        """
    
    # Price factors analysis
    price_factor_cols = [c for c in df.columns if c.startswith("price_") and c not in ['price_midpoint', 'price_min', 'price_max', 'price_mid']]
    
    if price_factor_cols:
        price_means = df[price_factor_cols].mean().sort_values(ascending=False)
        
        # Create Thai names for price factors
        factor_name_mapping = {
            'price_within_budget': 'อยู่ในงบประมาณ',
            'price_value_for_quality': 'คุ้มค่าต่อคุณภาพ', 
            'price_vs_competitor': 'เทียบกับคู่แข่ง',
            'price_image_boost': 'เพิ่มภาพลักษณ์'
        }
        
        price_names = [factor_name_mapping.get(col, col.replace("price_", "").replace("_", " ").title()) for col in price_means.index]
        
        # Create price factors chart
        try:
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
                height=400,
                font=dict(size=14), 
                title=dict(font=dict(size=18))
            )
            
            price_factors_img = plotly_to_base64(fig_price_factors)
            if price_factors_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{price_factors_img}" style="max-width: 100%; height: auto;" alt="Price Factors Chart"></div>'
        except Exception as e:
            print(f"Error creating price factors chart: {e}")
        
        html_content += f"""
        <h3>ปัจจัยด้านราคา</h3>
        <table>
            <thead>
                <tr>
                    <th>อันดับ</th>
                    <th>ปัจจัยด้านราคา</th>
                    <th>คะแนนเฉลี่ย</th>
                    <th>ระดับความสำคัญ</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for i, (factor, score) in enumerate(price_means.items(), 1):
            factor_name = factor_name_mapping.get(factor, factor.replace("price_", "").replace("_", " ").title())
            
            # Determine importance level
            if score >= 4.5:
                importance = "สำคัญมาก"
            elif score >= 4.0:
                importance = "สำคัญ"
            elif score >= 3.5:
                importance = "ปานกลาง"
            elif score >= 3.0:
                importance = "น้อย"
            else:
                importance = "น้อยมาก"
            
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{factor_name}</td>
                    <td>{score:.2f}</td>
                    <td>{importance}</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
    
    # Price vs Income analysis
    if 'income_group' in df.columns and price_col in df.columns:
        # Clean data first - remove NaN income groups
        clean_df = df.dropna(subset=['income_group', price_col])
        
        if len(clean_df) > 0:
            # Cross-tabulation
            price_income = pd.crosstab(clean_df['income_group'], clean_df[price_col])
            
            # Only proceed if we have data
            if not price_income.empty and price_income.sum().sum() > 0:
                try:
                    fig_price_income = px.imshow(
                        price_income.values,
                        x=price_income.columns,
                        y=price_income.index,
                        title="ความสัมพันธ์ระหว่างรายได้กับช่วงราคาที่ต้องการ",
                        labels=dict(x="ช่วงราคา", y="กลุ่มรายได้", color="จำนวนคน"),
                        color_continuous_scale='Blues',
                        text_auto=True
                    )
                    fig_price_income.update_traces(texttemplate="%{z}", textfont_size=12)
                    fig_price_income.update_layout(
                        xaxis={'side': 'bottom'},
                        height=400,
                        font=dict(size=14), 
                        title=dict(font=dict(size=18))
                    )
                    
                    price_income_img = plotly_to_base64(fig_price_income)
                    if price_income_img:
                        charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{price_income_img}" style="max-width: 100%; height: auto;" alt="Price vs Income Heatmap"></div>'
                except Exception as e:
                    print(f"Error creating price vs income heatmap: {e}")
                
                # Add summary table
                html_content += f"""
                <h3>ราคา vs รายได้ - ตารางสรุป</h3>
                <table>
                    <thead>
                        <tr>
                            <th>กลุ่มรายได้</th>
                """
                
                for price_range in price_income.columns:
                    html_content += f"<th>{price_range}</th>"
                
                html_content += """
                        </tr>
                    </thead>
                    <tbody>
                """
                
                for income_group in price_income.index:
                    html_content += f"<tr><td>{income_group}</td>"
                    for price_range in price_income.columns:
                        value = price_income.loc[income_group, price_range]
                        html_content += f"<td>{value}</td>"
                    html_content += "</tr>"
                
                html_content += """
                    </tbody>
                </table>
                """
    
    # Add charts section
    html_content += f"""
    <div class="page-break"></div>
    <h2>กราฟความอ่อนไหวต่อราคา</h2>
    {charts_html}
    """
    
    return html_content

def generate_channels_html(df):
    """Generate HTML content for channels page"""
    html_content = "<h2>ช่องทางการขาย</h2>"
    
    # Create charts
    charts_html = ""
    
    # Platform usage
    if 'most_used_platform' in df.columns:
        platform_counts = df['most_used_platform'].value_counts().head(10)
        
        # Create platform pie chart
        try:
            import plotly.express as px
            fig_platforms = px.pie(
                values=platform_counts.values,
                names=platform_counts.index,
                title="แพลตฟอร์มที่ผู้บริโภคใช้มากที่สุด",
                color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF7675', '#A29BFE']
            )
            fig_platforms.update_traces(textposition='inside', textinfo='percent+label')
            fig_platforms.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            
            platforms_img = plotly_to_base64(fig_platforms)
            if platforms_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{platforms_img}" style="max-width: 100%; height: auto;" alt="Platforms Chart"></div>'
        except Exception as e:
            print(f"Error creating platforms chart: {e}")
        
        html_content += f"""
        <h3>แพลตฟอร์มที่ใช้มากที่สุด</h3>
        <table>
            <thead>
                <tr>
                    <th>อันดับ</th>
                    <th>แพลตฟอร์ม</th>
                    <th>จำนวนคน</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for i, (platform, count) in enumerate(platform_counts.items(), 1):
            percentage = (count / len(df)) * 100
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{platform}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
    
    # Purchase channels
    if 'purchase_channels' in df.columns:
        channel_long = explode_multiselect(df['purchase_channels'], clean_func=normalize_th)
        channel_counts = channel_long['value'].value_counts().head(10)
        
        # Create channels chart
        try:
            fig_channels = px.bar(
                x=channel_counts.values,
                y=channel_counts.index,
                orientation='h',
                title="ช่องทางการซื้อที่นิยม",
                labels={'x': 'จำนวนครั้งที่เลือก', 'y': 'ช่องทางการซื้อ'},
                color=channel_counts.values,
                color_continuous_scale='viridis'
            )
            fig_channels.update_layout(height=500, font=dict(size=14), title=dict(font=dict(size=18)))
            
            channels_img = plotly_to_base64(fig_channels)
            if channels_img:
                charts_html += f'<div style="text-align: center; margin: 30px 0;"><img src="{channels_img}" style="max-width: 100%; height: auto;" alt="Channels Chart"></div>'
        except Exception as e:
            print(f"Error creating channels chart: {e}")
        
        html_content += f"""
        <h3>ช่องทางการซื้อ</h3>
        <table>
            <thead>
                <tr>
                    <th>อันดับ</th>
                    <th>ช่องทางการซื้อ</th>
                    <th>จำนวนครั้งที่เลือก</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        total_responses = len(df)
        for i, (channel, count) in enumerate(channel_counts.items(), 1):
            percentage = (count / total_responses) * 100
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{channel}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
    
    # Add charts section
    html_content += f"""
    <div class="page-break"></div>
    <h2>กราฟช่องทางการขาย</h2>
    {charts_html}
    """
    
    return html_content

def generate_marketing_html(df):
    """Generate HTML content for marketing page"""
    import plotly.express as px
    import pandas as pd
    
    html_content = "<h2>การตลาด</h2>"
    
    # Promotion preferences
    promo_cols = [c for c in df.columns if c.startswith("promo_")]
    
    if promo_cols:
        html_content += "<h3>ประสิทธิภาพของโปรโมชั่นแต่ละประเภท</h3>"
        
        # Calculate average scores for each promotion type
        promo_means = df[promo_cols].mean().sort_values(ascending=False)
        promo_names = [col.replace("promo_", "").replace("_", " ").title() for col in promo_means.index]
        
        # Create table
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>อันดับ</th>
                    <th>ประเภทโปรโมชั่น</th>
                    <th>คะแนนเฉลี่ย</th>
                    <th>ระดับประสิทธิภาพ</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for i, (promo, score) in enumerate(promo_means.items(), 1):
            promo_name = promo.replace("promo_", "").replace("_", " ").title()
            
            if score >= 4.5:
                level = "ยอดเยี่ยม"
            elif score >= 4.0:
                level = "ดีมาก"
            elif score >= 3.5:
                level = "ดี"
            elif score >= 3.0:
                level = "ปานกลาง"
            else:
                level = "ต้องปรับปรุง"
            
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{promo_name}</td>
                    <td>{score:.2f}</td>
                    <td>{level}</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
        
        # Create bar chart for promotions
        try:
            fig_promo = px.bar(
                x=promo_means.values,
                y=promo_names,
                orientation='h',
                title="คะแนนเฉลี่ยประสิทธิภาพโปรโมชั่น (1-5)",
                labels={'x': 'คะแนนเฉลี่ย', 'y': 'ประเภทโปรโมชั่น'},
                color=promo_means.values,
                color_continuous_scale='RdYlGn'
            )
            fig_promo.update_layout(
                height=max(400, len(promo_names) * 40),  # Dynamic height based on number of items
                font=dict(size=12),
                title=dict(font=dict(size=16)),
                margin=dict(l=200, r=50, t=80, b=80),  # Extra left margin for long labels
                yaxis=dict(tickfont=dict(size=10))
            )
            promo_chart = plotly_to_base64(fig_promo)
            if promo_chart:
                html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{promo_chart}" style="max-width: 100%; height: auto;" alt="Promotion Effectiveness Chart"></div>'
        except Exception as e:
            print(f"Error creating promotion chart: {e}")
        
        # Key insights
        top_promo = promo_names[0]
        top_score = promo_means.iloc[0]
        worst_promo = promo_names[-1]  
        worst_score = promo_means.iloc[-1]
        
        html_content += f"""
        <div class="insight-box">
            <h4>โปรโมชั่นที่ได้ผลที่สุด</h4>
            <p><strong>{top_promo}</strong><br>คะแนนเฉลี่ย: {top_score:.2f}/5</p>
        </div>
        
        <div class="warning-box">
            <h4>โปรโมชั่นที่ได้ผลต่ำสุด</h4>
            <p><strong>{worst_promo}</strong><br>คะแนนเฉลี่ย: {worst_score:.2f}/5</p>
            <p><small>ควรพิจารณาปรับกลยุทธ์หรือลดการลงทุน</small></p>
        </div>
        """
    
    # Presenter preferences
    if 'preferred_presenter' in df.columns:
        html_content += "<h3>พรีเซนเตอร์ที่ต้องการ</h3>"
        
        presenter_counts = df['preferred_presenter'].value_counts().head(10)
        presenter_counts = presenter_counts[presenter_counts.index != '-']  # Remove empty values
        
        if len(presenter_counts) > 0:
            # Create table
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th>อันดับ</th>
                        <th>พรีเซนเตอร์</th>
                        <th>จำนวนคนที่เลือก</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            total_responses = presenter_counts.sum()
            for i, (presenter, count) in enumerate(presenter_counts.items(), 1):
                percentage = (count / total_responses) * 100
                html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{presenter}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
                """
            
            html_content += """
                </tbody>
            </table>
            """
            
            try:
                fig_presenter = px.bar(
                    x=presenter_counts.values,
                    y=presenter_counts.index,
                    orientation='h',
                    title="พรีเซนเตอร์ที่ได้รับความนิยม",
                    labels={'x': 'จำนวนครั้งที่เลือก', 'y': 'พรีเซนเตอร์'},
                    color=presenter_counts.values,
                    color_continuous_scale='viridis'
                )
                fig_presenter.update_layout(height=500, font=dict(size=14), title=dict(font=dict(size=18)))
                presenter_chart = plotly_to_base64(fig_presenter)
                if presenter_chart:
                    html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{presenter_chart}" style="max-width: 100%; height: auto;" alt="Presenter Preferences Chart"></div>'
            except Exception as e:
                print(f"Error creating presenter chart: {e}")
    
    return html_content

def generate_brand_awareness_html(df):
    """Generate HTML content for brand awareness page"""
    import plotly.express as px
    import pandas as pd
    
    html_content = "<h2>Brand Awareness - T.Partner</h2>"
    
    # Brand recognition level
    if 'know_tpartner' in df.columns:
        html_content += "<h3>ระดับการรู้จักแบรนด์ T.Partner</h3>"
        
        awareness_counts = df['know_tpartner'].value_counts()
        
        # Create table first
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>ระดับการรู้จัก</th>
                    <th>จำนวน (คน)</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        total_respondents = len(df)
        for awareness_level, count in awareness_counts.items():
            percentage = (count / total_respondents) * 100
            html_content += f"""
                <tr>
                    <td>{awareness_level}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
        
        # Create pie chart
        try:
            fig_awareness = px.pie(
                values=awareness_counts.values,
                names=awareness_counts.index,
                title="สัดส่วนการรู้จักแบรนด์ T.Partner",
                color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            )
            fig_awareness.update_traces(textposition='inside', textinfo='percent+label')
            fig_awareness.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            awareness_chart = plotly_to_base64(fig_awareness)
            if awareness_chart:
                html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{awareness_chart}" style="max-width: 100%; height: auto;" alt="Brand Awareness Chart"></div>'
        except Exception as e:
            print(f"Error creating awareness chart: {e}")
        
        # Calculate key metrics
        know_brand = (df['know_tpartner'] == 'รู้จัก และรู้ว่าเป็นแบรนด์กระเป๋าเดินทาง').sum()
        seen_before = (df['know_tpartner'] == 'เคยเห็นผ่านตา แต่ไม่แน่ใจว่าแบรนด์ทำอะไร').sum()
        never_heard = (df['know_tpartner'] == 'ไม่รู้จักมาก่อนเลย').sum()
        
        html_content += f"""
        <div class="metric-card">
            <h4>Brand Recognition Metrics</h4>
            <p><strong>รู้จักแบรนด์:</strong> {know_brand} คน ({know_brand/total_respondents*100:.1f}%)</p>
            <p><strong>เคยเห็นผ่านตา:</strong> {seen_before} คน ({seen_before/total_respondents*100:.1f}%)</p>
            <p><strong>ไม่รู้จักเลย:</strong> {never_heard} คน ({never_heard/total_respondents*100:.1f}%)</p>
        </div>
        """
    
    # First channel awareness
    if 'tpartner_first_channel' in df.columns:
        html_content += "<h3>📡 ช่องทางที่รู้จักแบรนด์ครั้งแรก</h3>"
        
        # Filter out non-responses
        first_channel_data = df[df['tpartner_first_channel'].notna() & 
                                (df['tpartner_first_channel'] != '') & 
                                (df['tpartner_first_channel'] != '-')]
        
        if len(first_channel_data) > 0:
            channel_counts = first_channel_data['tpartner_first_channel'].value_counts().head(10)
            
            # Create table
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th>อันดับ</th>
                        <th>ช่องทาง</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            total_responses = len(first_channel_data)
            for i, (channel, count) in enumerate(channel_counts.items(), 1):
                percentage = (count / total_responses) * 100
                html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{channel}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
                """
            
            html_content += """
                </tbody>
            </table>
            """
            
            try:
                fig_channels = px.bar(
                    x=channel_counts.index,
                    y=channel_counts.values,
                    title="ช่องทางที่ทำให้รู้จักแบรนด์ T.Partner ครั้งแรก",
                    labels={'x': 'ช่องทาง', 'y': 'จำนวนคน'},
                    color=channel_counts.values,
                    color_continuous_scale='blues'
                )
                fig_channels.update_layout(xaxis_tickangle=45, font=dict(size=14), title=dict(font=dict(size=18)))
                channels_chart = plotly_to_base64(fig_channels)
                if channels_chart:
                    html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{channels_chart}" style="max-width: 100%; height: auto;" alt="First Channel Awareness Chart"></div>'
            except Exception as e:
                print(f"Error creating channels chart: {e}")
            
            # Key insight
            top_channel = channel_counts.index[0]
            top_count = channel_counts.iloc[0]
            
            html_content += f"""
            <div class="insight-box">
                <h4>ช่องทางหลักในการสร้าง Brand Awareness</h4>
                <p><strong>{top_channel}</strong> เป็นช่องทางที่ทำให้คนรู้จักแบรนด์มากที่สุด</p>
                <p>คิดเป็น {top_count} คนจาก {total_responses} คนที่ตอบ ({top_count/total_responses*100:.1f}%)</p>
                <p><small>ควรเพิ่มการลงทุนในช่องทางนี้เพื่อเพิ่ม brand awareness</small></p>
            </div>
            """
    
    return html_content

def generate_brand_image_html(df):
    """Generate HTML content for brand image page"""
    import plotly.express as px
    import pandas as pd
    
    html_content = "<h2>🏢 Brand Image & Barriers to Purchase</h2>"
    
    # Brand positioning perception
    if 'tpartner_positioning' in df.columns:
        html_content += "<h3>การรับรู้ positioning ของแบรนด์</h3>"
        
        positioning_data = df[df['tpartner_positioning'].notna() & 
                             (df['tpartner_positioning'] != '') & 
                             (df['tpartner_positioning'] != '-')]
        
        if len(positioning_data) > 0:
            positioning_counts = positioning_data['tpartner_positioning'].value_counts().head(8)
            
            # Create table
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th>อันดับ</th>
                        <th>Positioning ที่รับรู้</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            total_positioning = len(positioning_data)
            for i, (positioning, count) in enumerate(positioning_counts.items(), 1):
                percentage = (count / total_positioning) * 100
                html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{positioning}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
                """
            
            html_content += """
                </tbody>
            </table>
            """
            
            try:
                fig_positioning = px.bar(
                    x=positioning_counts.values,
                    y=positioning_counts.index,
                    orientation='h',
                    title="การรับรู้ positioning ของ T.Partner",
                    labels={'x': 'จำนวนคน', 'y': 'Positioning'},
                    color=positioning_counts.values,
                    color_continuous_scale='viridis'
                )
                fig_positioning.update_layout(height=400, font=dict(size=14), title=dict(font=dict(size=18)))
                positioning_chart = plotly_to_base64(fig_positioning)
                if positioning_chart:
                    html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{positioning_chart}" style="max-width: 100%; height: auto;" alt="Brand Positioning Chart"></div>'
            except Exception as e:
                print(f"Error creating positioning chart: {e}")
    
    # First impression and consideration analysis
    html_content += "<h3>💭 First Impression & การพิจารณาซื้อ</h3>"
    
    # First impression sentiment analysis
    if 'first_impression' in df.columns:
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
            
            # Create sentiment table
            html_content += "<h4>การวิเคราะห์ First Impression</h4>"
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th>ลักษณะ First Impression</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            total_impressions = len(impression_data)
            for sentiment, count in sentiment_counts.items():
                percentage = (count / total_impressions) * 100
                html_content += f"""
                    <tr>
                        <td>{sentiment}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
                """
            
            html_content += """
                </tbody>
            </table>
            """
            
            try:
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
                fig_sentiment.update_traces(textposition='inside', textinfo='percent+label')
                fig_sentiment.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
                sentiment_chart = plotly_to_base64(fig_sentiment)
                if sentiment_chart:
                    html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{sentiment_chart}" style="max-width: 100%; height: auto;" alt="First Impression Sentiment Chart"></div>'
            except Exception as e:
                print(f"Error creating sentiment chart: {e}")
    
    # Purchase consideration
    if 'considered_tpartner' in df.columns:
        html_content += "<h4>🤔 การพิจารณาซื้อแบรนด์ T.Partner</h4>"
        considered_counts = df['considered_tpartner'].value_counts()
        
        # Create table
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>ระดับการพิจารณา</th>
                    <th>จำนวน (คน)</th>
                    <th>สัดส่วน (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        total_considered = len(df)
        for consideration, count in considered_counts.items():
            percentage = (count / total_considered) * 100
            html_content += f"""
                <tr>
                    <td>{consideration}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
        
        try:
            fig_considered = px.pie(
                values=considered_counts.values,
                names=considered_counts.index,
                title="การพิจารณาซื้อแบรนด์ T.Partner",
                color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1']
            )
            fig_considered.update_traces(textposition='inside', textinfo='percent+label')
            fig_considered.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
            considered_chart = plotly_to_base64(fig_considered)
            if considered_chart:
                html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{considered_chart}" style="max-width: 100%; height: auto;" alt="Purchase Consideration Chart"></div>'
        except Exception as e:
            print(f"Error creating consideration chart: {e}")
    
    # Barriers to purchase
    if 'reason_not_chosen' in df.columns:
        html_content += "<h3>🚧 เหตุผลที่ยังไม่ซื้อ / Barriers to Purchase</h3>"
        
        barrier_data = df[df['reason_not_chosen'].notna() & 
                         (df['reason_not_chosen'] != '') & 
                         (df['reason_not_chosen'] != '-')]
        
        if len(barrier_data) > 0:
            # Count common barriers
            barrier_counts = barrier_data['reason_not_chosen'].value_counts().head(10)
            
            # Create table
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th>อันดับ</th>
                        <th>เหตุผลที่ไม่เลือกซื้อ</th>
                        <th>จำนวน (คน)</th>
                        <th>สัดส่วน (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            total_barriers = len(barrier_data)
            for i, (barrier, count) in enumerate(barrier_counts.items(), 1):
                percentage = (count / total_barriers) * 100
                html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{barrier}</td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
                """
            
            html_content += """
                </tbody>
            </table>
            """
            
            try:
                fig_barriers = px.bar(
                    x=barrier_counts.values,
                    y=barrier_counts.index,
                    orientation='h',
                    title="เหตุผลที่ยังไม่ได้เลือกซื้อ T.Partner",
                    labels={'x': 'จำนวนคน', 'y': 'เหตุผล'},
                    color=barrier_counts.values,
                    color_continuous_scale='Reds'
                )
                fig_barriers.update_layout(height=500, font=dict(size=14), title=dict(font=dict(size=18)))
                barriers_chart = plotly_to_base64(fig_barriers)
                if barriers_chart:
                    html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{barriers_chart}" style="max-width: 100%; height: auto;" alt="Barriers to Purchase Chart"></div>'
            except Exception as e:
                print(f"Error creating barriers chart: {e}")
            
            # Key insights
            top_barrier = barrier_counts.index[0]
            top_barrier_count = barrier_counts.iloc[0]
            
            html_content += f"""
            <div class="warning-box">
                <h4>�� อุปสรรคหลักในการซื้อ</h4>
                <p><strong>"{top_barrier}"</strong></p>
                <p>{top_barrier_count} คนจาก {total_barriers} คนที่ให้เหตุผล ({top_barrier_count/total_barriers*100:.1f}%)</p>
                <p><small>นี่คือประเด็นที่แบรนด์ควรแก้ไขเป็นอันดับแรก</small></p>
            </div>
            """
            
            # Actionable insights
            html_content += "<h3>ข้อเสนอแนะเชิงกลยุทธ์</h3>"
            
            # Analyze barriers and provide recommendations
            price_related = barrier_data['reason_not_chosen'].str.contains('แพง|ราคา|คุ้ม', case=False, na=False).sum()
            quality_related = barrier_data['reason_not_chosen'].str.contains('คุณภาพ|ทน|รีวิว', case=False, na=False).sum()
            availability_related = barrier_data['reason_not_chosen'].str.contains('หา|ซื้อ|ไม่รู้', case=False, na=False).sum()
            
            html_content += f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div class="metric-card">
                    <h4>Price-related Issues</h4>
                    <h2>{price_related}</h2>
                    <p>คน ({price_related/total_barriers*100:.1f}%)</p>
                </div>
                <div class="metric-card">
                    <h4>Quality-related Issues</h4>
                    <h2>{quality_related}</h2>
                    <p>คน ({quality_related/total_barriers*100:.1f}%)</p>
                </div>
                <div class="metric-card">
                    <h4>Availability Issues</h4>
                    <h2>{availability_related}</h2>
                    <p>คน ({availability_related/total_barriers*100:.1f}%)</p>
                </div>
            </div>
            """
    
    return html_content

def generate_personas_html(df):
    """Generate HTML content for personas page"""
    import plotly.express as px
    import pandas as pd
    import numpy as np
    
    html_content = "<h2>👥 Customer Personas - การวิเคราะห์กลุ่มลูกค้าเชิงลึก</h2>"
    
    html_content += """
    <div class="insight-box">
        <h4>การสร้าง Persona แบบ 360 องศา</h4>
        <p>การรวมวิเคราะห์ <strong>พฤติกรรม + ความเชื่อ + เหตุผล + ช่องทาง + ราคา</strong> เพื่อเข้าใจลูกค้าอย่างลึกซึ้ง</p>
    </div>
    """
    
    # Prepare data for clustering
    factor_cols = [c for c in df.columns if c.startswith('factor_')]
    price_cols = [c for c in df.columns if c.startswith('price_') and c not in ['price_midpoint', 'price_min', 'price_max', 'price_mid']]
    channel_cols = [c for c in df.columns if c.startswith('channel_')]
    promo_cols = [c for c in df.columns if c.startswith('promo_')]
    
    # Create persona analysis
    html_content += "<h3>การวิเคราะห์แบบกลุ่ม (Cluster Analysis)</h3>"
    
    # Prepare numerical data for clustering
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
    
    # Create persona distribution table
    html_content += """
    <table>
        <thead>
            <tr>
                <th>Persona Type</th>
                <th>จำนวน (คน)</th>
                <th>สัดส่วน (%)</th>
                <th>คุณลักษณะหลัก</th>
            </tr>
        </thead>
        <tbody>
    """
    
    persona_descriptions = {
        "Premium Quality Seeker": "มุ่งเน้นคุณภาพสูง ไม่ค่อยอ่อนไหวต่อราคา",
        "Value Hunter": "ต้องการคุณภาพดีในราคาที่คุ้มค่า",
        "Brand Loyalist": "ให้ความสำคัญกับแบรนด์และภาพลักษณ์",
        "Convenience Lover": "ต้องการความสะดวกสบายในการซื้อ",
        "Practical Buyer": "เน้นความเป็นจริงและการใช้งาน"
    }
    
    total_respondents = len(df_analysis)
    for persona_name, count in persona_counts.items():
        percentage = (count / total_respondents) * 100
        description = persona_descriptions.get(persona_name, "")
        html_content += f"""
            <tr>
                <td><strong>{persona_name}</strong></td>
                <td>{count}</td>
                <td>{percentage:.1f}%</td>
                <td>{description}</td>
            </tr>
        """
    
    html_content += """
        </tbody>
    </table>
    """
    
    try:
        fig_personas = px.pie(
            values=persona_counts.values,
            names=persona_counts.index,
            title="การกระจายตัวของ Persona",
            color_discrete_sequence=['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
        fig_personas.update_traces(textposition='inside', textinfo='percent+label')
        fig_personas.update_layout(font=dict(size=14), title=dict(font=dict(size=18)))
        personas_chart = plotly_to_base64(fig_personas)
        if personas_chart:
            html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{personas_chart}" style="max-width: 100%; height: auto;" alt="Persona Distribution Chart"></div>'
    except Exception as e:
        print(f"Error creating personas chart: {e}")
    
    # Price vs Quality Matrix
    try:
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
        fig_matrix.update_layout(height=400, font=dict(size=14), title=dict(font=dict(size=18)))
        matrix_chart = plotly_to_base64(fig_matrix)
        if matrix_chart:
            html_content += f'<div style="text-align: center; margin: 30px 0;"><img src="{matrix_chart}" style="max-width: 100%; height: auto;" alt="Price vs Quality Matrix"></div>'
    except Exception as e:
        print(f"Error creating matrix chart: {e}")
    
    # Detailed Persona Profiles
    html_content += "<h3>รายละเอียด Persona แต่ละกลุ่ม</h3>"
    
    for persona_name in persona_counts.index:
        persona_df = df_analysis[df_analysis['persona_type'] == persona_name]
        persona_count = persona_counts[persona_name]
        persona_percent = persona_count/len(df)*100
        
        html_content += f"""
        <div style="border: 2px solid #ddd; border-radius: 10px; padding: 20px; margin: 20px 0; background-color: #f9f9f9;">
            <h4 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                {persona_name} ({persona_count} คน - {persona_percent:.1f}%)
            </h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
        """
        
        # Demographics
        gender_dist = persona_df['gender'].value_counts()
        avg_age = persona_df['age'].mean()
        top_income = persona_df['monthly_income'].mode().iloc[0] if len(persona_df) > 0 else "ไม่ระบุ"
        
        html_content += f"""
            <div>
                <h5 style="color: #e74c3c;">Demographics</h5>
                <p>• <strong>เพศหลัก:</strong> {gender_dist.index[0]} ({gender_dist.iloc[0]} คน)</p>
                <p>• <strong>อายุเฉลี่ย:</strong> {avg_age:.0f} ปี</p>
                <p>• <strong>รายได้หลัก:</strong> {top_income}</p>
                
                <h5 style="color: #e74c3c;">พฤติกรรม</h5>
        """
        
        if 'luggage_frequency' in persona_df.columns:
            top_freq = persona_df['luggage_frequency'].mode().iloc[0] if len(persona_df) > 0 else "ไม่ระบุ"
            html_content += f"<p>• <strong>ความถี่ใช้งาน:</strong> {top_freq}</p>"
        
        if 'most_used_platform' in persona_df.columns:
            top_platform = persona_df['most_used_platform'].mode().iloc[0] if len(persona_df) > 0 else "ไม่ระบุ"
            html_content += f"<p>• <strong>แพลตฟอร์มหลัก:</strong> {top_platform}</p>"
        
        html_content += "</div><div>"
        
        # Values & Beliefs
        html_content += "<h5 style='color: #27ae60;'>ความเชื่อ & ค่านิยม</h5>"
        factor_scores = persona_df[factor_cols].mean().sort_values(ascending=False)
        html_content += "<p><strong>ปัจจัยสำคัญ Top 3:</strong></p>"
        for i, (factor, score) in enumerate(factor_scores.head(3).items()):
            factor_name = factor.replace('factor_', '').replace('_', ' ').title()
            html_content += f"<p>{i+1}. {factor_name}: {score:.1f}/5</p>"
        
        html_content += "<h5 style='color: #27ae60;'>ความอ่อนไหวต่อราคา</h5>"
        price_scores = persona_df[price_cols].mean().sort_values(ascending=False)
        for factor, score in price_scores.head(2).items():
            factor_name = factor.replace('price_', '').replace('_', ' ').title()
            html_content += f"<p>• {factor_name}: {score:.1f}/5</p>"
        
        html_content += "</div><div>"
        
        # Channels & Marketing
        html_content += "<h5 style='color: #9b59b6;'>ช่องทางที่ต้องการ</h5>"
        channel_scores = persona_df[channel_cols].mean().sort_values(ascending=False)
        for factor, score in channel_scores.head(3).items():
            factor_name = factor.replace('channel_', '').replace('_', ' ').title()
            html_content += f"<p>• {factor_name}: {score:.1f}/5</p>"
        
        html_content += "<h5 style='color: #9b59b6;'>การตลาดที่ได้ผล</h5>"
        promo_scores = persona_df[promo_cols].mean().sort_values(ascending=False)
        for factor, score in promo_scores.head(2).items():
            factor_name = factor.replace('promo_', '').replace('_', ' ').title()
            html_content += f"<p>• {factor_name}: {score:.1f}/5</p>"
        
        html_content += "</div></div></div>"
    
    # Marketing Strategy Recommendations
    html_content += "<h3>กลยุทธ์การตลาดเฉพาะกลุ่ม</h3>"
    
    strategy_mapping = {
        "Premium Quality Seeker": {
            "strategy": "เน้นคุณภาพพรีเมี่ยม",
            "messaging": "ความทนทาน, การรับประกัน, คุณภาพระดับโลก", 
            "channels": "ร้านค้าอย่างเป็นทางการ, เว็บไซต์แบรนด์",
            "promotion": "Bundle premium, ข้อมูลเชิงลึกเรื่องคุณภาพ",
            "color": "#e74c3c"
        },
        "Value Hunter": {
            "strategy": "เน้นความคุ้มค่า",
            "messaging": "คุณภาพดีในราคาที่เหมาะสม, เปรียบเทียบกับคู่แข่ง",
            "channels": "E-commerce, ส่วนลดออนไลน์",
            "promotion": "Flash sale, ส่วนลดพิเศษ, Bundle deal",
            "color": "#f39c12"
        },
        "Brand Loyalist": {
            "strategy": "เสริมสร้างภาพลักษณ์แบรนด์",
            "messaging": "ประวัติแบรนด์, เอกลักษณ์, สถานะทางสังคม",
            "channels": "Social media, Influencer, Event",
            "promotion": "Exclusive member, Limited edition",
            "color": "#9b59b6"
        },
        "Convenience Lover": {
            "strategy": "เน้นความสะดวกสบาย",
            "messaging": "ง่าย, รวดเร็ว, หาซื้อง่าย",
            "channels": "Online marketplace, ส่งด่วน",
            "promotion": "Free shipping, Same day delivery",
            "color": "#3498db"
        },
        "Practical Buyer": {
            "strategy": "เน้นความเป็นจริง",
            "messaging": "ใช้งานได้จริง, ตอบโจทย์ทุกการใช้งาน",
            "channels": "รีวิวจากผู้ใช้จริง, เปรียบเทียบสินค้า",
            "promotion": "ทดลองใช้, การันตีคืนเงิน",
            "color": "#27ae60"
        }
    }
    
    for persona_name in persona_counts.index:
        if persona_name in strategy_mapping:
            strategy = strategy_mapping[persona_name]
            color = strategy.get('color', '#2c3e50')
            html_content += f"""
            <div style="border-left: 5px solid {color}; padding: 15px; margin: 15px 0; background-color: #f8f9fa;">
                <h4 style="color: {color};">{persona_name} Strategy</h4>
                <p><strong>กลยุทธ์:</strong> {strategy['strategy']}</p>
                <p><strong>ข้อความ:</strong> {strategy['messaging']}</p>
                <p><strong>ช่องทาง:</strong> {strategy['channels']}</p>
                <p><strong>โปรโมชั่น:</strong> {strategy['promotion']}</p>
            </div>
            """
    
    return html_content

def export_current_page_to_pdf(page_name, df):
    """Export current page to PDF"""
    # Check PDF availability at runtime
    try:
        from weasyprint import HTML, CSS
        from jinja2 import Template
    except ImportError as e:
        return None, f"ไม่พบไลบรารี PDF: {str(e)} - กรุณาติดตั้ง weasyprint และ jinja2"
    
    try:
        # Get page content as HTML
        content_html = get_page_content_as_html(page_name, df)
        
        # Create template and render
        template = create_pdf_template()
        html_content = template.render(
            title="Suitcase Insights Dashboard",
            subtitle=f"หน้า: {page_name}",
            date=datetime.now().strftime("%d/%m/%Y %H:%M"),
            current_year=datetime.now().year,
            content=content_html
        )
        
        # Generate PDF with landscape orientation
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            HTML(string=html_content).write_pdf(
                tmp_file.name,
                stylesheets=[CSS(string='@page { size: A4 landscape; margin: 2cm; }')]
            )
            
            # Read PDF content
            with open(tmp_file.name, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            
            # Clean up
            os.unlink(tmp_file.name)
            
            return pdf_bytes, None
    
    except Exception as e:
        return None, f"เกิดข้อผิดพลาดในการสร้าง PDF: {str(e)}"

def create_pdf_download_button(page_name, df):
    """Create PDF download button for current page"""
    if st.button(f"Export หน้า '{page_name}' เป็น PDF", key=f"pdf_export_{page_name}"):
        with st.spinner("กำลังสร้าง PDF..."):
            pdf_bytes, error = export_current_page_to_pdf(page_name, df)
            
            if error:
                st.error(error)
            elif pdf_bytes:
                # Create download button
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                filename = f"suitcase_insights_{page_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
                href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{filename}">คลิกที่นี่เพื่อดาวน์โหลด PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("สร้าง PDF สำเร็จ! คลิกลิงค์ด้านบนเพื่อดาวน์โหลด")

def generate_complete_report_html(df):
    """Generate HTML content for complete report with all pages"""
    html_content = """
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #2c3e50; font-size: 2.5em; margin-bottom: 10px;">Suitcase Insights Report</h1>
        <h2 style="color: #7f8c8d; font-size: 1.5em; margin-bottom: 30px;">การวิเคราะห์พฤติกรรมผู้บริโภคกระเป๋าเดินทางแบบครบถ้วน</h2>
        <p style="color: #95a5a6; font-size: 1.1em;">สร้างเมื่อ: """ + pd.Timestamp.now().strftime("%d/%m/%Y %H:%M") + """</p>
    </div>
    
    <div style="page-break-after: always;"></div>
    
    <div style="margin-bottom: 40px;">
        <h2 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">สารบัญ</h2>
        <div style="margin-left: 20px; line-height: 2;">
            <p><strong>1. ภาพรวม (Overview)</strong> ................................. หน้า 3</p>
            <p><strong>2. ข้อมูลประชากร (Demographics)</strong> .................... หน้า 4</p>
            <p><strong>3. ปัจจัยในการตัดสินใจ (Decision Factors)</strong> ......... หน้า 5</p>
            <p><strong>4. ความชอบสินค้า (Product Preferences)</strong> .......... หน้า 6</p>
            <p><strong>5. ความอ่อนไหวต่อราคา (Price Sensitivity)</strong> ........ หน้า 7</p>
            <p><strong>6. ช่องทางการขาย (Sales Channels)</strong> ................ หน้า 8</p>
            <p><strong>7. การตลาด (Marketing Preferences)</strong> ............... หน้า 9</p>
            <p><strong>8. การรู้จักแบรนด์ (Brand Awareness)</strong> .............. หน้า 10</p>
            <p><strong>9. ภาพลักษณ์แบรนด์ (Brand Image & Barriers)</strong> ... หน้า 11</p>
            <p><strong>10. กลุ่มลูกค้า (Customer Personas)</strong> ............... หน้า 12</p>
        </div>
    </div>
    
    <div style="page-break-after: always;"></div>
    """
    
    # Add each page with page breaks
    pages = [
        ("1. ภาพรวม", generate_overview_html(df)),
        ("2. ข้อมูลประชากร", generate_demographics_html(df)),
        ("3. ปัจจัยในการตัดสินใจ", generate_factors_html(df)),
        ("4. ความชอบสินค้า", generate_products_html(df)),
        ("5. ความอ่อนไหวต่อราคา", generate_pricing_html(df)),
        ("6. ช่องทางการขาย", generate_channels_html(df)),
        ("7. การตลาด", generate_marketing_html(df)),
        ("8. การรู้จักแบรนด์", generate_brand_awareness_html(df)),
        ("9. ภาพลักษณ์แบรนด์", generate_brand_image_html(df)),
        ("10. กลุ่มลูกค้า", generate_personas_html(df))
    ]
    
    for i, (title, content) in enumerate(pages):
        html_content += f"""
        <div style="margin-bottom: 30px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 2em;">{title}</h1>
            </div>
            {content}
        </div>
        """
        
        # Add page break except for the last page
        if i < len(pages) - 1:
            html_content += '<div style="page-break-after: always;"></div>'
    
    return html_content

def create_complete_pdf_download_button(df):
    """Create download button for complete report PDF"""
    if not PDF_AVAILABLE:
        st.error("PDF export ไม่สามารถใช้งานได้ กรุณาติดตั้ง weasyprint และ jinja2")
        return
    
    if st.button("Export รายงานฉบับสมบูรณ์ (All Pages)", 
                 key="export_complete_pdf",
                 help="Export ทุกหน้าในรายงานเดียว"):
        
        try:
            with st.spinner("กำลังสร้างรายงานฉบับสมบูรณ์..."):
                # Generate complete HTML
                html_content = generate_complete_report_html(df)
                
                # Create PDF template
                template = create_pdf_template()
                full_html = template.render(
                    title="Suitcase Insights - Complete Report",
                    subtitle="การวิเคราะห์พฤติกรรมผู้บริโภคกระเป๋าเดินทางแบบครบถ้วน",
                    date=pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                    current_year=pd.Timestamp.now().year,
                    content=html_content
                )
                
                # Generate PDF with landscape orientation
                pdf_bytes = HTML(string=full_html).write_pdf(
                    stylesheets=[CSS(string='@page { size: A4 landscape; margin: 2cm; }')]
                )
                
                if pdf_bytes:
                    # Create download
                    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"suitcase_insights_complete_report_{timestamp}.pdf"
                    
                    st.download_button(
                        label="Download รายงานฉบับสมบูรณ์",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key="download_complete_pdf"
                    )
                    
                    st.success(f"สร้างรายงานฉบับสมบูรณ์เรียบร้อย! ({len(pdf_bytes)/1024:.1f} KB)")
                else:
                    st.error("ไม่สามารถสร้าง PDF ได้")
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการสร้าง PDF: {str(e)}")
            print(f"Complete PDF export error: {e}")

def main():
    st.title("Suitcase Insights Dashboard")
    st.markdown("### การวิเคราะห์ข้อมูลการสำรวจพฤติกรรมผู้บริโภคกระเป๋าเดินทาง")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Add complete report export button at the top
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        create_complete_pdf_download_button(df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("ภาพรวม", df)
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>ผู้เข้าร่วม</h3>
            <h2>{}</h2>
            <p>คน</p>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        avg_age = df['age'].mean()
        st.markdown("""
        <div class="metric-card">
            <h3>อายุเฉลี่ย</h3>
            <h2>{:.1f}</h2>
            <p>ปี</p>
        </div>
        """.format(avg_age), unsafe_allow_html=True)
    
    with col3:
        gender_counts = df['gender'].value_counts()
        female_count = gender_counts.get('หญิง', 0)
        st.markdown("""
        <div class="metric-card">
            <h3>เพศหญิง</h3>
            <h2>{}</h2>
            <p>คน ({:.1f}%)</p>
        </div>
        """.format(female_count, (female_count/len(df)*100)), unsafe_allow_html=True)
    
    with col4:
        student_pct = (df['occupation'] == 'นักเรียน/นักศึกษา').mean() * 100
        st.markdown("""
        <div class="metric-card">
            <h3>นักเรียน/นักศึกษา</h3>
            <h2>{:.1f}%</h2>
            <p>ของผู้ตอบ</p>
        </div>
        """.format(student_pct), unsafe_allow_html=True)
    
    # Gender breakdown section
    st.markdown("---")
    st.subheader("การกระจายตามเพศ")
    
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
    st.subheader("ข้อค้นพบสำคัญ")
    
    # Factor analysis
    factor_cols = [c for c in df.columns if c.startswith("factor_")]
    if factor_cols:
        factor_means = df[factor_cols].mean().sort_values(ascending=False)
        top_factor = factor_means.index[0].replace("factor_", "").replace("_", " ")
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>ปัจจัยสำคัญที่สุด</h4>
            <p><strong>{top_factor}</strong> ได้คะแนนเฉลี่ย {factor_means.iloc[0]:.2f} จาก 5</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Price sensitivity
    if 'preferred_price_range' in df.columns:
        popular_price = df['preferred_price_range'].mode().iloc[0] if not df['preferred_price_range'].mode().empty else "ไม่ระบุ"
        st.markdown(f"""
        <div class="insight-box">
            <h4>ช่วงราคาที่นิยม</h4>
            <p><strong>{popular_price}</strong> เป็นช่วงราคาที่ผู้ตอบแบบสำรวจเลือกมากที่สุด</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Travel frequency
    if 'luggage_frequency' in df.columns:
        popular_freq = df['luggage_frequency'].mode().iloc[0] if not df['luggage_frequency'].mode().empty else "ไม่ระบุ"
        st.markdown(f"""
        <div class="insight-box">
            <h4>ความถี่ในการเดินทาง</h4>
            <p><strong>{popular_freq}</strong> เป็นความถี่ที่พบมากที่สุด</p>
        </div>
        """, unsafe_allow_html=True)

def show_demographics(df):
    """Show demographics analysis"""
    st.header("ข้อมูลประชากรศาสตร์")
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("ข้อมูลประชากรศาสตร์", df)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        st.subheader("การกระจายตามเพศ")
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
        st.subheader("การกระจายตามอายุ")
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
        st.subheader("การกระจายตามรายได้")
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
    st.header("ปัจจัยการตัดสินใจซื้อกระเป๋าเดินทาง")
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("ปัจจัยการตัดสินใจ", df)
    st.markdown("---")
    
    factor_cols = [c for c in df.columns if c.startswith("factor_")]
    
    if not factor_cols:
        st.warning("ไม่พบข้อมูลปัจจัยการตัดสินใจ")
        return
    
    # Overall importance ranking
    st.subheader("ลำดับความสำคัญของปัจจัยโดยรวม")
    
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
        st.subheader("ปัจจัยความสำคัญตามเพศ")
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
        st.subheader("ปัจจัยความสำคัญตามรายได้")
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("ความต้องการผลิตภัณฑ์", df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("ความอ่อนไหวต่อราคา", df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("ช่องทางการขาย", df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("การตลาด", df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("Brand Awareness", df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("Brand Image & Barriers", df)
    st.markdown("---")
    
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
    
    # PDF Export Button
    st.markdown("---")
    create_pdf_download_button("Customer Personas", df)
    st.markdown("---")
    
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
        with st.expander(f"{persona_name} ({persona_counts[persona_name]} คน - {persona_counts[persona_name]/len(df)*100:.1f}%)"):
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
            "promotion": "Bundle premium, ข้อมูลเชิงลึกเรื่องคุณภาพ",
            "color": "#e74c3c"
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