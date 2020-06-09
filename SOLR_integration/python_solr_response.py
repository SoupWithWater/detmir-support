import urllib.request
from python_solr_solrConfig import read_solr_config

solr_config = read_solr_config()
webUrl = urllib.request.urlopen('http://cubic01:8983/solr/#/detmir-stocks/query')

requestS = urllib.request.urlopen('http://cubic01:8983/solr/detmir-stocks/select?q=product_code:%201000024611')
request1 = requestS.read()
print(request1)

