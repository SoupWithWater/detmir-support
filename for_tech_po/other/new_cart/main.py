from mysql.connector import MySQLConnection, Error, cursor
from mysql_dbconfig import read_db_config
from iter_row import iter_row

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

    orders = open('order_list')
    orders = orders.read()
    phones = []

    cursor.execute(f"SELECT distinct\
                    a.p_phone1\
                    FROM orders as o\
                    LEFT JOIN addresses as a ON a.PK = o.deliveryaddresspk\
                    WHERE o.code IN ({orders})")

    for row in iter_row(cursor, 10):
        phones.extend(list(row))

    print(phones)

    phones_pars = str()
    for phone in phones:
        phones_pars += ("'" + phone + "',")
       
    print(phones_pars)

    cursor.execute(f'SELECT distinct  o.code, o.createdTS \
                FROM orders as o\
                left join addresses as a on a.PK = o.deliveryaddresspk\
                WHERE a.p_phone1 IN ({phones_pars[0:-1]})')

    all_orders = []

    for row in iter_row(cursor, 10):
        phones.extend(list(row))

    print(all_orders)

except Error as e:
    print(e)