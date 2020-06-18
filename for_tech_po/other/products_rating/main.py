import urllib.request
import json
from parsing_data import parsing

# выгрузка товаров с рейтингом < 3, на выходе получаем список товаров (products_list)
webUrl = urllib.request.urlopen('http://cubic01:8983/solr/detmir-products/select?fl=product_code&q=product_rating:%20[1%20TO%203]&rows=5000&wt=python')
products_list = (webUrl.read()).decode('utf-8')
products_list = products_list[(products_list.find(':[')) + 9:(products_list.find('  }}') - 2)].replace("        'product_code':'", "").replace("      {", "").replace("'}", '').replace("\n", '').replace("{", '')
products_list = products_list.split(',')

#запускается цикл: к каждому товару подтягиваются необходимые данные
for product in products_list:
    solr_request = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-products/select?fl=product_all_categories,product_rating,product_code,product_article,product_name_ru,product_category_primary,product_review_count,product_brand&q=product_code:{product}')
    product_response = parsing(solr_request)
    print(product_response['product_code'], ',', product_response['product_name_ru'], ',', end='')

    main_category = ''
    level_two_category = ''
    for category in product_response["product_all_categories"]:
        category_data = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-categories/select?fl=category_name_txt_ru,category_level&q=category_id:{product}')
        category_data = parsing(category_data)

        if category_data != '':
            if category == product_response['product_category_primary']:
                main_category = category_data['category_name_txt_ru']

            if (str(category_data['category_level']) == '2') & (level_two_category == ''):
                    level_two_category = category_data['category_name_txt_ru']

    print(main_category, ',', level_two_category, ',', end='')

    brand_data = urllib.request.urlopen(f'http://cubic01:8983/solr/detmir-brands/select?fl=name&q=id:{product_response["product_brand"]}')
    brand_data = parsing(brand_data)
    if brand_data != '':
        brand = brand_data["name"]
    else: brand = '0'

    print(product_response['product_article'], ',', brand, ',', round(product_response['product_rating'], 1))



