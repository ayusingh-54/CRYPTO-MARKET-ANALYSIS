# 🎯 Bitcoin Trader Performance vs Market Sentiment Analysis

**Complete Enhanced Project with Advanced Streamlit Dashboard**

---

## 👨‍💻 Author Information

**Name:** Ayush Singh  
**Email:** Ayusingh693@gmail.com  
**Phone:** +91 7031678999

---

## 📋 Project Overview

This comprehensive data analysis project explores the relationship between Bitcoin trader performance and market sentiment (Fear & Greed Index). It includes:

- ✅ **Enhanced Jupyter Notebook** with 15+ analysis sections
- ✅ **Advanced Multi-Page Streamlit Dashboard** with 5 interactive pages
- ✅ **Statistical Testing** (ANOVA, Chi-square, Mann-Whitney, Kruskal-Wallis)
- ✅ **Risk Analysis** (Volatility, Drawdown, Sharpe Ratio, Streaks)
- ✅ **40+ Visualizations** (Static in notebook, Interactive in dashboard)
- ✅ **14 Engineered Features** for deep behavioral analysis

---

## 📁 Project Structure

```
New folder/
│
├── 📓 Jupyter Notebook
│   └── trader_sentiment_analysis.ipynb          # Enhanced notebook with all analysis
│
├── 📊 Data Files
│   ├── historical_data.csv                      # Trading data
│   └── fear_greed_index.csv                     # Sentiment data
│
├── 🌐 Streamlit Application Files
│   ├── streamlit_app_enhanced.py                # Base file with Assignment Details page
│   ├── streamlit_continuation_part1.py          # Dashboard page
│   ├── streamlit_continuation_part2.py          # Advanced Analytics & Risk Analysis (partial)
│   ├── streamlit_continuation_part3.py          # Risk Analysis (completion) & Deep Dive
│   ├── streamlit_complete_integrated.py         # Alternative integrated version
│   └── merge_streamlit_files.py                 # Auto-merge script (Python)
│
└── 📄 Documentation
    ├── ENHANCEMENT_SUMMARY.md                   # Complete notebook enhancement documentation
    ├── PROJECT_README.md                        # This file
    └── INTEGRATION_GUIDE.md                     # Streamlit integration instructions
```

---

## 🚀 Quick Start Guide

### Option 1: Run Jupyter Notebook (Recommended First)

1. **Open the enhanced notebook:**

   ```bash
   jupyter notebook trader_sentiment_analysis.ipynb
   ```

2. **Run all cells** to see the complete analysis

3. **Review all 15 sections:**
   - Data loading & exploration
   - Feature engineering (14 features)
   - Statistical significance testing
   - Volatility analysis
   - Drawdown analysis
   - Position sizing analysis
   - Win/loss streak analysis
   - Performance metrics dashboard
   - Comprehensive insights

### Option 2: Run Streamlit Dashboard (Auto-Merge Method)

1. **Merge all Streamlit files automatically:**

   ```powershell
   python merge_streamlit_files.py
   ```

2. **Run the merged application:**

   ```powershell
   streamlit run streamlit_app_final.py
   ```

3. **Navigate through 5 pages:**
   - 🏠 Dashboard (Overview & KPIs)
   - 📊 Advanced Analytics (Statistical tests, volatility, drawdown, streaks)
   - 📈 Risk Analysis (Risk-reward, position sizing, time patterns)
   - 🔍 Deep Dive (Trade explorer, sides analysis, fees, advanced metrics)
   - 📋 Assignment Details (Complete project explanation)

### Option 3: Manual Integration (If Auto-Merge Fails)

1. **Copy code sections manually:**

   - Open `streamlit_app_enhanced.py`
   - Find the comment: `# NOTE: INSERT CONTINUATION PARTS HERE`
   - Copy content from part1, part2, part3 files in order
   - Paste into the marked location

2. **Run the application:**
   ```powershell
   streamlit run streamlit_app_enhanced.py
   ```

---

## 📊 Dashboard Features

