import time
from utils.config import config

db = config['db']

def default_timestamp():
    return int(time.time() * 1000)

class Link(db.Model):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.BIGINT, default=default_timestamp)
    long_url = db.Column(db.String(1000), index=True, nullable=False)
    short_code = db.Column(db.String(6), unique=True, index=True, nullable=False)
