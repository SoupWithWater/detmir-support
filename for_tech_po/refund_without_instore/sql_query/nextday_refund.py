from sql_query.mysql_dbconfig import read_db_config
from sql_query.list_to_string import list_to_string
from sql_query.iter_row import iter_row

def sql_nextday_refund(date_refund, cursor):
        need_refund_all = []
        refund_follow_on_accepted = []


        cursor.execute(f"")

        for row in iter_row(cursor, 10):
            need_refund_all.extend(list(row))


        orders = list_to_string(need_refund_all)

        cursor.execute(f"")


        for row in iter_row(cursor, 10):
            refund_follow_on_accepted.extend(list(row))

        need_refund = need_refund_all

        for order in refund_follow_on_accepted:
            need_refund.remove(order)

        return need_refund

if __name__ == '__main__':
    sql_nextday_refund()