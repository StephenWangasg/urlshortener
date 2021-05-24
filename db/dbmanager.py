from .link import Link
from utils.hash import HashDigest
from utils.config import config
from sqlalchemy import desc


class DBManager:

    def __init__(self):
        self.db = config['db']
        self.db.create_all()

    def next_short_code(self):
        link = Link.query.order_by(desc(Link.id)).first()

        if link is None:
            base_id = 100032531
            base_str = HashDigest().shorten(base_id)
        else:
            base_id = HashDigest().decode(link.short_code) + 1
            base_str = HashDigest().shorten(base_id)
            while self.find(short_code=base_str):
                base_id += 1
                base_str = HashDigest().shorten(base_id)
        return base_str

    def getall(self):
        return Link.query.all()
        
    def get(self, long_url):
        return Link.query.filter_by(long_url=long_url).first()

    def find(self, short_code):
        return Link.query.filter_by(short_code=short_code).first()
        
    def add(self, long_url):
        link = Link(long_url=long_url, short_code=self.next_short_code())
        try:
            self.db.session.add(link)
            self.db.session.commit()
            return link
        except Exception as e:
            self.db.session.rollback()
            raise e
