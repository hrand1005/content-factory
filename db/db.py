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
            Column('time_entered', DateTime, default=datetime.datetime.now())
        )

        self.metadata_obj.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
        self.db_conn = self.engine.connect()

    def insert_clips(self, clips):
        for clip in clips:
            stmt = insert(self.table).values(url=clip).prefix_with('OR IGNORE')
            self.db_conn.execute(stmt)
        
        self.session.commit()

    def verify_clips(self, clips):
        verified_unique_urls = []
        for url in clips:
            # stmt = select.where(self.table.c.url == url)
            if not self.session.query(exists().where(self.table.c.url == url)).scalar():
                verified_unique_urls.append(url)
        
        return verified_unique_urls