### Page 1: 🏠 Dashboard

- **KPI Metrics:** Total Trades, Net PnL, Win Rate, Avg PnL, Volume
- **Tab 1 - Overview:** Sentiment distribution, PnL by sentiment, performance table
- **Tab 2 - Profitability:** Win rates, average PnL, distribution box plots
- **Tab 3 - Time Series:** Cumulative PnL, sentiment zones, rolling statistics
- **Tab 4 - Sentiment Analysis:** Trade counts, position sizes, correlation heatmap

### Page 2: 📊 Advanced Analytics

- **Tab 1 - Statistical Tests:**
  - One-Way ANOVA (F-statistic, p-value)
  - Kruskal-Wallis Test (non-parametric)
  - Chi-Square Test (profitability vs sentiment)
  - Mann-Whitney U Test (pairwise comparisons)
- **Tab 2 - Volatility Analysis:**
  - PnL volatility by sentiment
  - Coefficient of variation
  - Most/least volatile sentiments
  - Most efficient risk-return
- **Tab 3 - Drawdown Analysis:**
  - Cumulative PnL with running max
  - Drawdown percentage over time
  - Maximum drawdown metrics
  - Recovery time calculation
- **Tab 4 - Win/Loss Streaks:**
  - Streak length distribution
  - Win vs loss streak comparison
  - Streak metrics by sentiment
  - Momentum indicators

### Page 3: 📈 Risk Analysis

- **Tab 1 - Risk-Reward:**
  - Sharpe ratio by sentiment
  - Risk-return scatter plot
  - Complete risk metrics table
- **Tab 2 - Position Sizing:**
  - Position size distribution
  - Size vs PnL correlation
  - Size statistics by sentiment
  - Average position by outcome
  - Weekly size trends
- **Tab 3 - Time Analysis:**
  - Hourly PnL patterns
  - Day of week performance
  - Trading session analysis
  - Session vs sentiment heatmap
- **Tab 4 - Key Insights:**
  - Best/worst risk-adjusted performers
  - Most consistent sentiment
  - Actionable recommendations

### Page 4: 🔍 Deep Dive

- **Tab 1 - Trade Explorer:**
  - Advanced filtering (PnL threshold, side, sorting)
  - Top 10 trades table
  - CSV export functionality
  - Summary statistics
- **Tab 2 - Trade Sides:**
  - BUY vs SELL performance
  - Win rate comparison
  - Detailed side metrics
- **Tab 3 - Fee Analysis:**
  - Total fees and impact
  - Fees by sentiment
  - Fee ratio analysis
  - High vs low fee trade comparison
- **Tab 4 - Advanced Metrics:**
  - Performance radar chart
  - Complete metrics table
  - Final performance summary

### Page 5: 📋 Assignment Details

- **Author Information:** Name, email, phone with professional card design
- **Assignment Overview:** Comprehensive project description
- **Key Objectives:** 6 main goals clearly listed
- **Research Questions:** 5 detailed questions guiding the analysis
- **Dataset Summary:** Key metrics and statistics
- **Methodology:** Data collection, processing, analysis methods
- **Technical Stack:** Complete list of tools and libraries
- **Key Features:** 8 major features implemented
- **Key Findings:** Preview of main discoveries
- **Deliverables:** Complete checklist
- **References:** Data sources, tools, academic papers

---

## 🔧 Technical Requirements

### Required Python Packages:

```bash
pip install streamlit==1.28.0
pip install pandas==2.0.0
pip install numpy==1.24.0
pip install plotly==5.17.0
pip install scipy==1.10.0
pip install scikit-learn==1.3.0
pip install matplotlib==3.7.0
pip install seaborn==0.12.0
pip install jupyter
```

Or install all at once:

```bash
pip install streamlit pandas numpy plotly scipy scikit-learn matplotlib seaborn jupyter
```

### System Requirements:

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Edge, Safari)

---

## 📈 Notebook Enhancements

### New Sections Added:

