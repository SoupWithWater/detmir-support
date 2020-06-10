import urllib.request

def stocks_finder(**sql_result):
    alert_products = []
    work_notification = 0
    processing_count = 0
    for product_code in sql_result:

        work_notification += 1
        processing_count +=1
        if work_notification == 20:
            print('processing...')
            work_notification = 0

        product_id = str(sql_result.get(product_code))

        solr_response_http = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-delivery/select?fl=offline_stock&q=product_id:{product_id}&rows=200&wt=python')
        solr_response = (solr_response_http.read()).decode('utf-8')
        stock_str = solr_response[(solr_response.find('[')) + 2:-7]
        stock_str = stock_str.replace('\n', '').replace(' ', '').replace("'", "").replace('{', '').replace('}', '')
        offline_stock = stock_str.split(',')

        for stock in offline_stock:
            if stock != 'offline_stock:NoStock':
                if (alert_products.count(product_code)) < 1:
                    alert_products.append(product_code)
                    print(f'У товара {product_code} найдены offline стоки')
                    print(f'Всего обработано {processing_count} из {len(sql_result)}')

        solr_response_http = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-delivery/select?fl=online_stock&q=product_id:{product_id}&rows=200&wt=python')
        solr_response = (solr_response_http.read()).decode('utf-8')
        stock_str = solr_response[(solr_response.find('[')) + 2:-7]
        stock_str = stock_str.replace('\n', '').replace(' ', '').replace("'", "").replace('{', '').replace('}', '')
        online_stock = stock_str.split(',')

        for stock in online_stock:
            if stock != 'online_stock:NoStock':
                if (alert_products.count(product_code)) < 1:
                    alert_products.append(product_code)
                    print(f'У товара {product_code} найдены online стоки')
                    print(f'Всего обработано {processing_count} из {len(sql_result)}')


    return alert_products

if __name__ == '__main__':
    stocks_finder()