import logging
import os

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

# todo: what if this folder does not exist?
input_folder = './input/'
input_file_list = os.listdir(input_folder)
input_file_list = [item for item in input_file_list if item.endswith('.xlsx')]

for input_file in input_file_list:
    full_input_file = input_folder + input_file
    logger.info('full input file name: %s' % full_input_file)
    df = pd.read_excel(full_input_file, sheetname=0, skiprows=[0, 1, 2, 3, 4])

    # https://stackoverflow.com/questions/28538536/deleting-multiple-columns-based-on-column-names-in-pandas
    df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
    logger.info('head after dropping unnamed columns:')
    logger.info(df.head(26))

    # convert the Date column, if it exists, to a date
    # https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas
    # https://stackoverflow.com/questions/39604094/pandas-delete-all-rows-that-are-not-a-datetime-type
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        logger.info('head after converting dates:')
        logger.info(df.head(26))

    # now do the group-by
    # https://pandas.pydata.org/pandas-docs/stable/groupby.html
    if 'Date' in df.columns:
        df = df.groupby(['Date']).sum()
        logger.info('head group by dates:')
        logger.info(df.head(26))

    # rename the remaining columns to their short names
    # https://stackoverflow.com/questions/33543337/replace-string-in-pandas-df-column-name
    df = df.rename(columns={column: column.split(' ')[0] for column in df.columns})
    logger.info(df.columns)

    # write the result to CSV
    # todo: what if this folder does not exist?
    output_folder = './output/'
    output_file = input_file.replace('.xlsx', '.csv')
    logger.info('short output file name: %s' % output_file)
    full_output_file = output_folder + output_file
    logger.info('writing result to %s' % full_output_file)
    df.to_csv(full_output_file)

    # before we go let's scale by the total for each month and write that to a separate file
    # todo: add a list of columns to exclude from the sum
    df['Sum'] = df.sum(axis=1)
    for column in df.columns:
        df[column] = df[column] / df['Sum']
    df = df.drop(['Sum'], axis=1)

    output_file = input_file.replace('.xlsx', '-scaled.csv')
    logger.info('short output file name: %s' % output_file)
    full_output_file = output_folder + output_file
    logger.info('writing result to %s' % full_output_file)
    df.to_csv(full_output_file)

logger.info('done.')
