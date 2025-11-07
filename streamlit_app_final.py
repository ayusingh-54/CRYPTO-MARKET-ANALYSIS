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
# DASHBOARD, ANALYTICS, RISK ANALYSIS, AND DEEP DIVE PAGES
# Integrated from continuation files
# =============================================================================

# Common sidebar filters (used across all pages except Assignment Details)
if page != "📋 Assignment Details":
    st.sidebar.markdown("---")
    st.sidebar.title("🎛️ Filter Options")
    
    # Date range filter
    min_date = merged_df['Date'].min().date()
    max_date = merged_df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Sentiment filter
    selected_sentiments = st.sidebar.multiselect(
        "😊 Select Sentiments",
        options=sentiment_order,
        default=sentiment_order
    )
    
    # Trade side filter
    selected_sides = st.sidebar.multiselect(
        "📊 Select Trade Sides",
        options=['BUY', 'SELL'],
        default=['BUY', 'SELL']
    )
    
    # PnL filter
    pnl_filter = st.sidebar.radio(
        "💰 PnL Filter",
        options=['All Trades', 'Profitable Only', 'Unprofitable Only']
    )
    
    # Apply filters
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = merged_df[
            (merged_df['Date'].dt.date >= start_date) & 
            (merged_df['Date'].dt.date <= end_date)
        ]
    else:
        filtered_df = merged_df
    
    filtered_df = filtered_df[filtered_df['sentiment_category'].isin(selected_sentiments)]
    filtered_df = filtered_df[filtered_df['Side'].isin(selected_sides)]
    
    if pnl_filter == 'Profitable Only':
        filtered_df = filtered_df[filtered_df['is_profitable']]
    elif pnl_filter == 'Unprofitable Only':
        filtered_df = filtered_df[~filtered_df['is_profitable']]
    
    # Display filter summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Current Filter")
    st.sidebar.info(f"""
    **Trades:** {len(filtered_df):,}  
    **Date Range:** {len(filtered_df['Date'].dt.date.unique())} days  
    **Sentiments:** {len(selected_sentiments)}  
    **Sides:** {', '.join(selected_sides)}
    """)

# =============================================================================
# PAGE 2: DASHBOARD
# =============================================================================

