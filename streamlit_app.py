"""
Advanced Bitcoin Trader Performance vs Market Sentiment Dashboard
Interactive Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Bitcoin Sentiment & Trading Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 5px solid #1f77b4;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    """Load and preprocess the datasets"""
    try:
        # Load datasets
        fear_greed_df = pd.read_csv('fear_greed_index.csv')
        historical_df = pd.read_csv('historical_data.csv')
        
        # Clean Fear & Greed data
        fear_greed_df['date'] = pd.to_datetime(fear_greed_df['date'])
        fear_greed_df = fear_greed_df.sort_values('date').reset_index(drop=True)
        
        # Clean Historical Trading Data
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
        
        # Remove invalid dates
        historical_df = historical_df.dropna(subset=['Date'])
        
        # Merge datasets
        merged_df = pd.merge(
            historical_df,
            fear_greed_df[['date', 'value', 'classification']],
            left_on='Date',
            right_on='date',
            how='left'
        )
        
        # Forward fill missing sentiment data
        merged_df['classification'] = merged_df.groupby(merged_df['Date'].notna())['classification'].fillna(method='ffill')
        merged_df['value'] = merged_df.groupby(merged_df['Date'].notna())['value'].fillna(method='ffill')
        merged_df = merged_df.dropna(subset=['classification'])
        
        # Feature engineering
        merged_df['Net_PnL'] = merged_df['Closed PnL'] - merged_df['Fee']
        merged_df['is_profitable'] = merged_df['Net_PnL'] > 0
        merged_df['Hour'] = merged_df['Timestamp IST'].dt.hour
        merged_df['DayOfWeek'] = merged_df['Timestamp IST'].dt.dayofweek
        merged_df['Month'] = merged_df['Timestamp IST'].dt.month
        
        # Categorize sentiment
        def categorize_sentiment(classification):
            if classification == 'Extreme Fear':
                return 'Extreme Fear'
            elif classification == 'Fear':
                return 'Fear'
            elif classification == 'Neutral':
                return 'Neutral'
            elif classification == 'Greed':
                return 'Greed'
            else:
                return 'Extreme Greed'
        
        merged_df['sentiment_category'] = merged_df['classification'].apply(categorize_sentiment)
        
        return fear_greed_df, historical_df, merged_df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

# Load data
fear_greed_df, historical_df, merged_df = load_data()

if merged_df is None:
    st.error("Failed to load data. Please ensure fear_greed_index.csv and historical_data.csv are in the current directory.")
    st.stop()

# Sidebar filters
st.sidebar.title("🎛️ Filter Options")

# Date range filter
min_date = merged_df['Date'].min().date()
max_date = merged_df['Date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Sentiment filter
sentiment_order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
selected_sentiments = st.sidebar.multiselect(
    "Select Sentiments",
    options=sentiment_order,
    default=sentiment_order
)

# Trade side filter
selected_sides = st.sidebar.multiselect(
    "Select Trade Sides",
    options=['BUY', 'SELL'],
    default=['BUY', 'SELL']
)

# PnL filter
pnl_filter = st.sidebar.radio(
    "PnL Filter",
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

# Main header
st.markdown('<h1 class="main-header">📊 Bitcoin Trader Performance vs Market Sentiment Dashboard</h1>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;'>
    <p style='font-size: 18px; color: #555;'>
        <b>Comprehensive Analysis of Hyperliquid Trading Performance Against Fear & Greed Index</b>
    </p>
</div>
""", unsafe_allow_html=True)

# Key Metrics Dashboard
st.markdown('<h2 class="sub-header">📈 Key Performance Metrics</h2>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

total_trades = len(filtered_df)
total_pnl = filtered_df['Net_PnL'].sum()
win_rate = (filtered_df['is_profitable'].sum() / total_trades * 100) if total_trades > 0 else 0
avg_pnl = filtered_df['Net_PnL'].mean()
total_volume = filtered_df['Size USD'].sum()

with col1:
    st.metric("Total Trades", f"{total_trades:,}")
with col2:
    st.metric("Total Net PnL", f"${total_pnl:,.2f}", delta=f"{total_pnl:,.2f}")
with col3:
    st.metric("Win Rate", f"{win_rate:.2f}%")
with col4:
    st.metric("Avg PnL/Trade", f"${avg_pnl:.2f}")
with col5:
    st.metric("Total Volume", f"${total_volume/1e6:.2f}M")

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", 
    "💰 PnL Analysis", 
    "📈 Time Series", 
    "🎯 Risk Metrics",
    "🔍 Deep Dive",
    "💡 Insights"
])

