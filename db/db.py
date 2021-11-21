# Defines database to manage downloaded clips. The big idea is to prevent
# duplicate downloads.

import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

#TODO: make this slightly more generic, content instead of clips
class ClipDatabase():
    def __init__(self, name):    
        self.engine = create_engine(f"sqlite:///db/{name}.db")
        self.metadata_obj = MetaData()

        self.table = Table("clips", self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("url", String(100), nullable=False, unique=True),
            Column("time_entered", DateTime, default=datetime.datetime.now())
        )

        self.metadata_obj.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
        self.db_conn = self.engine.connect()

    def insert_clips(self, clips):
        for clip in clips:
            clip_url = clip["url"]
            stmt = insert(self.table).values(url=clip_url).prefix_with("OR IGNORE")
            self.db_conn.execute(stmt)
        
        self.session.commit()

    def verify_clips(self, clips):
        verified_clips = []
        for clip in clips:
            url = clip["url"]
            if not self.session.query(exists().where(self.table.c.url == url)).scalar():
                verified_clips.append(clip)
        
        return verified_clips
