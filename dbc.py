# dbcon.py holds functions that give a db connection

# functions:
# connection
# connection_string
# db_uri

import pyodbc
import configparser
import os
from pathlib import Path

# connection returns a database connection
def connection(target=None):
    if target == None:
        target = 'num_test'
    return pyodbc.connect(connection_string(target))

# connection_string returns a connection string
def connection_string(target='num_test') -> str:
    info = _getinfo(target)
    
    connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + '; encrypt=no;'

    return connection_string

# db_uri returns a database uri
def db_uri(target = 'num_test'):
    info = _getinfo(target)
    
    # for uri see https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    # ?driver= from https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
    uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
    return uri

# _getinfo gets database info from .ini files
def _getinfo(target):
    # we don't want the db.ini in the same directory as the code, so that it does't accidentaly end up in github. its location is stored in dbc.ini, along with the db driver of the client.
    ini = configparser.ConfigParser()
    base_name = os.path.dirname(__file__)
    ini.read(os.path.join(base_name, 'dbc.ini'))
    dbinipath = ini["db"]["ini"]

    # read db auth info from db.ini
    config = configparser.ConfigParser()
    config.read(Path(dbinipath))
    dbtype = config[target]['type']
    info = {
        'database': config[target]['database_name'],
        'username': config[target]['username'],
        'password': config[target]['password'],
        'server': config[target]['server'],
        'port': config[target]['port'],
        # read the driver from dbc.ini
        'driver': ini["driver"][dbtype]
    }
    # driver = '{SQL Server}' # for num-etl
    # driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1' # for ubuntu on wsl
    return info
