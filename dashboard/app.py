import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import difflib
import ast
import operator
import re

st.set_page_config(page_title="Aswini B2B Analytics", page_icon="📊", layout="wide")

theme = st.query_params.get("theme", "light")
if theme not in ["light", "dark"]:
    theme = "light"
opposite_theme = "dark" if theme == "light" else "light"
theme_icon = "🌙 Dark Mode" if theme == "light" else "☀️ Light Mode"

# Define Ronas IT Logistics Theme for all charts
RONAS_COLORS = ["#10B981", "#3B82F6", "#6366F1", "#8B5CF6", "#EC4899", "#F43F5E", "#F59E0B", "#14B8A6"]

pio.templates["ronas_light"] = go.layout.Template(
    layout=go.Layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6B7280", family='"Glogmy", Copperplate, "SF Pro Display", sans-serif', size=15),
        hoverlabel=dict(font_size=16),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
        legend=dict(font=dict(size=15)),
        colorway=RONAS_COLORS
    )
)

pio.templates["ronas_dark"] = go.layout.Template(
    layout=go.Layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9CA3AF", family='"Glogmy", Copperplate, "SF Pro Display", sans-serif', size=15),
        hoverlabel=dict(font_size=16),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
        legend=dict(font=dict(size=15)),
        colorway=RONAS_COLORS
    )
)

pio.templates.default = f"ronas_{theme}"

from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit.components.v1 as components
import os
def render_chart(fig, **kwargs):
    fig.update_traces(textfont_size=18)
    st.plotly_chart(fig, **kwargs)



current_nav = st.query_params.get("nav", "matrix")

if theme == "light":
    css_vars = """
  --app-bg: #F9FAFB;
  --card-bg: #FFFFFF;
  --text-main: #111827;
  --text-muted: #6B7280;
  --accent: #10B981;
  --accent-hover: #059669;
  --border: #E5E7EB;
  --nav-bg: rgba(255, 255, 255, 0.85);
  --nav-border: rgba(229, 231, 235, 0.5);
  --nav-hover-bg: rgba(243, 244, 246, 0.8);
"""
else:
    css_vars = """
  --app-bg: #0B0F19;
  --card-bg: #111827;
  --text-main: #F9FAFB;
  --text-muted: #9CA3AF;
  --accent: #10B981;
  --accent-hover: #059669;
  --border: #1F2937;
  --nav-bg: rgba(17, 24, 39, 0.85);
  --nav-border: rgba(31, 41, 55, 0.5);
  --nav-hover-bg: rgba(31, 41, 55, 0.8);
"""

