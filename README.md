# Bitcoin Trader Performance vs Market Sentiment Analysis

## 📊 Project Overview

This project provides a comprehensive analysis of the relationship between Bitcoin trader performance on Hyperliquid and market sentiment (Fear & Greed Index). It includes both a detailed Jupyter Notebook for exploratory analysis and an advanced, interactive Streamlit dashboard.

## 📁 Project Structure

```
.
├── fear_greed_index.csv              # Bitcoin Fear & Greed Index data
├── historical_data.csv                # Hyperliquid trading data
├── trader_sentiment_analysis.ipynb    # Comprehensive Jupyter Notebook analysis
├── streamlit_app.py                   # Interactive Streamlit dashboard
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Install required packages:**

```powershell
pip install -r requirements.txt
```

Or install packages individually:

```powershell
pip install pandas numpy matplotlib seaborn streamlit plotly jupyter notebook ipykernel
```

## 📓 Running the Jupyter Notebook

### Option 1: Using Jupyter Notebook

```powershell
jupyter notebook trader_sentiment_analysis.ipynb
```

### Option 2: Using Jupyter Lab

```powershell
jupyter lab trader_sentiment_analysis.ipynb
```

### Option 3: Using VS Code

1. Open `trader_sentiment_analysis.ipynb` in VS Code
2. Select Python kernel
3. Run all cells or run cells individually

## 🌐 Running the Streamlit Dashboard

```powershell
streamlit run streamlit_app.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## 📊 Features

### Jupyter Notebook Analysis

The notebook provides:

✅ **Data Loading & Cleaning**

- Automated data preprocessing
- Date/time formatting
- Missing data handling

✅ **Exploratory Data Analysis**

- Overall performance metrics
- Sentiment distribution analysis
- Trade side patterns

✅ **Advanced Visualizations**

- PnL by sentiment (bar charts)
- Win rate analysis
- Cumulative PnL time series
- Sentiment vs performance correlation heatmaps
- Risk-adjusted return metrics
- Distribution box plots

✅ **Behavioral Pattern Analysis**

- Trading activity by hour
- Monthly performance breakdown
- Buy vs Sell patterns by sentiment
- Risk metrics calculation

✅ **Key Insights & Recommendations**

- Best/worst performing sentiments
- Risk-reward optimization
- Strategic trading recommendations
- Fee impact analysis

### Streamlit Dashboard Features

The interactive dashboard includes:

🎯 **Interactive Filters**

- Date range selection
- Sentiment category filtering
- Trade side filtering (BUY/SELL)
- PnL filtering (All/Profitable/Unprofitable)

📊 **Multiple Analysis Tabs**

1. **Overview Tab:**

   - Sentiment distribution pie charts
   - PnL contribution by sentiment
   - Comprehensive performance tables

2. **PnL Analysis Tab:**

   - Win rate comparisons
   - Average PnL metrics
   - Distribution box plots

3. **Time Series Tab:**

   - Cumulative PnL vs sentiment index
   - Rolling performance metrics
   - Customizable moving averages

4. **Risk Metrics Tab:**

   - Sharpe ratio analysis
   - Volatility metrics
   - Risk-adjusted returns

5. **Deep Dive Tab:**

   - Behavioral pattern analysis
   - Correlation heatmaps
   - Monthly performance breakdown
   - Hourly trading activity

6. **Insights Tab:**
   - Automated key findings
   - Strategic recommendations
   - Risk management suggestions
   - Fee impact analysis

## 📈 Data Sources

### 1. fear_greed_index.csv

**Columns:**

- `timestamp`: Unix timestamp
- `value`: Fear & Greed index value (0-100)
- `classification`: Sentiment category (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)
- `date`: Date in YYYY-MM-DD format

**Sentiment Ranges:**

- Extreme Fear: 0-24
- Fear: 25-44
- Neutral: 45-55
- Greed: 56-75
- Extreme Greed: 76-100

### 2. historical_data.csv

**Key Columns:**

- `Account`: Trader account address
- `Coin`: Trading symbol
- `Execution Price`: Trade execution price
- `Size Tokens`: Position size in tokens
- `Size USD`: Position size in USD
- `Side`: Trade direction (BUY/SELL)
- `Timestamp IST`: Trade timestamp
- `Closed PnL`: Profit/Loss from closed positions
- `Fee`: Trading fees
- `Leverage`: Position leverage

