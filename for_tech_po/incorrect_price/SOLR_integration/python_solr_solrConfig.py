from configparser import ConfigParser


def read_solr_config(filename='config.ini', section='solr'):

    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to solr
    solr = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            solr[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return solr