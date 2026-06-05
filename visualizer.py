"""
Lightweight visualization module
Memory-efficient with automatic cleanup
"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend - saves memory
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.figsize = (10, 5)
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 for HTML"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)  # Memory cleanup
        return img_base64
    
    def missing_data_chart(self, df):
        """Visualize missing data"""
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        
        if len(missing) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=self.figsize)
        bars = ax.bar(missing.index, missing.values, color='#FF6B6B')
        ax.set_title('Missing Data by Column', fontsize=14, fontweight='bold')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Missing Values')
        plt.xticks(rotation=45, ha='right')
        
        # Add values on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def distribution_chart(self, df, column=None):
        """Distribution with KDE"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return None
        
        if column is None:
            column = numeric_cols[0]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Histogram with KDE
        ax1.hist(df[column].dropna(), bins=20, color='#4ECDC4', edgecolor='black', alpha=0.7)
        ax1.set_title(f'Distribution of {column}', fontweight='bold')
        ax1.set_xlabel(column)
        ax1.set_ylabel('Frequency')
        
        # Box plot
        ax2.boxplot(df[column].dropna(), vert=True, patch_artist=True, 
                   boxprops=dict(facecolor='#FFE66D'))
        ax2.set_title(f'Box Plot - {column}', fontweight='bold')
        ax2.set_ylabel(column)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def correlation_heatmap(self, df):
        """Interactive correlation heatmap"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return None
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Correlation Heatmap',
            height=500,
            width=700
        )
        
        return fig.to_html(full_html=False)
    
    def category_chart(self, df, column=None):
        """Bar chart for categorical data"""
        cat_cols = df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) == 0:
            return None
        
        if column is None:
            column = cat_cols[0]
        
        value_counts = df[column].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=self.figsize)
        bars = ax.barh(value_counts.index, value_counts.values, color='#95E1D3')
        ax.set_title(f'Top Categories - {column}', fontweight='bold')
        ax.set_xlabel('Count')
        
        # Add values
        for i, (bar, val) in enumerate(zip(bars, value_counts.values)):
            ax.text(val, bar.get_y() + bar.get_height()/2, 
                   f' {val}', va='center')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def trend_line_chart(self, df, date_col, value_col):
        """Time series trend visualization"""
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            df_sorted = df.sort_values(date_col)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_sorted[date_col],
                y=df_sorted[value_col],
                mode='lines+markers',
                name=value_col,
                line=dict(color='#FF6B6B', width=2)
            ))
            
            # Add trend line
            x_numeric = np.arange(len(df_sorted))
            z = np.polyfit(x_numeric, df_sorted[value_col], 1)
            p = np.poly1d(z)
            
            fig.add_trace(go.Scatter(
                x=df_sorted[date_col],
                y=p(x_numeric),
                mode='lines',
                name='Trend',
                line=dict(color='#4ECDC4', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title=f'Trend Analysis: {value_col} over time',
                xaxis_title=date_col,
                yaxis_title=value_col,
                height=400,
                hovermode='x unified'
            )
            
            return fig.to_html(full_html=False)
        except:
            return None
    
    def insight_dashboard(self, df, analysis_results):
        """Create comprehensive insight cards"""
        charts = {}
        
        # Generate all applicable charts
        charts['missing'] = self.missing_data_chart(df)
        
        if len(df.select_dtypes(include=[np.number]).columns) > 0:
            charts['distribution'] = self.distribution_chart(df)
            charts['correlation'] = self.correlation_heatmap(df)
        
        if len(df.select_dtypes(include=['object']).columns) > 0:
            charts['categories'] = self.category_chart(df)
        
        return charts
