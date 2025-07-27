#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import gzip
from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Keep the original compressed filename
    if url.endswith('.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator = True, chunksize = 100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con= engine, if_exists = 'replace')

    df.to_sql(name=table_name, con= engine, if_exists = 'append')

    try:
        while True:
         t_start = time()
         df = next(df_iter)
         df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
         df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
         df.to_sql(name=table_name, con= engine, if_exists = 'append')
         t_end = time()
         print('inserted another chunk.... took %.3f seconds' % (t_end - t_start))
    except StopIteration:
        print("Finished inserting all data!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSVB Data to Postgres')
    # get the argument values from user
    parser.add_argument('--user', help = 'username for postgres')
    parser.add_argument('--password', help = 'password for postgres')
    parser.add_argument('--host', help = 'host for postgres')
    parser.add_argument('--port', help = 'port for postgres')
    parser.add_argument('--db', help = 'DB name for postgres')
    parser.add_argument('--table_name', help = 'table name where results will be written')
    parser.add_argument('--url', help = 'url of the csv')
    args = parser.parse_args()
    main(args)

