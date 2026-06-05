"""
Professional report generation with security features
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
from fpdf import FPDF
import base64
from datetime import datetime
import hashlib

class ReportBuilder:
    def __init__(self):
        self.report_date = datetime.now().strftime("%B %d, %Y")
        self.company = "ApexDynamics Solutions"
        self.developer = "Rotimi Ugbana"
        self.year = "2026"
    
    def add_watermark(self, html_content, buyer_email="PREVIEW", purchase_id="DEMO"):
        """Add buyer-specific watermark to prevent unauthorized sharing"""
        watermark = f"""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
             pointer-events: none; z-index: 9999; opacity: 0.03; font-size: 42px; 
             color: #000; display: flex; align-items: center; justify-content: center;
             transform: rotate(-25deg); text-align: center; white-space: pre-line;">
            LICENSED TO:{buyer_email}
            ORDER: {purchase_id}
            APEXDYNAMICS SOLUTIONS
        </div>
        """
        
        confidential_footer = f"""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; 
             text-align: center; padding: 12px; background: #f8f9fa; 
             font-size: 10px; color: #666; border-top: 2px solid #667eea;
             z-index: 10000;">
            <strong>CONFIDENTIAL</strong> | Prepared exclusively for {buyer_email} | 
            Order #{purchase_id} | Copyright {self.year} {self.company} | 
            Built by {self.developer} | <strong>UNAUTHORIZED DISTRIBUTION PROHIBITED</strong>
        </div>
        """
        
        html_content = html_content.replace('</body>', f'{watermark}{confidential_footer}</body>')
        return html_content
    
    def generate_report_id(self, email):
        """Generate unique report tracking ID"""
        timestamp = datetime.now().isoformat()
        raw = f"{email}{timestamp}{self.company}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()
    
    def generate_html_report(self, analysis_results, charts, df, buyer_email="PREVIEW", purchase_id="DEMO"):
        """Create beautiful HTML report with security features"""
        
        rows, cols = df.shape
        missing_pct = df.isnull().sum().sum() / (rows * cols) * 100 if (rows * cols) > 0 else 0
        report_id = self.generate_report_id(buyer_email)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Analysis Report - {self.company}</title>
            <meta name="author" content="{self.company} - {self.developer}">
            <meta name="copyright" content="Copyright {self.year} {self.company}">
            <meta name="description" content="Professional Data Analysis Report">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: relative; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
                .company-badge {{ background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; display: inline-block; font-size: 14px; }}
                .report-id {{ font-size: 10px; color: rgba(255,255,255,0.7); margin-top: 10px; }}
                .confidential-stamp {{ position: absolute; top: 20px; right: 20px; border: 3px solid #ff6b6b; color: #ff6b6b; padding: 10px 20px; border-radius: 5px; font-weight: bold; font-size: 14px; transform: rotate(15deg); opacity: 0.8; }}
                .score-card {{ display: inline-block; padding: 20px; margin: 10px; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; min-width: 150px; }}
                .metric {{ font-size: 36px; font-weight: bold; color: #667eea; }}
                .label {{ color: #666; font-size: 14px; }}
                .section {{ margin: 30px 0; }}
                .insight {{ padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; background: #f8f9fa; }}
                .warning {{ border-left-color: #ff6b6b; }}
                .alert {{ border-left-color: #ffd93d; }}
                img {{ max-width: 100%; margin: 20px 0; border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #667eea; color: white; }}
                .footer {{ text-align: center; margin-top: 50px; padding: 20px; background: #f8f9fa; border-radius: 10px; border-top: 3px solid #667eea; }}
                .security-notice {{ background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 20px 0; font-size: 12px; }}
                @media print {{
                    .confidential-stamp {{ display: block; }}
                    .security-notice {{ display: block; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="confidential-stamp">CONFIDENTIAL</div>
                
                <div class="header">
                    <span class="company-badge">{self.company}</span>
                    <h1>📊 Data Analysis Report</h1>
                    <p>Generated on {self.report_date}</p>
                    <p class="report-id">Report ID: {report_id} | Order: {purchase_id}</p>
                </div>
                
                <div class="security-notice">
                    <strong>🔒 CONFIDENTIALITY NOTICE:</strong> This report is prepared exclusively for 
                    <strong>{buyer_email}</strong>. It contains proprietary analysis and insights from 
                    {self.company}. Unauthorized distribution, copying, or sharing of this report 
                    is strictly prohibited and may result in legal action. Report ID: {report_id}
                </div>
                
                <div style="text-align: center;">
                    <div class="score-card">
                        <div class="metric">{analysis_results['quality_score']}/100</div>
                        <div class="label">Data Quality Score</div>
                    </div>
                    <div class="score-card">
                        <div class="metric">{rows:,}</div>
                        <div class="label">Rows Analyzed</div>
                    </div>
                    <div class="score-card">
                        <div class="metric">{cols}</div>
                        <div class="label">Variables</div>
                    </div>
                    <div class="score-card">
                        <div class="metric">{missing_pct:.1f}%</div>
                        <div class="label">Missing Data</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📋 Executive Summary</h2>
                    <p>This comprehensive analysis examined <strong>{rows:,} records</strong> across 
                    <strong>{cols} variables</strong>. The overall data quality score is 
                    <strong>{analysis_results['quality_score']}/100</strong>.</p>
                    <p><strong>Prepared for:</strong> {buyer_email}</p>
                    <p><strong>Order Number:</strong> {purchase_id}</p>
                </div>
        """
        
        if analysis_results.get('insights'):
            html += '<div class="section"><h2>💡 Key Insights</h2>'
            for insight in analysis_results['insights']:
                html += f'<div class="insight {insight["type"]}">{insight["message"]}</div>'
            html += '</div>'
        
        if charts:
            html += '<div class="section"><h2>📈 Visualizations</h2>'
            for name, chart in charts.items():
                if chart:
                    if name == 'correlation':
                        html += chart
                    elif isinstance(chart, str):
                        html += f'<div><h3>{name.replace("_", " ").title()}</h3><img src="data:image/png;base64,{chart}" alt="{name}"></div>'
            html += '</div>'
        
        if analysis_results.get('statistics'):
            stats = analysis_results['statistics']
            html += '<div class="section"><h2>📊 Statistical Summary</h2><table><tr><th>Metric</th>'
            for col in stats.keys():
                html += f'<th>{col}</th>'
            html += '</tr>'
            
            metrics = ['mean', 'median', 'std', 'min', 'max']
            for metric in metrics:
                html += f'<tr><td><strong>{metric.title()}</strong></td>'
                for col in stats.keys():
                    html += f'<td>{stats[col].get(metric, "N/A")}</td>'
                html += '</tr>'
            html += '</table></div>'
        
        html += f"""
                <div class="footer">
                    <p><strong>DataInsight Pro v1.0</strong></p>
                    <p>Copyright {self.year} {self.company} | Built by {self.developer}</p>
                    <p>Report ID: {report_id} | Prepared for: {buyer_email}</p>
                    <p style="font-size: 11px; color: #ff6b6b; margin-top: 10px;">
                        ⚠️ CONFIDENTIAL - DO NOT DISTRIBUTE
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Add watermark
        html = self.add_watermark(html, buyer_email, purchase_id)
        
        return html
    
    def generate_pdf_report(self, analysis_results, df, buyer_email="PREVIEW", purchase_id="DEMO"):
        """Generate downloadable PDF with security features"""
        pdf = FPDF()
        pdf.add_page()
        
        report_id = self.generate_report_id(buyer_email)
        
        # Header
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, 'DATA ANALYSIS REPORT', ln=True, align='C')
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'{self.company}', ln=True, align='C')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 8, f'Generated: {self.report_date}', ln=True, align='C')
        pdf.cell(0, 8, f'Report ID: {report_id}', ln=True, align='C')
        pdf.ln(5)
        
        # Confidential Notice
        pdf.set_fill_color(255, 243, 205)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 15, 'CONFIDENTIAL - FOR AUTHORIZED RECIPIENT ONLY', ln=True, align='C', fill=True)
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 8, f'Prepared for: {buyer_email} | Order: {purchase_id}', ln=True, align='C')
        pdf.cell(0, 8, f'Unauthorized distribution prohibited | Copyright {self.year} {self.company}', ln=True, align='C')
        pdf.ln(8)
        
        # Quality Score
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Quality Score: {analysis_results["quality_score"]}/100', ln=True)
        pdf.ln(5)
        
        # Dataset Info
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Dataset Information:', ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 7, f'Rows: {analysis_results["profile"]["shape"][0]}', ln=True)
        pdf.cell(0, 7, f'Columns: {analysis_results["profile"]["shape"][1]}', ln=True)
        pdf.ln(5)
        
        # Insights
        if analysis_results.get('insights'):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Key Insights:', ln=True)
            pdf.set_font('Arial', '', 10)
            for insight in analysis_results['insights']:
                bullet = chr(149)  # bullet point
                pdf.multi_cell(0, 7, f'{bullet} {insight["message"]}')
            pdf.ln(5)
        
        # Statistics
        if analysis_results.get('statistics'):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Statistical Summary:', ln=True)
            pdf.set_font('Arial', '', 9)
            
            for col, stats in analysis_results['statistics'].items():
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 7, f'  {col}', ln=True)
                pdf.set_font('Arial', '', 9)
                for metric, value in stats.items():
                    pdf.cell(0, 6, f'    {metric}: {value}', ln=True)
                pdf.ln(2)
        
        # Footer with security
        pdf.ln(15)
        pdf.set_fill_color(248, 249, 250)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(0, 10, f'CONFIDENTIAL - Report ID: {report_id}', ln=True, align='C', fill=True)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 7, f'Copyright {self.year} {self.company} | Built by {self.developer}', ln=True, align='C')
        pdf.cell(0, 7, f'Prepared exclusively for: {buyer_email}', ln=True, align='C')
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        return base64.b64encode(pdf_output).decode()