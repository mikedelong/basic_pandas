import logging

import pandas as pd

# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logging_level = logging.INFO
logger.setLevel(logging_level)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging_level)
logger.debug('started')

input_folder = './input/'
input_file = 'gridExport_20180109T1540Z.xlsx'

full_input_file = input_folder + input_file
logger.info('full input file name: %s' % full_input_file)
df = pd.read_excel(full_input_file, sheetname=0, skiprows=[0, 1, 2, 3, 4])
# https://stackoverflow.com/questions/28538536/deleting-multiple-columns-based-on-column-names-in-pandas
df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
logger.info(df.head(26))
