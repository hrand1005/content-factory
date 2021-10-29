import os
import sys
import requests
import urllib.request
from db.db import ClipDatabase

def insert_clips(strategy, clip_urls):
    db = ClipDatabase(strategy)
    db.insert_clips(clip_urls)

def verified_unique(strategy, clip_urls):
    db = ClipDatabase(strategy)
    return db.verify_clips(clip_urls)