# TAB 1: Overview
with tab1:
    st.markdown('<h2 class="sub-header">Market Sentiment Distribution</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution pie chart
        sentiment_dist = filtered_df['sentiment_category'].value_counts().reindex(sentiment_order, fill_value=0)
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_dist.index,
            values=sentiment_dist.values,
            hole=0.4,
            marker=dict(colors=['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c'])
        )])
        fig.update_layout(
            title="Market Sentiment Distribution in Trading Period",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # PnL contribution by sentiment
        pnl_contribution = filtered_df.groupby('sentiment_category')['Net_PnL'].sum().reindex(sentiment_order, fill_value=0)
        
        fig = go.Figure(data=[go.Bar(
            x=pnl_contribution.index,
            y=pnl_contribution.values,
            marker=dict(color=['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c'])
        )])
        fig.update_layout(
            title="Total PnL by Market Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Total Net PnL ($)",
            height=400
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance table by sentiment
    st.markdown('<h2 class="sub-header">Performance Breakdown by Sentiment</h2>', unsafe_allow_html=True)
    
    sentiment_performance = filtered_df.groupby('sentiment_category').agg({
        'Net_PnL': ['sum', 'mean', 'std'],
        'Size USD': ['sum', 'mean'],
        'Fee': 'sum',
        'is_profitable': 'mean',
        'Account': 'count'
    }).round(2)
    
    sentiment_performance.columns = ['Total_PnL', 'Avg_PnL', 'Std_PnL', 'Total_Volume', 'Avg_Trade_Size', 'Total_Fees', 'Win_Rate', 'Trade_Count']
    sentiment_performance['Win_Rate'] = sentiment_performance['Win_Rate'] * 100
    sentiment_performance = sentiment_performance.reindex(sentiment_order, fill_value=0)
    
    st.dataframe(sentiment_performance.style.format({
        'Total_PnL': '${:,.2f}',
        'Avg_PnL': '${:,.2f}',
        'Std_PnL': '${:,.2f}',
        'Total_Volume': '${:,.2f}',
        'Avg_Trade_Size': '${:,.2f}',
        'Total_Fees': '${:,.2f}',
        'Win_Rate': '{:.2f}%',
        'Trade_Count': '{:,.0f}'
    }).background_gradient(cmap='RdYlGn', subset=['Total_PnL', 'Win_Rate']), use_container_width=True)

# TAB 2: PnL Analysis
with tab2:
    st.markdown('<h2 class="sub-header">Profitability Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Win rate by sentiment
        win_rate_by_sentiment = (filtered_df.groupby('sentiment_category')['is_profitable'].mean() * 100).reindex(sentiment_order, fill_value=0)
        
        fig = go.Figure(data=[go.Bar(
            x=win_rate_by_sentiment.index,
            y=win_rate_by_sentiment.values,
            marker=dict(color=['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c']),
            text=win_rate_by_sentiment.values.round(1),
            texttemplate='%{text}%',
            textposition='outside'
        )])
        fig.update_layout(
            title="Win Rate by Market Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Win Rate (%)",
            height=400
        )
        fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="50% Baseline")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average PnL by sentiment
        avg_pnl_by_sentiment = filtered_df.groupby('sentiment_category')['Net_PnL'].mean().reindex(sentiment_order, fill_value=0)
        
        fig = go.Figure(data=[go.Bar(
            x=avg_pnl_by_sentiment.index,
            y=avg_pnl_by_sentiment.values,
            marker=dict(color=['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c']),
            text=avg_pnl_by_sentiment.values.round(2),
            texttemplate='$%{text}',
            textposition='outside'
        )])
        fig.update_layout(
            title="Average Net PnL by Market Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Average Net PnL ($)",
            height=400
        )
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig, use_container_width=True)
    
    # PnL distribution box plot
    st.markdown('<h2 class="sub-header">PnL Distribution Analysis</h2>', unsafe_allow_html=True)
    
    # Filter extreme outliers for better visualization
    pnl_filtered = filtered_df[filtered_df['Net_PnL'].between(
        filtered_df['Net_PnL'].quantile(0.01), 
        filtered_df['Net_PnL'].quantile(0.99)
    )]
    
    fig = go.Figure()
    
    colors_map = {
        'Extreme Fear': '#d32f2f',
        'Fear': '#f57c00',
        'Neutral': '#fbc02d',
        'Greed': '#689f38',
        'Extreme Greed': '#388e3c'
    }
    
    for sentiment in sentiment_order:
        if sentiment in pnl_filtered['sentiment_category'].values:
            sentiment_data = pnl_filtered[pnl_filtered['sentiment_category'] == sentiment]['Net_PnL']
            fig.add_trace(go.Box(
                y=sentiment_data,
                name=sentiment,
                marker_color=colors_map[sentiment]
            ))
    
    fig.update_layout(
        title="Distribution of Net PnL by Market Sentiment (1st-99th Percentile)",
        yaxis_title="Net PnL ($)",
        height=500,
        showlegend=False
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: Time Series
with tab3:
    st.markdown('<h2 class="sub-header">Time Series Analysis</h2>', unsafe_allow_html=True)
    
    # Daily performance with sentiment
    daily_performance = filtered_df.groupby('Date').agg({
        'Net_PnL': 'sum',
        'value': 'first',
        'classification': 'first'
    }).reset_index()
    
    daily_performance['Cumulative_PnL'] = daily_performance['Net_PnL'].cumsum()
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add cumulative PnL
    fig.add_trace(
        go.Scatter(
            x=daily_performance['Date'],
            y=daily_performance['Cumulative_PnL'],
            name="Cumulative PnL",
            line=dict(color='#1976d2', width=3)
        ),
        secondary_y=False
    )
    
    # Add sentiment index
    fig.add_trace(
        go.Scatter(
            x=daily_performance['Date'],
            y=daily_performance['value'],
            name="Fear & Greed Index",
            line=dict(color='#f57c00', width=2, dash='dot')
        ),
        secondary_y=True
    )
    
    # Add sentiment zones
    fig.add_hrect(y0=0, y1=25, fillcolor="red", opacity=0.1, layer="below", line_width=0, secondary_y=True)
    fig.add_hrect(y0=25, y1=45, fillcolor="orange", opacity=0.1, layer="below", line_width=0, secondary_y=True)
    fig.add_hrect(y0=45, y1=55, fillcolor="yellow", opacity=0.1, layer="below", line_width=0, secondary_y=True)
    fig.add_hrect(y0=55, y1=75, fillcolor="lightgreen", opacity=0.1, layer="below", line_width=0, secondary_y=True)
    fig.add_hrect(y0=75, y1=100, fillcolor="green", opacity=0.1, layer="below", line_width=0, secondary_y=True)
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Cumulative Net PnL ($)", secondary_y=False)
    fig.update_yaxes(title_text="Fear & Greed Index Value", secondary_y=True, range=[0, 100])
    
    fig.update_layout(
        title="Cumulative PnL vs Market Sentiment Over Time",
        height=600,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Rolling statistics
    st.markdown('<h2 class="sub-header">Rolling Performance Metrics</h2>', unsafe_allow_html=True)
    
    window = st.slider("Select Rolling Window (days)", 1, 30, 7)
    
    daily_performance[f'{window}D_Avg_PnL'] = daily_performance['Net_PnL'].rolling(window=window).mean()
    daily_performance[f'{window}D_Std_PnL'] = daily_performance['Net_PnL'].rolling(window=window).std()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_performance['Date'],
        y=daily_performance['Net_PnL'],
        name="Daily PnL",
        line=dict(color='lightgray', width=1),
        opacity=0.5
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_performance['Date'],
        y=daily_performance[f'{window}D_Avg_PnL'],
        name=f"{window}-Day Moving Average",
        line=dict(color='#1976d2', width=3)
    ))
    
    fig.update_layout(
        title=f"Daily PnL with {window}-Day Moving Average",
        xaxis_title="Date",
        yaxis_title="Net PnL ($)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: Risk Metrics
with tab4:
    st.markdown('<h2 class="sub-header">Risk-Adjusted Performance</h2>', unsafe_allow_html=True)
    
    # Calculate risk metrics
    risk_metrics = filtered_df.groupby('sentiment_category').agg({
        'Net_PnL': ['mean', 'std', 'min', 'max'],
        'Size USD': ['mean', 'std']
    }).round(2)
    
    risk_metrics.columns = ['Avg_PnL', 'PnL_StdDev', 'Max_Loss', 'Max_Profit', 'Avg_Trade_Size', 'Trade_Size_StdDev']
    risk_metrics['Sharpe_Ratio'] = (risk_metrics['Avg_PnL'] / risk_metrics['PnL_StdDev']).round(3)
    risk_metrics = risk_metrics.reindex(sentiment_order, fill_value=0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk-reward ratio
        fig = go.Figure(data=[go.Bar(
            x=risk_metrics.index,
            y=risk_metrics['Sharpe_Ratio'],
            marker=dict(color=['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c']),
            text=risk_metrics['Sharpe_Ratio'].round(3),
            texttemplate='%{text}',
            textposition='outside'
        )])
        fig.update_layout(
            title="Sharpe Ratio by Market Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Sharpe Ratio (Mean/StdDev)",
            height=400
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Volatility
        fig = go.Figure(data=[go.Bar(
            x=risk_metrics.index,
            y=risk_metrics['PnL_StdDev'],
            marker=dict(color=['#d32f2f', '#f57c00', '#fbc02d', '#689f38', '#388e3c']),
            text=risk_metrics['PnL_StdDev'].round(2),
            texttemplate='$%{text}',
            textposition='outside'
        )])
        fig.update_layout(
            title="PnL Volatility by Market Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Standard Deviation of PnL ($)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk metrics table
    st.markdown('<h2 class="sub-header">Comprehensive Risk Metrics</h2>', unsafe_allow_html=True)
    
    st.dataframe(risk_metrics.style.format({
        'Avg_PnL': '${:,.2f}',
        'PnL_StdDev': '${:,.2f}',
        'Max_Loss': '${:,.2f}',
        'Max_Profit': '${:,.2f}',
        'Avg_Trade_Size': '${:,.2f}',
        'Trade_Size_StdDev': '${:,.2f}',
        'Sharpe_Ratio': '{:.3f}'
    }).background_gradient(cmap='RdYlGn', subset=['Sharpe_Ratio', 'Avg_PnL']), use_container_width=True)

# TAB 5: Deep Dive
with tab5:
    st.markdown('<h2 class="sub-header">Behavioral Pattern Analysis</h2>', unsafe_allow_html=True)
    
    # Buy vs Sell by sentiment
    col1, col2 = st.columns(2)
    
    with col1:
        side_sentiment = pd.crosstab(filtered_df['sentiment_category'], filtered_df['Side'], normalize='index') * 100
        side_sentiment = side_sentiment.reindex(sentiment_order, fill_value=0)
        
        fig = go.Figure()
        
        if 'BUY' in side_sentiment.columns:
            fig.add_trace(go.Bar(
                x=side_sentiment.index,
                y=side_sentiment['BUY'],
                name='BUY',
                marker_color='#4caf50'
            ))
        
        if 'SELL' in side_sentiment.columns:
            fig.add_trace(go.Bar(
                x=side_sentiment.index,
                y=side_sentiment['SELL'],
                name='SELL',
                marker_color='#f44336'
            ))
        
        fig.update_layout(
            title="Buy vs Sell Distribution by Sentiment",
            xaxis_title="Sentiment",
            yaxis_title="Percentage (%)",
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Trade count by hour
        hourly_trades = filtered_df.groupby('Hour').size()
        
        fig = go.Figure(data=[go.Bar(
            x=hourly_trades.index,
            y=hourly_trades.values,
            marker_color='#1976d2'
        )])
        fig.update_layout(
            title="Trading Activity by Hour of Day",
            xaxis_title="Hour (24h format)",
            yaxis_title="Number of Trades",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.markdown('<h2 class="sub-header">Feature Correlation Analysis</h2>', unsafe_allow_html=True)
    
    numeric_features = filtered_df[['value', 'Net_PnL', 'Size USD', 'Fee', 'Hour', 'DayOfWeek']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=numeric_features.values,
        x=['Sentiment Value', 'Net PnL', 'Trade Size', 'Fee', 'Hour', 'Day of Week'],
        y=['Sentiment Value', 'Net PnL', 'Trade Size', 'Fee', 'Hour', 'Day of Week'],
        colorscale='RdBu',
        zmid=0,
        text=numeric_features.values.round(3),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Correlation Heatmap: Trading Metrics vs Market Sentiment",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly performance
    st.markdown('<h2 class="sub-header">Monthly Performance Breakdown</h2>', unsafe_allow_html=True)
    
    monthly_performance = filtered_df.groupby('Month').agg({
        'Net_PnL': ['sum', 'mean', 'count'],
        'is_profitable': 'mean'
    }).round(2)
    
    monthly_performance.columns = ['Total_PnL', 'Avg_PnL', 'Trade_Count', 'Win_Rate']
    monthly_performance['Win_Rate'] = monthly_performance['Win_Rate'] * 100
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_performance.index = [month_names[i-1] for i in monthly_performance.index]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=monthly_performance.index, y=monthly_performance['Total_PnL'], name="Total PnL", marker_color='#1976d2'),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_performance.index, y=monthly_performance['Win_Rate'], name="Win Rate", 
                   line=dict(color='#f57c00', width=3), mode='lines+markers'),
        secondary_y=True
    )
    
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Total PnL ($)", secondary_y=False)
    fig.update_yaxes(title_text="Win Rate (%)", secondary_y=True)
    
    fig.update_layout(title="Monthly Performance: PnL and Win Rate", height=400)
    st.plotly_chart(fig, use_container_width=True)

# TAB 6: Insights
with tab6:
    st.markdown('<h2 class="sub-header">💡 Key Insights & Recommendations</h2>', unsafe_allow_html=True)
    
    # Calculate insights
    if len(sentiment_performance) > 0:
        best_sentiment = sentiment_performance['Total_PnL'].idxmax()
        best_pnl = sentiment_performance.loc[best_sentiment, 'Total_PnL']
        worst_sentiment = sentiment_performance['Total_PnL'].idxmin()
        worst_pnl = sentiment_performance.loc[worst_sentiment, 'Total_PnL']
        
        # Insight 1
        st.markdown(f"""
        <div class="insight-box">
            <h3>🎯 Best Performing Sentiment: {best_sentiment}</h3>
            <p><b>Total PnL:</b> ${best_pnl:,.2f}</p>
            <p><b>Average PnL per trade:</b> ${sentiment_performance.loc[best_sentiment, 'Avg_PnL']:.2f}</p>
            <p><b>Win Rate:</b> {sentiment_performance.loc[best_sentiment, 'Win_Rate']:.2f}%</p>
            <p><b>Recommendation:</b> Increase trading activity during {best_sentiment} periods for optimal returns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Insight 2
        st.markdown(f"""
        <div class="insight-box">
            <h3>⚠️ Worst Performing Sentiment: {worst_sentiment}</h3>
            <p><b>Total PnL:</b> ${worst_pnl:,.2f}</p>
            <p><b>Average PnL per trade:</b> ${sentiment_performance.loc[worst_sentiment, 'Avg_PnL']:.2f}</p>
            <p><b>Win Rate:</b> {sentiment_performance.loc[worst_sentiment, 'Win_Rate']:.2f}%</p>
            <p><b>Recommendation:</b> Reduce position sizes or avoid trading during {worst_sentiment} periods.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk-reward insight
    if len(risk_metrics) > 0 and 'Sharpe_Ratio' in risk_metrics.columns:
        best_risk_reward = risk_metrics['Sharpe_Ratio'].idxmax()
        
        st.markdown(f"""
        <div class="insight-box">
            <h3>📊 Best Risk-Adjusted Returns: {best_risk_reward}</h3>
            <p><b>Sharpe Ratio:</b> {risk_metrics.loc[best_risk_reward, 'Sharpe_Ratio']:.3f}</p>
            <p><b>Volatility:</b> ${risk_metrics.loc[best_risk_reward, 'PnL_StdDev']:.2f}</p>
            <p><b>Recommendation:</b> Focus on {best_risk_reward} periods for most consistent risk-adjusted returns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Correlation insight
    sentiment_pnl_corr = filtered_df['value'].corr(filtered_df['Net_PnL'])
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>🔗 Sentiment-Performance Correlation</h3>
        <p><b>Correlation Coefficient:</b> {sentiment_pnl_corr:.4f}</p>
        <p><b>Interpretation:</b> {'Positive' if sentiment_pnl_corr > 0 else 'Negative'} correlation - 
        {'Higher sentiment (Greed) tends to correlate with better performance' if sentiment_pnl_corr > 0 else 'Lower sentiment (Fear) tends to correlate with better performance'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trading volume insight
    overall_buy_pct = (filtered_df['Side'] == 'BUY').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>📈 Trading Bias Analysis</h3>
        <p><b>Buy Orders:</b> {overall_buy_pct:.1f}%</p>
        <p><b>Sell Orders:</b> {100-overall_buy_pct:.1f}%</p>
        <p><b>Observation:</b> {'Portfolio is heavily skewed toward BUY trades' if overall_buy_pct > 60 else 'Portfolio is heavily skewed toward SELL trades' if overall_buy_pct < 40 else 'Balanced buy/sell distribution'}</p>
        {f'<p><b>Recommendation:</b> Consider more short-selling opportunities to balance portfolio.</p>' if overall_buy_pct > 60 else f'<p><b>Recommendation:</b> Consider more long positions during bullish sentiments.</p>' if overall_buy_pct < 40 else '<p><b>Recommendation:</b> Maintain current balanced approach.</p>'}
    </div>
    """, unsafe_allow_html=True)
    
    # Fee impact
    total_fees = filtered_df['Fee'].sum()
    gross_pnl = filtered_df['Closed PnL'].sum()
    fee_impact = (total_fees / abs(gross_pnl)) * 100 if gross_pnl != 0 else 0
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>💸 Fee Impact Analysis</h3>
        <p><b>Total Fees:</b> ${total_fees:,.2f}</p>
        <p><b>Fee as % of Gross PnL:</b> {fee_impact:.2f}%</p>
        <p><b>Recommendation:</b> {'Fees are significant - consider reducing trade frequency or using maker orders' if fee_impact > 10 else 'Fee impact is reasonable for current trading strategy'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic recommendations
    st.markdown('<h2 class="sub-header">🎯 Strategic Recommendations</h2>', unsafe_allow_html=True)
    
    recommendations = [
        f"**Sentiment-Based Strategy:** Maximize trading during {best_sentiment} periods where profitability is highest",
        f"**Risk Management:** Implement stricter stop-losses during {worst_sentiment} to minimize losses",
        f"**Position Sizing:** Use larger positions during {best_risk_reward if 'best_risk_reward' in locals() else 'favorable'} periods for better risk-adjusted returns",
        "**Diversification:** Consider balanced exposure across different sentiment periods to reduce volatility",
        "**Fee Optimization:** Monitor trading frequency and consider maker orders to reduce transaction costs",
        "**Time-Based Strategy:** Analyze hourly patterns to identify optimal trading windows",
        "**Stop-Loss Implementation:** Set dynamic stop-losses based on sentiment-specific volatility levels"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p><b>Bitcoin Trader Performance vs Market Sentiment Dashboard</b></p>
    <p>Data Analysis Tool for Hyperliquid Trading Performance</p>
    <p>Built with Streamlit • Powered by Plotly</p>
</div>
""", unsafe_allow_html=True)
