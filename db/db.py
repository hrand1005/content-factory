import os
import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

class ClipDatabase():
    def __init__(self, name):    
        self.engine = create_engine(f"sqlite:///db/{name}.db")
        self.metadata_obj = MetaData()

        self.table = Table('clips', self.metadata_obj,
            Column('id', Integer, primary_key=True),
            Column('url', String(100), nullable=False, unique=True),
            Column('time_entered', DateTime, default=datetime.datetime.now)
        )

        self.metadata_obj.create_all(engine)
        Session = sessionmaker(bind = engine)
        self.session = Session()
    
    def get_conn(self):
        return self.engine.connect()