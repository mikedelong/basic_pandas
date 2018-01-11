import json
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

# todo what if this folder does not exist?
input_folder = './input/'
input_file = 'gridExport_20180109T1540Z.xlsx'

full_input_file = input_folder + input_file
logger.info('full input file name: %s' % full_input_file)
df = pd.read_excel(full_input_file, sheetname=0, skiprows=[0, 1, 2, 3, 4])
# https://stackoverflow.com/questions/28538536/deleting-multiple-columns-based-on-column-names-in-pandas
df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
logger.info('head after dropping unnamed columns:')
logger.info(df.head(26))

# convert the Date column, if it exists, to a date
# https://stackoverflow.com/questions/39604094/pandas-delete-all-rows-that-are-not-a-datetime-type
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

logger.info('head after converting dates:')
logger.info(df.head(26))

# read the sorting instructions
# todo what if this file is missing
# todo what if this file is empty
sort_keys_file = './sort.json'
keys = []
ascending = []
with open(sort_keys_file, 'rb') as file_fp:
    settings = json.load(file_fp)
    logger.info(settings)
    for key, value in settings.items():
        keys.append(value['name'])
        ascending.append(value['ascending'])
logger.info(keys)
logger.info(ascending)

# sort the rows
df = df.sort_values(keys, ascending=ascending)

# write the result to CSV
# todo what if this folder does not exist?
output_folder = './output/'
output_file = input_file.replace('.xlsx', '.csv')
logger.info('short output file name: %s' % output_file)
full_output_file = output_folder + output_file
logger.info('writing result to %s' % full_output_file)
df.to_csv(full_output_file)
logger.info('done.')
