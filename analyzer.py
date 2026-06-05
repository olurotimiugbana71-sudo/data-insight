"""
Advanced Data Analysis Engine
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    def __init__(self):
        self.insights = {}
        self.score = 0
        self.company = "ApexDynamics Solutions"
        
    def load_data(self, file):
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            elif file.name.endswith('.json'):
                df = pd.read_json(file)
            else:
                raise ValueError("Unsupported format")
            return df
        except Exception as e:
            raise Exception(f"Load error: {str(e)}")
    
    def generate_profile(self, df):
        profile = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": {str(k): str(v) for k, v in df.dtypes.to_dict().items()},
            "missing": df.isnull().sum().to_dict(),
            "missing_percent": (df.isnull().sum() / len(df) * 100).to_dict(),
            "duplicates": int(df.duplicated().sum()),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        return profile
    
    def statistical_summary(self, df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats = {}
        for col in numeric_cols:
            stats[str(col)] = {
                "mean": round(float(df[col].mean()), 2),
                "median": round(float(df[col].median()), 2),
                "std": round(float(df[col].std()), 2),
                "min": round(float(df[col].min()), 2),
                "max": round(float(df[col].max()), 2),
                "skew": round(float(df[col].skew()), 2)
            }
        return stats
    
    def find_outliers(self, df):
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_mask = (df[col] < lower) | (df[col] > upper)
            outlier_count = outlier_mask.sum()
            if outlier_count > 0:
                outliers[str(col)] = {
                    "count": int(outlier_count),
                    "percentage": round(float(outlier_count / len(df) * 100), 2),
                    "lower_bound": round(float(lower), 2),
                    "upper_bound": round(float(upper), 2)
                }
        return outliers
    
    def correlation_analysis(self, df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return None
        corr_matrix = df[numeric_cols].corr()
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.5:
                    strong_corr.append({
                        "var1": str(corr_matrix.columns[i]),
                        "var2": str(corr_matrix.columns[j]),
                        "correlation": round(float(corr_matrix.iloc[i, j]), 2)
                    })
        return {"matrix": corr_matrix.to_dict(), "strong_correlations": strong_corr}
    
    def trend_analysis(self, df):
        date_cols = df.select_dtypes(include=["datetime64"]).columns
        if len(date_cols) == 0:
            for col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols = [col]
                    break
                except:
                    continue
        trends = {}
        for date_col in date_cols:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for num_col in numeric_cols:
                df_sorted = df.sort_values(date_col)
                values = df_sorted[num_col].values
                if len(values) > 2:
                    x = np.arange(len(values))
                    slope = np.polyfit(x, values, 1)[0]
                    trend_type = "Upward" if slope > 0 else "Downward" if slope < 0 else "Stable"
                    trends[f"{num_col}_over_{date_col}"] = {
                        "trend": trend_type,
                        "slope": round(float(slope), 2),
                        "change_percent": round(float(((values[-1] - values[0]) / values[0]) * 100), 2) if values[0] != 0 else 0
                    }
        return trends
    
    def generate_business_insights(self, df):
        insights = []
        missing = df.isnull().sum()
        high_missing = missing[missing > len(df) * 0.3]
        if len(high_missing) > 0:
            cols_list = ", ".join(high_missing.index)
            insights.append({"type": "warning", "message": f"Columns with over 30 percent missing data: {cols_list}. Consider data quality improvement."})
        outliers = self.find_outliers(df)
        if outliers:
            insights.append({"type": "alert", "message": f"Found outliers in {len(outliers)} columns. These may need investigation."})
        corr = self.correlation_analysis(df)
        if corr and corr["strong_correlations"]:
            for c in corr["strong_correlations"][:3]:
                insights.append({"type": "insight", "message": f"Strong correlation ({c['correlation']}) between {c['var1']} and {c['var2']}"})
        if len(df) < 100:
            insights.append({"type": "warning", "message": f"Small dataset ({len(df)} rows). Results may not be statistically significant."})
        categorical_cols = df.select_dtypes(include=["object"]).columns
        for col in categorical_cols[:2]:
            value_counts = df[col].value_counts()
            if len(value_counts) > 0:
                ratio = value_counts.iloc[0] / len(df)
                if ratio > 0.9:
                    insights.append({"type": "info", "message": f"Column {col} is imbalanced. 90 percent of values are {value_counts.index[0]}"})
        return insights
    
    def full_analysis(self, file):
        df = self.load_data(file)
        results = {
            "profile": self.generate_profile(df),
            "statistics": self.statistical_summary(df),
            "outliers": self.find_outliers(df),
            "correlations": self.correlation_analysis(df),
            "trends": self.trend_analysis(df),
            "insights": self.generate_business_insights(df),
            "data_sample": df.head(10).to_dict(),
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        score = 100
        if results["profile"]["missing_percent"]:
            keys = list(results["profile"]["missing_percent"].keys())
            if keys:
                score -= results["profile"]["missing_percent"][keys[0]]
        if len(df) > 0:
            score -= (results["profile"]["duplicates"] / len(df) * 100)
        results["quality_score"] = max(0, min(100, round(score, 1)))
        results["company"] = self.company
        return results, df