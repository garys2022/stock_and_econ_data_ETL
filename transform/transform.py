import datetime
import pandas as pd
import numpy as np
from constant.constant import econ_datas,sma_period,econ_col_list,stock_percentage_change

###Stock_data

# Function to clearn stock data after combing stock data and stock's event datas
# Bronze to Silver cleaning
def stock_data_clean(merged_stock_df):
    cols_list = ['id','date', 'open', 'high', 'low', 'close', 'adj_close', 'volume',
                 'dividends', 'stock_splits']
    col_check_fail="Columns check failed, columns shall include exactly one ['id','date', 'open', 'high', 'low', 'close'," \
                   "'adj_close', 'volume','dividends', 'stock_splits'] "
    if merged_stock_df.columns.isin(cols_list).sum() != len(cols_list):
        return print(col_check_fail)

    merged_stock_df['dividends'].fillna(value=0, inplace=True)
    merged_stock_df['stock_splits'].fillna(value=0, inplace=True)
    merged_stock_df['is_dividends'] = merged_stock_df['dividends'].apply(lambda x: 0 if x == 0 else 1)
    merged_stock_df['is_stock_splits'] = merged_stock_df['stock_splits'].apply(lambda x: 0 if x == 0 else 1)
    merged_stock_df.columns = merged_stock_df.columns.to_series().replace('id','bronze_id')
    return merged_stock_df


###econ_data

def bronze_to_silver_econ_datas(raw_data:dict):
    for data in raw_data.keys():
        raw_data[data] = bronze_to_silver_single_econ_data(raw_data[data])
    return raw_data


def bronze_to_silver_single_econ_data(econ_data:pd.DataFrame):
    econ_data_2=pd.DataFrame()
    econ_data_2['raw_id']=econ_data['id']

    # transform string type release date to datetime.date format
    try:
        econ_data_2[['release_date','period']]=econ_data['release_date'].str.split("(",expand=True)
        econ_data_2.loc[:,'period']=econ_data_2['period'].str.strip(')')
    except ValueError:
        econ_data_2['release_date']=econ_data['release_date']
    econ_data_2.loc[:,'release_date']=econ_data_2['release_date'].str.strip(' ')
    econ_data_2.loc[:,'release_date']=pd.to_datetime(econ_data_2['release_date'],format = "%b %d, %Y")
    econ_data_2.loc[:, 'release_date'] = econ_data_2.loc[:, 'release_date'].dt.date

    #Transform string format number data with k or % to float format
    for col in ['actual','forecast','previous']:
        econ_data_2.loc[:,col]=number_cleaner(econ_data[col])


    econ_data_2.loc[:,'beat_forecast'] = econ_data_2.apply(lambda x: 1 if x.actual>x.forecast else 0 , axis=1)
    econ_data_2.loc[:,'beat_previous'] = econ_data_2.apply(lambda x: 1 if x.actual>x.previous else 0 , axis=1)

    econ_data_2=econ_data_2.replace([np.nan],[None])
    return econ_data_2

# Function to take string format data with % / K and convert to float
def number_cleaner(col):
    if col.str.contains('%').sum()==col.notnull().sum():
        return col.str.strip('%').astype('float')/100
    elif col.str.contains('K').sum()==col.notnull().sum():
        return col.str.strip('K').str.replace(',','').astype('float')
    else:
        print('unable to clean number, please check data format')
        return None

###merged data
# combine stock_silver data and econ_silver data
# clean combined data
# add features in combined data
def silver_to_gold_merge_and_clean(stock_data_silver,econ_datas_silver):
    """
    Comebine stock and econ silver data , cleaned the combine data and add features in combined data
    :param stock_data_silver: silver stock data:pd.DataFrame
    :param econ_datas_silver: silver econ data:dict
        with econ_datas_silver['name of econ_data'] = econ_data:pd.DataFrame
    :return: combined data:pd.DataFrame
    """
    stock_data=stock_data_silver.copy()
    stock_data.drop('bronze_id',axis=1,inplace=True)
    stock_data.columns = stock_data.columns.str.replace(r'^id$','stock_silver_id',regex=True)
    stock_data.sort_values(by='date',ascending=True,inplace=True,ignore_index=True)

    for data in econ_datas.category.keys():
        econ_data= econ_datas_silver[data].loc[:,econ_datas_silver[data].columns.isin(econ_col_list)]
        econ_data.columns = f"{data}_"+ econ_data.columns.to_series()
        econ_data.loc[:,f'{data}_silver_id']=econ_datas_silver[data].loc[:,'id']

        #using outer join to ensure future econ_data release date data is intact for fill na process
        print('before merge',stock_data['date'].isna().sum())
        stock_data = stock_data.merge(econ_data,how="outer",left_on="date",right_on=f"{data}_release_date",
                                      validate=None)

        stock_data['date'].fillna(stock_data[f'{data}_release_date'],inplace=True)

        stock_data[f'is_{data}_release_date'] = stock_data[f'{data}_release_date'].apply(
            lambda x: 0 if pd.isnull([x]) else 1)

        stock_data.sort_values(by=["date"],inplace=True)

        stock_data[f'{data}_actual'].fillna(method='ffill',inplace=True)
        stock_data[f'{data}_forecast'].fillna(method='ffill',inplace=True)
        stock_data[f'{data}_previous'].fillna(method='ffill',inplace=True)
        stock_data[f'{data}_beat_forecast'].fillna(method='ffill',inplace=True)
        stock_data[f'{data}_beat_previous'].fillna(method='ffill',inplace=True)
        stock_data[f'{data}_next_release_date'] = stock_data[f'{data}_release_date'].fillna(method='bfill')
        stock_data[f'{data}_day_to_next_release'] = stock_data[f'{data}_next_release_date'] - stock_data['date']
        stock_data[f'{data}_day_to_next_release'] = stock_data[f'{data}_day_to_next_release'].dt.days

        stock_data.drop(f'{data}_release_date',axis=1,inplace=True)

    # adding features
    stock_data['is_release_date']=stock_data[[f'is_{i}_release_date' for i in econ_datas.category.keys()]].max(axis=1)
    for period in sma_period:
        stock_data[f'sma_{str(period)}_diff']= (stock_data['open'].rolling(period).mean()/stock_data['open'])-1
    for period in stock_percentage_change:
        stock_data[f'change_after_{period}_day']= (stock_data['open'].shift(-1*period)/stock_data['open'])-1


    #drop rows where open is null (rows without stock data)
    stock_data.dropna(axis=0,subset=['open'],inplace=True)

    #replace np.nan with None for insert  to SQL server
    stock_data.replace([np.nan],[None],inplace=True)
    return stock_data

if __name__ == '__main__':
    pass


