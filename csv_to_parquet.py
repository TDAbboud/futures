#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert CSV files to snappy compressed
Parquet files using Spark RDDs

Running:
    Make sure the SPARK_HOME environment variable is set,
    since spark-submit will use the default configs from there
    $ spark-submit --deploy-mode cluster --master yarn csv_to_parquet.py \
            's3://tickerdata/raw/ES_2016/@ES#_2016*.csv'\
            's3://tickerdata/cleaned/ES_2016/ES_2016.parquet'

Debugging:
    Check the applications that were run
    $ yarn application --list -appStates FINISHED 

    Since we are running on Yarn, use the following
    to check stderr and stdout logs
    $ yarn logs -applicationID <app_id>

"""
import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types as T

class SparkSessionManager(object):
    """ Context Manager for a SparkSession """
    def __init__(self, app_name):
        self.app_name = app_name

    def __enter__(self):
        self.spark = SparkSession.builder.appName(self.app_name).getOrCreate()
        return self.spark

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spark.stop()


def csv_to_parquet(csv_path, parquet_path, csv_read_options=None, cleaning_steps=None):
    """ Convert csv files into snappy compressed parquet files
    Args:
        csv_path (str): Path to the csv files
        parquet_path (str): Output path for the parquet files
        csv_read_options (dict): dictionary of options for reading a csv.
            All options in pyspark.sql.DataframeReader.csv are valid
        cleaning_steps (function): custom cleaning function before writing
            back as a parquet file. The function must take the
            spark session as an argument and return an RDD
    """
    with SparkSessionManager('csv-to-parquet') as sm:
        # Read in the CSVs
        df = sm.read.csv(csv_path, **csv_read_options)

        if cleaning_steps is not None:
            df = cleaning_steps(sm)

        # Write back as parquet files
        df.write.parquet(parquet_path, compression='snappy', mode='overwrite')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'USAGE: %s <csv_path> <parquet_path>' % sys.argv[0]
    else:
        # Tickerdata Schema
        schema = T.StructType([
            T.StructField('datetime', T.TimestampType()),
            T.StructField('execution_price', T.DoubleType()),
            T.StructField('execution_size', T.IntegerType()),
            T.StructField('total_volume', T.IntegerType()),
            T.StructField('bid', T.DoubleType()),
            T.StructField('ask', T.DoubleType()),
            T.StructField('ticker_id', T.IntegerType()),
            T.StructField('basis', T.StringType()),
            T.StructField('trade_market_center', T.StringType()),
            T.StructField('trade_condition', T.StringType()),
        ])

        csv_options = {
                    'schema': schema,
                    'header': False,
                }
        def drop_columns(sm): 
            cols = ['basis', 'trade_market_center', 'trade_condition']
            return sm.drop(*cols)

        csv_to_parquet(sys.argv[1], sys.argv[2], csv_options, cleaning_steps=drop_columns)