st.markdown(f"""
<style>
/* Hide the default streamlit header */
[data-testid="stHeader"] {{
    display: none;
}}
/* Push the main app content down */
[data-testid="stAppViewBlockContainer"] {{
    margin-top: 10px;
    padding-right: 230px !important;
}}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root{{
{css_vars}
  --font-main: "Inter", "SF Pro Display", -apple-system, sans-serif;
  --transition-smooth: 0.2s ease-in-out;
}}
.stApp {{
    background-color: var(--app-bg) !important;
    color: var(--text-main) !important;
    font-family: var(--font-main);
}}
h1, h2, h3, h4, h5, h6 {{
    color: var(--text-main) !important;
    font-family: var(--font-main) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}}
p, li, span, label {{
    color: var(--text-main);
    font-family: var(--font-main);
}}
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span, .stMarkdown h3, .stMarkdown h4, .stMarkdown p strong {{
    color: var(--text-main) !important;
    font-weight: 600 !important;
}}
/* Apply Principle Font safely without breaking icons */
.stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp table, .stApp td, .stApp th {{
    font-family: var(--font-main);
}}
/* Fix Expander (Filter) Titles and Arrows */
[data-testid="stExpander"] summary p {{
    color: var(--text-main) !important;
    font-weight: 600 !important;
}}
[data-testid="stExpander"] summary svg {{
    color: var(--text-main) !important;
    fill: var(--text-main) !important;
}}

/* Clean Premium Elevation for Cards and Charts */
.stMetric, [data-testid="stMetric"] {{
    background-color: var(--card-bg) !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 6px rgba(0,0,0,0.02) !important;
    border: 1px solid var(--border) !important;
    transition: transform var(--transition-smooth), box-shadow var(--transition-smooth), border-color var(--transition-smooth);
}}
.stMetric:hover, [data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
    border-color: #D1D5DB !important; 
}}

.stPlotlyChart, .stVegaLiteChart, [data-testid="stDataFrame"] {{
    background-color: var(--card-bg) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 6px rgba(0,0,0,0.02) !important;
    border: 1px solid var(--border) !important;
    transition: transform var(--transition-smooth), box-shadow var(--transition-smooth), border-color var(--transition-smooth);
}}
.stPlotlyChart:hover, .stVegaLiteChart:hover, [data-testid="stDataFrame"]:hover {{
    transform: translateY(-1px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}}

.stMetric label {{
    color: var(--text-muted) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}}
.stMetric [data-testid="stMetricValue"] {{
    color: var(--text-main) !important;
    font-family: var(--font-main) !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}}

/* Right-Side Vertical Navbar */
.liquid-nav {{
    position: fixed;
    top: 0;
    right: 0;
    width: 210px;
    height: 100vh;
    background: linear-gradient(180deg, rgba(236, 72, 153, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border-left: 1px solid rgba(236, 72, 153, 0.3);
    z-index: 999999;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    padding: 20px 12px 20px 12px;
    box-shadow: -6px 0 30px rgba(139, 92, 246, 0.08);
    overflow-y: auto;
    overflow-x: hidden;
}}
.liquid-nav::-webkit-scrollbar {{ display: none; }}

.nav-logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 0 18px 0;
    border-bottom: 1px solid rgba(236, 72, 153, 0.15);
    margin-bottom: 16px;
}}
.nav-logo-wrap img {{
    height: 36px;
    object-fit: contain;
}}

.nav-search-input {{
    width: 100%;
    padding: 8px 12px;
    border-radius: 10px;
    border: 1px solid rgba(236, 72, 153, 0.3);
    background: rgba(255,255,255,0.08);
    color: var(--text-main);
    font-family: var(--font-main);
    font-size: 0.82rem;
    outline: none;
    box-sizing: border-box;
    margin-bottom: 14px;
    transition: border-color var(--transition-smooth), box-shadow var(--transition-smooth);
}}
.nav-search-input:focus {{
    border-color: rgba(236, 72, 153, 0.6);
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.15);
}}

.nav-section-label {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0 6px;
    margin: 10px 0 4px 0;
    opacity: 0.6;
}}

.liquid-nav a {{
    text-decoration: none;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.87rem;
    padding: 9px 12px;
    border-radius: 9px;
    transition: all var(--transition-smooth);
    font-family: var(--font-main);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
    border: 1px solid transparent;
}}
.liquid-nav a:hover {{
    color: var(--text-main) !important;
    background: rgba(236, 72, 153, 0.1);
    border-color: rgba(236, 72, 153, 0.2);
    transform: translateX(-3px);
}}
.liquid-nav a.active-nav {{
    color: var(--text-main) !important;
    background: linear-gradient(90deg, rgba(236,72,153,0.15), rgba(139,92,246,0.15));
    border-color: rgba(236, 72, 153, 0.35);
    font-weight: 600;
}}

.nav-bottom {{
    margin-top: auto;
    padding-top: 14px;
    border-top: 1px solid rgba(236, 72, 153, 0.15);
    display: flex;
    flex-direction: column;
    gap: 6px;
}}
.gdrive-btn {{
    background: linear-gradient(135deg, #EC4899, #8B5CF6) !important;
    color: white !important;
    padding: 9px 12px !important;
    border-radius: 9px !important;
    border: none !important;
    font-size: 0.87rem !important;
    font-weight: 600 !important;
    text-align: center;
    justify-content: center;
    transition: opacity 0.2s, transform 0.2s;
    box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3);
    margin-bottom: 2px;
}}
.gdrive-btn:hover {{
    opacity: 0.88 !important;
    transform: translateX(-2px);
}}
.theme-btn {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(236, 72, 153, 0.2) !important;
    color: var(--text-muted) !important;
    font-size: 0.84rem !important;
    padding: 8px 12px !important;
    border-radius: 9px !important;
    cursor: pointer;
    text-align: center;
    justify-content: center;
    transition: all 0.2s;
}}
.theme-btn:hover {{
    background: rgba(236,72,153,0.1) !important;
    color: var(--text-main) !important;
}}
/* Style Streamlit Tabs */
[data-baseweb="tab-list"] {{
    gap: 10px;
    background-color: var(--card-bg);
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}}
[data-baseweb="tab"] {{
    background-color: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    color: var(--text-muted) !important;
    font-weight: 600;
}}
[aria-selected="true"] {{
    background-color: var(--accent) !important;
    color: white !important;
}}
</style>
<div class="liquid-nav">
    <div class="nav-logo-wrap">
        <img src="https://www.aswinicalicut.net/assets/img/logo/logo.png">
    </div>

    <form method="GET" style="margin:0;">
        <input type="hidden" name="nav" value="{current_nav}">
        <input type="hidden" name="theme" value="{theme}">
        <input type="hidden" name="splash" value="0">
        <input type="text" class="nav-search-input" name="search" placeholder="🔍 Search insights...">
    </form>

    <div class="nav-section-label">Navigation</div>
    <a href="?nav=executive&theme={theme}&splash=0" target="_self" class="{'active-nav' if current_nav == 'executive' else ''}">📊 Executive Summary</a>
    <a href="?nav=matrix&theme={theme}&splash=0" target="_self" class="{'active-nav' if current_nav == 'matrix' else ''}">🔢 B2B Matrix</a>
    <a href="?nav=specialty&theme={theme}&splash=0" target="_self" class="{'active-nav' if current_nav == 'specialty' else ''}">👨‍⚕️ Specialty Analysis</a>
    <a href="?nav=forecast&theme={theme}&splash=0" target="_self" class="{'active-nav' if current_nav == 'forecast' else ''}">🔮 Forecast</a>
    <a href="?nav=team&theme={theme}&splash=0" target="_self" class="{'active-nav' if current_nav == 'team' else ''}">👨‍💻 Application Team</a>

    <div class="nav-bottom">
        <a href="?nav={current_nav}&theme={opposite_theme}&splash=0" target="_self" class="theme-btn">{theme_icon} Toggle Theme</a>
        <a href="https://docs.google.com/spreadsheets/d/1uKVfuy_i6cZShQc4gWz69e-cYCSND6eT/edit?usp=sharing" class="gdrive-btn" target="_blank">💾 Master Data</a>
    </div>
</div>
""", unsafe_allow_html=True)

skip_splash = st.query_params.get("splash") == "0"
if "splash" in st.query_params:
    del st.query_params["splash"]

