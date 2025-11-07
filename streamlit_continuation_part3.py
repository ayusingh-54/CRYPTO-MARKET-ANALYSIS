# =============================================================================
# PART 3: POSITION SIZING, TIME ANALYSIS & DEEP DIVE PAGE
# Add these sections to complete the Risk Analysis page
# =============================================================================

# TAB 2: Position Sizing (add this to Risk Analysis page)
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            use_container_width=True
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
    
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
        st.plotly_chart(fig, use_container_width=True)
        
        # Session stats table
        st.dataframe(
            session_perf.style.format({
                'Total_PnL': '${:,.2f}',
                'Avg_PnL': '${:,.2f}',
                'Trade_Count': '{:,.0f}',
                'Win_Rate': '{:.1f}%'
            }).background_gradient(cmap='RdYlGn', subset=['Total_PnL', 'Avg_PnL', 'Win_Rate']),
            use_container_width=True
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
            sort_by = st.selectbox("Sort By", ["Net_PnL", "Size USD", "Fee USD", "PnL_Percentage"])
        
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
                       'Realized Profit', 'Fee USD', 'Net_PnL', 'PnL_Percentage', 'Trading_Session']
        
        top_10 = explore_df.head(10)[display_cols].reset_index(drop=True)
        
        st.dataframe(
            top_10.style.format({
                'Size USD': '${:,.2f}',
                'Realized Profit': '${:,.2f}',
                'Fee USD': '${:,.2f}',
                'Net_PnL': '${:,.2f}',
                'PnL_Percentage': '{:.2f}%'
            }).background_gradient(cmap='RdYlGn', subset=['Net_PnL', 'PnL_Percentage']),
            use_container_width=True,
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
            st.metric("Total Fees", f"${explore_df['Fee USD'].sum():,.2f}")
    
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
        # Side comparison table
        st.markdown("---")
        st.markdown("### 📊 Detailed Side Comparison")
        
        side_comparison = filtered_df.groupby('Side').agg({
            'Net_PnL': ['sum', 'mean', 'std'],
            'Size USD': 'mean',
            'Fee USD': 'sum',
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
            use_container_width=True
        )
    
    # TAB 3: Fee Analysis
    with tabs[2]:
        st.markdown('<h3 class="sub-header">Trading Fee Impact</h3>', unsafe_allow_html=True)
        
        total_fees = filtered_df['Fee USD'].sum()
        total_gross_profit = filtered_df['Realized Profit'].sum()
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
            fee_by_sentiment = filtered_df.groupby('sentiment_category')['Fee USD'].sum().reindex(sentiment_order, fill_value=0)
            
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
        st.plotly_chart(fig, use_container_width=True)
        
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
            use_container_width=True
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
