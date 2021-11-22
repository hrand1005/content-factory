# Defines database to manage downloaded content. The big idea is to prevent
# duplicate downloads.

import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

#TODO: make this slightly more generic, content instead of content
class ContentDatabase():
    def __init__(self, name):    
        self.engine = create_engine(f"sqlite:///db/{name}.db")
        self.metadata_obj = MetaData()
        self.table = Table("content", self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("url", String(100), nullable=False, unique=True),
            Column("time_entered", DateTime, default=datetime.datetime.now())
        )
        self.metadata_obj.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
        self.db_conn = self.engine.connect()

    def insert_content(self, content_dict):
        for content in content_dict:
            content_url = content["url"]
            stmt = insert(self.table).values(url=content_url).prefix_with("OR IGNORE")
            self.db_conn.execute(stmt)
        self.session.commit()

    def verify_content(self, content_dict):
        verified_content = []
        for content in content_dict:
            content_url = content["url"]
            if not self.session.query(exists().where(self.table.c.url == content_url)).scalar():
                verified_content.append(content)
        return verified_content
