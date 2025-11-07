# =============================================================================
# CONTINUATION OF streamlit_app_enhanced.py
# Add this code to the end of streamlit_app_enhanced.py
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            use_container_width=True
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
        st.plotly_chart(fig, use_container_width=True)
    
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
        
        st.plotly_chart(fig, use_container_width=True)
        
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
        
        st.plotly_chart(fig, use_container_width=True)
    
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
        st.plotly_chart(fig, use_container_width=True)

# Continue to next page...
