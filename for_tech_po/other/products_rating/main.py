import urllib.request
import json
from parsing_data import parsing
from create_category_dict import get_category_list
from create_brand_list import get_brand_list

# выгрузка товаров с рейтингом < 3, на выходе получаем список товаров (products_list)
webUrl = urllib.request.urlopen('http://cubic-solr-01:8983/solr/detmir-products/select?fl=product_code&q=product_rating:%20[1%20TO%203]&rows=5000&wt=python')
products_list = (webUrl.read()).decode('utf-8')
products_list = products_list[(products_list.find(':[')) + 9:(products_list.find('  }}') - 2)].replace("        'product_code':'", "").replace("      {", "").replace("'}", '').replace("\n", '').replace("{", '')
products_list = products_list.split(',')

category_list = get_category_list()
brand_list = get_brand_list()

#запускается цикл: к каждому товару подтягиваются необходимые данные
for product in products_list:
    solr_request = urllib.request.urlopen(f'http://cubic-solr-01:8983/solr/detmir-products/select?fl=product_all_categories,product_rating,product_code,product_article,product_name_ru,product_category_primary,product_review_count,product_brand&q=product_code:{product}')
    product_response = parsing(solr_request)
    print(product_response['product_code'], ';', product_response['product_name_ru'], ';', end='')

    main_category = ''
    level_two_category = ''
    for category in product_response["product_all_categories"]:

        for category_data in category_list:
            if str(category_data[0]) == str(category):
                if (str(category_data[1]) == '2') & (str(level_two_category) == ''):
                    level_two_category = category_data[2]

                if str(category_data[0]) == str(product_response['product_category_primary']):
                    main_category = category_data[2]
            if (main_category != '') & (level_two_category != ''):
                break


    print(main_category, ';', level_two_category, ';', end='')

    brand = ''
    for brands in brand_list:
        if str(brands[0]) == str(product_response['product_brand']):
            brand = brands[1]

    print(product_response['product_article'], ';', brand, ';', round(product_response['product_rating'], 1), ';', product_response['product_review_count'])



