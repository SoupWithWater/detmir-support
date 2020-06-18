import urllib.request

def get_brand_list():
    solr_request = urllib.request.urlopen('http://cubic01:8983/solr/detmir-brands/select?fl=id,%20name&q=*:*&rows=4000&wt=csv')
    solr_request = (solr_request.read()).decode('utf-8')
    solr_request = solr_request.split('\n')

    brand_list = []
    for brand in solr_request:
        brand = brand.split(',')
        brand_list.append(brand)

    return brand_list

if __name__ == '__main__':
    get_brand_list()