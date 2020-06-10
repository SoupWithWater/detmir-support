from mysql.connector import MySQLConnection, Error
from sql_query.mysql_dbconfig import read_db_config
from sql_query.list_to_string import list_to_string

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row
if __name__ == '__main__':
    iter_row()

def sql_courier_refund(date_refund):
    try:
        print('Connecting to hbs-mysql02-prod [...', end='')
        dbconfig = read_db_config()
        print('...', end='')
        conn = MySQLConnection(**dbconfig)
        print('...', end='')
        need_refund = []
        print('...', end='')
        cursor = conn.cursor()
        print('........]')
        if conn.is_connected():
            print('Connection established.')
        else:
            print('connection failed.')

        print('Выгружаю заказы по которым требуется возврат...')
        cursor.execute(f"SELECT DISTINCT o.code \
                            FROM orders AS o \
                                JOIN enumerationvalueslp AS elp\
                                    ON elp.ITEMPK=o.statuspk\
                                JOIN deliverymodes AS d\
                                    ON o.deliverymodepk=d.PK\
                                JOIN ordersubstatuslp AS oelp\
                                    ON oelp.ITEMPK=o.p_ordersubstatus\
                                JOIN paymentmodes AS p\
                                    ON p.pk=o.paymentmodepk\
                                JOIN orderhistoryentries AS oh\
                                    ON oh.p_order=o.pk\
                                JOIN paymenttransactions AS pt\
                                    ON pt.p_order=o.PK\
                                JOIN paymnttrnsctentries AS pte\
                                    ON pte.p_paymenttransaction=pt.PK\
                            WHERE elp.LANGPK=8796093349920 \
                                AND oelp.LANGPK=8796093349920\
                                AND oelp.p_name='частичная комплектация'\
                                AND o.createdTS>'20200520'\
                                AND p.code='card'\
                                and d.code='logist' AND oh.p_description like '%%новый статус=Отгружен%%'\
                                AND  date (oh.createdts) = '{date_refund}'\
                                AND pte.p_transactionstatus ='CREATE_SUBSCRIPTION_ACCEPTED'")

        need_refund_all = []

        for row in iter_row(cursor, 10):
            need_refund_all.extend(list(row))


        orders = list_to_string(need_refund_all)

        print('Выгружаю заказы, по которым возврат произведен')
        cursor.execute(f"SELECT DISTINCT o.code \
                                    FROM orders AS o \
                                        JOIN enumerationvalueslp AS elp\
                                            ON elp.ITEMPK=o.statuspk\
                                        JOIN deliverymodes AS d\
                                            ON o.deliverymodepk=d.PK\
                                        JOIN ordersubstatuslp AS oelp\
                                            ON oelp.ITEMPK=o.p_ordersubstatus\
                                        JOIN paymentmodes AS p\
                                            ON p.pk=o.paymentmodepk\
                                        JOIN orderhistoryentries AS oh\
                                            ON oh.p_order=o.pk\
                                        JOIN paymenttransactions AS pt\
                                            ON pt.p_order=o.PK\
                                        JOIN paymnttrnsctentries AS pte\
                                            ON pte.p_paymenttransaction=pt.PK\
                                    WHERE elp.LANGPK=8796093349920 \
                                        AND oelp.LANGPK=8796093349920\
                                        AND oelp.p_name='частичная комплектация'\
                                        AND o.createdTS>'20200520'\
                                        AND p.code='card'\
                                        AND pte.p_transactionstatus='REFUND_FOLLOW_ON_ACCEPTED'\
                                        and o.code IN ({orders})")

        refund_follow_on_accepted = []

        for row in iter_row(cursor, 10):
            refund_follow_on_accepted.extend(list(row))

        need_refund = need_refund_all

        for order in refund_follow_on_accepted:
            need_refund.remove(order)

        print("Заказы, по которым требуется ручной возврат:")
        for order in need_refund:
            print(order.decode('utf-8'))

    except Error as e:
        print(e)

    return need_refund
if __name__ == '__main__':
    sql_courier_refund()