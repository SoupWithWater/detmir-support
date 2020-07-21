from sql_query.mysql_dbconfig import read_db_config
from sql_query.list_to_string import list_to_string
from sql_query.iter_row import iter_row


def sql_instore_refund(date_refund, cursor):
    need_refund_all_1 = []
    need_refund_all_2 = []
    refund_follow_on_accepted_1 = []
    refund_follow_on_accepted_2 = []

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
                                WHERE o.createdTS > '20200701'\
                                AND p.code='card'\
                                AND d.code='instore'\
                                AND (oh.p_description like '%Готов к выдаче частично%')\
                                     AND date(oh.createdTS) = '{date_refund}'\
                                AND pte.p_transactionstatus='CREATE_SUBSCRIPTION_ACCEPTED'")

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
                        WHERE oh.p_description like '%ВОЗВРАТ%'\
                         AND pte.p_transactionstatus='REFUND_FOLLOW_ON_ACCEPTED'\
                        AND o.code IN ({orders})\
                        GROUP BY o.code ")

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
                                    WHERE o.createdTS > '20200701'\
                                    AND p.code='card'\
                                    AND d.code='instore'\
                                    AND oh.p_description like '%Реализация%'\
                                      AND (ce.p_quantity > ce.p_collected)\
                                       AND date(oh.createdTS) = '{date_refund}'\
                                AND pte.p_transactionstatus='CREATE_SUBSCRIPTION_ACCEPTED'\
                                #group by o.code")

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
                                        WHERE oh.p_description like '%ВОЗВРАТ%'\
                                         AND pte.p_transactionstatus='REFUND_FOLLOW_ON_ACCEPTED'\
                                        AND o.code IN ({orders})\
                                        GROUP BY o.code ")

            for row in iter_row(cursor, 10):
                refund_follow_on_accepted_2.extend(list(row))


        """print('need_refund_all_1')
        print(need_refund_all_1)
        print('refund_follow_on_accepted_1')
        print(refund_follow_on_accepted_1)
        print('need_refund_all_2')
        print(need_refund_all_2)
        print('refund_follow_on_accepted_2')
        print(refund_follow_on_accepted_2)"""


        for order in refund_follow_on_accepted_1:
            need_refund_all_1.remove(order)

        for order in refund_follow_on_accepted_2:
            need_refund_all_2.remove(order)

        need_refund = need_refund_all_1 + need_refund_all_2
        print(need_refund_all_1)
        print(need_refund_all_2)


        return need_refund

if __name__ == '__main__':
    sql_instore_refund()