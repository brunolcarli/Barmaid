"""
Main common system settings
"""
from decouple import config


__version__ = '0.0.0'

ENV_REF = config('ENV_REF', 'development')
TOKEN = config('TOKEN')
MAIN_CHANNEL = config('MAIN_CHANNEL')

MYSQL_HOST = config('MYSQL_HOST', 'localhost')
MYSQL_USER = config('MYSQL_USER', 'mysql_user')
MYSQL_PASSWORD = config('MYSQL_PASSWORD', 'db_pwd')
MYSQL_DATABASE = config('MYSQL_DATABASE', 'db_name')
