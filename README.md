# influxdb-dataframeclient
Simple Python script using the influx DataframeClient to import data from a csv file into an influxdb.

Arguments:
- c: relative path to a config json file. A config file is required.
- l: relative path to a log file. A new file is created and used if the file does not exist. Using a log file is optional. 

Use the config file to hand over the neccessary information about the db connection and the data:
- influx_connection: information about the database
- data_path: location of the csv files. The script will try to insert all files in this path.
- measurement: name of the measurement you want to insert. All csv files should contain data for the same measurement.
- time_stamp: Determine the column that contains the time stamp of the datapoints.
- tags: Determine a list of columns that should be tags
- fields: Determine a list of columns that should be fields

The script is converting tag values to strings, as influxdb requires strings as tags, and field values to ints, which should be changed depending to the data. The reason for these convertions are the formats of the dataframe when it is created. 


Example command to execute the script:

python csv-to-line-df.py -c conf/conf.json -l log.txt
