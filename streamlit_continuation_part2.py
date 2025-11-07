# =============================================================================
# PART 2: ADVANCED ANALYTICS & RISK ANALYSIS PAGES
# Add this after the Dashboard page
# =============================================================================

# =============================================================================
# PAGE 3: ADVANCED ANALYTICS
# =============================================================================

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
            
            st.dataframe(contingency_table, use_container_width=True)
            
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
        st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
        st.plotly_chart(fig, use_container_width=True)

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
            st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig, use_container_width=True)
        
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
            use_container_width=True
        )
    
    # Continue with remaining tabs...
    # (Position Sizing, Time Analysis, Key Insights)
    # Due to length, these can be added separately

# Footer for all pages
if page != "📋 Assignment Details":
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p><b>Bitcoin Trader Performance vs Market Sentiment Dashboard</b></p>
        <p>Created by Ayush Singh | Ayusingh693@gmail.com | +91 7031678999</p>
        <p>Built with Streamlit • Powered by Plotly • Analyzed with Pandas</p>
    </div>
    """, unsafe_allow_html=True)