if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">🏠 Performance Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 25px; color: white;'>
        <p style='font-size: 20px; margin: 0;'>
            <b>📊 Comprehensive Analysis of Trading Performance Against Fear & Greed Index</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Dashboard
    st.markdown('<h2 class="sub-header">📈 Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_trades = len(filtered_df)
    total_pnl = filtered_df['Net_PnL'].sum()
    win_rate = (filtered_df['is_profitable'].sum() / total_trades * 100) if total_trades > 0 else 0
    avg_pnl = filtered_df['Net_PnL'].mean()
    total_volume = filtered_df['Size USD'].sum()
    
    with col1:
        st.metric("Total Trades", f"{total_trades:,}", 
                 delta=f"{total_trades - len(merged_df)}" if total_trades != len(merged_df) else None)
    with col2:
        st.metric("Net PnL", f"${total_pnl:,.2f}", 
                 delta=f"${total_pnl:,.2f}", 
                 delta_color="normal" if total_pnl >= 0 else "inverse")
    with col3:
        st.metric("Win Rate", f"{win_rate:.2f}%",
                 delta=f"{win_rate - 50:.2f}%" if win_rate != 50 else None,
                 delta_color="normal" if win_rate >= 50 else "inverse")
    with col4:
        st.metric("Avg PnL/Trade", f"${avg_pnl:.2f}",
                 delta=f"${avg_pnl:.2f}",
                 delta_color="normal" if avg_pnl >= 0 else "inverse")
    with col5:
        st.metric("Total Volume", f"${total_volume/1e6:.2f}M")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "💰 Profitability", 
        "📈 Time Series",
        "🎯 Sentiment Analysis"
    ])
    
    # TAB 1: Overview
    with tab1:
        st.markdown('<h3 class="sub-header">Market Sentiment Distribution</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment pie chart
            sentiment_dist = filtered_df['sentiment_category'].value_counts().reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Pie(
                labels=sentiment_dist.index,
                values=sentiment_dist.values,
                hole=0.4,
                marker=dict(colors=colors),
                textinfo='label+percent',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>Trades: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            fig.update_layout(
                title="Market Sentiment Distribution",
                height=400,
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5)
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # PnL by sentiment
            pnl_by_sentiment = filtered_df.groupby('sentiment_category')['Net_PnL'].sum().reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=pnl_by_sentiment.index,
                y=pnl_by_sentiment.values,
                marker=dict(
                    color=pnl_by_sentiment.values,
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="PnL ($)")
                ),
                text=[f'${v:,.0f}' for v in pnl_by_sentiment.values],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Total PnL: $%{y:,.2f}<extra></extra>'
            )])
            fig.update_layout(
                title="Total PnL by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Total Net PnL ($)",
                height=400
            )
            fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
            st.plotly_chart(fig, width='stretch')
        
        # Performance table
        st.markdown('<h3 class="sub-header">Detailed Performance Breakdown</h3>', unsafe_allow_html=True)
        
        sentiment_performance = filtered_df.groupby('sentiment_category').agg({
            'Net_PnL': ['sum', 'mean', 'std'],
            'Size USD': ['sum', 'mean'],
            'Fee': 'sum',
            'is_profitable': 'mean',
            'Account': 'count'
        }).round(2)
        
        sentiment_performance.columns = ['Total_PnL', 'Avg_PnL', 'Std_PnL', 'Total_Volume', 
                                         'Avg_Trade_Size', 'Total_Fees', 'Win_Rate', 'Trade_Count']
        sentiment_performance['Win_Rate'] = sentiment_performance['Win_Rate'] * 100
        sentiment_performance = sentiment_performance.reindex(sentiment_order, fill_value=0)
        
        st.dataframe(
            sentiment_performance.style.format({
                'Total_PnL': '${:,.2f}',
                'Avg_PnL': '${:,.2f}',
                'Std_PnL': '${:,.2f}',
                'Total_Volume': '${:,.2f}',
                'Avg_Trade_Size': '${:,.2f}',
                'Total_Fees': '${:,.2f}',
                'Win_Rate': '{:.2f}%',
                'Trade_Count': '{:,.0f}'
            }).background_gradient(cmap='RdYlGn', subset=['Total_PnL', 'Win_Rate', 'Avg_PnL']),
            width='stretch'
        )
    
    # TAB 2: Profitability
    with tab2:
        st.markdown('<h3 class="sub-header">Profitability Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Win rate comparison
            win_rate_by_sentiment = (filtered_df.groupby('sentiment_category')['is_profitable'].mean() * 100).reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=win_rate_by_sentiment.index,
                y=win_rate_by_sentiment.values,
                marker=dict(color=colors),
                text=[f'{v:.1f}%' for v in win_rate_by_sentiment.values],
                textposition='outside'
            )])
            fig.update_layout(
                title="Win Rate by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Win Rate (%)",
                height=400
            )
            fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="50% Baseline")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Average PnL
            avg_pnl_by_sentiment = filtered_df.groupby('sentiment_category')['Net_PnL'].mean().reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=avg_pnl_by_sentiment.index,
                y=avg_pnl_by_sentiment.values,
                marker=dict(color=colors),
                text=[f'${v:.2f}' for v in avg_pnl_by_sentiment.values],
                textposition='outside'
            )])
            fig.update_layout(
                title="Average PnL per Trade",
                xaxis_title="Sentiment",
                yaxis_title="Avg PnL ($)",
                height=400
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, width='stretch')
        
        # PnL Distribution
        st.markdown('<h3 class="sub-header">PnL Distribution (1st-99th Percentile)</h3>', unsafe_allow_html=True)
        
        pnl_filtered = filtered_df[filtered_df['Net_PnL'].between(
            filtered_df['Net_PnL'].quantile(0.01),
            filtered_df['Net_PnL'].quantile(0.99)
        )]
        
        fig = go.Figure()
        for sentiment in sentiment_order:
            if sentiment in pnl_filtered['sentiment_category'].values:
                sentiment_data = pnl_filtered[pnl_filtered['sentiment_category'] == sentiment]['Net_PnL']
                fig.add_trace(go.Box(
                    y=sentiment_data,
                    name=sentiment,
                    marker_color=colors_map[sentiment],
                    boxmean='sd'
                ))
        
        fig.update_layout(
            title="PnL Distribution by Sentiment",
            yaxis_title="Net PnL ($)",
            height=500,
            showlegend=True
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, width='stretch')
    
    # TAB 3: Time Series
    with tab3:
        st.markdown('<h3 class="sub-header">Temporal Analysis</h3>', unsafe_allow_html=True)
        
        # Daily cumulative PnL
        daily_perf = filtered_df.groupby('Date').agg({
            'Net_PnL': 'sum',
            'value': 'first'
        }).reset_index()
        daily_perf['Cumulative_PnL'] = daily_perf['Net_PnL'].cumsum()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=daily_perf['Date'],
                y=daily_perf['Cumulative_PnL'],
                name="Cumulative PnL",
                line=dict(color='#1976d2', width=3),
                fill='tonexty',
                fillcolor='rgba(25, 118, 210, 0.1)'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=daily_perf['Date'],
                y=daily_perf['value'],
                name="Fear & Greed Index",
                line=dict(color='#ff9800', width=2, dash='dot')
            ),
            secondary_y=True
        )
        
        # Add sentiment zones
        fig.add_hrect(y0=0, y1=25, fillcolor="red", opacity=0.1, layer="below", 
                     line_width=0, secondary_y=True, annotation_text="Extreme Fear", annotation_position="left")
        fig.add_hrect(y0=75, y1=100, fillcolor="green", opacity=0.1, layer="below",
                     line_width=0, secondary_y=True, annotation_text="Extreme Greed", annotation_position="left")
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Cumulative PnL ($)", secondary_y=False)
        fig.update_yaxes(title_text="Fear & Greed Index", secondary_y=True, range=[0, 100])
        
        fig.update_layout(
            title="Cumulative PnL vs Market Sentiment",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Rolling statistics
        st.markdown('<h3 class="sub-header">Rolling Performance Metrics</h3>', unsafe_allow_html=True)
        
        window = st.slider("Rolling Window (days)", 1, 30, 7, key="rolling_window")
        
        daily_perf[f'{window}D_MA'] = daily_perf['Net_PnL'].rolling(window=window).mean()
        daily_perf[f'{window}D_Std'] = daily_perf['Net_PnL'].rolling(window=window).std()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_perf['Date'],
            y=daily_perf['Net_PnL'],
            name="Daily PnL",
            line=dict(color='lightgray', width=1),
            opacity=0.5
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_perf['Date'],
            y=daily_perf[f'{window}D_MA'],
            name=f"{window}-Day MA",
            line=dict(color='#1976d2', width=3)
        ))
        
        fig.update_layout(
            title=f"Daily PnL with {window}-Day Moving Average",
            xaxis_title="Date",
            yaxis_title="PnL ($)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # TAB 4: Sentiment Analysis
    with tab4:
        st.markdown('<h3 class="sub-header">Sentiment Impact Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Trade distribution by sentiment
            trade_counts = filtered_df['sentiment_category'].value_counts().reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=trade_counts.index,
                y=trade_counts.values,
                marker=dict(color=colors),
                text=[f'{v:,}' for v in trade_counts.values],
                textposition='outside'
            )])
            fig.update_layout(
                title="Trade Count by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Number of Trades",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Average position size
            avg_position = filtered_df.groupby('sentiment_category')['Size USD'].mean().reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=avg_position.index,
                y=avg_position.values,
                marker=dict(color=colors),
                text=[f'${v:,.0f}' for v in avg_position.values],
                textposition='outside'
            )])
            fig.update_layout(
                title="Average Position Size",
                xaxis_title="Sentiment",
                yaxis_title="Avg Size (USD)",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        # Correlation heatmap
        st.markdown('<h3 class="sub-header">Feature Correlation Matrix</h3>', unsafe_allow_html=True)
        
        numeric_features = filtered_df[['value', 'Net_PnL', 'Size USD', 'Fee', 'Hour']].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=numeric_features.values,
            x=['Sentiment', 'PnL', 'Trade Size', 'Fee', 'Hour'],
            y=['Sentiment', 'PnL', 'Trade Size', 'Fee', 'Hour'],
            colorscale='RdBu',
            zmid=0,
            text=numeric_features.values.round(3),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Correlation Heatmap",
            height=500
        )
        st.plotly_chart(fig, width='stretch')

# Continue to next page...


