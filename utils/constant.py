
default_configs = {
    'database': {
        'engine': 'sqlite3',
        'sqlite3': {
            'path': 'data',
            'file': 'urlshortener.db'
        },
        'mysql': {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'port': 3306,
            'database': 'urlshortener',
        }
    }
}