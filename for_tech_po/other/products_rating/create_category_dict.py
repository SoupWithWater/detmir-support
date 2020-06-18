import json
import urllib.request


solr_request = urllib.request.urlopen('http://cubic01:8983/solr/detmir-categories/select?fl=category_id,category_level,category_name&q=*:*')