from sqlalchemy import Column, Integer, Date, Float, String, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.schema import ForeignKey
from constant.config import db_login
import signal
from contextlib import contextmanager

Base = declarative_base()


def init_db(engine=create_engine(db_login['root'], pool_recycle=3600, echo=True)):
    Base.metadata.create_all(engine, checkfirst=True)


class Spy(Base):
    __tablename__ = "spy"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('date', Date, unique=True)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    adj_close = Column('adj_close', Float)
    volume = Column('volume', Integer)
    dividends = Column('dividends', Float)
    stock_splits = Column('stock_splits', Float)

    silver = relationship('Spy_silver', backref='bronze_data', passive_deletes=True)

    def __repr__(self):
        return f"spy_bronze(id={self.id!r}, date={self.date!r}, open={self.open!r})"


class Spy_silver(Base):
    __tablename__ = "spy_silver"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('date', Date, unique=True)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    adj_close = Column('adj_close', Float)
    volume = Column('volume', Integer)
    dividends = Column('dividends', Float)
    stock_splits = Column('stock_splits', Float)
    is_dividends = Column('is_dividends', Integer)
    is_stock_splits = Column('is_stock_splits', Integer)

    bronze_id = Column('bronze_id', Integer, ForeignKey('spy.id', ondelete='CASCADE'), unique=True)
    gold = relationship('Gold_stock_and_econ_data', backref='silver_spy', passive_deletes=True)

    # bronze= relationship("Spy",uselist=False,back_populates="silver")

    def __repr__(self):
        return f"spy_silver(id={self.id!r}, date={self.date!r}, open={self.open!r})"


class Jobless_claim_bronze(Base):
    __tablename__ = "jobless_claim_bronze"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('release_date', String(20), unique=True)
    time = Column('time', String(20))
    actual = Column('actual', String(10))
    forecast = Column('forecast', String(10))
    previous = Column('previous', String(10))
    revised = Column('revised', String(10))

    silver = relationship('Jobless_claim_silver', backref='bronze_data', passive_deletes=True)

    def __repr__(self):
        return f"jobless_claim_silver(id={self.id!r}, " \
               f"date={self.date!r}, " \
               f"forecast={self.forecast!r} ," \
               f"actual={self.actual!r})"

    # def __init__(self):
    #    econ_datas.category['jobless_claim'].bronze_db=self


class Jobless_claim_silver(Base):
    __tablename__ = "jobless_claim_silver"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('release_date', Date, unique=True)
    actual = Column('actual', Float)
    forecast = Column('forecast', Float)
    previous = Column('previous', Float)
    beat_forecast = Column('beat_forecast', Float)
    beat_previous = Column('beat_previous', Integer)

    bronze_id = Column('bronze_id', Integer, ForeignKey('jobless_claim_bronze.id', ondelete='CASCADE'), unique=True)
    gold = relationship('Gold_stock_and_econ_data', backref='silver_jobless_claim', passive_deletes=True)

    def __repr__(self):
        return f"jobless_claim_silver(id={self.id!r}, " \
               f"date={self.date!r}, " \
               f"forecast={self.forecast!r} ," \
               f"actual={self.actual!r})"

    # def __init__(self):
    #    econ_datas.category['jobless_claim'].silver_db=self


class Cpi_bronze(Base):
    __tablename__ = "cpi_bronze"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')
    date = Column('release_date', String(20), unique=True)
    time = Column('time', String(20))
    actual = Column('actual', String(10))
    forecast = Column('forecast', String(10))
    previous = Column('previous', String(10))
    revised = Column('revised', String(10))

    silver = relationship('Cpi_silver', backref='bronze_data', passive_deletes=True)


    def __repr__(self):
        return f"cpi_bronze(id={self.id!r}, date={self.date!r}, forecast={self.forecast!r} ,actual={self.actual!r})"


class Cpi_silver(Base):
    __tablename__ = "cpi_silver"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('release_date', Date, unique=True)
    actual = Column('actual', Float)
    forecast = Column('forecast', Float)
    previous = Column('previous', Float)
    beat_forecast = Column('beat_forecast', Float)
    beat_previous = Column('beat_previous', Integer)

    bronze_id = Column('bronze_id', Integer, ForeignKey('cpi_bronze.id', ondelete='CASCADE'), unique=True)
    gold = relationship('Gold_stock_and_econ_data', backref='silver_cpi', passive_deletes=True)

    def __repr__(self):
        return f"cpi_silver(id={self.id!r}, date={self.date!r}, forecast={self.forecast!r} ,actual={self.actual!r})"


