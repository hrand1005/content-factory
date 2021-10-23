def get_db():
    db

def insert_clips(db_conn, table, clip_urls):
    stmt = insert(table).values(clip_urls).prefix_with('OR IGNORE')
    db_conn.execute(stmt)

# def verifiedUnique(db_conn, table, clip_urls):

#     verified_unique_urls = []
#     for url in clip_urls:
#         stmt = select.where(table.c.url == url)
#         if not db_conn.query(db_conn.exists().where(table.c.url == url)).scalar():
#             verified_unique_urls.add(url)
    
#     return verified_unique_urls