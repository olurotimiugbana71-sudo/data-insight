"""
DataInsight Pro - Secure Main Application
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
import base64

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"
YEAR = "2026"
VERSION = "v1.0"

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .license-box {
        background: #f0f8ff;
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_components():
    return DataAnalyzer(), Visualizer(), ReportBuilder(), MonetizationEngine()

analyzer, visualizer, report_builder, monetizer = init_components()

# Sidebar
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### 💰 Pricing Plans")
    
    for tier, details in monetizer.price_tiers.items():
        with st.expander(f"{details['name']} - ${details['price']:.2f}"):
            for feature in details['features']:
                st.write(f"✓ {feature}")
    
    st.markdown("---")
    st.markdown("### 📈 Profit Calculator")
    calc_tier = st.selectbox("Tier", list(monetizer.price_tiers.keys()))
    calc_clients = st.slider("Monthly Clients", 1, 50, 10)
    profit = monetizer.calculate_profit(calc_tier, calc_clients)
    st.metric("Monthly Net", f"${profit['net_revenue']:,.2f}")
    st.metric("Annual", f"${profit['projected_annual']:,.2f}")

# Main Content
st.markdown(f'<h1 class="main-header">📊 DataInsight Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Professional Data Analysis | {COMPANY}")

# ============ ORDER INFORMATION SECTION ============
st.markdown("---")
st.markdown("## 🔐 Report Licensing & Security")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    buyer_email = st.text_input(
        "📧 Your Email Address",
        placeholder="client@example.com",
        help="Will be embedded as watermark in your report"
    )

with col2:
    purchase_id = st.text_input(
        "🧾 Order / Invoice Number",
        placeholder="INV-2026-001",
        help="Your order reference for tracking"
    )

with col3:
    if buyer_email and purchase_id:
        st.markdown("""
        <div style="background:#d4edda; padding:20px; border-radius:10px; text-align:center; margin-top:10px;">
            <h2 style="color:#155724; margin:0;">✅<br>LICENSED</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#fff3cd; padding:20px; border-radius:10px; text-align:center; margin-top:10px;">
            <h3 style="color:#856404; margin:0;">⚠️<br>PREVIEW MODE</h3>
        </div>
        """, unsafe_allow_html=True)

if buyer_email and purchase_id:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
         color: white; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <strong>🔒 SECURE LICENSED REPORT</strong><br>
        Licensed to: {buyer_email} | Order: {purchase_id}<br>
        <small>✓ Watermarked | ✓ Tracked | ✓ Confidential</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
# ============ END ORDER SECTION ============

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
            
            if buyer_email:
                st.success(f"✅ Analysis complete! Licensed to: {buyer_email}")
            else:
                st.success(f"✅ Analysis complete! (Preview Mode)")
            
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
                st.markdown("### Data Profile")
                for col, dtype in results['profile']['dtypes'].items():
                    st.text(f"{col}: {dtype}")
            
            with tab2:
                if charts.get('missing'):
                    st.image(f"data:image/png;base64,{charts['missing']}", use_column_width=True)
                if charts.get('distribution'):
                    st.image(f"data:image/png;base64,{charts['distribution']}", use_column_width=True)
                if charts.get('correlation'):
                    st.components.v1.html(charts['correlation'], height=500)
                if charts.get('categories'):
                    st.image(f"data:image/png;base64,{charts['categories']}", use_column_width=True)
            
            with tab3:
                if results.get('insights'):
                    for insight in results['insights']:
                        if insight['type'] == 'warning':
                            st.warning(insight['message'])
                        elif insight['type'] == 'alert':
                            st.error(insight['message'])
                        else:
                            st.info(insight['message'])
            
            with tab4:
                st.markdown("### 📥 Export Reports")
                
                email = buyer_email if buyer_email else "PREVIEW"
                order_id = purchase_id if purchase_id else "DEMO"
                
                # Security info box
                st.markdown(f"""
                <div style="background:#fff3cd; border-left:5px solid #ffc107; padding:15px; margin:15px 0; border-radius:5px;">
                    <h4>🔐 Report Security</h4>
                    <table style="width:100%;">
                        <tr><td>📧 Licensed To:</td><td><strong>{email}</strong></td></tr>
                        <tr><td>🧾 Order:</td><td><strong>{order_id}</strong></td></tr>
                        <tr><td>💧 Watermark:</td><td><strong>Embedded</strong></td></tr>
                        <tr><td>🔒 Status:</td><td><strong style="color:{'green' if buyer_email else 'orange'};">{'LICENSED' if buyer_email else 'PREVIEW'}</strong></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(df.head(5))
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Download CSV", csv, "data.csv", "text/csv")
                
                with col2:
                    if st.button("🔓 Generate Full Report", type="primary"):
                        st.session_state.show_report = True
                    
                    if st.session_state.get('show_report'):
                        html_report = report_builder.generate_html_report(
                            results, charts, df, buyer_email=email, purchase_id=order_id
                        )
                        st.components.v1.html(html_report, height=600, scrolling=True)
                        
                        st.download_button(
                            "📥 Download HTML (Watermarked)",
                            html_report,
                            f"report_{order_id}.html",
                            "text/html"
                        )
                        
                        pdf_report = report_builder.generate_pdf_report(
                            results, df, buyer_email=email, purchase_id=order_id
                        )
                        st.download_button(
                            "📥 Download PDF (Watermarked)",
                            base64.b64decode(pdf_report),
                            f"report_{order_id}.pdf",
                            "application/pdf"
                        )
                        
                        st.markdown("""
                        ---
                        ### 🔒 Security Applied:
                        ✅ Watermarked with your email  
                        ✅ Unique Report ID  
                        ✅ Confidentiality notice  
                        ✅ Order number embedded  
                        """)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🚀 How It Works\n1. Enter order details\n2. Upload data\n3. Get analysis\n4. Download secure report")
    with col2:
        st.markdown("### 📊 Features\n- Statistics\n- Charts\n- Insights\n- Watermarked reports")
    with col3:
        st.markdown("### 💡 Use Cases\n- Sales data\n- Customer analytics\n- Financial reports\n- Market research")
    
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