
import logging
import argparse
import json
import sys
import pandas as pd
from datetime import datetime

from influxdb import InfluxDBClient
from influxdb import DataFrameClient


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
if __name__ == "__main__":

    #load config file
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', help='configuration file')
    arg_parser.add_argument('-l', help='log file')

    args = arg_parser.parse_args()
    config = json.loads(open(args.c).read())

    # --------------------------------------------------------------------------- # 
    # Set logging object
    # --------------------------------------------------------------------------- #
    if not args.l:
        log_file = None
    else:
        log_file = args.l

    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)-15s::%(levelname)s::%(funcName)s::%(message)s', level=logging.INFO,
                        filename=log_file)

    # --------------------------------------------------------------------------- #
    # InfluxDB connection
    # --------------------------------------------------------------------------- #
    logger.info("Connection to InfluxDB server on [%s:%s]" % (config['influxdb_connection']['host'],
                                                              config['influxdb_connection']['port']))
    try:
        idb_client = DataFrameClient(host=config['influxdb_connection']['host'],
                                    port=int(config['influxdb_connection']['port']),
                                    username=config['influxdb_connection']['user'],
                                    password=config['influxdb_connection']['password'],
                                    database=config['influxdb_connection']['db'])
    except Exception as e:
        logger.error("EXCEPTION: %s" % str(e))
        sys.exit(2)
    logger.info("Connection successful")
    
    
    # --------------------------------------------------------------------------- #
    # Starting program
    # --------------------------------------------------------------------------- #
    logger.info("Starting program")
    
    #determine measurement, tags, fields and data file
    measurement = config['measurement']
    tag_list = config['tags']
    field_list = config['fields']
    time_stamp = config['time_stamp']
    data_path = config['data_path']
    
    logger.info("data file: " + data_path) 
    
    #read csv
    df = pd.read_csv(data_path)
    df[time_stamp] = pd.to_datetime(df[time_stamp])
    df = df.set_index(time_stamp)
    logger.info(df.dtypes)
    for f in field_list:
        #delete rows with unkown field-values, here marked as "-" in the csv
        df = df[df[f] != "-"]
        #convert field-values to float, convertion can differ depending on the data
        df[f] = df[f].astype(int).fillna(0)
    #tags for influxdb are required to be strings
    for t in tag_list:
        df[t] = df[t].astype(str)
            
    #logger.info(df.dtypes)
    
    counter = len(df.index)
    
    logger.info("Inserting " + measurement + "to DB...")
    idb_client.write_points(df,measurement, tag_columns=tag_list, field_columns=field_list, time_precision='s')
    #logger.info("Inserted " +  str(counter) +  " rows")
    logger.info("Ending program")