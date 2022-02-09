 CREATE OR REPLACE EXTERNAL TABLE `clear-rock-338918.nytaxi.external_fhv_trip`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_clear-rock-338918/fhv_trip/fhv_trip_2019-*.parquet']
);

# check total rows
SELECT count(*) 
FROM `clear-rock-338918.nytaxi.external_fhv_trip`; 

# Distinct dispatching_base_num in fhv taxi table

SELECT DISTINCT dispatching_base_num,count(*)
FROM `clear-rock-338918.nytaxi.external_fhv_trip`
GROUP BY dispatching_base_num;

SELECT count(DISTINCT dispatching_base_num)
FROM `clear-rock-338918.nytaxi.external_fhv_trip`;

#Best strategy to optimise if query always filter by dropoff_datetime and order by dispatching_base_num
# Partition by dropoff_datetime and cluster by dispatching_base_num

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `clear-rock-338918.nytaxi.fhv_trip` AS
SELECT * FROM `clear-rock-338918.nytaxi.external_fhv_trip`;


#What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num B00987, B02060, B02279

SELECT count(*)
FROM `clear-rock-338918.nytaxi.fhv_partitoned_clustered`
WHERE DATE(pickup_datetime) BETWEEN '2019-01-01' AND '2019-03-31' AND (dispatching_base_num = "B00987" OR  dispatching_base_num = "B02060" OR dispatching_base_num = "B02279");

# partionind and clustering

CREATE OR REPLACE TABLE `clear-rock-338918.nytaxi.fhv_partitoned_clustered`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY dispatching_base_num AS
SELECT * FROM `clear-rock-338918.nytaxi.external_fhv_trip`;

# SR Flag count 
SELECT COUNT(DISTINCT  SR_Flag)
FROM `clear-rock-338918.nytaxi.fhv_trip`;


