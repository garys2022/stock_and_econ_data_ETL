import cloudscraper
from datetime import datetime, timedelta, date
from tqdm import tqdm
import pandas as pd
import numpy as np
from constant.constant import econ_datas
import yfinance as yf


# get stock data
def load_stock_data(ticker='SPY', start=date(2000, 1, 1), end=date.today()):
    """
    load_stock_data(ticker='SPY', start=date(2000, 1, 1):datetime.date, end=date.today():datetime.date)
    Using yfinance to extract stock price data from start(datetime.date) to end (datetime.date)
    return stock_data in the format of pd.DataFrame
    """
    stock_data = yf.download(ticker, start=start, end=end)
    stock_data = stock_data.reset_index()
    return stock_data


"""
load_stock_data(ticker="Spy",start=date(2000,1,1),end=date.today()):
To load stock_action data from yahoo finance
Parameter:
ticker : string type , stock ticket to be search in yahoo finance 
start : date.date type , start date for stock data loaded
end : date.date type, end date for stock data loaded

return pd.DataFrame 
"""


# get stock_action_data
def load_stock_action_data(ticker='SPY', start=date(2000, 1, 1), end=date.today()):
    stock = yf.Ticker(ticker)
    stock_actions = stock.actions.reset_index()
    stock_actions.loc[:, 'Date'] = stock_actions.loc[:, 'Date'].apply(lambda x: x.replace(tzinfo=None))
    timerange = (stock_actions['Date'] >= np.datetime64(start)) & (stock_actions['Date'] <= np.datetime64(end))
    stock_actions = stock_actions[timerange]
    return stock_actions


"""
load_stock_action_data(ticker="Spy",start=date(2000,1,1),end=date.today()):
To load stock_action data from yahoo finance
Parameter:
ticker : string type , stock ticket to be search in yahoo finance 
start : date.date type , start date for stock action data loaded
end : date.date type, end date for stock action data loaded

return pd.DataFrame
"""


def tqdm_generator():
    while True:
        yield


def extract_one_econ_data(event_id="733", start_date=None, end_date=None):
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    scraper = cloudscraper.create_scraper()
    big_df = pd.DataFrame()
    DD = timedelta(days=42)
    for _ in tqdm(tqdm_generator()):
        payload = f'eventID=1&event_attr_ID={event_id}&event_timestamp={end_date}'

        r = scraper.post('https://www.investing.com/economic-calendar/more-history', data=payload, headers=headers)
        if (r.json()['hasMoreHistory'] == '1') & \
            (datetime.strptime(end_date, '%Y-%m-%d') > datetime.strptime(start_date, '%Y-%m-%d')):
            df = pd.read_html('<table>' + r.json()['historyRows'] + '</table>')[0]
            big_df = pd.concat([big_df, df], axis=0, ignore_index=True)
            end_date = str(datetime.strptime(end_date, '%Y-%m-%d') - DD).split()[0]
        else:
            break
    big_df = big_df.drop_duplicates()
    big_df.columns = ['Release Date', 'Time', 'Actual', 'Forecast', 'Previous', 'Revised']
    return big_df


def extract_stock_data(ticker='SPY', start=date(2000, 1, 1), end=date.today()):
    """
    load_stock_data(ticker='SPY', start=date(2000, 1, 1):datetime.date, end=date.today():datetime.date)
    Using yfinance to extract stock price data from start(datetime.date) to end (datetime.date)
    return stock_data in the format of pd.DataFrame
    column includes:
    Date: datetime64[ns]
    Open: float64
    High: float64
    Low: float64
    Close: float64
    Adj Close float64
    Volume: int64
    Dividends: float64
    Stock Splits:  float64
    """
    stock_data = load_stock_data(ticker, start, end)
    stock_action_data = load_stock_action_data(ticker, start, end)
    return stock_data.merge(stock_action_data, how='left', on='Date')


def extract_econ_data(events= econ_datas.category.keys(),
                      start_date="2000-01-01",
                      end_date=date.today().strftime("%Y-%m-%d")):
    """
    :param events: econ_data_type : list
    :param start_date: start date string for date in %Y-%m-%d format
    :param end_date: end date string for date in %Y-%m-%d format
    :return: dict of pandas dataFrame for each event required.
    """
    econ_data = {}
    for event in events:
        econ_data[event] = extract_one_econ_data(event_id=econ_datas.category[event].event_id,
                                                 start_date=start_date,
                                                 end_date=end_date)
    return econ_data


###################################################### from db
###### Bronze_data(unclean)


if __name__ == '__main__':
    print(extract_econ_data(start_date="2023-01-01"))