if page == "📊 Advanced Analytics":
    st.markdown('<h1 class="main-header">📊 Advanced Analytics</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📈 Statistical Tests",
        "📉 Volatility Analysis",
        "💹 Drawdown Analysis",
        "🎯 Win/Loss Streaks"
    ])
    
    # TAB 1: Statistical Significance
    with tabs[0]:
        st.markdown('<h3 class="sub-header">Statistical Significance Testing</h3>', unsafe_allow_html=True)
        
        st.info("💡 **Purpose**: Determine if performance differences across sentiments are statistically significant or due to random chance.")
        
        # Prepare sentiment groups
        sentiment_groups = {}
        for sentiment in sentiment_order:
            if sentiment in filtered_df['sentiment_category'].values:
                sentiment_groups[sentiment] = filtered_df[filtered_df['sentiment_category'] == sentiment]['Net_PnL'].dropna()
        
        if len(sentiment_groups) >= 2:
            # ANOVA Test
            st.markdown("#### 1️⃣ One-Way ANOVA Test")
            st.markdown("Tests if mean PnL differs significantly across sentiment categories")
            
            f_stat, p_value = stats.f_oneway(*[sentiment_groups[s] for s in sentiment_groups.keys()])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("F-Statistic", f"{f_stat:.4f}")
            with col2:
                st.metric("P-Value", f"{p_value:.6f}")
            with col3:
                significance = "✅ SIGNIFICANT" if p_value < 0.05 else "❌ NOT SIGNIFICANT"
                st.metric("Result (α=0.05)", significance)
            
            if p_value < 0.05:
                st.success(f"**Conclusion**: PnL differs significantly across sentiments (p = {p_value:.6f} < 0.05)")
            else:
                st.warning(f"**Conclusion**: No significant difference detected (p = {p_value:.6f} ≥ 0.05)")
            
            # Kruskal-Wallis Test
            st.markdown("---")
            st.markdown("#### 2️⃣ Kruskal-Wallis Test (Non-Parametric)")
            st.markdown("Alternative to ANOVA that doesn't assume normal distribution")
            
            h_stat, p_value_kw = stats.kruskal(*[sentiment_groups[s] for s in sentiment_groups.keys()])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("H-Statistic", f"{h_stat:.4f}")
            with col2:
                st.metric("P-Value", f"{p_value_kw:.6f}")
            with col3:
                significance_kw = "✅ SIGNIFICANT" if p_value_kw < 0.05 else "❌ NOT SIGNIFICANT"
                st.metric("Result (α=0.05)", significance_kw)
            
            # Chi-Square Test
            st.markdown("---")
            st.markdown("#### 3️⃣ Chi-Square Test (Profitability vs Sentiment)")
            st.markdown("Tests if profitability is independent of market sentiment")
            
            contingency_table = pd.crosstab(filtered_df['sentiment_category'], filtered_df['is_profitable'])
            chi2, p_value_chi, dof, expected = stats.chi2_contingency(contingency_table)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Chi-Square", f"{chi2:.4f}")
            with col2:
                st.metric("P-Value", f"{p_value_chi:.6f}")
            with col3:
                st.metric("DOF", f"{dof}")
            with col4:
                significance_chi = "✅ SIGNIFICANT" if p_value_chi < 0.05 else "❌ NOT SIGNIFICANT"
                st.metric("Result", significance_chi)
            
            st.dataframe(contingency_table, width='stretch')
            
            # Pairwise Comparison
            if 'Extreme Fear' in sentiment_groups and 'Extreme Greed' in sentiment_groups:
                st.markdown("---")
                st.markdown("#### 4️⃣ Mann-Whitney U Test: Extreme Fear vs Extreme Greed")
                
                stat, p_value_mw = stats.mannwhitneyu(
                    sentiment_groups['Extreme Fear'],
                    sentiment_groups['Extreme Greed'],
                    alternative='two-sided'
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("U-Statistic", f"{stat:.4f}")
                with col2:
                    st.metric("P-Value", f"{p_value_mw:.6f}")
                
                if p_value_mw < 0.05:
                    st.success("**Conclusion**: Significant difference between Extreme Fear and Extreme Greed")
                else:
                    st.warning("**Conclusion**: No significant difference detected")
    
    # TAB 2: Volatility Analysis
    with tabs[1]:
        st.markdown('<h3 class="sub-header">Volatility & Risk Analysis</h3>', unsafe_allow_html=True)
        
        # Volatility by sentiment
        volatility_data = filtered_df.groupby('sentiment_category')['Net_PnL'].std().reindex(sentiment_order, fill_value=0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[go.Bar(
                x=volatility_data.index,
                y=volatility_data.values,
                marker=dict(color=colors),
                text=[f'${v:,.2f}' for v in volatility_data.values],
                textposition='outside'
            )])
            fig.update_layout(
                title="PnL Volatility (Standard Deviation)",
                xaxis_title="Sentiment",
                yaxis_title="Std Dev ($)",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Coefficient of Variation
            cv_data = filtered_df.groupby('sentiment_category').agg({
                'Net_PnL': ['mean', 'std']
            })
            cv_data['CV'] = (cv_data[('Net_PnL', 'std')] / cv_data[('Net_PnL', 'mean')].abs()) * 100
            cv_values = cv_data['CV'].reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=cv_values.index,
                y=cv_values.values,
                marker=dict(color=colors),
                text=[f'{v:.1f}%' for v in cv_values.values],
                textposition='outside'
            )])
            fig.update_layout(
                title="Coefficient of Variation (Risk/Return)",
                xaxis_title="Sentiment",
                yaxis_title="CV (%)",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        # Volatility insights
        st.markdown("---")
        st.markdown("### 💡 Volatility Insights")
        
        most_volatile = volatility_data.idxmax()
        least_volatile = volatility_data.idxmin()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="warning-box">
                <h4>⚠️ Most Volatile</h4>
                <h3>{most_volatile}</h3>
                <p>Std Dev: ${volatility_data[most_volatile]:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="success-box">
                <h4>✅ Least Volatile</h4>
                <h3>{least_volatile}</h3>
                <p>Std Dev: ${volatility_data[least_volatile]:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            most_efficient = cv_values.idxmin()
            st.markdown(f"""
            <div class="insight-box">
                <h4>🎯 Most Efficient</h4>
                <h3>{most_efficient}</h3>
                <p>CV: {cv_values[most_efficient]:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: Drawdown Analysis
    with tabs[2]:
        st.markdown('<h3 class="sub-header">Maximum Drawdown Analysis</h3>', unsafe_allow_html=True)
        
        st.info("💡 **Drawdown**: The peak-to-trough decline during a specific period. Critical for understanding worst-case scenarios.")
        
        # Calculate drawdown
        daily_pnl = filtered_df.groupby('Date')['Net_PnL'].sum().sort_index()
        cumulative_pnl = daily_pnl.cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = cumulative_pnl - running_max
        drawdown_pct = (drawdown / running_max.replace(0, np.nan)) * 100
        
        # Visualization
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Cumulative PnL with Drawdown", "Drawdown Percentage"),
            row_heights=[0.6, 0.4],
            shared_xaxes=True
        )
        
        fig.add_trace(
            go.Scatter(x=cumulative_pnl.index, y=cumulative_pnl.values,
                      name="Cumulative PnL", line=dict(color='#1976d2', width=2)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=running_max.index, y=running_max.values,
                      name="Running Max", line=dict(color='#4caf50', width=2, dash='dash')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=drawdown_pct.index, y=drawdown_pct.values,
                      name="Drawdown %", fill='tozeroy', 
                      line=dict(color='#f44336', width=1),
                      fillcolor='rgba(244, 67, 54, 0.3)'),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="PnL ($)", row=1, col=1)
        fig.update_yaxes(title_text="Drawdown (%)", row=2, col=1)
        
        fig.update_layout(height=600, hovermode='x unified', showlegend=True)
        st.plotly_chart(fig, width='stretch')
        
        # Drawdown metrics
        max_dd = drawdown.min()
        max_dd_pct = drawdown_pct.min()
        max_dd_date = drawdown.idxmin()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Maximum Drawdown", f"${max_dd:,.2f}",
                     delta=f"{max_dd_pct:.2f}%", delta_color="inverse")
        with col2:
            st.metric("Max DD Date", max_dd_date.strftime('%Y-%m-%d'))
        with col3:
            recovery_dates = cumulative_pnl[cumulative_pnl.index > max_dd_date]
            peak_before = running_max.loc[max_dd_date]
            if len(recovery_dates[recovery_dates >= peak_before]) > 0:
                recovery_date = recovery_dates[recovery_dates >= peak_before].index[0]
                recovery_days = (recovery_date - max_dd_date).days
                st.metric("Recovery Time", f"{recovery_days} days")
            else:
                st.metric("Recovery Time", "Not yet recovered", delta_color="inverse")
    
    # TAB 4: Streak Analysis
    with tabs[3]:
        st.markdown('<h3 class="sub-header">Win/Loss Streak Analysis</h3>', unsafe_allow_html=True)
        
        st.info("💡 **Streaks**: Consecutive winning or losing trades. Understanding streaks helps identify momentum and potential reversals.")
        
        # Calculate streaks
        sorted_df = filtered_df.sort_values('Timestamp IST').reset_index(drop=True)
        sorted_df['streak_id'] = (sorted_df['is_profitable'] != sorted_df['is_profitable'].shift()).cumsum()
        
        streak_analysis = sorted_df.groupby('streak_id').agg({
            'is_profitable': 'first',
            'Net_PnL': ['sum', 'count'],
            'sentiment_category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
        })
        
        streak_analysis.columns = ['is_win_streak', 'total_pnl', 'streak_length', 'dominant_sentiment']
        
        win_streaks = streak_analysis[streak_analysis['is_win_streak'] == True]['streak_length']
        loss_streaks = streak_analysis[streak_analysis['is_win_streak'] == False]['streak_length']
        
        # Streak distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=win_streaks, name="Win Streaks",
                                      marker_color='#4caf50', opacity=0.7, nbinsx=20))
            fig.add_trace(go.Histogram(x=loss_streaks, name="Loss Streaks",
                                      marker_color='#f44336', opacity=0.7, nbinsx=20))
            fig.update_layout(
                title="Streak Length Distribution",
                xaxis_title="Streak Length (# trades)",
                yaxis_title="Frequency",
                barmode='overlay',
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Streak metrics
            st.markdown("### 📊 Streak Metrics")
            st.markdown(f"""
            <div class="success-box">
                <h4>🏆 Win Streaks</h4>
                <p><b>Longest:</b> {win_streaks.max()} trades</p>
                <p><b>Average:</b> {win_streaks.mean():.2f} trades</p>
                <p><b>Total Count:</b> {len(win_streaks)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="warning-box">
                <h4>📉 Loss Streaks</h4>
                <p><b>Longest:</b> {loss_streaks.max()} trades</p>
                <p><b>Average:</b> {loss_streaks.mean():.2f} trades</p>
                <p><b>Total Count:</b> {len(loss_streaks)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Streak by sentiment
        st.markdown("---")
        st.markdown("### Streak Distribution by Sentiment")
        
        streak_by_sentiment = streak_analysis.groupby(['dominant_sentiment', 'is_win_streak'])['streak_length'].mean().unstack(fill_value=0)
        streak_by_sentiment = streak_by_sentiment.reindex(sentiment_order)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Loss Streaks',
            x=streak_by_sentiment.index,
            y=streak_by_sentiment[False] if False in streak_by_sentiment.columns else [0]*len(streak_by_sentiment),
            marker_color='#f44336'
        ))
        fig.add_trace(go.Bar(
            name='Win Streaks',
            x=streak_by_sentiment.index,
            y=streak_by_sentiment[True] if True in streak_by_sentiment.columns else [0]*len(streak_by_sentiment),
            marker_color='#4caf50'
        ))
        
        fig.update_layout(
            title="Average Streak Length by Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Avg Streak Length",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, width='stretch')

# =============================================================================
# PAGE 4: RISK ANALYSIS
# =============================================================================

if page == "📈 Risk Analysis":
    st.markdown('<h1 class="main-header">📈 Risk & Performance Metrics</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs([
        "⚖️ Risk-Reward",
        "💼 Position Sizing",
        "⏰ Time Analysis",
        "💡 Key Insights"
    ])
    
    # TAB 1: Risk-Reward
    with tabs[0]:
        st.markdown('<h3 class="sub-header">Risk-Adjusted Performance</h3>', unsafe_allow_html=True)
        
        risk_metrics = filtered_df.groupby('sentiment_category').agg({
            'Net_PnL': ['mean', 'std', 'min', 'max'],
            'Size USD': ['mean', 'std']
        }).round(2)
        
        risk_metrics.columns = ['Avg_PnL', 'PnL_StdDev', 'Max_Loss', 'Max_Profit',
                               'Avg_Trade_Size', 'Trade_Size_StdDev']
        risk_metrics['Sharpe_Ratio'] = (risk_metrics['Avg_PnL'] / risk_metrics['PnL_StdDev']).round(3)
        risk_metrics = risk_metrics.reindex(sentiment_order, fill_value=0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[go.Bar(
                x=risk_metrics.index,
                y=risk_metrics['Sharpe_Ratio'],
                marker=dict(color=colors),
                text=[f'{v:.3f}' for v in risk_metrics['Sharpe_Ratio']],
                textposition='outside'
            )])
            fig.update_layout(
                title="Sharpe Ratio by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Sharpe Ratio",
                height=400
            )
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Risk-Return scatter
            fig = go.Figure()
            for i, sentiment in enumerate(sentiment_order):
                if sentiment in risk_metrics.index:
                    fig.add_trace(go.Scatter(
                        x=[risk_metrics.loc[sentiment, 'PnL_StdDev']],
                        y=[risk_metrics.loc[sentiment, 'Avg_PnL']],
                        mode='markers+text',
                        name=sentiment,
                        marker=dict(size=20, color=colors[i]),
                        text=[sentiment],
                        textposition='top center'
                    ))
            
            fig.update_layout(
                title="Risk-Return Profile",
                xaxis_title="Risk (Std Dev)",
                yaxis_title="Return (Avg PnL)",
                height=400,
                showlegend=False
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, width='stretch')
        
        # Risk metrics table
        st.markdown("---")
        st.markdown("### Complete Risk Metrics Table")
        st.dataframe(
            risk_metrics.style.format({
                'Avg_PnL': '${:,.2f}',
                'PnL_StdDev': '${:,.2f}',
                'Max_Loss': '${:,.2f}',
                'Max_Profit': '${:,.2f}',
                'Avg_Trade_Size': '${:,.2f}',
                'Trade_Size_StdDev': '${:,.2f}',
                'Sharpe_Ratio': '{:.3f}'
            }).background_gradient(cmap='RdYlGn', subset=['Sharpe_Ratio', 'Avg_PnL']),
            width='stretch'
        )
    
    # TAB 2: Position Sizing
    with tabs[1]:
        st.markdown('<h3 class="sub-header">Position Size Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Position size distribution
            fig = go.Figure()
            for i, sentiment in enumerate(sentiment_order):
                sentiment_data = filtered_df[filtered_df['sentiment_category'] == sentiment]
                if len(sentiment_data) > 0:
                    fig.add_trace(go.Box(
                        y=sentiment_data['Size USD'],
                        name=sentiment,
                        marker_color=colors[i],
                        boxmean='sd'
                    ))
            
            fig.update_layout(
                title="Position Size Distribution by Sentiment",
                yaxis_title="Position Size (USD)",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Position size vs PnL
            fig = go.Figure()
            for i, sentiment in enumerate(sentiment_order):
                sentiment_data = filtered_df[filtered_df['sentiment_category'] == sentiment]
                if len(sentiment_data) > 0:
                    fig.add_trace(go.Scatter(
                        x=sentiment_data['Size USD'],
                        y=sentiment_data['Net_PnL'],
                        mode='markers',
                        name=sentiment,
                        marker=dict(color=colors[i], size=8, opacity=0.6)
                    ))
            
            fig.update_layout(
                title="Position Size vs PnL",
                xaxis_title="Position Size (USD)",
                yaxis_title="Net PnL (USD)",
                height=400,
                hovermode='closest'
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, width='stretch')
        
        # Position size insights
        st.markdown("---")
        position_stats = filtered_df.groupby('sentiment_category').agg({
            'Size USD': ['mean', 'median', 'std', 'min', 'max']
        }).round(2)
        position_stats.columns = ['Mean', 'Median', 'Std Dev', 'Min', 'Max']
        position_stats = position_stats.reindex(sentiment_order, fill_value=0)
        
        st.markdown("### Position Size Statistics")
        st.dataframe(
            position_stats.style.format('${:,.2f}').background_gradient(cmap='Blues'),
            width='stretch'
        )
        
        # Average position by profitability
        col1, col2 = st.columns(2)
        
        with col1:
            avg_size_profit = filtered_df.groupby(['sentiment_category', 'is_profitable'])['Size USD'].mean().unstack(fill_value=0)
            avg_size_profit = avg_size_profit.reindex(sentiment_order)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Losing Trades',
                x=avg_size_profit.index,
                y=avg_size_profit[False] if False in avg_size_profit.columns else [0]*len(avg_size_profit),
                marker_color='#f44336'
            ))
            fig.add_trace(go.Bar(
                name='Winning Trades',
                x=avg_size_profit.index,
                y=avg_size_profit[True] if True in avg_size_profit.columns else [0]*len(avg_size_profit),
                marker_color='#4caf50'
            ))
            
            fig.update_layout(
                title="Average Position Size by Outcome",
                xaxis_title="Sentiment",
                yaxis_title="Avg Position Size (USD)",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Position size over time
            weekly_size = filtered_df.groupby(filtered_df['Date'].dt.to_period('W'))['Size USD'].mean()
            weekly_size.index = weekly_size.index.to_timestamp()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=weekly_size.index,
                y=weekly_size.values,
                mode='lines+markers',
                line=dict(color='#1976d2', width=2),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(25, 118, 210, 0.1)'
            ))
            
            fig.update_layout(
                title="Average Weekly Position Size Trend",
                xaxis_title="Week",
                yaxis_title="Avg Position Size (USD)",
                height=400,
                hovermode='x'
            )
            st.plotly_chart(fig, width='stretch')
    
    # TAB 3: Time Analysis
    with tabs[2]:
        st.markdown('<h3 class="sub-header">Temporal Patterns</h3>', unsafe_allow_html=True)
        
        # Add time columns if not present
        if 'Hour' not in filtered_df.columns:
            filtered_df['Hour'] = pd.to_datetime(filtered_df['Timestamp IST']).dt.hour
        if 'DayOfWeek' not in filtered_df.columns:
            filtered_df['DayOfWeek'] = pd.to_datetime(filtered_df['Timestamp IST']).dt.day_name()
        if 'Month' not in filtered_df.columns:
            filtered_df['Month'] = pd.to_datetime(filtered_df['Timestamp IST']).dt.month_name()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Hourly performance
            hourly_pnl = filtered_df.groupby('Hour')['Net_PnL'].sum()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=hourly_pnl.index,
                y=hourly_pnl.values,
                marker_color=['#4caf50' if v > 0 else '#f44336' for v in hourly_pnl.values],
                text=[f'${v:,.0f}' for v in hourly_pnl.values],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Total PnL by Hour of Day",
                xaxis_title="Hour (IST)",
                yaxis_title="Total PnL (USD)",
                height=400,
                xaxis=dict(tickmode='linear', tick0=0, dtick=2)
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Day of week performance
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pnl = filtered_df.groupby('DayOfWeek')['Net_PnL'].sum().reindex(day_order, fill_value=0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=daily_pnl.index,
                y=daily_pnl.values,
                marker_color=['#4caf50' if v > 0 else '#f44336' for v in daily_pnl.values],
                text=[f'${v:,.0f}' for v in daily_pnl.values],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Total PnL by Day of Week",
                xaxis_title="Day",
                yaxis_title="Total PnL (USD)",
                height=400
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, width='stretch')
        
        # Trading session analysis
        st.markdown("---")
        st.markdown("### 🌐 Trading Session Performance")
        
        session_perf = filtered_df.groupby('Trading_Session').agg({
            'Net_PnL': ['sum', 'mean', 'count'],
            'is_profitable': 'mean'
        }).round(2)
        session_perf.columns = ['Total_PnL', 'Avg_PnL', 'Trade_Count', 'Win_Rate']
        session_perf['Win_Rate'] = (session_perf['Win_Rate'] * 100).round(1)
        
        # Heatmap: Session vs Sentiment
        heatmap_data = filtered_df.pivot_table(
            values='Net_PnL',
            index='Trading_Session',
            columns='sentiment_category',
            aggfunc='mean'
        ).reindex(columns=sentiment_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn',
            zmid=0,
            text=heatmap_data.values.round(2),
            texttemplate='$%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Avg PnL")
        ))
        
        fig.update_layout(
            title="Average PnL: Trading Session vs Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Trading Session",
            height=400
        )
        st.plotly_chart(fig, width='stretch')
        
        # Session stats table
        st.dataframe(
            session_perf.style.format({
                'Total_PnL': '${:,.2f}',
                'Avg_PnL': '${:,.2f}',
                'Trade_Count': '{:,.0f}',
                'Win_Rate': '{:.1f}%'
            }).background_gradient(cmap='RdYlGn', subset=['Total_PnL', 'Avg_PnL', 'Win_Rate']),
            width='stretch'
        )
    
    # TAB 4: Key Insights
    with tabs[3]:
        st.markdown('<h3 class="sub-header">💡 Comprehensive Risk Insights</h3>', unsafe_allow_html=True)
        
        # Best/worst performers
        sentiment_summary = filtered_df.groupby('sentiment_category').agg({
            'Net_PnL': ['sum', 'mean', 'std'],
            'is_profitable': 'mean',
            'Size USD': 'mean'
        }).round(2)
        sentiment_summary.columns = ['Total_PnL', 'Avg_PnL', 'PnL_StdDev', 'Win_Rate', 'Avg_Size']
        sentiment_summary['Sharpe'] = (sentiment_summary['Avg_PnL'] / sentiment_summary['PnL_StdDev']).round(3)
        sentiment_summary = sentiment_summary.reindex(sentiment_order)
        
        col1, col2, col3 = st.columns(3)
        
        best_sharpe = sentiment_summary['Sharpe'].idxmax()
        worst_sharpe = sentiment_summary['Sharpe'].idxmin()
        most_consistent = sentiment_summary['PnL_StdDev'].idxmin()
        
        with col1:
            st.markdown(f"""
            <div class="success-box">
                <h4>🏆 Best Risk-Adjusted</h4>
                <h3>{best_sharpe}</h3>
                <p><b>Sharpe Ratio:</b> {sentiment_summary.loc[best_sharpe, 'Sharpe']:.3f}</p>
                <p><b>Avg PnL:</b> ${sentiment_summary.loc[best_sharpe, 'Avg_PnL']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="warning-box">
                <h4>⚠️ Worst Risk-Adjusted</h4>
                <h3>{worst_sharpe}</h3>
                <p><b>Sharpe Ratio:</b> {sentiment_summary.loc[worst_sharpe, 'Sharpe']:.3f}</p>
                <p><b>Avg PnL:</b> ${sentiment_summary.loc[worst_sharpe, 'Avg_PnL']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="insight-box">
                <h4>📊 Most Consistent</h4>
                <h3>{most_consistent}</h3>
                <p><b>Std Dev:</b> ${sentiment_summary.loc[most_consistent, 'PnL_StdDev']:,.2f}</p>
                <p><b>Win Rate:</b> {sentiment_summary.loc[most_consistent, 'Win_Rate']*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Actionable recommendations
        st.markdown("---")
        st.markdown("### 🎯 Actionable Recommendations")
        
        recommendations = []
        
        # Check for high volatility
        high_vol_sentiments = sentiment_summary[sentiment_summary['PnL_StdDev'] > sentiment_summary['PnL_StdDev'].median()].index.tolist()
        if high_vol_sentiments:
            recommendations.append(f"⚠️ **High Volatility Alert**: {', '.join(high_vol_sentiments)} show above-median volatility. Consider reducing position sizes.")
        
        # Check for negative Sharpe
        negative_sharpe = sentiment_summary[sentiment_summary['Sharpe'] < 0].index.tolist()
        if negative_sharpe:
            recommendations.append(f"❌ **Negative Sharpe Ratios**: {', '.join(negative_sharpe)} have negative risk-adjusted returns. Re-evaluate strategy.")
        
        # Check for best opportunities
        positive_sharpe = sentiment_summary[sentiment_summary['Sharpe'] > 0.5].index.tolist()
        if positive_sharpe:
            recommendations.append(f"✅ **Strong Opportunities**: {', '.join(positive_sharpe)} show favorable risk-adjusted returns (Sharpe > 0.5).")
        
        # Position sizing recommendation
        avg_pos_size = filtered_df['Size USD'].mean()
        if sentiment_summary.loc[best_sharpe, 'Avg_Size'] < avg_pos_size:
            recommendations.append(f"💡 **Position Sizing**: Best performer ({best_sharpe}) uses below-average position sizes. Consider conservative sizing.")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        if not recommendations:
            st.success("✅ No major risk concerns detected. Performance appears balanced across sentiments.")

# =============================================================================
# Footer for all pages (except Assignment Details)
# =============================================================================
if page != "📋 Assignment Details":
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p><b>Bitcoin Trader Performance vs Market Sentiment Dashboard</b></p>
        <p>Created by Ayush Singh | Ayusingh693@gmail.com | +91 7031678999</p>
        <p>Built with Streamlit • Powered by Plotly • Analyzed with Pandas</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE 5: DEEP DIVE
# =============================================================================

if page == "🔍 Deep Dive":
    st.markdown('<h1 class="main-header">🔍 Deep Dive Analysis</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📊 Trade Explorer",
        "🔄 Trade Sides",
        "💰 Fee Analysis",
        "📈 Advanced Metrics"
    ])
    
    # TAB 1: Trade Explorer
    with tabs[0]:
        st.markdown('<h3 class="sub-header">Individual Trade Analysis</h3>', unsafe_allow_html=True)
        
        # Filters for trade exploration
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pnl_threshold = st.slider("Min Absolute PnL ($)", 0, 500, 0, 10)
        with col2:
            selected_side = st.selectbox("Trade Side", ["All", "BUY", "SELL"])
        with col3:
            sort_by = st.selectbox("Sort By", ["Net_PnL", "Size USD", "Fee", "PnL_Percentage"])
        
        # Filter trades
        explore_df = filtered_df.copy()
        if pnl_threshold > 0:
            explore_df = explore_df[abs(explore_df['Net_PnL']) >= pnl_threshold]
        if selected_side != "All":
            explore_df = explore_df[explore_df['Side'] == selected_side]
        
        explore_df = explore_df.sort_values(sort_by, ascending=False)
        
        # Top trades
        st.markdown(f"### 🔝 Top 10 Trades (Sorted by {sort_by})")
        
        display_cols = ['Timestamp IST', 'sentiment_category', 'Side', 'Size USD', 
                       'Closed PnL', 'Fee', 'Net_PnL', 'PnL_Percentage', 'Trading_Session']
        
        top_10 = explore_df.head(10)[display_cols].reset_index(drop=True)
        
        st.dataframe(
            top_10.style.format({
                'Size USD': '${:,.2f}',
                'Closed PnL': '${:,.2f}',
                'Fee': '${:,.2f}',
                'Net_PnL': '${:,.2f}',
                'PnL_Percentage': '{:.2f}%'
            }).background_gradient(cmap='RdYlGn', subset=['Net_PnL', 'PnL_Percentage']),
            width='stretch',
            height=400
        )
        
        # Download button
        csv = explore_df[display_cols].to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Trades as CSV",
            data=csv,
            file_name=f"filtered_trades_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Summary stats
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Filtered Trades", f"{len(explore_df):,}")
        with col2:
            st.metric("Total PnL", f"${explore_df['Net_PnL'].sum():,.2f}")
        with col3:
            st.metric("Avg PnL", f"${explore_df['Net_PnL'].mean():,.2f}")
        with col4:
            st.metric("Win Rate", f"{(explore_df['is_profitable'].mean() * 100):.1f}%")
        with col5:
            st.metric("Total Fees", f"${explore_df['Fee'].sum():,.2f}")
    
    # TAB 2: Trade Sides Analysis
    with tabs[1]:
        st.markdown('<h3 class="sub-header">BUY vs SELL Performance</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Side performance by sentiment
            side_sentiment = filtered_df.pivot_table(
                values='Net_PnL',
                index='sentiment_category',
                columns='Side',
                aggfunc='sum'
            ).reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure()
            for side in side_sentiment.columns:
                fig.add_trace(go.Bar(
                    name=side,
                    x=side_sentiment.index,
                    y=side_sentiment[side],
                    text=[f'${v:,.0f}' for v in side_sentiment[side]],
                    textposition='outside'
                ))
            
            fig.update_layout(
                title="Total PnL: BUY vs SELL by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Total PnL (USD)",
                barmode='group',
                height=400
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Win rate by side
            side_winrate = filtered_df.groupby(['sentiment_category', 'Side'])['is_profitable'].mean().unstack(fill_value=0) * 100
            side_winrate = side_winrate.reindex(sentiment_order)
            
            fig = go.Figure()
            for side in side_winrate.columns:
                fig.add_trace(go.Bar(
                    name=side,
                    x=side_winrate.index,
                    y=side_winrate[side],
                    text=[f'{v:.1f}%' for v in side_winrate[side]],
                    textposition='outside'
                ))
            
            fig.update_layout(
                title="Win Rate: BUY vs SELL by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Win Rate (%)",
                barmode='group',
                height=400
            )
            fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="50% Baseline")
            st.plotly_chart(fig, width='stretch')
        
        # Side comparison table
        st.markdown("---")
        st.markdown("### 📊 Detailed Side Comparison")
        
        side_comparison = filtered_df.groupby('Side').agg({
            'Net_PnL': ['sum', 'mean', 'std'],
            'Size USD': 'mean',
            'Fee': 'sum',
            'is_profitable': 'mean',
            'Timestamp IST': 'count'
        }).round(2)
        
        side_comparison.columns = ['Total_PnL', 'Avg_PnL', 'PnL_StdDev', 'Avg_Position', 'Total_Fees', 'Win_Rate', 'Trade_Count']
        side_comparison['Win_Rate'] = (side_comparison['Win_Rate'] * 100).round(1)
        
        st.dataframe(
            side_comparison.style.format({
                'Total_PnL': '${:,.2f}',
                'Avg_PnL': '${:,.2f}',
                'PnL_StdDev': '${:,.2f}',
                'Avg_Position': '${:,.2f}',
                'Total_Fees': '${:,.2f}',
                'Win_Rate': '{:.1f}%',
                'Trade_Count': '{:,.0f}'
            }).background_gradient(cmap='RdYlGn', subset=['Total_PnL', 'Avg_PnL', 'Win_Rate']),
            width='stretch'
        )
    
    # TAB 3: Fee Analysis
    with tabs[2]:
        st.markdown('<h3 class="sub-header">Trading Fee Impact</h3>', unsafe_allow_html=True)
        
        total_fees = filtered_df['Fee'].sum()
        total_gross_profit = filtered_df['Closed PnL'].sum()
        fee_percentage = (total_fees / total_gross_profit * 100) if total_gross_profit != 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Fees Paid", f"${total_fees:,.2f}")
        with col2:
            st.metric("Gross Profit", f"${total_gross_profit:,.2f}")
        with col3:
            st.metric("Fees as % of Profit", f"{fee_percentage:.2f}%")
        
        # Fee analysis by sentiment
        col1, col2 = st.columns(2)
        
        with col1:
            fee_by_sentiment = filtered_df.groupby('sentiment_category')['Fee'].sum().reindex(sentiment_order, fill_value=0)
            
            fig = go.Figure(data=[go.Bar(
                x=fee_by_sentiment.index,
                y=fee_by_sentiment.values,
                marker=dict(color=colors),
                text=[f'${v:,.2f}' for v in fee_by_sentiment.values],
                textposition='outside'
            )])
            
            fig.update_layout(
                title="Total Fees by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Total Fees (USD)",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Fee ratio by sentiment
            fee_ratio = filtered_df.groupby('sentiment_category')['Fee_Ratio'].mean().reindex(sentiment_order, fill_value=0) * 100
            
            fig = go.Figure(data=[go.Bar(
                x=fee_ratio.index,
                y=fee_ratio.values,
                marker=dict(color=colors),
                text=[f'{v:.2f}%' for v in fee_ratio.values],
                textposition='outside'
            )])
            
            fig.update_layout(
                title="Average Fee Ratio by Sentiment",
                xaxis_title="Sentiment",
                yaxis_title="Fee Ratio (%)",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        
        # Fee impact insights
        st.markdown("---")
        st.markdown("### 💡 Fee Impact Insights")
        
        high_fee_trades = filtered_df[filtered_df['Fee_Ratio'] > filtered_df['Fee_Ratio'].quantile(0.75)]
        low_fee_trades = filtered_df[filtered_df['Fee_Ratio'] <= filtered_df['Fee_Ratio'].quantile(0.25)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="warning-box">
                <h4>⚠️ High Fee Ratio Trades (Top 25%)</h4>
                <p><b>Count:</b> {len(high_fee_trades):,}</p>
                <p><b>Avg Fee Ratio:</b> {high_fee_trades['Fee_Ratio'].mean()*100:.2f}%</p>
                <p><b>Avg Net PnL:</b> ${high_fee_trades['Net_PnL'].mean():,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="success-box">
                <h4>✅ Low Fee Ratio Trades (Bottom 25%)</h4>
                <p><b>Count:</b> {len(low_fee_trades):,}</p>
                <p><b>Avg Fee Ratio:</b> {low_fee_trades['Fee_Ratio'].mean()*100:.2f}%</p>
                <p><b>Avg Net PnL:</b> ${low_fee_trades['Net_PnL'].mean():,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 4: Advanced Metrics
    with tabs[3]:
        st.markdown('<h3 class="sub-header">Advanced Performance Metrics</h3>', unsafe_allow_html=True)
        
        # Calculate advanced metrics
        metrics_df = filtered_df.groupby('sentiment_category').agg({
            'Net_PnL': ['sum', 'mean', 'std', 'count'],
            'Win_Loss_Magnitude': 'mean',
            'is_profitable': 'mean',
            'Size USD': 'mean'
        }).round(2)
        
        metrics_df.columns = ['Total_PnL', 'Avg_PnL', 'Volatility', 'Trades', 'Avg_Magnitude', 'Win_Rate', 'Avg_Size']
        metrics_df['Sharpe_Ratio'] = (metrics_df['Avg_PnL'] / metrics_df['Volatility']).round(3)
        metrics_df['Profit_Factor'] = metrics_df['Total_PnL'] / (metrics_df['Trades'] * metrics_df['Volatility'])
        metrics_df = metrics_df.reindex(sentiment_order)
        
        # Radar chart for comprehensive view
        fig = go.Figure()
        
        # Normalize metrics for radar chart
        for sentiment in sentiment_order[:3]:  # Top 3 sentiments for clarity
            if sentiment in metrics_df.index:
                normalized_sharpe = (metrics_df.loc[sentiment, 'Sharpe_Ratio'] + 2) / 4 * 100  # Scale to 0-100
                normalized_winrate = metrics_df.loc[sentiment, 'Win_Rate'] * 100
                normalized_magnitude = metrics_df.loc[sentiment, 'Avg_Magnitude'] / metrics_df['Avg_Magnitude'].max() * 100
                
                fig.add_trace(go.Scatterpolar(
                    r=[normalized_winrate, normalized_sharpe, normalized_magnitude],
                    theta=['Win Rate', 'Sharpe Ratio', 'Magnitude'],
                    fill='toself',
                    name=sentiment
                ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Performance Radar: Top 3 Sentiments",
            height=500
        )
        st.plotly_chart(fig, width='stretch')
        
        # Complete metrics table
        st.markdown("---")
        st.markdown("### 📊 Complete Advanced Metrics")
        
        st.dataframe(
            metrics_df.style.format({
                'Total_PnL': '${:,.2f}',
                'Avg_PnL': '${:,.2f}',
                'Volatility': '${:,.2f}',
                'Trades': '{:,.0f}',
                'Avg_Magnitude': '{:.2f}',
                'Win_Rate': '{:.2%}',
                'Avg_Size': '${:,.2f}',
                'Sharpe_Ratio': '{:.3f}',
                'Profit_Factor': '{:.3f}'
            }).background_gradient(cmap='RdYlGn', subset=['Total_PnL', 'Sharpe_Ratio', 'Win_Rate']),
            width='stretch'
        )
        
        # Final summary
        st.markdown("---")
        st.markdown("### 🎯 Final Performance Summary")
        
        best_overall = metrics_df['Total_PnL'].idxmax()
        best_sharpe = metrics_df['Sharpe_Ratio'].idxmax()
        best_winrate = metrics_df['Win_Rate'].idxmax()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="success-box">
                <h4>💰 Best Total Return</h4>
                <h3>{best_overall}</h3>
                <p>${metrics_df.loc[best_overall, 'Total_PnL']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="success-box">
                <h4>📈 Best Risk-Adjusted</h4>
                <h3>{best_sharpe}</h3>
                <p>Sharpe: {metrics_df.loc[best_sharpe, 'Sharpe_Ratio']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="success-box">
                <h4>🎯 Best Win Rate</h4>
                <h3>{best_winrate}</h3>
                <p>{metrics_df.loc[best_winrate, 'Win_Rate']*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# FOOTER FOR ALL ANALYSIS PAGES
# =============================================================================

if page != "📋 Assignment Details":
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p><b>Bitcoin Trader Performance vs Market Sentiment Dashboard</b></p>
        <p>Created by Ayush Singh | Ayusingh693@gmail.com | +91 7031678999</p>
        <p>Built with Streamlit • Powered by Plotly • Analyzed with Pandas</p>
    </div>
    """, unsafe_allow_html=True)

