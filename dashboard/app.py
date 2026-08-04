import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Aswini B2B Analytics", page_icon="📊", layout="wide")

sound_js = """
<script>
if (window.parent && window.parent.document && !window.parent.window.__soundEngineInit) {
    window.parent.window.__soundEngineInit = true;
    const AudioContext = window.parent.window.AudioContext || window.parent.window.webkitAudioContext;
    const audioCtx = new AudioContext();
    
    window.parent.window.playClickSound = function() {
        if (audioCtx.state === 'suspended') { audioCtx.resume(); }
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
    };

    window.parent.window.playIntroSound = function() {
        if (audioCtx.state === 'suspended') { audioCtx.resume(); }
        const freqs = [220, 277.18, 329.63, 440]; 
        freqs.forEach(f => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.value = f;
            gain.gain.setValueAtTime(0, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.03, audioCtx.currentTime + 2);
            gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 6);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 6);
        });
    };

    window.parent.document.addEventListener('click', function(e) {
        window.parent.window.playClickSound();
    });
}
</script>
"""
components.html(sound_js, height=0, width=0)

st.markdown("""
<style>
/* Hide the default streamlit header */
[data-testid="stHeader"] {
    display: none;
}
/* Push the main app content down */
[data-testid="stAppViewBlockContainer"] {
    margin-top: 90px;
}
:root{
  --brown-900:#4A3428;
  --brown-700:#6C4A34;
  --brown-600:#8B5E3C;
  --brown-500:#A97852;
  --brown-300:#C8A27C;
  --cream:#F8F4EE;
  --offwhite:#FCFAF7;
  --beige:#F1E8DE;
  --text:#1A1A1A;
  --text-secondary:#4A4A4A;
  --border:#DED4C7;
  --aswini-blue: #0B6FB8;
  --aswini-dark: #0A4E8A;
  --font-apple: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}
.stApp {
    background-color: var(--cream);
    color: var(--text) !important;
    font-family: var(--font-apple);
}
h1, h2, h3, h4, h5, h6 {
    color: var(--brown-900) !important;
    font-family: var(--font-apple) !important;
    font-weight: 700 !important;
}
p, li, span, label {
    color: var(--text);
    font-family: var(--font-apple);
}
.stMetric {
    background-color: var(--offwhite) !important;
    padding: 15px !important;
    border-radius: 12px !important;
    border-left: 5px solid var(--brown-600) !important;
    border: 1px solid var(--border);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.stMetric label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}
.stMetric [data-testid="stMetricValue"] {
    color: var(--brown-900) !important;
    font-family: var(--font-apple) !important;
    font-weight: 700 !important;
}
/* The Liquid Glass Navbar */
.liquid-nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    z-index: 999999;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}
.liquid-nav a {
    text-decoration: none;
    color: var(--text);
    font-weight: 600;
    font-size: 0.95rem;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-family: var(--font-apple);
}
.liquid-nav a:hover {
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
    color: #FFFFFF !important;
}
.nav-center {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 15px;
}
.nav-center img {
    height: 55px;
    object-fit: contain;
}
.gdrive-btn {
    background: linear-gradient(135deg, var(--aswini-blue), var(--aswini-dark)) !important;
    color: white !important;
    padding: 8px 20px !important;
    border-radius: 30px !important;
    box-shadow: 0 4px 15px rgba(11, 111, 184, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    animation: pulse 2s infinite;
}
.gdrive-btn:hover {
    background: linear-gradient(135deg, var(--aswini-dark), #05325c) !important;
    transform: scale(1.05);
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(11, 111, 184, 0.6); }
    70% { box-shadow: 0 0 0 10px rgba(11, 111, 184, 0); }
    100% { box-shadow: 0 0 0 0 rgba(11, 111, 184, 0); }
}
</style>
<div class="liquid-nav">
    <a href="?nav=matrix&splash=0">📊 B2B Matrix</a>
    <a href="?nav=executive&splash=0">📈 Executive Summary</a>
    <img src="https://www.aswinicalicut.net/assets/img/logo/logo.png" style="height:40px; margin:0 15px;">
    <a href="?nav=specialty&splash=0">👨‍⚕️ Specialty Analysis</a>
    <a href="?nav=forecast&splash=0">🔮 Forecast</a>
    <a href="?nav=team&splash=0">👨‍💻 Application Team</a>
    <a href="https://docs.google.com/spreadsheets/d/1uKVfuy_i6cZShQc4gWz69e-cYCSND6eT/edit?usp=sharing&ouid=109163273083599607293&rtpof=true&sd=true" class="gdrive-btn" target="_blank">💾 Master Data</a>
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
        .splash-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: #000000;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: fadeOut 1.5s ease-in-out 4s forwards;
        }
        .splash-logo {
            width: 280px;
            opacity: 0;
            position: absolute;
            animation: showLogo 2s ease-in-out 0.5s forwards;
        }
        .splash-text-container {
            position: absolute;
            top: 65%;
            text-align: center;
            opacity: 0;
            animation: showText 1.5s ease-in-out 1.5s forwards;
        }
        .splash-text-container h1 {
            color: #FFFFFF;
            font-family: var(--font-apple);
            font-size: 3rem;
            margin: 0 0 10px 0;
            font-weight: 300;
            letter-spacing: 1px;
        }
        .splash-text-container p {
            color: #A78BFA;
            font-family: var(--font-apple);
            font-size: 1.2rem;
            margin: 0;
            letter-spacing: 3px;
            animation: showSubText 1s ease-in-out 2.5s forwards;
            opacity: 0;
        }
        @keyframes showLogo {
            0% { opacity: 0; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1); }
        }
        @keyframes showText {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes showSubText {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeOut {
            0% { opacity: 1; visibility: visible; }
            100% { opacity: 0; visibility: hidden; pointer-events: none; }
        }
        </style>
        <div class="splash-overlay">
            <img src="https://www.aswinicalicut.net/assets/img/logo/logo.png" class="splash-logo">
            <div class="splash-text-container">
                <h1>ADS - B2B Analysis</h1>
                <p>by Application Team</p>
            </div>
        </div>
        """
        st.markdown(splash_html, unsafe_allow_html=True)
        components.html("""
        <script>
        setTimeout(() => {
            if (window.parent && window.parent.window.playIntroSound) {
                window.parent.window.playIntroSound();
            }
        }, 500);
        </script>
        """, height=0, width=0)

# ══════════════════════════════════════════════════════════════════
# DATA LOADING & PREPROCESSING
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, 'master_b2b_institution_records.csv')
    cols = ['report_month', 'institution_name', 'test_count', 'total_bill_amount', 
            'department', 'histo_cyto_group', 'is_outsourced']
    df = pd.read_csv(file_path, usecols=cols, low_memory=False)
    
    df['total_bill_amount'] = pd.to_numeric(df['total_bill_amount'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['test_count'] = pd.to_numeric(df['test_count'], errors='coerce').fillna(0).astype(int)
    
    lal_path_df = df[df['institution_name'] == 'Lal Path Labs'].copy()
    df = df[df['institution_name'] != 'Lal Path Labs']
    
    df['date'] = pd.to_datetime(df['report_month'], format='%B %Y', errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values('date')
    
    SPECIALTY_MAP = {
        'CLINICAL BIOCHEMISTRY': 'General Medicine',
        'CLINICAL PATHOLOGY': 'General Medicine',
        'HISTOPATHOLOGY & CYTOPATHOLOGY': 'Oncology & Surgery',
        'MOLECULAR BIOLOGY': 'Genetics / Molecular Oncology',
        'HAEMATOLOGY': 'Hematology',
        'MICROBIOLOGY': 'Infectious Diseases',
        'SEROLOGY': 'Infectious Diseases',
        'IMMUNOLOGY': 'Rheumatology / Immunology'
    }
    df['doctor_specialty'] = df['department'].str.upper().map(SPECIALTY_MAP).fillna('Other / Unmapped')
    
    lal_path_df['date'] = pd.to_datetime(lal_path_df['report_month'], format='%B %Y', errors='coerce')
    lal_path_df = lal_path_df.dropna(subset=['date'])
    lal_path_df = lal_path_df.sort_values('date')
    
    return df, lal_path_df

with st.spinner("Loading Aswini B2B Data..."):
    df, lal_path_df = load_data()

months_ordered = sorted(df['date'].unique())
month_labels = [pd.to_datetime(m).strftime('%B %Y') for m in months_ordered]

# ══════════════════════════════════════════════════════════════════
# ROUTING & FILTERS
# ══════════════════════════════════════════════════════════════════
nav = st.query_params.get("nav", "executive")

with st.expander("🛠️ Filter Data & Slicers", expanded=False if nav == 'team' else True):
    c1, c2 = st.columns(2)
    with c1:
        start_month, end_month = st.select_slider(
            '📅 Select Time Period',
            options=month_labels,
            value=(month_labels[0], month_labels[-1])
        )
    with c2:
        top_n = st.slider("🏢 Number of Top Institutions", min_value=5, max_value=50, value=20, step=5)

# Date Filtering Logic
start_date = pd.to_datetime(start_month, format='%B %Y')
end_date = pd.to_datetime(end_month, format='%B %Y')

mask = (df['date'] >= start_date) & (df['date'] <= end_date)
filtered_df = df.loc[mask]

inst_totals = filtered_df.groupby('institution_name')['total_bill_amount'].sum().reset_index()
top_institutions = inst_totals.nlargest(top_n, 'total_bill_amount')['institution_name'].tolist()
top_df = filtered_df[filtered_df['institution_name'].isin(top_institutions)]

st.markdown(f"""
<div style="background-color: var(--offwhite); padding: 15px; border-radius: 12px; border-left: 6px solid var(--brown-500); margin-bottom: 25px; border: 1px solid var(--border); box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
    <h4 style="margin-top: 0; margin-bottom: 8px; color: var(--brown-900) !important; font-size: 1.5rem; font-family: var(--font-apple);">
        📅 <strong>Period:</strong> {start_month} to {end_month} &nbsp;|&nbsp; 🏢 <strong>Analyzing Top {top_n} Institutions</strong>
    </h4>
    <p style="margin: 0; color: var(--brown-600) !important; font-weight: 500; font-size: 0.95rem; font-family: var(--font-apple);">
        ✨ <span style="background-color: #F8F4EE; padding: 2px 6px; border-radius: 4px;">Created by Application Team, Aswini Diagnostic Services</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════
if nav == "executive":
    st.header("📈 Overall Performance & Department Split")
    
    total_rev = filtered_df['total_bill_amount'].sum()
    total_tests = filtered_df['test_count'].sum()
    hc_tests = filtered_df[filtered_df['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
    other_tests = total_tests - hc_tests
    hc_pct = (hc_tests / total_tests * 100) if total_tests > 0 else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total B2B Revenue", f"₹ {total_rev:,.0f}")
    c2.metric("📋 Total Tests Billed", f"{total_tests:,}")
    c3.metric("🔬 Histo-Cyto Tests", f"{hc_tests:,}", f"{hc_pct:.1f}% of total", delta_color="off")
    c4.metric("🧪 Other Dept Tests", f"{other_tests:,}", f"{(100-hc_pct):.1f}% of total", delta_color="off")
        
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
    st.plotly_chart(fig_bar, use_container_width=True)
    
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
        st.plotly_chart(fig_donut, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PARTNER EVALUATION MATRIX
# ══════════════════════════════════════════════════════════════════
elif nav == "matrix":
    st.header("⚖️ Partner Risk & Evaluation Matrix")
    
    eval_data = []
    for inst in top_institutions:
        idf = filtered_df[filtered_df['institution_name'] == inst]
        vol = idf['test_count'].sum()
        rev = idf['total_bill_amount'].sum()
        hc_vol = idf[idf['histo_cyto_group'] == 'Histopathology & Cytopathology']['test_count'].sum()
        oth_vol = vol - hc_vol
        hc_share = (hc_vol / vol * 100) if vol > 0 else 0
        
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
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.subheader("📋 Partner Action Table")
    st.dataframe(filtered_eval_df.sort_values('HC Share %', ascending=False).style.background_gradient(subset=['HC Share %'], cmap='Reds'), use_container_width=True)
    
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
        st.plotly_chart(fig_drill, use_container_width=True)
        
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
    st.plotly_chart(fig_spec_trend, use_container_width=True)
    
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
        st.plotly_chart(fig_spec_hosp, use_container_width=True)
    
    st.divider()
    
    # 3. Specialty to Department Mapping Visualization
    st.subheader("🔗 Prescription Pattern: Specialty to Department Flow")
    st.markdown("Understand which specific lab departments make up the selected Doctor Specialty.")
    flow_df = filtered_df.groupby(['doctor_specialty', 'department'])['test_count'].sum().reset_index()
    fig_flow = px.sunburst(flow_df, path=['doctor_specialty', 'department'], values='test_count',
                           title="Distribution of Tests from Specialty down to Department",
                           color='test_count', color_continuous_scale='Teal')
    fig_flow.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig_flow, use_container_width=True)

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
        
        c1, c2 = st.columns(2)
        
        with c1:
            fig_vol_proj = px.line(combined, x='Date', y='Total Volume', color='Type', markers=True, title="📈 Test Volume Projection", line_dash='Type')
            st.plotly_chart(fig_vol_proj, use_container_width=True)
            
        with c2:
            fig_share_proj = px.line(combined, x='Date', y='HC Share %', color='Type', markers=True, title="📉 Histo-Cyto Share % Projection", line_dash='Type')
            fig_share_proj.update_layout(yaxis=dict(range=[0, 100]))
            fig_share_proj.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Cutoff Danger Zone")
            st.plotly_chart(fig_share_proj, use_container_width=True)
            
        trend_dir = "increasing ↗️" if future_share[-1] > ts['hc_share'].iloc[-1] else "decreasing ↘️"
        st.info(f"**🤖 AI Insight for {forecast_inst}:** The Histo-Cyto share is projected to **{trend_dir}**, reaching **{future_share[-1]:.1f}%** by {future_dates[-1].strftime('%B %Y')}.")

# ══════════════════════════════════════════════════════════════════
# APPLICATION TEAM
# ══════════════════════════════════════════════════════════════════
elif nav == "team":
    st.header("👨‍💻 Application Team")
    st.markdown("Meet the team responsible for building and maintaining the B2B Analytics infrastructure at Aswini Diagnostic Services.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div style="background-color: var(--offwhite); padding: 25px; border-radius: 12px; border-top: 5px solid var(--aswini-blue); text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid var(--border);">
            <div style="font-size: 3rem; margin-bottom: 10px;">👔</div>
            <h3 style="margin: 0; color: var(--aswini-dark) !important; font-size: 1.3rem;">Mr. Harikrishnan R</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin-top: 5px;">Application Manager</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div style="background-color: var(--offwhite); padding: 25px; border-radius: 12px; border-top: 5px solid var(--aswini-blue); text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid var(--border);">
            <div style="font-size: 3rem; margin-bottom: 10px;">💻</div>
            <h3 style="margin: 0; color: var(--aswini-dark) !important; font-size: 1.3rem;">Mr. Mohammed Falah K</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin-top: 5px;">Application Specialist</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div style="background-color: var(--offwhite); padding: 25px; border-radius: 12px; border-top: 5px solid var(--aswini-blue); text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid var(--border);">
            <div style="font-size: 3rem; margin-bottom: 10px;">🚀</div>
            <h3 style="margin: 0; color: var(--aswini-dark) !important; font-size: 1.3rem;">Mr. Nidhin U K</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin-top: 5px;">Application Specialist</p>
        </div>
        """, unsafe_allow_html=True)
