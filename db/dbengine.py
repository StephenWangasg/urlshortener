import os
from abc import ABCMeta, abstractmethod
from utils import config
from pathlib import Path 

class DBSQLEngine(metaclass=ABCMeta):
    
    @abstractmethod
    def dburl(self):
        pass
    
    @abstractmethod
    def dict(self):
        pass

    def __getattr__(self, name):
        return self.dict()[name]


class MySQLEngine(DBSQLEngine):

    def dict(self):
        return config.config['database']['mysql']

    def dburl(self):
        return 'mysql://{user}:{password}@{host}:{port}/{database}'.format(
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port,
                database = self.database,
            )


class Sqlite3Engine(DBSQLEngine):
    
    def dict(self):
        return config.config['database']['sqlite3']

    def dburl(self):
        self.sqlite3file = '{root}/{path}/{file}'.format(
                root = config.config['root'],
                path = self.path,
                file = self.file
        )
        Path(os.path.dirname(self.sqlite3file)).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.sqlite3file):
            with open(self.sqlite3file, 'a+') as _:
                pass

        return 'sqlite:///{}'.format(self.sqlite3file)

class DBSQLURL:

    def __init__(self):
        self.engine = {'sqlite3': Sqlite3Engine, 'mysql': MySQLEngine}.get(config.config['database']['engine'], Sqlite3Engine)()


    def get(self):
        return self.engine.dburl()
