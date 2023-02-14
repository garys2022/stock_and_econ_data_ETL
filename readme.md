# Stock_modelling(Underdevelopment)

# Introduction
This is a package that need to be combined to be used in my other repo
"myairflow-dockerserver' to perform ETL process for
* Stock information (from Yahoo Finance)
* US Economics data (from Investing.com)

# Data architecture
This project is trying to practice a medallion architecture that classified and store data in 3 stages
* Bronze - Raw data
* Silver - Filtered and cleaned data
* Gold - Aggregated data

## file
### extract
include function for extract data
  * extract_stock_data(ticker:str, start:datetime.date, end:datetime.date)
    * usage: stock data for "ticker" from "start" date to "end" date
    * params: 
      * ticker: str
      * start: datetime.date
      * end: datetime.date
    * return data in pandas.DataFrame
  * extract_econ_data(events:list ,start_date:str, end_date:str)
    * usage:extract stock data for all "events" from start_date to "end" date
    * params:
      * events: list of str of event name for the economics data in investing.com, available economics data type in constant.constant.econ_datas.category.keys()
      * start_date: start date string in "%Y-%m-%d" format
      * end_date: end date string in "%Y-%m-%d" format
    * return dictionary of {'event name': pandas.DataFrame) pairs
  * extract_one_econ_data(event_id="733", start_date=None, end_date=None)
    * usage:extract one econ data by the use of event_id , does not limit to economics data type available in constant.constant.econ_datas.category.keys()
    * params:
      * event_id: str , id for economics data events in investing.com
      * start_date: start date string in "%Y-%m-%d" format
      * end_date: end date string in "%Y-%m-%d" format
    * return pandas.DataFrame of econ_data
### transform
include function of transforming data
  * stock_data_clean(merged_stock_df)
    * usage: clean stock data extracted from yf (bronze to silver data cleaning)
    * params:
      * merged_stock_df: pandas.DataFrame, product from extract_stock_data
    * return pandas.DataFrame 
  * bronze_to_silver_econ_datas(raw_data:dict)
    * usage:clean multiple econ_data (bronze to silver data cleaning)
    * params:
      * raw_data:dict , {'event name':pandas.DataFrame) paris from the product of extract_econ_data
    * return dict consist of {'event name' pandas.DataFrame} of cleaned df. 
  * bronze_to_silver_single_econ_data(econ_data:pd.DataFrame)
    * usage: clean single econ data (bronze to silver data cleaning)
    * params:
      * econ_data: pandas.DataFrame , product from extract_one_econ_data
    * return pandas.DataFrame , cleaned econ data
  * silver_to_gold_merge_and_clean(stock_data_silver,econ_datas_silver)
    * usage: merge cleaned silver stock and econ_datas, and further clean and add features
    * params:
      * stock_data_silver: pandas.DataFrame , silver stage stock data (product from stock_data_clean)
      * econ_datas_silver: dict of {'events': pd.DataFrame} , silver stage econ_datas(product from bronze_to_silver_econ_datas)
    * return pandas.DataFrame , cleaned and aggregated gold stage data
### load 
include function of loading data to db
for silver - gold data , the uploading function is done in the airflow package
* load_raw_stock_to_db_sqlorm(raw_stock_data, engine)
  * Usage: upload bronze stock data to db SPY(bronze_db) which set in model.db.py by SQLAlchemy approach
  * params:
    * raw_stock_data : pd.DataFrame, product of extract_stock_data
    * engine : sql connection engine , default engine set in constant.config.db_login['root']
* load_bronze_econ_data_to_db_orm(bronze_econ_data, engine)
  * Usage: upload bronze stock data to bronze_db set in model.db.py by SQLAlchemy approach
  * params:
    * raw_stock_data : pd.DataFrame, product of extract_econ_data
    * engine : sql connection engine , default engine set in constant.config.db_login['root']



### model.db
include db model of bronze , silver , and gold data using SQLAlchemy 
### constant
#### constant.constant
include constant/pre-set value used in this package
#### constant.config
include config for preset sql database connection, see template in constant.config_template


