import urllib.request

def get_category_list():
    solr_request = urllib.request.urlopen('http://cubic-solr-01:8983/solr/detmir-categories/select?fl=category_id,%20category_level,%20category_name&q=*:*&rows=6000&wt=csv')
    solr_request = (solr_request.read()).decode('utf-8')
    solr_request = solr_request.split('\n')

    category_list = []
    for category in solr_request:
        category = category.split(',')
        category_list.append(category)

    return category_list