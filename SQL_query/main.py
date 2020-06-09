from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from SQL_query_incorrect_price import query_with_fetchmany

result = query_with_fetchmany()
print(result)
