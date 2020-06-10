from SQL_query.SQL_query_incorrect_price import query_with_fetchmany
from stocks_finder import stocks_finder

def incorrect_price_alarm():

    sql_result = query_with_fetchmany()
    print(f'Товары со скидкой более 90% выгружены из базы, всего {len(sql_result)}')

    print('Проверяю наличие в cubic01')
    alert_products = stocks_finder(**sql_result)

    print('Проверить корректность цены следующих товаров:')
    print(alert_products)

if __name__ == '__main__':
    incorrect_price_alarm()