1. **Section 7.9:** Statistical Significance Testing
   - ANOVA, Chi-square, Mann-Whitney U, Kruskal-Wallis tests
2. **Section 7.10:** Volatility Analysis
   - 4-panel visualization (rolling volatility, distribution, CV, sessions)
3. **Section 7.11:** Drawdown Analysis
   - Max drawdown, recovery periods, sentiment-colored viz
4. **Section 8.4:** Position Size Analysis
   - 4-panel behavioral analysis (box plots, size vs PnL, trends)
5. **Section 8.5:** Win/Loss Streak Analysis
   - Consecutive trade patterns, momentum indicators
6. **Section 9.1:** Performance Metrics Dashboard
   - 7-panel comprehensive view (radar, cumulative, heatmap, etc.)

### Enhanced Features:

- **8 New Engineered Features:** PnL_Percentage, Fee_Ratio, sentiment_score, Trading_Session, Win_Loss_Magnitude, Month, Week, temporal features
- **Upgraded Imports:** Added scipy.stats, sklearn.preprocessing, version tracking
- **Better Error Handling:** Try-except blocks, memory usage reporting
- **Enhanced Insights:** 10 categories with tree structure, action items

---

## 🎨 Dashboard Design Features

### Professional Styling:

- **Gradient Headers:** Beautiful blue gradient headers for main sections
- **Custom Card Styles:** 8 different box styles (insight-box, warning-box, success-box, author-card, etc.)
- **Color Schemes:**
  - Sentiment colors: Red (Extreme Fear) → Green (Extreme Greed)
  - PnL colors: Red (negative) → Green (positive)
  - Risk colors: Blue gradients for metrics

### Interactive Elements:

- **Real-Time Filtering:** Date range, sentiment, trade sides, PnL status
- **Filter Summary:** Live count of filtered trades
- **Hover Information:** Detailed tooltips on all charts
- **Downloadable Reports:** CSV export for filtered data
- **Responsive Layout:** Adapts to different screen sizes

### User Experience:

- **Clear Navigation:** Sidebar radio with emoji icons
- **Tab Organization:** Multi-tab layouts for related content
- **Metric Cards:** Large, colorful KPI displays
- **Data Tables:** Formatted with gradient backgrounds
- **Loading States:** Caching for instant re-loads

---

## 🐛 Troubleshooting

### Issue: Files not found error

**Solution:** Ensure `historical_data.csv` and `fear_greed_index.csv` are in the same directory as the Streamlit app.

### Issue: ModuleNotFoundError

**Solution:** Install missing packages:

```bash
pip install <missing-package-name>
```

### Issue: Streamlit won't start

**Solution:**

1. Check Python version: `python --version` (must be 3.8+)
2. Try: `python -m streamlit run streamlit_app_final.py`
3. Clear cache: Delete `.streamlit` folder in project directory

### Issue: Auto-merge script fails

**Solution:** Use manual integration (Option 3 in Quick Start)

### Issue: Charts not displaying

**Solution:**

1. Clear browser cache
2. Try different browser
3. Check console for JavaScript errors (F12)

### Issue: Filters not working

**Solution:**

1. Ensure date range has both start and end dates
2. Check that at least one sentiment is selected
3. Reload the page (R or Ctrl+R)

---

## 📞 Support & Contact

### For Questions or Issues:

**Ayush Singh**

- 📧 Email: Ayusingh693@gmail.com
- 📱 Phone: +91 7031678999

### Project Information:

- **Created:** 2024
- **Version:** 2.0 (Enhanced)
- **Status:** Complete & Production-Ready
- **License:** Educational Project

---

## 🙏 Acknowledgments

This project uses:

- **Streamlit** for the web framework
- **Plotly** for interactive visualizations
- **Pandas** for data manipulation
- **Scipy** for statistical testing
- **Scikit-learn** for preprocessing

Special thanks to the open-source community for these amazing tools!

---

**🎉 Thank you for reviewing this project!**

_Built with ❤️ by Ayush Singh | Last Updated: 2024_