## 🔍 Analysis Objectives

1. **Explore Performance Variations:**

   - How do PnL, leverage, and trade sides vary with market sentiment?

2. **Detect Correlations:**

   - Identify relationships between sentiment and profitability

3. **Identify Behavioral Patterns:**

   - Do traders use higher leverage during Greed?
   - Are losses higher during Fear?

4. **Generate Insights:**
   - Clear visualizations and actionable recommendations
   - Smarter trading strategies based on sentiment

## 📊 Key Metrics Analyzed

- **Total Net PnL**: Overall profitability after fees
- **Win Rate**: Percentage of profitable trades
- **Average PnL per Trade**: Mean profit/loss per transaction
- **Trading Volume**: Total USD traded
- **Sharpe Ratio**: Risk-adjusted returns (Mean PnL / Std Dev)
- **Volatility**: Standard deviation of PnL
- **Fee Impact**: Trading costs as percentage of PnL

## 🎨 Visualizations

The analysis includes:

- 📊 Bar charts (PnL, Win Rate, Volume)
- 📈 Time series plots (Cumulative PnL, Sentiment trends)
- 📉 Box plots (PnL distribution)
- 🔥 Heatmaps (Correlation matrices)
- 🥧 Pie charts (Sentiment distribution)
- 📐 Stacked bars (Buy vs Sell patterns)
- 📉 Rolling averages (Performance trends)

## 💡 Example Insights

The analysis can reveal:

- **Best performing sentiment periods** for maximizing profits
- **Risk-adjusted optimal trading conditions** (highest Sharpe ratio)
- **Leverage usage patterns** across different market sentiments
- **Fee optimization opportunities** to reduce costs
- **Temporal patterns** (best hours/days for trading)
- **Directional bias** in trading strategy

## 🔧 Troubleshooting

### Issue: Missing packages

```powershell
pip install --upgrade -r requirements.txt
```

### Issue: CSV file not found

Ensure `fear_greed_index.csv` and `historical_data.csv` are in the same directory as the scripts.

### Issue: Streamlit not opening

```powershell
# Try specifying the port
streamlit run streamlit_app.py --server.port 8501
```

### Issue: Jupyter kernel not found

```powershell
python -m ipykernel install --user --name=myenv
```

## 📝 Usage Examples

### Running Complete Analysis

```powershell
# 1. Run Jupyter Notebook for detailed analysis
jupyter notebook trader_sentiment_analysis.ipynb

# 2. Launch interactive dashboard
streamlit run streamlit_app.py
```

### Customizing the Analysis

**In Jupyter Notebook:**

- Modify date ranges in filtering cells
- Adjust visualization parameters
- Add custom metrics and calculations

**In Streamlit Dashboard:**

- Use sidebar filters for dynamic analysis
- Adjust rolling window sizes
- Export filtered data views

## 📤 Exporting Results

The Jupyter Notebook automatically exports:

- `sentiment_performance_summary.csv`
- `risk_metrics_by_sentiment.csv`
- `daily_performance_with_sentiment.csv`

The Streamlit dashboard allows:

- Screenshot captures of visualizations
- Interactive data exploration
- Real-time filtering and analysis

## 🎯 Best Practices

1. **Data Quality:**

   - Verify CSV files are properly formatted
   - Check for missing or corrupted data

2. **Analysis:**

   - Run the Jupyter Notebook first for comprehensive insights
   - Use Streamlit dashboard for interactive exploration

3. **Interpretation:**
   - Consider multiple metrics together
   - Account for market conditions and external factors
   - Validate findings with statistical significance

## 📚 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Plotly Documentation**: https://plotly.com/python/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Fear & Greed Index**: https://alternative.me/crypto/fear-and-greed-index/

## 🤝 Contributing

Feel free to:

- Add new visualizations
- Enhance filtering capabilities
- Implement additional metrics
- Improve performance optimization

## 📄 License

This project is for educational and analytical purposes.

## ⚠️ Disclaimer

This analysis is for informational purposes only and should not be considered financial advice. Always conduct your own research and consult with financial professionals before making trading decisions.

---

**Built with:** Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Jupyter

**Author:** Data Analysis Assignment

**Last Updated:** November 2025
#   C R Y P T O - M A R K E T - A N A L Y S I S  
 