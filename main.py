from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime

app = Flask(__name__)
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    # Fetch real-time data from Yahoo Finance
    data = stock.info

    # Extract relevant stock information
    stock_data = {
        'name': data.get('shortName', 'N/A'),
        'symbol': data.get('symbol', 'N/A'),
        'price': float(data.get('currentPrice', 0.0)),
        'previous_close': float(data.get('regularMarketPreviousClose', 0.0)),
        'marketCap': format_number(data.get('marketCap', 'N/A')),
        'currency': data.get('currency', 'N/A'),
        'description': data.get('longBusinessSummary', 'N/A'),
        'forwardPE': data.get('forwardPE', 'N/A'),
        'trailingPE': data.get('trailingPE', 'N/A'),
        'dividendYield': data.get('dividendYield', 'N/A'),
        'dividendRate': data.get('dividendRate', 'N/A'),
    }

    return stock_data

def format_date(date_obj):
    try:
        date_str = str(date_obj)
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
    except ValueError:
        return date_str

def format_number(value):
    try:
        return "{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value

app.jinja_env.filters['format_number'] = format_number

def get_additional_info(ticker):
    stock = yf.Ticker(ticker)
    balance_sheet = stock.quarterly_balance_sheet
    income_statement = stock.quarterly_financials
    quarter_cash_flow = stock.quarterly_cashflow
    annual_cash_flow = stock.cashflow

    def sum_quarters(series):
        return sum(series.iloc[i] if i < len(series) else 0.0 for i in range(4))

    quarterCashflow = [
        format_number(quarter_cash_flow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in quarter_cash_flow.index else 0.0),
        format_number(quarter_cash_flow.loc['Free Cash Flow'].iloc[1] if 'Free Cash Flow' in quarter_cash_flow.index else 0.0),
        format_number(quarter_cash_flow.loc['Free Cash Flow'].iloc[2] if 'Free Cash Flow' in quarter_cash_flow.index else 0.0),
        format_number(quarter_cash_flow.loc['Free Cash Flow'].iloc[3] if 'Free Cash Flow' in quarter_cash_flow.index else 0.0),
    ]

    annualCashflow = [
        format_number(annual_cash_flow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in annual_cash_flow.index else 0.0),
        format_number(annual_cash_flow.loc['Free Cash Flow'].iloc[1] if 'Free Cash Flow' in annual_cash_flow.index else 0.0),
        format_number(annual_cash_flow.loc['Free Cash Flow'].iloc[2] if 'Free Cash Flow' in annual_cash_flow.index else 0.0),
        format_number(annual_cash_flow.loc['Free Cash Flow'].iloc[3] if 'Free Cash Flow' in annual_cash_flow.index else 0.0),
    ]

    quarterDate = [
        format_date(quarter_cash_flow.axes[1][0]),
        format_date(quarter_cash_flow.axes[1][1]),
        format_date(quarter_cash_flow.axes[1][2]),
        format_date(quarter_cash_flow.axes[1][3]),
    ]

    annualDate = [
        format_date(annual_cash_flow.axes[1][0]),
        format_date(annual_cash_flow.axes[1][1]),
        format_date(annual_cash_flow.axes[1][2]),
        format_date(annual_cash_flow.axes[1][3]),
    ]



    additional_info = {
        'currentAssets': balance_sheet.loc['Current Assets'].iloc[0] if 'Current Assets' in balance_sheet.index else 0.0,
        'currentLiabilities': balance_sheet.loc['Current Liabilities'].iloc[0] if 'Current Liabilities' in balance_sheet.index else 0.0,
        'operatingIncome': sum_quarters(income_statement.loc['Operating Income']) if 'Operating Income' in income_statement.index else 0.0,
        'totalRevenue': sum_quarters(income_statement.loc['Total Revenue']) if 'Total Revenue' in income_statement.index else 0.0,
        'TTM_Cashflow': format_number(sum_quarters(quarter_cash_flow.loc['Free Cash Flow']) if 'Free Cash Flow' in quarter_cash_flow.index else 0.0),
        'quarterlyCashflow': quarterCashflow,
        'annualCashflow': annualCashflow,
        'quarterDate': quarterDate,
        'annualDate': annualDate,
    }

    return additional_info

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    additional_info = None
    ticker = None
    if request.method == 'POST':
        ticker = request.form.get('ticker').upper()
        try:
            stock_data = get_stock_data(ticker)
            additional_info = get_additional_info(ticker)
        except Exception as e:
            stock_data = {'error': str(e)}
            additional_info = {'error': str(e)}

    return render_template('index.html', stock_data=stock_data, stats=additional_info, ticker=ticker)

if __name__ == '__main__':
    app.run()