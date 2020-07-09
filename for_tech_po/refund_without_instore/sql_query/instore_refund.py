from sql_query.mysql_dbconfig import read_db_config
from sql_query.list_to_string import list_to_string
from sql_query.iter_row import iter_row

def sql_instore_refund(date_refund, cursor):
        need_refund_all = []
        refund_follow_on_accepted = []

        #выгрузка заказов

       

        #print('1)need_refund_all')
        #print(need_refund_all)

        cursor.execute(f"SELECT DISTINCT o.code\
                            from orders AS o\
                            JOIN enumerationvalueslp AS elp\
                            ON elp.ITEMPK=o.statuspk\
                            JOIN deliverymodes AS d\
                              ON o.deliverymodepk=d.PK\
                            JOIN paymentmodes AS p\
                            ON p.pk=o.paymentmodepk\
                              JOIN orderhistoryentries AS oh\
                              ON oh.p_order=o.pk\
                            JOIN paymenttransactions AS pt\
                            ON pt.p_order=o.PK\
                            JOIN paymnttrnsctentries AS pte\
                            ON pte.p_paymenttransaction=pt.PK\
                            WHERE o.createdTS > '20200610'\
                            AND p.code='card'\
                            AND d.code='instore'\
                            AND ((oh.p_description like '%Перемещён в розницу%') or (oh.p_description like '%Готов к выдаче частично%'))\
                                 AND date(oh.createdTS)>= '{date_refund}'\
                            AND pte.p_transactionstatus='CREATE_SUBSCRIPTION_ACCEPTED'\
                            AND elp.p_name = ('Реализация') ")

        for row in iter_row(cursor, 10):
            need_refund_all.extend(list(row))

        #print('2)need_refund_all')
        #print(need_refund_all)

        #проверка

        orders = list_to_string(need_refund_all)

        if orders != '':
            cursor.execute(f"SELECT o.code\
                                from orders AS o\
                                JOIN enumerationvalueslp AS elp\
                                ON elp.ITEMPK=o.statuspk\
                                JOIN deliverymodes AS d\
                                  ON o.deliverymodepk=d.PK\
                                JOIN paymentmodes AS p\
                                ON p.pk=o.paymentmodepk\
                                  JOIN orderhistoryentries AS oh\
                                  ON oh.p_order=o.pk\
                                JOIN paymenttransactions AS pt\
                                ON pt.p_order=o.PK\
                                JOIN paymnttrnsctentries AS pte\
                                ON pte.p_paymenttransaction=pt.PK\
                                WHERE oh.p_description like '%[ВОЗВРАТ] Возврат выполнен.%'\
                                AND o.code IN ({orders})\
                                group by o.code")


        for row in iter_row(cursor, 10):
            refund_follow_on_accepted.extend(list(row))

        #print('refund_follow_on_accepted')
        #print(refund_follow_on_accepted)

        need_refund = need_refund_all

        for order in refund_follow_on_accepted:
            need_refund.remove(order)

        #print('need_refund')
        #print(need_refund)

        return need_refund

if __name__ == '__main__':
    sql_instore_refund()