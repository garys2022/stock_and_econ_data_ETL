import datetime

from sqlalchemy import create_engine,text, select,and_
import sqlalchemy as sa
import pandas as pd
from pathlib import Path
from constant.config import db_login
from constant.constant import sma_period,econ_datas
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from model.db import Spy
import numpy as np
#import numpy as np
#import pymysql


######################econ data
######################stock data

def load_raw_stock_to_db_sqlorm(raw_stock_data,
                                engine=None):
    #ref: https://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy

    if engine == None:
        engine = create_engine(db_login['root'], pool_recycle=3600)

    #change type for date from np.datetime64ns to datetime.date to input to db
    if type(raw_stock_data.Date[0]) != datetime.date:
        raw_stock_data.loc[:,"Date"]= raw_stock_data.loc[:,"Date"].dt.date
    raw_stock_data = raw_stock_data.replace(np.nan, None)
    with Session(engine) as session:
        try:
            session.query(Spy).filter(
            Spy.date.in_(raw_stock_data["Date"].tolist())
            ).delete(synchronize_session='evaluate')
            record=raw_stock_data.apply(lambda x:
                Spy(**
                    {
                        'date': x['Date'],
                        'open': x['Open'],
                        'high': x['High'],
                        'low': x['Low'],
                        'close': x['Close'],
                        'adj_close': x['Adj Close'],
                        'volume': x['Volume'],
                        'dividends':x['Dividends'],
                        'stock_splits':x['Stock Splits']
                    }),
            axis=1).tolist()
            session.add_all(record)
            session.commit()
            print('data upload success')
        except:
            session.rollback()
            print('data upload failed')


def load_bronze_econ_data_to_db_orm(bronze_econ_data,
                                    engine=create_engine(db_login['root'],
                                    pool_recycle=3600)):

    with Session(engine) as session:
        for econ_data_name,econ_data_obj in econ_datas.category.items():

            bronze_db = econ_data_obj.bronze_db

            # replace np.nan with None for data input
            one_bronze_econ_data=bronze_econ_data[econ_data_name].replace([np.nan], [None])

            # remove data tobe input in the database to avoid duplicate data
            session.query(bronze_db).filter(
                bronze_db.date.in_(one_bronze_econ_data['Release Date'].tolist())
            ).delete(synchronize_session='evaluate')

            # prepare records to be input in the db
            record = one_bronze_econ_data.apply(lambda x:
                bronze_db(**
                    {
                    'date': x['Release Date'],
                    'time': x['Time'],
                    'actual': x['Actual'],
                    'forecast': x['Forecast'],
                    'previous': x['Previous'],
                    'revised': x['Revised']
                    }
                ),
            axis=1).tolist()
            session.add_all(record)
        session.commit()
        print('data upload success')