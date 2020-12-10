from sql_query.mysql_dbconfig import read_db_config
from sql_query.list_to_string import list_to_string
from sql_query.iter_row import iter_row

def sql_instore_refund(date_refund, cursor):
        need_refund_all_1 = []
        need_refund_all_2 = []
        refund_follow_on_accepted_1 = []
        refund_follow_on_accepted_2 = []

        #выгрузка заказов

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
                AND o.createdTS > (CURDATE() - INTERVAL 20 DAY)\
                AND p.code='card'\
                AND d.code='instore'\
                AND ((oh.p_description like '%Перемещён в розницу%') or (oh.p_description like '%Готов к выдаче частично%'))\
                AND date(oh.createdTS)>= '{date_refund}'\
                AND pte.p_transactionstatus='CREATE_SUBSCRIPTION_ACCEPTED'\
                AND elp.p_name in ('Реализация')")

        for row in iter_row(cursor, 10):
            need_refund_all_1.extend(list(row))

        orders = list_to_string(need_refund_all_1)

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
                 AND oh.p_description like '%ВОЗВРАТ%'\
                 AND pte.p_transactionstatus='REFUND_FOLLOW_ON_ACCEPTED'\
                AND o.code IN ({orders})")

            for row in iter_row(cursor, 10):
                refund_follow_on_accepted_1.extend(list(row))

        cursor.execute(f"SELECT DISTINCT o.code\
                from orders AS o\
                JOIN enumerationvalueslp AS elp\
                ON elp.ITEMPK=o.statuspk\
                JOIN deliverymodes AS d\
                  ON o.deliverymodepk=d.PK\
                  JOIN orderentries AS oe\
                    ON oe.p_order=o.pk\
                  JOIN consignmententries AS ce\
                    ON oe.pk=ce.p_orderentry\
                  JOIN consignments AS c\
                    ON o.pk=c.p_order\
                 JOIN products AS pr\
                    ON oe.productpk = pr.PK\
                JOIN paymentmodes AS p\
                ON p.pk=o.paymentmodepk\
                  JOIN orderhistoryentries AS oh\
                  ON oh.p_order=o.pk\
                JOIN paymenttransactions AS pt\
                ON pt.p_order=o.PK\
                JOIN paymnttrnsctentries AS pte\
                ON pte.p_paymenttransaction=pt.PK\
                AND o.createdTS > (CURDATE() - INTERVAL 20 DAY)\
                AND o.modifiedTS < CURDATE() - INTERVAL 40 MINUTE\
                AND p.code='card'\
                AND d.code='instore'\
                AND oh.p_description like '%Реализация%'\
                  AND (ce.p_quantity > ce.p_collected)\
                   AND date(oh.createdTS)>= '{date_refund}'\
            AND pte.p_transactionstatus='CREATE_SUBSCRIPTION_ACCEPTED'")

        for row in iter_row(cursor, 10):
            need_refund_all_2.extend(list(row))

        orders = list_to_string(need_refund_all_2)
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
                 AND oh.p_description like '%ВОЗВРАТ%'\
                 AND pte.p_transactionstatus='REFUND_FOLLOW_ON_ACCEPTED'\
                AND o.code IN ({orders})")

            for row in iter_row(cursor, 10):
                refund_follow_on_accepted_2.extend(list(row))


        need_refund = need_refund_all_1 + need_refund_all_2
        refund_follow_on_accepted = refund_follow_on_accepted_1 + refund_follow_on_accepted_2
        need_refund = list(set(need_refund))
        refund_follow_on_accepted = list(set(refund_follow_on_accepted))

        """print(type(need_refund))
        print(need_refund)
        print(type(refund_follow_on_accepted))
        print(refund_follow_on_accepted)"""

        for order in refund_follow_on_accepted:
            need_refund.remove(order)

        return need_refund

if __name__ == '__main__':
    sql_instore_refund()