

# event type
econ_data_type= ["jobless_claim","cpi","unemploy"]
econ_col_list=('release_date', 'actual', 'forecast', 'previous','revised','beat_forecast','beat_previous')
econ_silver_to_gold=('release_date', 'actual', 'forecast', 'previous','beat_forecast','beat_previous')
sma_period =(7,20,50,100,200,500)
stock_percentage_change=(1,7,30,90)

# list to define win_loss ([days to win , win percentage , loss percentage])
win_loss =([7,1.01,0.99],[30,1.05,0.96])

# Use Class to set up metadata of db and attributes
from model.db import \
    Jobless_claim_bronze,Jobless_claim_silver,\
    Cpi_bronze,Cpi_silver,\
    Unemploy_bronze,Unemploy_silver

class econ_datas():
    category = {}
econ_datas =econ_datas()

class econ_data():
    """"""
    def __init__(self,
                 name:str,
                 bronze_db=None,
                 silver_db=None,
                 event_id:str=None,
                 parent=None):
        """
        :param name: name of economics data
        :param bronze_db: SQLalchemy db object for bronze db
        :param silver_db: SQLalchemy db object for silver db
        :param event_id:  event id for web scarpping from investing.com
        :param parent: object class that store all econ_datas
        """
        self.name=name
        self.bronze_db=bronze_db
        self.event_id=event_id
        self.silver_db=silver_db
        self.parent=parent
        if parent != None:
            parent.category[name]=self

jobless_claim = econ_data(
    name='jobless_claim',
    bronze_db=Jobless_claim_bronze,
    silver_db=Jobless_claim_silver,
    event_id='294',
    parent=econ_datas
)
cpi=econ_data(
    name='cpi',
    bronze_db=Cpi_bronze,
    event_id='733',
    parent=econ_datas,
    silver_db=Cpi_silver
)
unemploy=econ_data(
    name='unemploy',
    bronze_db=Unemploy_bronze,
    event_id='300',
    parent=econ_datas,
    silver_db=Unemploy_silver
)
