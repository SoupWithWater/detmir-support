import urllib.request
solr_response_http = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-delivery/select?fl=offline_stock&q=product_id:650&rows=200&wt=python')
solr_response = (solr_response_http.read()).decode('utf-8')
stock_str = solr_response[(solr_response.find('['))+2:-7]
stock_str = stock_str.replace('\n', '').replace(' ', '').replace("'", "").replace('{', '').replace('}', '')
stock = stock_str.split (',')
print(stock)
