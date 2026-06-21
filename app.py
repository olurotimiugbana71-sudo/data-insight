"""
DataInsight Pro - Secure Data Analysis
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import streamlit as st

st.set_page_config(
    page_title="DataInsight Pro | ApexDynamics Solutions",
    page_icon="📊",
    layout="wide"
)

import pandas as pd
import numpy as np
from analyzer import DataAnalyzer
from visualizer import Visualizer
from report_builder import ReportBuilder
from monetize import MonetizationEngine
from license_gen import LicenseManager
import base64
from datetime import datetime

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"
YEAR = "2026"
VERSION = "v2.0"

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .preview-banner {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_components():
    return DataAnalyzer(), Visualizer(), ReportBuilder(), MonetizationEngine(), LicenseManager()

analyzer, visualizer, report_builder, monetizer, license_mgr = init_components()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False

# Sidebar
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### 💰 Pricing Plans")
    
    for tier, details in monetizer.price_tiers.items():
        with st.expander(f"**{details['name']}** - ${details['price']:.2f}"):
            for feature in details['features']:
                st.write(f"✓ {feature}")
    
    st.markdown("---")
    st.markdown("### 🔑 License Activation")
    
    lic_key = st.text_input("License Key", placeholder="DAT-XXXX-XXXX-XXXX")
    lic_email = st.text_input("Email", placeholder="you@email.com")
    
    if st.button("Activate License", type="primary"):
        valid, msg = license_mgr.validate(lic_key, lic_email)
        if valid:
            st.success(f"✅ {msg} - Full Access Unlocked!")
            st.session_state.licensed = True
            st.session_state.buyer_email = lic_email
        else:
            st.error(f"❌ {msg}")
    
    if st.session_state.licensed:
        st.success("🔓 Licensed - Full Access")
    else:
        st.info("🔒 Preview Mode - Activate for full features")

# Main Content
st.markdown(f'<h1 class="main-header">📊 DataInsight Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Turn Raw Data into Actionable Insights | {COMPANY}")

# Preview Banner
if not st.session_state.licensed:
    st.markdown("""
    <div class="preview-banner">
        <h3>🔒 PREVIEW MODE</h3>
        <p>You're viewing limited results. <strong>Activate your license</strong> to unlock full analysis, 
        all charts, and downloadable reports.</p>
    </div>
    """, unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader(
    "📁 Upload your dataset (CSV, Excel, JSON)",
    type=['csv', 'xlsx', 'xls', 'json']
)

if uploaded_file is not None:
    with st.spinner("🔍 Analyzing your data..."):
        try:
            results, df = analyzer.full_analysis(uploaded_file)
            charts = visualizer.insight_dashboard(df, results)
            
            st.success(f"✅ Analysis complete! Quality Score: {results['quality_score']}/100")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", f"{results['profile']['shape'][0]:,}")
            with col2:
                st.metric("Columns", results['profile']['shape'][1])
            with col3:
                mp = sum(results['profile']['missing_percent'].values()) / len(results['profile']['missing_percent']) if results['profile']['missing_percent'] else 0
                st.metric("Missing Data", f"{mp:.1f}%")
            with col4:
                st.metric("Quality", f"{results['quality_score']}/100")
            
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📊 Charts", "💡 Insights", "📥 Export"])
            
            with tab1:
                for col, dtype in results['profile']['dtypes'].items():
                    st.text(f"{col}: {dtype}")
                if results['profile']['duplicates'] > 0:
                    st.warning(f"Found {results['profile']['duplicates']} duplicate rows")
            
            with tab2:
                if st.session_state.licensed:
                    if charts.get('missing'):
                        st.image(f"data:image/png;base64,{charts['missing']}", use_column_width=True)
                    if charts.get('distribution'):
                        st.image(f"data:image/png;base64,{charts['distribution']}", use_column_width=True)
                    if charts.get('correlation'):
                        st.components.v1.html(charts['correlation'], height=500)
                    if charts.get('categories'):
                        st.image(f"data:image/png;base64,{charts['categories']}", use_column_width=True)
                else:
                    if charts.get('missing'):
                        st.image(f"data:image/png;base64,{charts['missing']}", use_column_width=True)
                    st.warning("🔒 Activate license to see all charts and visualizations")
            
            with tab3:
                if results.get('insights'):
                    for insight in results['insights'][:3 if not st.session_state.licensed else len(results['insights'])]:
                        if insight['type'] == 'warning':
                            st.warning(insight['message'])
                        elif insight['type'] == 'alert':
                            st.error(insight['message'])
                        else:
                            st.info(insight['message'])
                    if not st.session_state.licensed:
                        st.warning("🔒 Activate license to see all insights")
            
            with tab4:
                st.markdown("### 📥 Export Reports")
                
                if st.session_state.licensed:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(df.head(5))
                        csv = df.to_csv(index=False)
                        st.download_button("📥 Download CSV", csv, "data.csv", "text/csv")
                    with col2:
                        if st.button("🔓 Generate Full Report", type="primary"):
                            st.session_state.show_report = True
                        if st.session_state.get('show_report'):
                            html_report = report_builder.generate_html_report(results, charts, df)
                            st.components.v1.html(html_report, height=600, scrolling=True)
                            st.download_button("📥 Download HTML Report", html_report, "report.html", "text/html")
                            pdf_report = report_builder.generate_pdf_report(results, df)
                            st.download_button("📥 Download PDF Report", base64.b64decode(pdf_report), "report.pdf", "application/pdf")
                else:
                    st.warning("🔒 Activate license to download reports")
                    st.dataframe(df.head(3))
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🚀 How It Works\n1. Activate license\n2. Upload data\n3. Get insights\n4. Download reports")
    with col2:
        st.markdown("### 📊 Features\n- Statistics\n- Charts\n- Insights\n- PDF Reports")
    with col3:
        st.markdown("### 💡 Use Cases\n- Sales data\n- Analytics\n- Financial reports\n- Research")
    
    if st.button("📁 Load Demo Data"):
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        demo_df = pd.DataFrame({
            'date': dates,
            'sales': np.random.normal(1000, 200, 100).cumsum(),
            'customers': np.random.poisson(50, 100),
            'revenue': np.random.normal(5000, 1000, 100),
            'category': np.random.choice(['A', 'B', 'C', 'D'], 100)
        })
        csv = demo_df.to_csv(index=False)
        st.download_button("📥 Download Demo CSV", csv, "demo.csv", "text/csv")

st.markdown("---")
st.markdown(f"<p style='text-align:center;'>© {YEAR} {COMPANY} | Built by {DEVELOPER} | {VERSION}</p>", unsafe_allow_html=True)