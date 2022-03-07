#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import argparse
from time import time
import os


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    taxi_table_name = params.table_taxi
    zone_table_name = params.table_zone
    csv_url_taxi = params.url1
    csv_url_zone = params.url2

    taxi_csv_name = "taxi_output_csv"
    zones_csv_name = "zones_output_csv"

    os.system(f"wget {csv_url_taxi} -O {taxi_csv_name}")
    os.system(f"wget {csv_url_zone} -O {zones_csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iterator = pd.read_csv(taxi_csv_name, iterator = True ,chunksize = 10000)

    df = next(df_iterator)

    df["tpep_pickup_datetime"] = pd.to_datetime(df.tpep_pickup_datetime)
    df["tpep_dropoff_datetime"] = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n = 0).to_sql(name = taxi_table_name, con = engine ,if_exists = 'replace')

    df.to_sql(name = taxi_table_name, con = engine ,if_exists= 'append')

    for chunk in df_iterator:
        df = chunk
        df["tpep_pickup_datetime"] = pd.to_datetime(df.tpep_pickup_datetime)
        df["tpep_dropoff_datetime"] = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name = taxi_table_name, con = engine ,if_exists= 'append')
        print("...chunk is added to the database")



    df_zones = pd.read_csv(zones_csv_name)
    df_zones.to_sql(name = zone_table_name, con = engine ,if_exists = 'replace')



# user
# pass
# host
# port 
# database name
# table name
# url of csv

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')
    
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='pass for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database for postgres')
    parser.add_argument('--table_taxi', help='table in  postgres')
    parser.add_argument('--table_zone', help='table in  postgres')
    parser.add_argument('--url1', help='url for yellow taxi csv')
    parser.add_argument('--url2', help='url for taxi zones csv')

    args = parser.parse_args()
    main(args)







