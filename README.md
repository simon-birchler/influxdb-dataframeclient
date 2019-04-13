# influxdb-dataframeclient
Simple script using the influx DataframeClient to import data from a csv file into an influxdb.

Use the config file to hand over the neccessary information about the db connection and the data. 
Optionally, use a log file to save the logger messages. 

The script is converting the tag values to strings, as influxdb requires strings as tags, and field values to floats, which can be changed according to the data. The reason for that are the formats of the data when creating the dataframe. 
