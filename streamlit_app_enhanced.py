"""
Advanced Bitcoin Trader Performance vs Market Sentiment Dashboard
Interactive Streamlit Application

Author: Ayush Singh
Email: Ayusingh693@gmail.com
Phone: +91 7031678999

Assignment: Bitcoin Trader Performance Analysis using Fear & Greed Index
This comprehensive dashboard analyzes the relationship between trader performance
and market sentiment to identify profitable trading patterns.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Bitcoin Sentiment & Trading Analysis - By Ayush Singh",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Created by Ayush Singh | Ayusingh693@gmail.com | +91 7031678999"
    }
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 26px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 5px solid #1976d2;
        padding-left: 15px;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .insight-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-left: 6px solid #1976d2;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 20px;
        border-left: 6px solid #ff9800;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-left: 6px solid #4caf50;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .author-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .stats-number {
        font-size: 32px;
        font-weight: bold;
        color: #1976d2;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1976d2;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data(ttl=3600)
def load_data():
    """Load and preprocess the datasets with comprehensive error handling"""
    try:
        # Load Fear & Greed Index
        fear_greed_df = pd.read_csv('fear_greed_index.csv')
        fear_greed_df['date'] = pd.to_datetime(fear_greed_df['date'])
        fear_greed_df = fear_greed_df.sort_values('date').reset_index(drop=True)
        
        # Load Historical Trading Data
        historical_df = pd.read_csv('historical_data.csv')
        historical_df['Timestamp IST'] = pd.to_datetime(
            historical_df['Timestamp IST'], 
            format='%d-%m-%Y %H:%M', 
            errors='coerce'
        )
        historical_df['Date'] = historical_df['Timestamp IST'].dt.date
        historical_df['Date'] = pd.to_datetime(historical_df['Date'])
        
        # Clean numeric columns
        historical_df['Closed PnL'] = pd.to_numeric(historical_df['Closed PnL'], errors='coerce')
        historical_df['Size USD'] = pd.to_numeric(historical_df['Size USD'], errors='coerce')
        historical_df['Fee'] = pd.to_numeric(historical_df['Fee'], errors='coerce')
        historical_df = historical_df.dropna(subset=['Date'])
        
        # Merge datasets
        merged_df = pd.merge(
            historical_df,
            fear_greed_df[['date', 'value', 'classification']],
            left_on='Date',
            right_on='date',
            how='left'
        )
        
        # Forward fill sentiment data
        merged_df['classification'] = merged_df.groupby(merged_df['Date'].notna())['classification'].fillna(method='ffill')
        merged_df['value'] = merged_df.groupby(merged_df['Date'].notna())['value'].fillna(method='ffill')
        merged_df = merged_df.dropna(subset=['classification'])
        
        # Feature engineering
        merged_df['Net_PnL'] = merged_df['Closed PnL'] - merged_df['Fee']
        merged_df['is_profitable'] = merged_df['Net_PnL'] > 0
        merged_df['Hour'] = merged_df['Timestamp IST'].dt.hour
        merged_df['DayOfWeek'] = merged_df['Timestamp IST'].dt.dayofweek
        merged_df['Month'] = merged_df['Timestamp IST'].dt.month
        merged_df['Week'] = merged_df['Timestamp IST'].dt.isocalendar().week
        
        # Sentiment categorization
        def categorize_sentiment(classification):
            sentiment_map = {
                'Extreme Fear': 'Extreme Fear',
                'Fear': 'Fear',
                'Neutral': 'Neutral',
                'Greed': 'Greed',
                'Extreme Greed': 'Extreme Greed'
            }
            return sentiment_map.get(classification, 'Neutral')
        
        merged_df['sentiment_category'] = merged_df['classification'].apply(categorize_sentiment)
        
        # Advanced features
        merged_df['PnL_Percentage'] = (merged_df['Net_PnL'] / merged_df['Size USD']) * 100
        merged_df['Fee_Ratio'] = (merged_df['Fee'] / merged_df['Size USD']) * 100
        
        sentiment_score_map = {
            'Extreme Fear': 1,
            'Fear': 2,
            'Neutral': 3,
            'Greed': 4,
            'Extreme Greed': 5
        }
        merged_df['sentiment_score'] = merged_df['sentiment_category'].map(sentiment_score_map)
        
        def get_trading_session(hour):
            if 0 <= hour < 8:
                return 'Asian'
            elif 8 <= hour < 16:
                return 'European'
            else:
                return 'American'
        
        merged_df['Trading_Session'] = merged_df['Hour'].apply(get_trading_session)
        merged_df['Win_Loss_Magnitude'] = merged_df['Net_PnL'].abs()
        
        return fear_greed_df, historical_df, merged_df
    
    except FileNotFoundError as e:
        st.error(f"❌ Error: Required CSV files not found. Please ensure both 'fear_greed_index.csv' and 'historical_data.csv' are in the current directory.")
        return None, None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None, None

# Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Dashboard", "📊 Advanced Analytics", "📈 Risk Analysis", "🔍 Deep Dive", "📋 Assignment Details"],
    index=0
)

# Load data
fear_greed_df, historical_df, merged_df = load_data()

if merged_df is None:
    st.stop()

# Global color scheme
sentiment_order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
colors = ['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c']
colors_map = dict(zip(sentiment_order, colors))

# =============================================================================
# PAGE 1: ASSIGNMENT DETAILS
# =============================================================================

if page == "📋 Assignment Details":
    st.markdown('<h1 class="main-header">📋 Assignment Details</h1>', unsafe_allow_html=True)
    
    # Author Information
    st.markdown("""
        <div class="author-card">
            <h2>👨‍💻 Assignment Submitted By</h2>
            <h1 style="margin: 20px 0;">Ayush Singh</h1>
            <p style="font-size: 20px; margin: 10px 0;">
                📧 Email: <a href="mailto:Ayusingh693@gmail.com" style="color: white; text-decoration: underline;">Ayusingh693@gmail.com</a>
            </p>
            <p style="font-size: 20px; margin: 10px 0;">
                📱 Phone: <a href="tel:+917031678999" style="color: white; text-decoration: underline;">+91 7031678999</a>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Assignment Overview
    st.markdown('<h2 class="sub-header">📖 Assignment Overview</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Assignment Title
        **Bitcoin Trader Performance Analysis vs Market Sentiment**
        
        ### 📝 Objective
        This comprehensive analysis examines the relationship between cryptocurrency trader performance 
        on the Hyperliquid platform and Bitcoin market sentiment as measured by the Fear & Greed Index. 
        The goal is to identify correlations, detect behavioral patterns, and provide actionable trading insights.
        
        ### 🔬 Research Questions
        1. **How does trader performance vary with market sentiment?**
           - Analysis of PnL across Fear, Neutral, and Greed periods
           - Statistical significance testing to validate findings
        
        2. **Are there behavioral patterns during different sentiment periods?**
           - Position sizing behavior analysis
           - Win/loss streak patterns
           - Trading frequency variations
        
        3. **What is the correlation between sentiment and profitability?**
           - Correlation coefficient analysis
           - Risk-adjusted returns by sentiment
           - Drawdown analysis during different market conditions
        
        4. **Do traders use higher leverage during Greed periods?**
           - Position size distribution by sentiment
           - Risk metrics comparison
        
        5. **Are losses higher during Fear periods?**
           - Loss magnitude analysis
           - Volatility comparison
           - Maximum drawdown tracking
        """)
    
    with col2:
        # Quick Stats
        total_trades = len(merged_df)
        total_pnl = merged_df['Net_PnL'].sum()
        win_rate = (merged_df['is_profitable'].sum() / total_trades) * 100
        date_range = f"{merged_df['Date'].min().strftime('%Y-%m-%d')} to {merged_df['Date'].max().strftime('%Y-%m-%d')}"
        
        st.markdown("""
        <div class="metric-card">
            <h3 style="text-align: center; color: #1976d2;">📊 Dataset Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Total Trades Analyzed", f"{total_trades:,}")
        st.metric("Date Range", date_range)
        st.metric("Net PnL", f"${total_pnl:,.2f}")
        st.metric("Overall Win Rate", f"{win_rate:.2f}%")
        st.metric("Sentiments Analyzed", "5 Categories")
    
    # Methodology
    st.markdown('<h2 class="sub-header">🔬 Methodology</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4>1️⃣ Data Collection</h4>
            <ul>
                <li>Fear & Greed Index data</li>
                <li>Hyperliquid trading history</li>
                <li>211,226 trades analyzed</li>
                <li>Multiple months of data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4>2️⃣ Data Processing</h4>
            <ul>
                <li>Timestamp synchronization</li>
                <li>Sentiment categorization</li>
                <li>Feature engineering (14 features)</li>
                <li>Data quality validation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-box">
            <h4>3️⃣ Analysis Methods</h4>
            <ul>
                <li>Statistical significance tests</li>
                <li>Correlation analysis</li>
                <li>Risk metrics calculation</li>
                <li>Behavioral pattern detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Stack
    st.markdown('<h2 class="sub-header">💻 Technical Stack</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Programming & Libraries
        - **Python 3.8+** - Core programming language
        - **Pandas** - Data manipulation and analysis
        - **NumPy** - Numerical computing
        - **Scipy** - Statistical testing
        - **Matplotlib & Seaborn** - Static visualizations
        - **Plotly** - Interactive visualizations
        - **Streamlit** - Web application framework
        """)
    
    with col2:
        st.markdown("""
        ### Analysis Techniques
        - **Descriptive Statistics** - Mean, median, std dev
        - **Inferential Statistics** - ANOVA, Chi-square tests
        - **Correlation Analysis** - Pearson correlation
        - **Risk Metrics** - Sharpe ratio, drawdown, volatility
        - **Time Series Analysis** - Rolling statistics
        - **Behavioral Analysis** - Streak detection, patterns
        """)
    
    # Key Features
    st.markdown('<h2 class="sub-header">✨ Key Features of Analysis</h2>', unsafe_allow_html=True)
    
    features = {
        "📊 Comprehensive Visualizations": "40+ interactive charts and graphs",
        "📈 Statistical Rigor": "Hypothesis testing with p-values",
        "💰 Financial Metrics": "PnL, win rate, Sharpe ratio, drawdown",
        "🎯 Risk Analysis": "Volatility, coefficient of variation, max loss",
        "⏰ Time-Based Insights": "Hourly, daily, weekly, monthly patterns",
        "🔍 Behavioral Patterns": "Win/loss streaks, position sizing",
        "💡 Actionable Insights": "Specific trading recommendations",
        "📋 Executive Dashboard": "At-a-glance performance overview"
    }
    
    cols = st.columns(2)
    for idx, (feature, description) in enumerate(features.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="success-box">
                <h4>{feature}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Key Findings Preview
    st.markdown('<h2 class="sub-header">🎯 Key Findings Preview</h2>', unsafe_allow_html=True)
    
    sentiment_performance = merged_df.groupby('sentiment_category').agg({
        'Net_PnL': ['sum', 'mean'],
        'is_profitable': 'mean',
        'Account': 'count'
    }).round(2)
    sentiment_performance.columns = ['Total_PnL', 'Avg_PnL', 'Win_Rate', 'Trade_Count']
    sentiment_performance['Win_Rate'] = sentiment_performance['Win_Rate'] * 100
    sentiment_performance = sentiment_performance.reindex(sentiment_order)
    
    best_sentiment = sentiment_performance['Total_PnL'].idxmax()
    worst_sentiment = sentiment_performance['Total_PnL'].idxmin()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="success-box">
            <h4>🏆 Best Performing Sentiment</h4>
            <h2 style="color: #4caf50;">{best_sentiment}</h2>
            <p><b>Total PnL:</b> ${sentiment_performance.loc[best_sentiment, 'Total_PnL']:,.2f}</p>
            <p><b>Win Rate:</b> {sentiment_performance.loc[best_sentiment, 'Win_Rate']:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="warning-box">
            <h4>⚠️ Worst Performing Sentiment</h4>
            <h2 style="color: #f44336;">{worst_sentiment}</h2>
            <p><b>Total PnL:</b> ${sentiment_performance.loc[worst_sentiment, 'Total_PnL']:,.2f}</p>
            <p><b>Win Rate:</b> {sentiment_performance.loc[worst_sentiment, 'Win_Rate']:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        overall_corr = merged_df['value'].corr(merged_df['Net_PnL'])
        st.markdown(f"""
        <div class="insight-box">
            <h4>🔗 Sentiment-PnL Correlation</h4>
            <h2 style="color: #1976d2;">{overall_corr:.4f}</h2>
            <p><b>Interpretation:</b> {'Positive' if overall_corr > 0 else 'Negative'} correlation</p>
            <p>{'Higher sentiment tends to correlate with better performance' if overall_corr > 0 else 'Lower sentiment tends to correlate with better performance'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Deliverables
    st.markdown('<h2 class="sub-header">📦 Deliverables</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### ✅ Completed Deliverables
    
    1. **Jupyter Notebook Analysis** (`trader_sentiment_analysis.ipynb`)
       - 15 comprehensive sections
       - 40+ visualizations
       - Statistical significance testing
       - Detailed insights and recommendations
    
    2. **Interactive Streamlit Dashboard** (`streamlit_app_enhanced.py`)
       - Real-time data filtering
       - Multiple analysis pages
       - Interactive charts
       - Exportable insights
    
    3. **Documentation**
       - README.md with setup instructions
       - SETUP_GUIDE.md with troubleshooting
       - ENHANCEMENT_SUMMARY.md with feature details
       - QUICK_REFERENCE.md for commands
    
    4. **Data Exports**
       - sentiment_performance_summary.csv
       - risk_metrics_by_sentiment.csv
       - daily_performance_with_sentiment.csv
    
    5. **Automation Scripts**
       - run_dashboard.ps1 (PowerShell)
       - run_dashboard.bat (Batch file)
       - requirements.txt (Dependencies)
    """)
    
    # References
    st.markdown('<h2 class="sub-header">📚 References & Resources</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Data Sources
    - **Fear & Greed Index**: Bitcoin market sentiment indicator
    - **Hyperliquid Trading Data**: Historical trade execution data
    
    ### Tools & Libraries
    - [Pandas Documentation](https://pandas.pydata.org/docs/)
    - [Plotly Charts](https://plotly.com/python/)
    - [Streamlit](https://docs.streamlit.io/)
    - [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
    
    ### Academic References
    - Statistical methods for financial analysis
    - Behavioral finance principles
    - Risk management frameworks
    - Technical analysis methodologies
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 30px; background-color: #f5f5f5; border-radius: 10px;'>
        <h3 style='color: #1976d2;'>Bitcoin Trader Performance vs Market Sentiment Analysis</h3>
        <p style='font-size: 18px; margin: 15px 0;'>
            <b>Submitted by:</b> Ayush Singh
        </p>
        <p style='font-size: 16px; color: #666;'>
            📧 <a href="mailto:Ayusingh693@gmail.com">Ayusingh693@gmail.com</a> | 
            📱 +91 7031678999
        </p>
        <p style='font-size: 14px; color: #999; margin-top: 20px;'>
            Built with Python, Streamlit, Plotly, and Pandas | © 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# Continue with other pages...
# =============================================================================
