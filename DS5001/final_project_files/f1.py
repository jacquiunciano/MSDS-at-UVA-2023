import pandas as pd
import configparser

class Convert():
    '''
    Converts the collection from their source formats (F0) into a set of tables that conform to the Standard Text Analytic Data Model (F2).
    '''

    config = configparser.ConfigParser()
    config.read("../../../env.ini")
    data_home = config['DEFAULT']['data_home']
    output_dir = config['DEFAULT']['output_dir']