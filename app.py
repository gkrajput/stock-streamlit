import yfinance as yf
import streamlit as st
import pandas as pd

valid_periods = {
    "1 Day": "1d",
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "10 Years": "10y",
    "Year To Date": "ytd",
    "Maximum": "max"
}

valid_intervals = {
    "1 Minute": "1m",
    "2 Minutes": "2m",
    "5 Minutes": "5m",
    "15 Minutes": "15m",
    "30 Minutes": "30m",
    "60 Minutes": "60m",
    "90 Minutes": "90m",
    "1 Hour": "1h",
    "1 Day": "1d",
    "5 Days": "1d",
    "1 Week": "1wk",
    "1 Month": "1mo",
    "3 Months": "3mo"
}


def is_valid(data):
    return data is not None and data.values.size > 0


st.write("""
# Stock Analyzer 🎲

Stock information to help you make better decision!

""")

st.sidebar.header('What do you want?')

news = st.sidebar.checkbox('News')

st.sidebar.text_input("Ticker: ", value='ADANIENT.NS', key="name")

all_i = st.sidebar.checkbox('All', value=True)
close_p = st.sidebar.checkbox('Closing Price')
open_p = st.sidebar.checkbox('Opening Price')
volume = st.sidebar.checkbox('Volume')
ss = st.sidebar.checkbox('Stock Splits')
dv = st.sidebar.checkbox('Dividends')

# 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
period_input = st.sidebar.selectbox(
    'Period:',
    ('Select...', '1 Day', '5 Days', '1 Month', '3 Months', '6 Months', '1 Year', '2 Years', '5 Years', '10 Years',
     'Year To Date', 'Maximum')
)
# 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
interval_input = st.sidebar.selectbox(
    'Interval:',
    ('Select...', '1 Minute', '2 Minutes', '5 Minutes', '15 Minutes', '30 Minutes', '60 Minutes', '90 Minutes',
     '1 Hour', '1 Day', '5 Days', '1 Week', '1 Month', '3 Months')
)

form = st.sidebar.form("date_form")
start_date = form.date_input('Start Date', value=None)
end_date = form.date_input('End Date', value=None)
submitted = form.form_submit_button("Submit")


def get_period(period_i):
    return valid_periods.get(period_i, "5d")


def get_interval(interval_i):
    return valid_intervals.get(interval_i, "1h")


period = get_period(period_input)
interval = get_interval(interval_input)
tickerSymbol = st.session_state.name

tickerData = yf.Ticker(tickerSymbol)

if submitted:
    submitted = False
    tickerDF = tickerData.history(start=start_date, end=end_date)
else:
    tickerDF = tickerData.history(period=period, interval=interval)

if news and tickerData.news is not None:
    st.title("News")
    n_df = pd.DataFrame.from_dict(tickerData.news)
    n_df = n_df.reset_index()  # make sure indexes pair with number of rows
    for index, row in n_df.iterrows():
        n_url = row['link']
        detail = row['title'] + " - " + row['publisher']
        st.markdown(f'''
        {detail} <a href={n_url}>Read</a>
        ''',
                    unsafe_allow_html=True)
        thumbnail = pd.DataFrame.from_dict(row['thumbnail']).head(1)
        st.image(thumbnail.get('resolutions')[0].get('url'))

st.title(tickerSymbol)
if tickerData.isin is not None:
    st.write("♟ISIN: " + tickerData.isin + "♟")

if is_valid(tickerData.recommendations):
    st.markdown(""" ### Recommendations """)
    rec_df = pd.DataFrame(tickerData.recommendations.drop(['Action'], axis=1))
    n_df = rec_df.sort_index(ascending=False).head(10)
    st.bar_chart(data=n_df, x='Firm', y='To Grade', height=300)

if all_i:
    filtered_df = tickerDF.drop(['Volume', 'Stock Splits', 'Dividends'], axis=1)
    st.line_chart(filtered_df)
if close_p:
    st.line_chart(tickerDF.Close)
if open_p:
    st.line_chart(tickerDF.Open)
if volume:
    st.line_chart(tickerDF.Volume)
if ss:
    st.line_chart(tickerDF['Stock Splits'])