class Unemploy_bronze(Base):
    __tablename__ = "unemploy_bronze"

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('release_date', String(20), unique=True)
    time = Column('time', String(20))
    actual = Column('actual', String(10))
    forecast = Column('forecast', String(10))
    previous = Column('previous', String(10))
    revised = Column('revised', String(10))

    silver = relationship('Unemploy_silver', backref='bronze_data', passive_deletes=True)

    def __repr__(self):
        return f"unemploy_bronze(id={self.id!r}, " \
               f"date={self.date!r}, " \
               f"forecast={self.forecast!r} ," \
               f"actual={self.actual!r})"


class Unemploy_silver(Base):
    __tablename__ = "unemploy_silver"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    date = Column('release_date', Date, unique=True)
    actual = Column('actual', Float)
    forecast = Column('forecast', Float)
    previous = Column('previous', Float)
    beat_forecast = Column('beat_forecast', Float)
    beat_previous = Column('beat_previous', Integer)

    bronze_id = Column('bronze_id', Integer, ForeignKey('unemploy_bronze.id', ondelete='CASCADE'), unique=True)
    gold = relationship('Gold_stock_and_econ_data', backref='silver_unemploy', passive_deletes=True)

    def __repr__(self):
        return f"unemploy_silver(id={self.id!r}, " \
               f"date={self.date!r}, " \
               f"forecast={self.forecast!r} ," \
               f"actual={self.actual!r})"


class Gold_stock_and_econ_data(Base):
    __tablename__ = "Spy_econ_gold"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True, autoincrement='auto')

    stock_silver_id = Column('stock_silver_id', Integer,
                             ForeignKey("spy_silver.id", ondelete="SET NULL")
                             , unique=True)
    date = Column('date', Date, unique=True)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    adj_close = Column('adj_close', Float)
    volume = Column('volume', Integer)
    dividends = Column('dividends', Float)
    stock_splits = Column('stock_splits', Float)
    is_dividends = Column('is_dividends', Integer)
    is_stock_splits = Column('is_stock_splits', Integer)
    jobless_claim_actual = Column('jobless_claim_actual', Float)
    jobless_claim_forecast = Column('jobless_claim_forecast', Float)
    jobless_claim_previous = Column('jobless_claim_previous', Float)
    jobless_claim_beat_forecast = Column('jobless_claim_beat_forecast', Integer)
    jobless_claim_beat_previous = Column('jobless_claim_beat_previous', Integer)
    jobless_claim_silver_id = Column('jobless_claim_silver_id', Integer,
                                     ForeignKey("jobless_claim_silver.id", ondelete="SET NULL"),
                                     unique=True)
    is_jobless_claim_release_date = Column('is_jobless_claim_release_date', Integer)
    jobless_claim_next_release_date = Column('jobless_claim_next_release_date', Date)
    jobless_claim_day_to_next_release = Column('jobless_claim_day_to_next_release', Integer)
    cpi_actual = Column('cpi_actual', Float)
    cpi_forecast = Column('cpi_forecast', Float)
    cpi_previous = Column('cpi_previous', Float)
    cpi_beat_forecast = Column('cpi_beat_forecast', Integer)
    cpi_beat_previous = Column('cpi_beat_previous', Integer)
    cpi_silver_id = Column('cpi_silver_id', Integer,
                           ForeignKey("cpi_silver.id", ondelete="SET NULL"),
                           unique=True)
    is_cpi_release_date = Column('is_cpi_release_date', Integer)
    cpi_next_release_date = Column('cpi_next_release_date', Date)
    cpi_day_to_next_release = Column('cpi_day_to_next_release', Integer)
    unemploy_actual = Column('unemploy_actual', Float)
    unemploy_forecast = Column('unemploy_forecast', Float)
    unemploy_previous = Column('unemploy_previous', Float)
    unemploy_beat_forecast = Column('unemploy_beat_forecast', Integer)
    unemploy_beat_previous = Column('unemploy_beat_previous', Integer)
    unemploy_silver_id = Column('unemploy_silver_id', Integer,
                                ForeignKey("unemploy_silver.id", ondelete="SET NULL"),
                                unique=True)
    is_unemploy_release_date = Column('is_unemploy_release_date', Integer)
    unemploy_next_release_date = Column('unemploy_next_release_date', Date)
    unemploy_day_to_next_release = Column('unemploy_day_to_next_release', Integer)
    is_release_date = Column('is_release_date', Integer)
    sma_7_diff = Column('sma_7_diff', Float)
    sma_20_diff = Column('sma_20_diff', Float)
    sma_50_diff = Column('sma_50_diff', Float)
    sma_100_diff = Column('sma_100_diff', Float)
    sma_200_diff = Column('sma_200_diff', Float)
    sma_500_diff = Column('sma_500_diff', Float)
    change_after_1_day = Column('change_after_1_day', Float)
    change_after_7_day = Column('change_after_7_day', Float)
    change_after_30_day = Column('change_after_30_day', Float)
    change_after_90_day = Column('change_after_90_day', Float)


if __name__ == '__main__':
    init_db()
