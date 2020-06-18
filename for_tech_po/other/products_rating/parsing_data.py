import json

def parsing(webUrl):

    json_dict = (webUrl.read()).decode('utf-8')
    num_found = int(json_dict[json_dict.find('"numFound":') + 11])

    if num_found > 1:
        json_dict = ''
    else:
        json_dict = json_dict[(json_dict.find(':[')) + 9:(json_dict.find('  }}') - 2)]

    if json_dict != '':
        json_dict = json.loads(json_dict)

    return json_dict

if __name__ == '__main__':
    parsing()