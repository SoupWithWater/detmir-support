from python_mysql_dbconfig import read_db_config
import mysql.connector
from mysql.connector import Error

dbconfig = read_db_config()
conn = mysql.connector.connect(**dbconfig)