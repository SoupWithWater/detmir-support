from mysql.connector import MySQLConnection, Error, cursor
from sql_query.courier_refund import sql_courier_refund
from sql_query.express_refund import sql_express_refund
from sql_query.logistpickup_refund import sql_logistpickup_refund
from sql_query.lastmile_refund import sql_lastmile_refund
from sql_query.storepickup_refund import sql_storepickup_refund
from sql_query.list_to_string import list_to_string
from sql_query.mysql_dbconfig import read_db_config
from sql_query.iter_row import iter_row




def refund():
    try:

        print('Connecting to hbs-mysql02-prod [...', end='')
        dbconfig = read_db_config()
        print('...', end='')
        conn = MySQLConnection(**dbconfig)
        print('...', end='')
        cursor = conn.cursor()
        print('........]')
        if conn.is_connected():
            print('Connection established.')
        else:
            print('connection failed.')

        print('Дата возврата в SQL формате: ', end='')
        date_refund = str(input())
        print('Выгружаю заказы \n')


        courier = sql_courier_refund(date_refund, cursor)
        print('[LOGIST]')
        if courier != []:
            for order in courier:
                print(str(order))
        else: print('_______')
        print()
        cursor = cursor.close()

        cursor = conn.cursor()
        express = sql_express_refund(date_refund, cursor)
        print('[EXPRESS]')
        if express != []:
            for order in express:
                print(str(order))
        else: print('_______')
        print()
        cursor = cursor.close()

        cursor = conn.cursor()
        logistpickup = sql_logistpickup_refund(date_refund, cursor)
        print('[STOREPICKUP]')
        if logistpickup != []:
            for order in logistpickup:
                print(str(order))
        else: print('_______')
        print()
        cursor = cursor.close()

        cursor = conn.cursor()
        lastmile = sql_lastmile_refund(date_refund, cursor)
        print('[LASTMILE]')
        if lastmile != []:
            for order in lastmile:
                print(str(order))
        else:
            print('_______')
        print()
        cursor = cursor.close()

        cursor = conn.cursor()
        logistpickup = sql_logistpickup_refund(date_refund, cursor)
        print('[LOGISTPICKUP]')
        if logistpickup != []:
            for order in logistpickup:
                print(str(order))
        else:
            print('_______')
        print()
        print('Выгружено')

    except Error as e:
        print(e)
if __name__ == '__main__':
    refund()