if dv:
    st.line_chart(tickerDF['Dividends'])

with st.expander("Financial Data"):
    if is_valid(tickerData.balance_sheet):
        st.markdown(""" ### Balance Sheet """)
        st.write(tickerData.balance_sheet)

    if is_valid(tickerData.quarterly_balance_sheet):
        st.markdown(""" ### Quarterly Balance Sheet """)
        st.write(tickerData.quarterly_balance_sheet)

    if is_valid(tickerData.income_stmt):
        st.markdown(""" ### Income Statement """)
        st.write(tickerData.income_stmt)
    if is_valid(tickerData.quarterly_income_stmt):
        st.markdown(""" ### Quarterly Income Statement """)
        st.write(tickerData.quarterly_income_stmt)

    if is_valid(tickerData.earnings):
        st.markdown(""" ### Earnings """)
        st.write(tickerData.earnings)
    if is_valid(tickerData.quarterly_earnings):
        st.markdown(""" ### Quarterly Earnings """)
        st.write(tickerData.quarterly_earnings)

    if is_valid(tickerData.cashflow):
        st.markdown(""" ### Cash Flow """)
        st.write(tickerData.cashflow)
    if is_valid(tickerData.quarterly_cashflow):
        st.markdown(""" ### Quarterly Cash Flow """)
        st.write(tickerData.quarterly_cashflow)

    if is_valid(tickerData.major_holders):
        st.markdown(""" ### Major Holders """)
        n_df = tickerData.major_holders
        n_df = n_df.reset_index()  # make sure indexes pair with number of rows
        for index, row in n_df.iterrows():
            st.write(row[1], " = ", row[0])

    if is_valid(tickerData.institutional_holders):
        st.markdown(""" ### Major Institutional Holders """)
        st.write(tickerData.institutional_holders)
    if is_valid(tickerData.mutualfund_holders):
        st.markdown(""" ### Major Mutual Fund Holders """)
        st.write(tickerData.mutualfund_holders)

    if is_valid(tickerData.actions):
        st.markdown(""" ### Corporate Actions """)
        st.write(tickerData.actions)

    if is_valid(tickerData.analyst_price_target):
        st.markdown(""" ### Analyst Price Target """)
        n_df = tickerData.analyst_price_target
        n_df = n_df.reset_index()  # make sure indexes pair with number of rows
        for index, row in n_df.iterrows():
            st.write(row['index'], " = ", row[0])

    if is_valid(tickerData.revenue_forecasts):
        st.markdown(""" ### Revenue Forecasts """)
        st.write(tickerData.revenue_forecasts)

    if is_valid(tickerData.earnings_forecasts):
        st.markdown(""" ### Earnings Forecasts """)
        st.write(tickerData.earnings_forecasts)

    if is_valid(tickerData.earnings_trend):
        st.markdown(""" ### Earnings Trend """)
        st.write(tickerData.earnings_trend)

    if is_valid(tickerData.calendar):
        st.markdown(""" ### Calendar """)
        n_df = tickerData.calendar.head(1)
        n_df = n_df.reset_index()  # make sure indexes pair with number of rows
        for index, row in n_df.iterrows():
            st.write(row['index'], ": ", row[0], " - ", row[1])

    if is_valid(tickerData.earnings_dates):
        st.markdown(""" ### Earnings Dates """)
        st.write(tickerData.earnings_dates)


with st.expander("See Raw Data"):
    res = dict((k, tickerData.info[k]) for k in ['sector', 'industry', 'country', 'financialCurrency', 'ebitdaMargins',
                                                 'profitMargins', 'grossMargins', 'totalCash', 'totalDebt',
                                                 'totalRevenue',
                                                 'totalCashPerShare', 'revenuePerShare', 'financialCurrency',
                                                 'lastSplitDate', 'lastSplitFactor', 'lastDividendDate']
               if k in tickerData.info)
    st.markdown(""" ### Stock Information """)
    ticker_info = {'Name': res.keys(), 'Value': res.values()}
    st.table(ticker_info)
    st.markdown(""" ### Raw Data """)
    st.dataframe(tickerDF)
    st.markdown(""" ### Meta Data """)
    st.write(tickerData.history_metadata)
