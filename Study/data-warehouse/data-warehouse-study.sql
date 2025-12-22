-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;


-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zc-data-warehouse.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zc-aparajita-data/yellow/yellow_tripdata_2019-*.parquet', 'gs://de-zc-aparajita-data/yellow/yellow_tripdata_2020-*.parquet']
);