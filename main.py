from SQL_query.SQL_query_incorrect_price import query_with_fetchmany
import urllib.request

def incorrect_price_alarm():
    #load products with sale > 90%
    sql_result = query_with_fetchmany()
    print('Товары со скидкой более 90% выгружены из базы')
    alert_products = []

    for key in sql_result:
        product_id = str(sql_result.get(key))
        #print(f'Поиск офлайн стоков по товару {product_id} в сервисах')

        solr_response_http = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-delivery/select?fl=offline_stock&q=product_id:{product_id}&rows=200&wt=python')
        solr_response = (solr_response_http.read()).decode('utf-8')
        stock_str = solr_response[(solr_response.find('[')) + 2:-7]
        stock_str = stock_str.replace('\n', '').replace(' ', '').replace("'", "").replace('{', '').replace('}', '')
        offline_stock = stock_str.split(',')

        for stock in offline_stock:
            if stock != 'offline_stock:NoStock':
                if (alert_products.count(key)) < 1:
                    alert_products.append(key)
                    print(f'У товара {product_id} найдены offline стоки')

        solr_response_http = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-delivery/select?fl=online_stock&q=product_id:{product_id}&rows=200&wt=python')
        solr_response = (solr_response_http.read()).decode('utf-8')
        stock_str = solr_response[(solr_response.find('[')) + 2:-7]
        stock_str = stock_str.replace('\n', '').replace(' ', '').replace("'", "").replace('{', '').replace('}', '')
        online_stock = stock_str.split(',')

        for stock in online_stock:
            if stock != 'online_stock:NoStock':
                if (alert_products.count(key)) < 1:
                    alert_products.append(key)
                    print(f'У товара {product_id} найдены online стоки')




if __name__ == '__main__':
    incorrect_price_alarm()

