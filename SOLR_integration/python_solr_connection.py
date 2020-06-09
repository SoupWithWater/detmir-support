import urllib.request


def connect():
    """ Connect to cubic01 """
    try:
        webUrl = urllib.request.urlopen('http://cubic01:8983/solr/#/detmir-stocks/query')
        print('code: ' + str(webUrl.getcode()))

        if webUrl.getcode() == 200:
            print('connection established.')
        else:
            print('connection failed: code ' + str(webUrl.getcode()))

    except Error as error:
        print(error)

    finally:
        urllib.request.urlcleanup()

    print(webUrl)

if __name__ == '__main__':
    connect()
