# 🚀 Bitcoin Trader Performance vs Market Sentiment Analysis# Bitcoin Trader Performance vs Market Sentiment Analysis

<div align="center">## 📊 Project Overview

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://crypto-market-analysis.streamlit.app)This project provides a comprehensive analysis of the relationship between Bitcoin trader performance on Hyperliquid and market sentiment (Fear & Greed Index). It includes both a detailed Jupyter Notebook for exploratory analysis and an advanced, interactive Streamlit dashboard.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)## 📁 Project Structure

_An advanced analytics platform for understanding the relationship between cryptocurrency trading performance and market sentiment_```

.

[Live Demo](https://crypto-market-analysis.streamlit.app) • [Report Bug](../../issues) • [Request Feature](../../issues)├── fear_greed_index.csv # Bitcoin Fear & Greed Index data

├── historical_data.csv # Hyperliquid trading data

</div>├── trader_sentiment_analysis.ipynb    # Comprehensive Jupyter Notebook analysis

├── streamlit_app.py # Interactive Streamlit dashboard

---├── requirements.txt # Python dependencies

└── README.md # This file

## 📋 Table of Contents```

- [Overview](#-overview)## 🚀 Quick Start

- [Key Features](#-key-features)

- [Live Demo](#-live-demo)### Prerequisites

- [Installation](#-installation)

- [Usage](#-usage)- Python 3.8 or higher

- [Project Structure](#-project-structure)- pip package manager

- [Data Sources](#-data-sources)

- [Analysis Methodology](#-analysis-methodology)### Installation

- [Dashboard Features](#-dashboard-features)

- [Technologies Used](#️-technologies-used)1. **Install required packages:**

- [Results & Insights](#-results--insights)

- [Troubleshooting](#-troubleshooting)```powershell

- [Contributing](#-contributing)pip install -r requirements.txt

- [Author](#-author)```

- [License](#-license)

Or install packages individually:

---

```powershell

## 🎯 Overviewpip install pandas numpy matplotlib seaborn streamlit plotly jupyter notebook ipykernel

```

This project provides a **comprehensive analytical framework** for examining the relationship between Bitcoin trader performance on the Hyperliquid DEX and market sentiment as measured by the Fear & Greed Index. The platform combines rigorous statistical analysis with interactive visualizations to uncover actionable trading insights.

## 📓 Running the Jupyter Notebook

### 🎓 Project Context

### Option 1: Using Jupyter Notebook

**Author:** Ayush Singh

**Email:** Ayusingh693@gmail.com ```powershell

**Phone:** +91 7031678999 jupyter notebook trader_sentiment_analysis.ipynb

**Purpose:** Advanced Data Analysis Assignment ```

**Domain:** Cryptocurrency Trading Analytics

### Option 2: Using Jupyter Lab

### 🔍 Research Questions

````powershell

1. How does market sentiment (Fear & Greed) correlate with trading profitability?jupyter lab trader_sentiment_analysis.ipynb

2. Do traders exhibit different behavioral patterns during extreme market conditions?```

3. What are the optimal sentiment conditions for maximizing risk-adjusted returns?

4. How do trading fees impact profitability across different sentiment regimes?### Option 3: Using VS Code



---1. Open `trader_sentiment_analysis.ipynb` in VS Code

2. Select Python kernel

## ✨ Key Features3. Run all cells or run cells individually



### 📊 **Comprehensive Analysis Suite**## 🌐 Running the Streamlit Dashboard



- ✅ **15 Analysis Sections** covering all aspects of sentiment-based trading```powershell

- ✅ **40+ Interactive Visualizations** using Plotly and Matplotlibstreamlit run streamlit_app.py

- ✅ **Statistical Testing** including ANOVA, Chi-Square, Mann-Whitney U, Kruskal-Wallis```

- ✅ **Risk Metrics** including Sharpe Ratio, Volatility, Drawdown Analysis

- ✅ **Time Series Analysis** with rolling statistics and trend detectionThe dashboard will automatically open in your default web browser at `http://localhost:8501`



### 🎨 **Interactive Streamlit Dashboard**## 📊 Features



- 🎯 **5 Specialized Pages** for different analytical perspectives### Jupyter Notebook Analysis

- 🔄 **Real-time Filtering** by date, sentiment, trade side, and profitability

- 📈 **Dynamic Visualizations** that update based on user selectionsThe notebook provides:

- 💾 **Data Export** capabilities for filtered datasets

- 📱 **Responsive Design** optimized for desktop and tablet viewing✅ **Data Loading & Cleaning**



### 🧠 **Advanced Analytics**- Automated data preprocessing

- Date/time formatting

- 🤖 Machine Learning feature engineering- Missing data handling

- 📊 Multi-dimensional correlation analysis

- ⏰ Temporal pattern detection (hourly, daily, monthly)✅ **Exploratory Data Analysis**

- 💰 Fee impact and optimization analysis

- 🎲 Monte Carlo simulations for risk assessment- Overall performance metrics

- Sentiment distribution analysis

---- Trade side patterns



## 🌐 Live Demo✅ **Advanced Visualizations**



**🔗 [Access the Live Dashboard](https://crypto-market-analysis.streamlit.app)**- PnL by sentiment (bar charts)

- Win rate analysis

The interactive dashboard is deployed on Streamlit Cloud and provides:- Cumulative PnL time series

- Real-time data filtering and visualization- Sentiment vs performance correlation heatmaps

- Complete assignment explanation with author details- Risk-adjusted return metrics

- Export functionality for custom reports- Distribution box plots

- Mobile-responsive interface

✅ **Behavioral Pattern Analysis**

---

- Trading activity by hour

## 🛠️ Installation- Monthly performance breakdown

- Buy vs Sell patterns by sentiment

### Prerequisites- Risk metrics calculation



- Python 3.8 or higher✅ **Key Insights & Recommendations**

- pip package manager

- Git (for cloning the repository)- Best/worst performing sentiments

- Risk-reward optimization

### Quick Start- Strategic trading recommendations

- Fee impact analysis

```bash

# Clone the repository### Streamlit Dashboard Features

git clone https://github.com/ayusingh-54/CRYPTO-MARKET-ANALYSIS.git

cd CRYPTO-MARKET-ANALYSISThe interactive dashboard includes:



# Install dependencies🎯 **Interactive Filters**

pip install -r requirements.txt

- Date range selection

# Run the Streamlit dashboard- Sentiment category filtering

streamlit run streamlit_app_final.py- Trade side filtering (BUY/SELL)

```- PnL filtering (All/Profitable/Unprofitable)



### Alternative: Using Virtual Environment📊 **Multiple Analysis Tabs**



```bash1. **Overview Tab:**

# Create virtual environment

python -m venv venv   - Sentiment distribution pie charts

   - PnL contribution by sentiment

# Activate virtual environment   - Comprehensive performance tables

# Windows:

venv\Scripts\activate2. **PnL Analysis Tab:**

# macOS/Linux:

source venv/bin/activate   - Win rate comparisons

   - Average PnL metrics

# Install dependencies   - Distribution box plots

pip install -r requirements.txt

3. **Time Series Tab:**

# Run the application

streamlit run streamlit_app_final.py   - Cumulative PnL vs sentiment index

```   - Rolling performance metrics

   - Customizable moving averages

---

4. **Risk Metrics Tab:**

## 📖 Usage

   - Sharpe ratio analysis

### 1️⃣ **Jupyter Notebook Analysis**   - Volatility metrics

   - Risk-adjusted returns

For in-depth statistical analysis and detailed insights:

5. **Deep Dive Tab:**

```bash

# Launch Jupyter Notebook   - Behavioral pattern analysis

jupyter notebook trader_sentiment_analysis.ipynb   - Correlation heatmaps

   - Monthly performance breakdown

# Or use Jupyter Lab   - Hourly trading activity

jupyter lab trader_sentiment_analysis.ipynb

```6. **Insights Tab:**

   - Automated key findings

**Notebook Contents:**   - Strategic recommendations

- Data loading and preprocessing   - Risk management suggestions

- Exploratory data analysis (EDA)   - Fee impact analysis

- Statistical hypothesis testing

- Correlation and regression analysis## 📈 Data Sources

- Visualization gallery

- Key findings and recommendations### 1. fear_greed_index.csv



### 2️⃣ **Streamlit Dashboard****Columns:**



For interactive exploration and presentation:- `timestamp`: Unix timestamp

- `value`: Fear & Greed index value (0-100)

```bash- `classification`: Sentiment category (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)

# Run the dashboard- `date`: Date in YYYY-MM-DD format

streamlit run streamlit_app_final.py

**Sentiment Ranges:**

# Custom port

streamlit run streamlit_app_final.py --server.port 8080- Extreme Fear: 0-24

- Fear: 25-44

# Open in browser- Neutral: 45-55

# Navigate to http://localhost:8501- Greed: 56-75

```- Extreme Greed: 76-100



**Dashboard Navigation:**### 2. historical_data.csv

1. **📋 Assignment Details** - Project overview and author information

2. **🏠 Dashboard** - High-level metrics and sentiment distribution**Key Columns:**

3. **📊 Advanced Analytics** - Statistical tests and correlations

4. **📈 Risk Analysis** - Risk-adjusted performance metrics- `Account`: Trader account address

5. **🔍 Deep Dive** - Granular trade analysis and data export- `Coin`: Trading symbol

- `Execution Price`: Trade execution price

---- `Size Tokens`: Position size in tokens

- `Size USD`: Position size in USD

## 📁 Project Structure- `Side`: Trade direction (BUY/SELL)

- `Timestamp IST`: Trade timestamp

```- `Closed PnL`: Profit/Loss from closed positions

CRYPTO-MARKET-ANALYSIS/- `Fee`: Trading fees

│- `Leverage`: Position leverage

├── 📊 Data Files

│   ├── fear_greed_index.csv           # Bitcoin Fear & Greed Index (2024)## 🔍 Analysis Objectives

│   └── historical_data.csv             # Hyperliquid trading data (211K+ trades)

│1. **Explore Performance Variations:**

├── 📓 Analysis

│   └── trader_sentiment_analysis.ipynb # Comprehensive Jupyter analysis   - How do PnL, leverage, and trade sides vary with market sentiment?

│

├── 🌐 Dashboard2. **Detect Correlations:**

│   ├── streamlit_app_final.py          # Main Streamlit application (2,102 lines)

│   ├── streamlit_app_enhanced.py       # Base application file   - Identify relationships between sentiment and profitability

│   ├── streamlit_continuation_part1.py # Dashboard page

│   ├── streamlit_continuation_part2.py # Advanced Analytics page3. **Identify Behavioral Patterns:**

│   └── streamlit_continuation_part3.py # Risk & Deep Dive pages

│   - Do traders use higher leverage during Greed?

├── 🔧 Configuration   - Are losses higher during Fear?

│   ├── requirements.txt                 # Python dependencies

│   ├── merge_streamlit_files.py        # File integration script4. **Generate Insights:**

│   └── test_app.py                     # Application test suite   - Clear visualizations and actionable recommendations

│   - Smarter trading strategies based on sentiment

├── 📚 Documentation

│   ├── README.md                        # This file## 📊 Key Metrics Analyzed

│   ├── PROJECT_README.md               # Detailed project documentation

│   ├── QUICKSTART.txt                  # Quick start guide- **Total Net PnL**: Overall profitability after fees

│   ├── FINAL_SUMMARY.md                # Project summary- **Win Rate**: Percentage of profitable trades

│   └── ISSUE_RESOLVED.md               # Issue tracking- **Average PnL per Trade**: Mean profit/loss per transaction

│- **Trading Volume**: Total USD traded

└── 🧪 Testing- **Sharpe Ratio**: Risk-adjusted returns (Mean PnL / Std Dev)

    └── test_app.py                     # Automated testing script- **Volatility**: Standard deviation of PnL

```- **Fee Impact**: Trading costs as percentage of PnL



---## 🎨 Visualizations



## 📊 Data SourcesThe analysis includes:



### 1. Fear & Greed Index (`fear_greed_index.csv`)- 📊 Bar charts (PnL, Win Rate, Volume)

- 📈 Time series plots (Cumulative PnL, Sentiment trends)

**Source:** Alternative.me API  - 📉 Box plots (PnL distribution)

**Period:** January 2024 - December 2024  - 🔥 Heatmaps (Correlation matrices)

**Records:** 365 daily observations- 🥧 Pie charts (Sentiment distribution)

- 📐 Stacked bars (Buy vs Sell patterns)

| Column | Type | Description |- 📉 Rolling averages (Performance trends)

|--------|------|-------------|

| `timestamp` | int | Unix timestamp |## 💡 Example Insights

| `value` | int | Index value (0-100) |

| `classification` | str | Sentiment category |The analysis can reveal:

| `date` | date | YYYY-MM-DD format |

- **Best performing sentiment periods** for maximizing profits

**Sentiment Classification:**- **Risk-adjusted optimal trading conditions** (highest Sharpe ratio)

- 🔴 **Extreme Fear** (0-24): Maximum pessimism- **Leverage usage patterns** across different market sentiments

- 🟠 **Fear** (25-44): Below-average sentiment- **Fee optimization opportunities** to reduce costs

- 🟡 **Neutral** (45-55): Balanced market- **Temporal patterns** (best hours/days for trading)

- 🟢 **Greed** (56-75): Above-average optimism- **Directional bias** in trading strategy

- 🔵 **Extreme Greed** (76-100): Maximum euphoria

## 🔧 Troubleshooting

### 2. Trading Data (`historical_data.csv`)

### Issue: Missing packages

**Source:** Hyperliquid DEX

**Period:** December 2024  ```powershell

**Records:** 211,226 tradespip install --upgrade -r requirements.txt

````

| Column | Type | Description |

|--------|------|-------------|### Issue: CSV file not found

| `Account` | str | Trader wallet address |

| `Coin` | str | Trading pair symbol |Ensure `fear_greed_index.csv` and `historical_data.csv` are in the same directory as the scripts.

| `Execution Price` | float | Trade execution price |

| `Size Tokens` | float | Position size in tokens |### Issue: Streamlit not opening

| `Size USD` | float | Position size in USD |

| `Side` | str | BUY or SELL |```powershell

| `Timestamp IST` | datetime | Trade timestamp (IST) |# Try specifying the port

| `Closed PnL` | float | Realized profit/loss |streamlit run streamlit_app.py --server.port 8501

| `Fee` | float | Trading fee (USD) |```

**Derived Metrics:**### Issue: Jupyter kernel not found

- `Net_PnL` = Closed PnL - Fee

- `PnL_Percentage` = (Net_PnL / Size USD) × 100```powershell

- `is_profitable` = Net_PnL > 0python -m ipykernel install --user --name=myenv

- `Trading_Session` = Asian / European / American```

- `sentiment_category` = Merged from Fear & Greed Index

## 📝 Usage Examples

---

### Running Complete Analysis

## 🔬 Analysis Methodology

````powershell

### Statistical Techniques# 1. Run Jupyter Notebook for detailed analysis

jupyter notebook trader_sentiment_analysis.ipynb

1. **Descriptive Statistics**

   - Mean, median, standard deviation# 2. Launch interactive dashboard

   - Percentile analysis (25th, 50th, 75th)streamlit run streamlit_app.py

   - Distribution analysis (skewness, kurtosis)```



2. **Hypothesis Testing**### Customizing the Analysis

   - ANOVA: Compare means across sentiment groups

   - Chi-Square: Test independence of categorical variables**In Jupyter Notebook:**

   - Mann-Whitney U: Non-parametric comparison

   - Kruskal-Wallis: Non-parametric multi-group test- Modify date ranges in filtering cells

- Adjust visualization parameters

3. **Correlation Analysis**- Add custom metrics and calculations

   - Pearson correlation for linear relationships

   - Spearman correlation for monotonic relationships**In Streamlit Dashboard:**

   - Feature correlation matrices

- Use sidebar filters for dynamic analysis

4. **Risk Metrics**- Adjust rolling window sizes

   - Sharpe Ratio = (Mean PnL - Risk-free rate) / Std Dev- Export filtered data views

   - Sortino Ratio = Downside deviation analysis

   - Maximum Drawdown = Peak-to-trough decline## 📤 Exporting Results

   - Value at Risk (VaR) = 5th percentile loss

The Jupyter Notebook automatically exports:

### Feature Engineering

- `sentiment_performance_summary.csv`

```python- `risk_metrics_by_sentiment.csv`

# Time-based features- `daily_performance_with_sentiment.csv`

- Hour of day (0-23)

- Day of week (0-6)The Streamlit dashboard allows:

- Month (1-12)

- Week of year (1-52)- Screenshot captures of visualizations

- Trading session (Asian/European/American)- Interactive data exploration

- Real-time filtering and analysis

# Performance features

- Net PnL (Closed PnL - Fee)## 🎯 Best Practices

- PnL Percentage ((Net PnL / Size USD) × 100)

- Is Profitable (Boolean)1. **Data Quality:**

- Fee Ratio ((Fee / Size USD) × 100)

   - Verify CSV files are properly formatted

# Sentiment features   - Check for missing or corrupted data

- Sentiment Score (1-5 ordinal)

- Sentiment Category (Categorical)2. **Analysis:**

- Previous Day Sentiment (Lag feature)

```   - Run the Jupyter Notebook first for comprehensive insights

   - Use Streamlit dashboard for interactive exploration

---

3. **Interpretation:**

## 🎨 Dashboard Features   - Consider multiple metrics together

   - Account for market conditions and external factors

### Page 1: 📋 Assignment Details   - Validate findings with statistical significance



- **Project Overview**: Complete assignment description## 📚 Additional Resources

- **Objectives**: Clear research questions and goals

- **Author Information**: Contact details and credentials- **Streamlit Documentation**: https://docs.streamlit.io/

- **Methodology**: Data sources and analytical approach- **Plotly Documentation**: https://plotly.com/python/

- **Technology Stack**: Tools and libraries used- **Pandas Documentation**: https://pandas.pydata.org/docs/

- **Fear & Greed Index**: https://alternative.me/crypto/fear-and-greed-index/

### Page 2: 🏠 Dashboard

## 🤝 Contributing

**4 Interactive Tabs:**

Feel free to:

1. **Overview**

   - Total trades, PnL, win rate metrics- Add new visualizations

   - Sentiment distribution pie chart- Enhance filtering capabilities

   - Performance summary table- Implement additional metrics

- Improve performance optimization

2. **Performance Analysis**

   - PnL by sentiment (bar chart)## 📄 License

   - Win rate by sentiment

   - Average trade size comparisonThis project is for educational and analytical purposes.



3. **Time Series**## ⚠️ Disclaimer

   - Cumulative PnL over time

   - Sentiment value trendsThis analysis is for informational purposes only and should not be considered financial advice. Always conduct your own research and consult with financial professionals before making trading decisions.

   - Rolling averages (7-day, 30-day)

---

4. **Distribution Analysis**

   - PnL distribution box plots**Built with:** Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Jupyter

   - Trade size distributions

   - Statistical summaries**Author:** Data Analysis Assignment



### Page 3: 📊 Advanced Analytics**Last Updated:** November 2025

#   C R Y P T O - M A R K E T - A N A L Y S I S 

**4 Analytical Tabs:** 

 
1. **Statistical Tests**
   - ANOVA results (PnL across sentiments)
   - Chi-Square test (Profitability independence)
   - Mann-Whitney U (BUY vs SELL)
   - Interpretation and p-values

2. **Correlation Analysis**
   - Feature correlation heatmap
   - Sentiment vs performance correlation
   - Multi-dimensional analysis

3. **Behavioral Patterns**
   - Trading activity by hour
   - Daily pattern analysis
   - Session performance (Asian/European/American)

4. **Key Insights**
   - Automated findings generation
   - Statistical significance indicators
   - Actionable recommendations

### Page 4: 📈 Risk Analysis

**4 Risk-focused Tabs:**

1. **Risk-Reward**
   - Sharpe Ratio by sentiment
   - Risk-return scatter plots
   - Complete risk metrics table

2. **Position Sizing**
   - Position size distribution
   - Size vs PnL relationships
   - Volume analysis

3. **Time Analysis**
   - Performance by trading session
   - Hourly profitability patterns
   - Temporal risk assessment

4. **Key Insights**
   - Best/worst risk-adjusted performers
   - Volatility warnings
   - Position sizing recommendations

### Page 5: 🔍 Deep Dive

**4 Exploration Tabs:**

1. **Trade Explorer**
   - Top 10 trades by selected metric
   - Customizable filters (PnL, side, size)
   - CSV export functionality

2. **Trade Sides**
   - BUY vs SELL performance comparison
   - Side-specific metrics by sentiment
   - Detailed comparison table

3. **Fee Analysis**
   - Total fees paid analysis
   - Fee impact on profitability
   - Fees by sentiment breakdown

4. **Advanced Metrics**
   - Custom metric calculations
   - Multi-dimensional analysis
   - Export capabilities

---

## 🛠️ Technologies Used

### Core Libraries

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Programming language |
| **Streamlit** | 1.28+ | Web dashboard framework |
| **Pandas** | 2.0+ | Data manipulation |
| **NumPy** | 1.24+ | Numerical computing |
| **Plotly** | 5.17+ | Interactive visualizations |
| **SciPy** | 1.10+ | Statistical analysis |
| **scikit-learn** | 1.3+ | Machine learning utilities |

### Development Tools

- **Jupyter Notebook**: Interactive analysis environment
- **Git**: Version control
- **VS Code**: Code editor
- **Streamlit Cloud**: Deployment platform

### Visualization Types

- 📊 Bar charts (categorical comparisons)
- 📈 Line charts (time series trends)
- 📉 Box plots (distribution analysis)
- 🔥 Heatmaps (correlation matrices)
- 🥧 Pie charts (composition analysis)
- 📐 Scatter plots (relationship analysis)
- 📊 Stacked charts (multi-dimensional data)

---

## 💡 Results & Insights

### Key Findings

1. **Sentiment-Performance Relationship**
   - Extreme Fear periods show higher volatility but mixed returns
   - Greed periods demonstrate more consistent profitability
   - Neutral sentiment provides best risk-adjusted returns

2. **Trading Behavior Patterns**
   - Trading activity correlates with market sentiment intensity
   - Position sizing varies significantly across sentiment regimes
   - Trading volume peaks during European session

3. **Risk Analysis**
   - Fee impact averages 2-3% of total PnL
   - Maximum drawdown occurs during Fear→Extreme Fear transitions
   - Win rate varies significantly across sentiment categories

4. **Optimization Opportunities**
   - Sentiment-based entry strategies show potential
   - Fee reduction opportunities identified
   - Risk-adjusted optimal sentiment zones discovered

### Statistical Significance

- **ANOVA p-value**: < 0.05 (Significant difference in PnL across sentiments)
- **Chi-Square p-value**: < 0.05 (Profitability depends on sentiment)
- **Correlation analysis**: Identifies key relationships

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ ModuleNotFoundError: scipy

```bash
# Solution: Install scipy
pip install scipy>=1.10.0

# Or reinstall all dependencies
pip install -r requirements.txt --upgrade
````

#### ❌ KeyError: 'Realized Profit' or 'Fee USD'

```bash
# These columns don't exist. Use:
# 'Closed PnL' instead of 'Realized Profit'
# 'Fee' instead of 'Fee USD'

# File has been corrected in latest version
```

#### ❌ Streamlit deprecation warning: use_container_width

```bash
# Already fixed in streamlit_app_final.py
# All instances replaced with width='stretch'
```

#### ❌ CSV file not found

```bash
# Ensure data files are in the same directory
ls fear_greed_index.csv historical_data.csv

# Or check file paths in code
```

#### ❌ Port already in use

```bash
# Use a different port
streamlit run streamlit_app_final.py --server.port 8080
```

### Performance Optimization

```python
# Enable caching for faster reloads
@st.cache_data(ttl=3600)
def load_data():
    # Data loading logic
    return df

# Use column selection to reduce memory
df = pd.read_csv('file.csv', usecols=['col1', 'col2'])
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its benefits
3. Provide examples or mockups

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author

**Ayush Singh**

- 📧 Email: [Ayusingh693@gmail.com](mailto:Ayusingh693@gmail.com)
- 📱 Phone: +91 7031678999
- 💼 GitHub: [@ayusingh-54](https://github.com/ayusingh-54)
- 🔗 Project: [CRYPTO-MARKET-ANALYSIS](https://github.com/ayusingh-54/CRYPTO-MARKET-ANALYSIS)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

---

## ⚠️ Disclaimer

**Important Notice:**

This project is for **educational and research purposes only**. The analysis, visualizations, and insights provided should **NOT** be considered as financial advice or trading recommendations.

**Key Points:**

- Past performance does not guarantee future results
- Cryptocurrency trading involves substantial risk
- Always conduct your own research (DYOR)
- Consult with qualified financial advisors before trading
- The author is not responsible for trading losses

---

## 🙏 Acknowledgments

- **Alternative.me** for Fear & Greed Index data
- **Hyperliquid** for DEX trading data
- **Streamlit** for the amazing dashboard framework
- **Plotly** for interactive visualization capabilities
- **Python Community** for excellent data science libraries

---

## 📞 Support

Need help? Have questions?

- 📧 Email: Ayusingh693@gmail.com
- 🐛 Issues: [GitHub Issues](../../issues)
- 💬 Discussions: [GitHub Discussions](../../discussions)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by [Ayush Singh](https://github.com/ayusingh-54)

Last Updated: November 2025

</div>