if 'splash_shown_final' not in st.session_state:
    st.session_state.splash_shown_final = True
    
    if not skip_splash:
        splash_html = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        
        .splash-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #111;
            background-image: radial-gradient(#444 20%, transparent 20%);
            background-size: 8px 8px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 9999999;
            animation: fadeOutSplash 1s ease-in-out forwards;
            animation-delay: 3.5s;
        }
        .splash-content {
            background: rgba(17, 17, 17, 0.85);
            padding: 40px;
            border: 2px solid #555;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            display: flex; flex-direction: column; align-items: center;
        }
        .splash-text-container {
            display: inline-block;
        }
        .splash-text {
            color: #fff;
            font-family: 'VT323', monospace;
            font-size: 48px;
            letter-spacing: 4px;
            margin: 0;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
            overflow: hidden;
            white-space: nowrap;
            border-right: 4px solid #fff;
            width: 0;
            animation: typing 1.5s steps(30, end) forwards, blink 0.75s step-end infinite;
            animation-delay: 0.5s;
        }
        .splash-sub {
            color: #aaa;
            font-family: 'VT323', monospace;
            font-size: 24px;
            letter-spacing: 2px;
            margin-top: 10px;
            opacity: 0;
            animation: fadeInDot 0.5s steps(5, end) forwards;
            animation-delay: 2.2s;
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        @keyframes blink {
            from, to { border-color: transparent }
            50% { border-color: #fff }
        }
        @keyframes fadeInDot {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        @keyframes fadeOutSplash {
            0% { opacity: 1; visibility: visible; }
            100% { opacity: 0; visibility: hidden; pointer-events: none; }
        }
        </style>
        <div class="splash-overlay">
            <div class="splash-content">
                <img src="https://www.aswinicalicut.net/assets/img/logo/logo.png" style="height: 50px; margin-bottom: 20px; filter: grayscale(100%) brightness(200%);">
                <div class="splash-text-container">
                    <div class="splash-text">ASWINI DIAGNOSTIC</div>
                </div>
                <div class="splash-sub">Executive Intelligence Platform</div>
            </div>
        </div>
        """
        st.markdown(splash_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DATA LOADING & PREPROCESSING
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, 'master_b2b_institution_records.csv')
    cols = ['report_month', 'institution_name', 'test_name', 'test_count', 'total_bill_amount', 
            'department', 'histo_cyto_group', 'is_outsourced']
    df = pd.read_csv(file_path, usecols=cols, low_memory=False)
    
    df['total_bill_amount'] = pd.to_numeric(df['total_bill_amount'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['test_count'] = pd.to_numeric(df['test_count'], errors='coerce').fillna(0).astype(int)
    
    lal_path_df = df[df['institution_name'] == 'Lal Path Labs'].copy()
    df = df[df['institution_name'] != 'Lal Path Labs']
    
    df['date'] = pd.to_datetime(df['report_month'], format='%B %Y', errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values('date')
    
    def classify_specialty(row):
        test = str(row['test_name']).upper()
        dept = str(row['department']).upper()
        
        if any(k in test for k in ['LIPID', 'CHOLESTEROL', 'TROPONIN', 'CK-MB', 'NT-PROBNP', 'APOLIPOPROTEIN', 'CPK']): return 'Cardiology'
        elif any(k in test for k in ['HCG', 'PROLACTIN', 'AMH', 'FSH', 'LH', 'TRIMESTER', 'PREGNANCY', 'PAP SMEAR', 'RUBELLA', 'OVARIAN']): return 'Gynecology'
        elif any(k in test for k in ['THYROID', 'TSH', 'T3', 'T4', 'HBA1C', 'GLUCOSE', 'INSULIN', 'CORTISOL', 'TESTOSTERONE', 'PTH', 'PARATHYROID']): return 'Endocrinology'
        elif any(k in test for k in ['PSA', 'SEMEN', 'URINE ROUTINE', 'URINE CULTURE']): return 'Urology'
        elif any(k in test for k in ['CREATININE', 'UREA', 'MICROALBUMIN', 'BUN', 'ELECTROLYTE', 'SODIUM', 'POTASSIUM']): return 'Nephrology'
        elif any(k in test for k in ['LIVER', 'LFT', 'BILIRUBIN', 'SGPT', 'SGOT', 'AMYLASE', 'LIPASE', 'ENDOSCOPY', 'STOOL', 'HCV', 'HBSAG']): return 'Gastroenterology'
        elif any(k in test for k in ['CA 125', 'CA 19', 'CA 15', 'CEA', 'AFP', 'TUMOR', 'BONE MARROW']) or 'CYTOLOGY' in dept: return 'Oncology'
        elif any(k in test for k in ['NEWBORN', 'METABOLIC SCREEN']): return 'Paediatrics'
        elif any(k in test for k in ['VITAMIN D', 'CALCIUM', 'URIC ACID', 'PHOSPHOROUS', 'BONE']): return 'Ortho'
        elif any(k in test for k in ['RHEUMATOID', 'ANTI CCP', 'ANA ', 'HLA']): return 'Physical Medicine'
        elif 'CSF' in test: return 'Neurology'
        elif any(k in test for k in ['FUNGUS', 'SKIN', 'SCRAPING']): return 'Dermatology'
        elif any(k in test for k in ['SPUTUM', 'TB', 'ACID FAST', 'AFB', 'MANTOUX']): return 'Pulmonology'
        elif any(k in test for k in ['SWAB', 'COVID']): return 'ENT'
        elif 'HISTOPATHOLOGY' in dept: return 'General Surgery'
        else: return 'General Medicine'
        
    df['doctor_specialty'] = df.apply(classify_specialty, axis=1)
    
    lal_path_df['date'] = pd.to_datetime(lal_path_df['report_month'], format='%B %Y', errors='coerce')
    lal_path_df = lal_path_df.dropna(subset=['date'])
    lal_path_df = lal_path_df.sort_values('date')
    lal_path_df['doctor_specialty'] = lal_path_df.apply(classify_specialty, axis=1)
    
    return df, lal_path_df

with st.spinner("Loading Aswini B2B Data..."):
    df, lal_path_df = load_data()

months_ordered = sorted(df['date'].unique())
month_labels = [pd.to_datetime(m).strftime('%B %Y') for m in months_ordered]

# ══════════════════════════════════════════════════════════════════
# ROUTING & FILTERS
# ══════════════════════════════════════════════════════════════════
nav = st.query_params.get("nav", "executive")

if nav not in ['team']:
    with st.expander("🛠️ Filter Data & Slicers", expanded=True):
        st.markdown("<div style='padding: 10px 0;'>", unsafe_allow_html=True)
        c_f1, c_f2 = st.columns([2, 1])
        with c_f1:
            start_month, end_month = st.select_slider(
                'Select Time Period',
                options=month_labels,
                value=(month_labels[0], month_labels[-1])
            )
        with c_f2:
            top_n = st.slider("Top Institutions", min_value=5, max_value=50, value=20, step=5)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    start_month, end_month = month_labels[0], month_labels[-1]
    top_n = 20

# Date Filtering Logic
start_date = pd.to_datetime(start_month, format='%B %Y')
end_date = pd.to_datetime(end_month, format='%B %Y')

mask = (df['date'] >= start_date) & (df['date'] <= end_date)
filtered_df = df.loc[mask]

inst_totals = filtered_df.groupby('institution_name')['total_bill_amount'].sum().reset_index()
top_institutions = inst_totals.nlargest(top_n, 'total_bill_amount')['institution_name'].tolist()
top_df = filtered_df[filtered_df['institution_name'].isin(top_institutions)]

if nav not in ['team']:
    hero_total_rev = filtered_df['total_bill_amount'].sum()
    hero_total_tests = filtered_df['test_count'].sum()
    hero_hc_tests = filtered_df[filtered_df['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
    hero_hc_pct = (hero_hc_tests / hero_total_tests * 100) if hero_total_tests > 0 else 0
    health_status = "🟢 Strong" if hero_hc_pct <= 50 else ("🟡 Monitor" if hero_hc_pct <= 80 else "🔴 High Risk")
    
    st.markdown(f"""
    <div style="background-color: var(--card-bg); padding: 24px; border-radius: 12px; margin-bottom: 24px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
            <div style="flex: 1; min-width: 300px;">
                <p style="color: var(--text-muted); font-size: 0.85rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">Executive Intelligence</p>
                <h2 style="margin: 0 0 12px 0; font-size: 1.5rem; font-weight: 600;">{start_month} to {end_month} Analysis</h2>
                <p style="margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5;">
                    Analyzing the top {top_n} institutions. Total B2B Revenue is at <strong>₹{hero_total_rev:,.0f}</strong> across <strong>{hero_total_tests:,}</strong> tests.
                </p>
            </div>
            <div style="background-color: var(--app-bg); padding: 16px; border-radius: 8px; border: 1px solid var(--border); min-width: 250px;">
                <p style="margin: 0 0 8px 0; font-size: 0.9rem; font-weight: 600;">Business Health: {health_status}</p>
                <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem; line-height: 1.4;">
                    Histo-Cyto concentration is {hero_hc_pct:.1f}%. 
                    {'Diversification is healthy.' if hero_hc_pct <= 50 else 'Monitor concentration risk.'}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ROUTING & SEARCH LOGIC
# ══════════════════════════════════════════════════════════════════
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

search_query = st.query_params.get("search", "").strip()

if search_query:
    if search_query not in st.session_state.recent_searches:
        st.session_state.recent_searches.insert(0, search_query)
        st.session_state.recent_searches = st.session_state.recent_searches[:5]
        
    st.header(f"🔎 Global Search Results for '{search_query}'")
    
    if st.session_state.recent_searches:
        st.markdown("**Recent Searches:** " + " • ".join([f"`{s}`" for s in st.session_state.recent_searches]))
    
    # 1. Math Evaluator
    try:
        clean_expr = re.sub(r'\s+', '', search_query)
        if re.match(r'^[\d\.\+\-\*\/\(\)]+$', clean_expr) and len(clean_expr) > 2:
            result = eval(clean_expr)
            st.info(f"🧮 **Spotlight Calculator:** `{search_query} = {result:,.2f}`")
    except Exception:
        pass
        
    # 2. Natural Language Aggregation
    query_lower = search_query.lower()
    agg_keywords = ['total', 'sum', 'avg', 'average', 'mean']
    metric_keywords = {{
        'revenue': 'total_bill_amount', 'bill': 'total_bill_amount', 'sales': 'total_bill_amount',
        'tests': 'test_count', 'count': 'test_count', 'volume': 'test_count'
    }}
    
    found_agg = next((kw for kw in agg_keywords if kw in query_lower), None)
    found_metric_word = next((kw for kw in metric_keywords.keys() if kw in query_lower), None)
    
    all_insts = df['institution_name'].dropna().unique().tolist()
    all_specs = df['doctor_specialty'].dropna().unique().tolist()
    all_depts = df['department'].dropna().unique().tolist()
    
    if found_agg and found_metric_word:
        target_col = metric_keywords[found_metric_word]
        subject = query_lower.replace(found_agg, "").replace(found_metric_word, "").replace("of", "").replace("for", "").replace("in", "").strip()
        
        if subject:
            inst_match = difflib.get_close_matches(subject, all_insts, n=1, cutoff=0.5)
            spec_match = difflib.get_close_matches(subject, all_specs, n=1, cutoff=0.5)
            dept_match = difflib.get_close_matches(subject, all_depts, n=1, cutoff=0.5)
            
            match_col, match_val = None, None
            if inst_match:
                match_col, match_val = 'institution_name', inst_match[0]
            elif spec_match:
                match_col, match_val = 'doctor_specialty', spec_match[0]
            elif dept_match:
                match_col, match_val = 'department', dept_match[0]
                
            if match_col:
                agg_df = df[df[match_col] == match_val]
                if found_agg in ['avg', 'average', 'mean']:
                    calc_val = agg_df[target_col].mean()
                    agg_name = "Average"
                else:
                    calc_val = agg_df[target_col].sum()
                    agg_name = "Total"
                st.success(f"✨ **Spotlight Intelligence:** {agg_name} {found_metric_word.title()} for **{match_val}** is **{calc_val:,.2f}**")
                
    # 3. Fuzzy Match Data Search
    st.markdown(f"Searching across Institutions, Doctor Specialties, and Lab Departments...")
    c1, c2, c3 = st.columns(3)
    
    inst_matches = difflib.get_close_matches(search_query, all_insts, n=15, cutoff=0.3)
    spec_matches = difflib.get_close_matches(search_query, all_specs, n=15, cutoff=0.3)
    dept_matches = difflib.get_close_matches(search_query, all_depts, n=15, cutoff=0.3)
    
    if not inst_matches:
        inst_matches = [x for x in all_insts if search_query.lower() in x.lower()]
    if not spec_matches:
        spec_matches = [x for x in all_specs if search_query.lower() in x.lower()]
    if not dept_matches:
        dept_matches = [x for x in all_depts if search_query.lower() in x.lower()]
        
    with c1:
        with st.expander(f"🏢 Institutions ({len(inst_matches)})", expanded=True):
            if inst_matches:
                st.dataframe(pd.DataFrame({"Matching Institutions": inst_matches}), use_container_width=True)
            else:
                st.info("No matches.")
                
    with c2:
        with st.expander(f"👨‍⚕️ Specialties ({len(spec_matches)})", expanded=True):
            if spec_matches:
                st.dataframe(pd.DataFrame({"Matching Specialties": spec_matches}), use_container_width=True)
            else:
                st.info("No matches.")
                
    with c3:
        with st.expander(f"🧪 Departments ({len(dept_matches)})", expanded=True):
            if dept_matches:
                st.dataframe(pd.DataFrame({"Matching Departments": dept_matches}), use_container_width=True)
            else:
                st.info("No matches.")
                
    st.subheader("Raw Data Preview")
    raw_matches = df[
        df['institution_name'].isin(inst_matches) |
        df['doctor_specialty'].isin(spec_matches) |
        df['department'].isin(dept_matches)
    ]
    if not raw_matches.empty:
        st.dataframe(raw_matches.head(100), use_container_width=True)
    else:
        st.warning("No data found.")

elif nav == "executive":
    st.header("Executive Summary")
    
    total_rev = filtered_df['total_bill_amount'].sum()
    total_tests = filtered_df['test_count'].sum()
    hc_tests = filtered_df[filtered_df['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
    other_tests = total_tests - hc_tests
    hc_pct = (hc_tests / total_tests * 100) if total_tests > 0 else 0
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px;">
        <div class="stMetric" title="Total revenue billed across selected institutions">
            <label>💰 Total B2B Revenue</label>
            <div data-testid="stMetricValue">₹ {total_rev:,.0f}</div>
        </div>
        <div class="stMetric" title="Total number of tests billed">
            <label>📋 Total Tests Billed</label>
            <div data-testid="stMetricValue">{total_tests:,}</div>
        </div>
        <div class="stMetric" title="Tests falling under Histopathology & Cytopathology">
            <label>🔬 Histo-Cyto Tests</label>
            <div data-testid="stMetricValue">{hc_tests:,}</div>
            <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 4px; font-weight: 500;">{hc_pct:.1f}% of total</div>
        </div>
        <div class="stMetric" title="Tests from all other departments">
            <label>🧪 Other Dept Tests</label>
            <div data-testid="stMetricValue">{other_tests:,}</div>
            <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 4px; font-weight: 500;">{(100-hc_pct):.1f}% of total</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader(f"🏆 Top {top_n} Institutions by Revenue")
    
    inst_breakdown = top_df.groupby(['institution_name', 'histo_cyto_group'])['total_bill_amount'].sum().reset_index()
    inst_order = inst_totals.nlargest(top_n, 'total_bill_amount').sort_values('total_bill_amount', ascending=True)['institution_name'].tolist()
    
    fig_bar = px.bar(
        inst_breakdown,
        x='total_bill_amount', 
        y='institution_name',
        color='histo_cyto_group',
        orientation='h',
        text_auto='.2s',
        title="📊 Revenue Breakdown by Category",
        labels={'total_bill_amount': 'Billed Amount (₹)', 'institution_name': '', 'histo_cyto_group': 'Category'},
        category_orders={'institution_name': inst_order},
        color_discrete_map={'Histopathology & Cytopathology': '#8B5E3C', 'Other Departments': '#C8A27C'}
    )
    fig_bar.update_layout(
        barmode='stack',
        height=650, 
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(rangeslider=dict(visible=True)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    render_chart(fig_bar, use_container_width=True)
    
    st.info(f"**Business Insight:** The top {top_n} institutions generate ₹{top_df['total_bill_amount'].sum():,.0f} in revenue. Focus retention and upsell efforts on the top 3 partners.")
    
    st.markdown("---")
    st.subheader("🥧 Department Share Analysis")
    
    c_filter, c_donut = st.columns([1, 2])
    
    with c_filter:
        st.markdown("#### 🏢 Filter by Institution")
        inst_options = ["Overall"] + top_institutions
        selected_inst = st.pills("Select Institution", options=inst_options, default="Overall")
        
        if selected_inst == "Overall":
            donut_df = filtered_df
            st.markdown("**Showing: Overall Share**")
        else:
            donut_df = filtered_df[filtered_df['institution_name'] == selected_inst]
            st.markdown(f"**Showing: {selected_inst}**")
            
    with c_donut:
        donut_hc_tests = donut_df[donut_df['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
        donut_total_tests = donut_df['test_count'].sum()
        donut_other_tests = donut_total_tests - donut_hc_tests
        
        labels = ['Histopathology & Cytopathology', 'Other Departments']
        values = [donut_hc_tests, donut_other_tests]
        
        fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#8B5E3C', '#C8A27C'])])
        fig_donut.update_layout(
            title="🎯 Share Distribution",
            height=500,
            showlegend=True, 
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1)
        )
        render_chart(fig_donut, use_container_width=True)
        st.info("**Business Insight:** A balanced share between Histo-Cyto and other departments indicates healthy service utilization and lower risk of dependency. Recommend cross-selling other lab tests to partners heavily skewed toward Histo-Cyto.")

# ══════════════════════════════════════════════════════════════════
# PARTNER EVALUATION MATRIX
# ══════════════════════════════════════════════════════════════════
elif nav == "matrix":
    st.header("⚖️ Partner Risk & Evaluation Matrix")
    
    total_overall_rev = filtered_df['total_bill_amount'].sum()
    
    eval_data = []
    for inst in top_institutions:
        idf = filtered_df[filtered_df['institution_name'] == inst]
        vol = idf['test_count'].sum()
        rev = idf['total_bill_amount'].sum()
        hc_vol = idf[idf['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
        oth_vol = vol - hc_vol
        hc_share = (hc_vol / vol * 100) if vol > 0 else 0
        
        rev_dependency = (rev / total_overall_rev * 100) if total_overall_rev > 0 else 0
        priority = "High" if rev_dependency > 5 else ("Medium" if rev_dependency > 2 else "Low")
        
        if hc_share > 80:
            status = "🔴 Cut Short (Excessive HC Concentration)"
        elif hc_share > 50:
            status = "🟡 Monitor (HC Dominant)"
        else:
            status = "🟢 Extend (Balanced / Other Dominant)"
            
        eval_data.append({
            'Institution': inst,
            'Total Volume': vol,
            'Total Revenue': rev,
            'Revenue Dependency %': round(rev_dependency, 1),
            'Business Priority': priority,
            'HC Volume': hc_vol,
            'Other Volume': oth_vol,
            'HC Share %': round(hc_share, 1),
            'Recommendation': status
        })
        
    eval_df = pd.DataFrame(eval_data)
    
    status_filter = st.multiselect("🎯 Filter Partner Recommendation Level", options=eval_df['Recommendation'].unique(), default=eval_df['Recommendation'].unique())
    filtered_eval_df = eval_df[eval_df['Recommendation'].isin(status_filter)]
    
    fig_scatter = px.scatter(
        filtered_eval_df,
        x='Total Volume',
        y='HC Share %',
        size='Total Revenue',
        color='Recommendation',
        hover_name='Institution',
        text='Institution',
        title="📌 Partner Risk Positioning",
        color_discrete_map={
            "🔴 Cut Short (Excessive HC Concentration)": "#4A3428",
            "🟡 Monitor (HC Dominant)": "#C8A27C",
            "🟢 Extend (Balanced / Other Dominant)": "#8B5E3C"
        },
        labels={'HC Share %': 'Histopathology & Cytopathology Share (%)'}
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Cutoff")
    fig_scatter.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="50% Threshold")
    fig_scatter.update_layout(height=600)
    render_chart(fig_scatter, use_container_width=True)
    
    st.info("**Business Insight:** Partners in the top-left quadrant are high-volume but overly dependent on Histo-Cyto. Diversify their test portfolio to reduce risk.")
    
    st.subheader("📋 Partner Action Table")
    
    def highlight_priority(val):
        if val == 'High': return 'background-color: #FEE2E2; color: #991B1B'
        elif val == 'Medium': return 'background-color: #FEF3C7; color: #92400E'
        return 'background-color: #D1FAE5; color: #065F46'
        
    st.dataframe(
        filtered_eval_df.sort_values('HC Share %', ascending=False)
        .style.background_gradient(subset=['HC Share %', 'Revenue Dependency %'], cmap='Reds')
        .map(highlight_priority, subset=['Business Priority']),
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Deep Drill-down: 'Other' Departments")
    
    st.markdown("#### 📅 Monthly Department Share Table")
    c1, c2, c3 = st.columns(3)
    with c1:
        inst_filter = st.multiselect("🏢 Filter by Institution", options=top_institutions, default=top_institutions[:5])
    with c2:
        dept_opts = top_df[~top_df['department'].str.contains('Unmapped', na=False, case=False)]['department'].dropna().unique().tolist()
        dept_filter = st.multiselect("🧪 Filter by Department", options=dept_opts, default=dept_opts[:5] if len(dept_opts)>5 else dept_opts)
    with c3:
        month_opts = top_df['report_month'].dropna().unique().tolist()
        month_filter = st.multiselect("🗓️ Filter by Month", options=month_opts, default=month_opts)
    
    top_df_clean = top_df[~top_df['department'].str.contains('Unmapped', na=False, case=False)]
    monthly_dept = top_df_clean.groupby(['institution_name', 'date', 'report_month', 'department'])['test_count'].sum().reset_index()
    monthly_totals = top_df_clean.groupby(['institution_name', 'date', 'report_month'])['test_count'].sum().reset_index().rename(columns={'test_count': 'total_tests'})
    
    monthly_dept = monthly_dept.merge(monthly_totals, on=['institution_name', 'date', 'report_month'])
    monthly_dept['Share %'] = (monthly_dept['test_count'] / monthly_dept['total_tests'] * 100).round(1)
    
    md_filtered = monthly_dept[
        (monthly_dept['institution_name'].isin(inst_filter)) & 
        (monthly_dept['department'].isin(dept_filter)) &
        (monthly_dept['report_month'].isin(month_filter))
    ]
    md_filtered = md_filtered.sort_values(['institution_name', 'date', 'test_count'], ascending=[True, True, False])
    
    st.dataframe(
        md_filtered[['institution_name', 'report_month', 'department', 'test_count', 'Share %']],
        use_container_width=True,
        hide_index=True
    )
    
    extend_insts = eval_df[eval_df['Recommendation'] == '🟢 Extend (Balanced / Other Dominant)']['Institution'].tolist()
    if extend_insts:
        drill_df = filtered_df[(filtered_df['institution_name'].isin(extend_insts)) & 
                               (filtered_df['histo_cyto_group'] != 'Histopathology & Cytopathology') & 
                               (~filtered_df['department'].str.contains('Unmapped', na=False, case=False))]
        drill_grouped = drill_df.groupby(['institution_name', 'department'])['test_count'].sum().reset_index()
        
        fig_drill = px.bar(
            drill_grouped,
            x='institution_name',
            y='test_count',
            color='department',
            title="📊 Breakdown of 'Other' Tests for Balanced Partners",
            labels={'institution_name': 'Institution', 'test_count': 'Volume'}
        )
        fig_drill.update_layout(barmode='stack', xaxis_tickangle=-45)
        render_chart(fig_drill, use_container_width=True)
        
    st.markdown("---")
    st.subheader("💡 Special Insight: Dr. Lal Path Labs")
    
    lal_rev = lal_path_df['total_bill_amount'].sum()
    lal_tests = lal_path_df['test_count'].sum()
    lal_hc = lal_path_df[lal_path_df['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
    lal_other = lal_tests - lal_hc
    lal_months = lal_path_df['report_month'].nunique()
    
    if lal_tests > 0:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Total Revenue", f"₹ {lal_rev:,.0f}")
        c2.metric("📋 Total Tests", f"{lal_tests:,}")
        c3.metric("🔬 Histo-Cyto Share", f"{lal_hc:,} ({(lal_hc/lal_tests*100) if lal_tests else 0:.1f}%)")
        c4.metric("🧪 Other Share", f"{lal_other:,} ({(lal_other/lal_tests*100) if lal_tests else 0:.1f}%)")
        
        st.info(f"**Note:** Dr. Lal Path Labs has been excluded from the main dashboard rankings to prevent skewing the partner analysis. Across all available data ({lal_months} months), they have contributed ₹{lal_rev:,.0f} from {lal_tests:,} tests.")
        
        st.markdown("**🗓️ Monthly Department Breakdown (Lal Path Labs)**")
        lal_monthly = lal_path_df.groupby(['report_month', 'department'])['test_count'].sum().reset_index()
        lal_pivot = lal_monthly.pivot(index='report_month', columns='department', values='test_count').fillna(0).astype(int)
        st.dataframe(lal_pivot.style.background_gradient(cmap='YlGnBu'), use_container_width=True)

elif nav == "specialty":
    st.header("👨‍⚕️ Doctor Specialty & Prescription Pattern Analysis")
    st.markdown("This section maps test departments to inferred Doctor Specialties to analyze prescription patterns from our top B2B partners.")
    
    # 1. Overall Specialty Volume Trend
    st.subheader("📈 Monthly Test Volume by Doctor Specialty")
    spec_monthly = filtered_df.groupby(['date', 'report_month', 'doctor_specialty'])['test_count'].sum().reset_index()
    fig_spec_trend = px.area(spec_monthly, x='date', y='test_count', color='doctor_specialty',
                             title="Test Volume Over Time by Specialty",
                             labels={'test_count': 'Total Tests', 'date': 'Month'},
                             template='plotly_white')
    render_chart(fig_spec_trend, use_container_width=True)
    
    st.divider()
    
    # 2. Top Hospitals by Specialty Breakdown
    st.subheader("🏥 Top Hospitals driving Specialty Volumes")
    c1, c2 = st.columns([1, 2])
    with c1:
        specialties = filtered_df['doctor_specialty'].unique().tolist()
        selected_spec = st.selectbox("Select a Doctor Specialty to analyze:", specialties)
    
    with c2:
        spec_inst_df = filtered_df[filtered_df['doctor_specialty'] == selected_spec]
        spec_inst_grouped = spec_inst_df.groupby('institution_name')['test_count'].sum().reset_index().sort_values('test_count', ascending=False).head(10)
        
        fig_spec_hosp = px.bar(spec_inst_grouped, x='test_count', y='institution_name', orientation='h',
                               title=f"Top 10 Partners prescribing {selected_spec} tests",
                               labels={'test_count': 'Total Tests', 'institution_name': 'Institution'},
                               color='test_count', color_continuous_scale='Purples')
        fig_spec_hosp.update_layout(yaxis={'categoryorder':'total ascending'})
        render_chart(fig_spec_hosp, use_container_width=True)
    
    st.divider()
    
    # 3. Specialty to Department Mapping Visualization
    st.subheader("🔗 Prescription Pattern: Specialty to Department Flow")
    st.markdown("Understand which specific lab departments make up the selected Doctor Specialty.")
    flow_df = filtered_df.groupby(['doctor_specialty', 'department'])['test_count'].sum().reset_index()
    fig_flow = px.sunburst(flow_df, path=['doctor_specialty', 'department'], values='test_count',
                           title="Distribution of Tests from Specialty down to Department",
                           color='test_count', color_continuous_scale='Teal')
    fig_flow.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    render_chart(fig_flow, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PREDICTIVE FORECAST
# ══════════════════════════════════════════════════════════════════
elif nav == "forecast":
    st.header("🔮 August 2027 Summary Forecast (Top 20 Partners)")
    
    aug_2027_data = []
    target_date = pd.to_datetime('August 2027', format='%B %Y')
    
    for inst in top_institutions:
        inst_df = df[df['institution_name'] == inst].copy()
        ts_inst = inst_df.groupby('date').apply(
            lambda x: pd.Series({'total_tests': x['test_count'].sum()}), include_groups=False
        ).reset_index()
        
        if len(ts_inst) >= 3:
            X_inst = np.arange(len(ts_inst)).reshape(-1, 1)
            model_vol_inst = LinearRegression().fit(X_inst, ts_inst['total_tests'])
            
            last_date_inst = ts_inst['date'].max()
            months_diff = (target_date.year - last_date_inst.year) * 12 + (target_date.month - last_date_inst.month)
            future_idx = len(ts_inst) - 1 + months_diff
            pred_vol = max(0, model_vol_inst.predict([[future_idx]])[0])
            
            aug_2027_data.append({'Institution': inst, 'Projected Test Volume': int(round(pred_vol))})
            
    if aug_2027_data:
        aug_df = pd.DataFrame(aug_2027_data).sort_values('Projected Test Volume', ascending=False)
        
        show_top_n = st.slider("🔢 Select Number of Partners to highlight in Summary", 3, 10, 5)
        
        c_top, c_least = st.columns(2)
            
        with c_top:
            st.success(f"🏆 Top {show_top_n} Performing Partners (Aug 2027)")
            st.dataframe(aug_df.head(show_top_n), hide_index=True, use_container_width=True)
        with c_least:
            st.error(f"📉 Least {show_top_n} Performing Partners (Aug 2027)")
            st.dataframe(aug_df.tail(show_top_n), hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    st.header("📈 6-Month Predictive Forecast (Individual Analysis)")
    
    forecast_inst = st.selectbox("🎯 Select Partner to Forecast", top_institutions)
    
    inst_df = df[df['institution_name'] == forecast_inst].copy()
    ts = inst_df.groupby('date').apply(
        lambda x: pd.Series({
            'total_tests': x['test_count'].sum(),
            'hc_tests': x[x['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
        }), include_groups=False
    ).reset_index()
    
    if len(ts) < 3:
        st.warning("⚠️ Not enough historical data to generate a forecast for this partner.")
    else:
        ts['hc_share'] = (ts['hc_tests'] / ts['total_tests'] * 100).fillna(0)
        
        ts['month_index'] = np.arange(len(ts))
        X = ts[['month_index']].values
        
        model_vol = LinearRegression().fit(X, ts['total_tests'])
        model_share = LinearRegression().fit(X, ts['hc_share'])
        
        last_date = ts['date'].max()
        future_dates = [last_date + relativedelta(months=i) for i in range(1, 7)]
        future_indices = np.arange(len(ts), len(ts) + 6).reshape(-1, 1)
        
        future_vol = np.maximum(0, model_vol.predict(future_indices))
        future_share = np.clip(model_share.predict(future_indices), 0, 100)
        
        hist_df = pd.DataFrame({'Date': ts['date'], 'Type': 'Historical', 'Total Volume': ts['total_tests'], 'HC Share %': ts['hc_share']})
        pred_df = pd.DataFrame({'Date': future_dates, 'Type': 'Forecast (6 Months)', 'Total Volume': future_vol, 'HC Share %': future_share})
        combined = pd.concat([hist_df, pred_df], ignore_index=True)
        
        r2_score = model_vol.score(X, ts['total_tests'])
        confidence = "High (Stable historical pattern)" if r2_score > 0.6 else "Moderate (High variance)"
        growth_outlook = "Positive 📈" if future_vol[-1] > ts['total_tests'].iloc[-1] else "Negative/Flat 📉"
        
        st.markdown(f"""
        <div style="background-color: var(--card-bg); padding: 16px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 24px; display: flex; gap: 24px; align-items: center;">
            <div>
                <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Growth Outlook</p>
                <p style="margin: 0; font-weight: 600; font-size: 1.1rem;">{growth_outlook}</p>
            </div>
            <div style="width: 1px; height: 30px; background-color: var(--border);"></div>
            <div>
                <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Confidence Level</p>
                <p style="margin: 0; font-weight: 600; font-size: 1.1rem;">{confidence}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        
        with c1:
            fig_vol_proj = px.line(combined, x='Date', y='Total Volume', color='Type', markers=True, title="📈 Test Volume Projection", line_dash='Type')
            render_chart(fig_vol_proj, use_container_width=True)
            
        with c2:
            fig_share_proj = px.line(combined, x='Date', y='HC Share %', color='Type', markers=True, title="📉 Histo-Cyto Share % Projection", line_dash='Type')
            fig_share_proj.update_layout(yaxis=dict(range=[0, 100]))
            fig_share_proj.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Cutoff Danger Zone")
            render_chart(fig_share_proj, use_container_width=True)
            
        trend_dir = "increasing ↗️" if future_share[-1] > ts['hc_share'].iloc[-1] else "decreasing ↘️"
        st.info(f"**🤖 AI Insight for {forecast_inst}:** The Histo-Cyto share is projected to **{trend_dir}**, reaching **{future_share[-1]:.1f}%** by {future_dates[-1].strftime('%B %Y')}.")

# ══════════════════════════════════════════════════════════════════
# APPLICATION TEAM
# ══════════════════════════════════════════════════════════════════
elif nav == "team":
    st.header("👨‍💻 Application Team")
    st.markdown("Meet the team responsible for building and maintaining the B2B Analytics infrastructure at Aswini Diagnostic Services.")
    
    st.markdown("""
    <style>
    .team-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 32px 24px;
        text-align: center;
        transition: transform var(--transition-smooth), box-shadow var(--transition-smooth);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .team-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
        border-color: #D1D5DB;
    }
    .team-icon {
        font-size: 3rem; margin-bottom: 16px;
    }
    .team-name {
        margin: 0; font-size: 1.25rem; font-weight: 600; color: var(--text-main);
    }
    .team-role {
        color: var(--accent); font-weight: 500; font-size: 0.95rem; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .team-desc {
        color: var(--text-muted); font-size: 0.9rem; margin-top: 16px; line-height: 1.5;
    }
    </style>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-top: 32px; padding-bottom: 40px;">
        <div class="team-card">
            <div class="team-icon">👔</div>
            <h3 class="team-name">Mr. Harikrishnan R</h3>
            <p class="team-role">Application Manager</p>
            <p class="team-desc">Strategic oversight and management, ensuring the B2B platform aligns with business objectives and scalability goals.</p>
        </div>
        <div class="team-card">
            <div class="team-icon">💻</div>
            <h3 class="team-name">Mr. Mohammed Falah K</h3>
            <p class="team-role">Application Specialist</p>
            <p class="team-desc">Lead developer driving architectural improvements, performance optimization, and UI/UX modernization.</p>
        </div>
        <div class="team-card">
            <div class="team-icon">🚀</div>
            <h3 class="team-name">Mr. Nidhin U K</h3>
            <p class="team-role">Application Specialist</p>
            <p class="team-desc">Focused on seamless deployment, feature integration, and maintaining high availability across all instances.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
