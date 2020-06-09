import mysql.connector
from mysql.connector import Error

def connect():
    """ Connect to hbs-mysql02-prod database """
    try:
        conn = mysql.connector.connect(host='hbs-mysql02-prod',
                                       database='hybrisdb',
                                       user='iborodin',
                                       password='ojaugohm4Uquie2kaela')
        if conn.is_connected():
            print('Connected to hbs-mysql02-prod DB')

    except Error as e:
        print(e)

    finally:
        conn.close()

if __name__ == '__main__':
    connect()