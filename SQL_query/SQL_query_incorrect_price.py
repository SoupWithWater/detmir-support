from mysql.connector import MySQLConnection, Error
from SQL_query.python_mysql_dbconfig import read_db_config

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row
if __name__ == '__main__':
    iter_row()

def query_with_fetchmany():
    try:
        print('Connecting to hbs-mysql02-prod [...', end='')
        dbconfig = read_db_config()
        print('...', end='')
        conn = MySQLConnection(**dbconfig)
        print('...', end='')
        result = dict()
        print('...', end='')
        cursor = conn.cursor()
        print('........]')
        if conn.is_connected():
            print('Connection established.')
        else:
            print('connection failed.')

        print('Выгружаю товары')

        cursor.execute("SELECT DISTINCT p.code, \
                                p.codeforurl \
                            FROM products as p\
                                LEFT JOIN (SELECT * FROM pricerows WHERE DATE(pricerows.p_starttime) <= CURDATE() AND DATE(pricerows.p_endtime) >= CURDATE() AND p_detmirpricerowtype = '8796117008475') AS pr_cross ON p.code = pr_cross.p_productid \
                                LEFT JOIN (SELECT * FROM pricerows WHERE DATE(pricerows.p_starttime) <= CURDATE() AND DATE(pricerows.p_endtime) >= CURDATE() AND p_detmirpricerowtype = '8796116975707') AS pr_sale ON p.code = pr_sale.p_productid \
                            WHERE ROUND(100 - (pr_sale.p_price / (pr_cross.p_price / 100)), 0) >= 90 \
                                AND p.p_approvalstatus = '8796099805275'")

        for row in iter_row(cursor, 10):
            #print(row)
            product = row[0]
            sale = row[1]
            result.update({product:sale})

        #print (result)

    except Error as e:
        print(e)

    #finally:
     #   if cursor():
      #      cursor.close()
       # if conn():
        #    conn.close()

    return result
if __name__ == '__main__':
    query_with_fetchmany()