from mysql.connector import MySQLConnection, Error
from DB_connection.python_mysql_dbconfig import read_db_config

def query_with_fetchone_incorrect_price():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT p.code as 'Код товара', \
                    pr_cross.p_price as 'cross цена', \
                    pr_sale.p_price as 'sale цена', \
                    ROUND(100 - (pr_sale.p_price / (pr_cross.p_price / 100)), 0) as 'скидка' \
                FROM products as p \
                    LEFT JOIN (SELECT * FROM pricerows WHERE DATE(pricerows.p_starttime) <= CURDATE() AND DATE(pricerows.p_endtime) >= CURDATE() AND p_detmirpricerowtype = '8796117008475') AS pr_cross ON p.code = pr_cross.p_productid \
                    LEFT JOIN (SELECT * FROM pricerows WHERE DATE(pricerows.p_starttime) <= CURDATE() AND DATE(pricerows.p_endtime) >= CURDATE() AND p_detmirpricerowtype = '8796116975707') AS pr_sale ON p.code = pr_sale.p_productid \
                WHERE ROUND(100 - (pr_sale.p_price / (pr_cross.p_price / 100)), 0) >= 90 \
                    AND p.p_approvalstatus = '8796099805275'")

        row = cursor.fetchone()
        print(cursor)

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    #finally:
     #   cursor.close()
     #   conn.close()

if __name__ == '__main__':
    query_with_fetchone_incorrect_price()