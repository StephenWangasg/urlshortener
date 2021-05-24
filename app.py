#!/usr/bin/env python3

import argparse
import os
import sys
import time
import flask
import flask_sqlalchemy

#find root dir
root_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root_dir)

from utils import config
from db.dbengine import DBSQLURL
app = flask.Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
   return flask.render_template('404.html', title = '404'), 404

@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s/1000) # datetime.datetime.fromtimestamp(s)

def main():
    parser = argparse.ArgumentParser(description="An URL Shortener Service")
    parser.add_argument("-p", "--param", help="parameter configuration file")
    args = parser.parse_args()
    config.config = config.Config(args.param).config_dict

    #append root_dir
    config.config['root'] = root_dir


    app.config['SQLALCHEMY_DATABASE_URI'] = DBSQLURL().get()
    config.config['db'] = flask_sqlalchemy.SQLAlchemy(app)

    import pprint
    pprint.pprint(config.config)

    import url
    app.register_blueprint(url.bp)
    app.run()


if __name__ == '__main__':
    main()
