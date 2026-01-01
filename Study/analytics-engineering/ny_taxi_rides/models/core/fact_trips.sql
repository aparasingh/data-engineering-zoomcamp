{{
    config(
        materialized = 'table'
    )
}}

with green_tripdata as (
    select *, 
        'Green' as service_type
    from {{ ref('stg_green_tripdata') }}
), 
yellow_tripdata as (
    select *, 
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
), 
trips_unioned as (
    select * from green_tripdata
    union all 
    select * from yellow_tripdata
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select t.tripid, 
    t.vendorid, 
    t.service_type,
    t.ratecodeid, 
    t.pulocationid, 
    pz.borough as pickup_borough, 
    pz.zone as pickup_zone, 
    t.dolocationid,
    dz.borough as dropoff_borough, 
    dz.zone as dropoff_zone,  
    t.pickup_datetime, 
    t.dropoff_datetime, 
    t.store_and_fwd_flag, 
    t.passenger_count, 
    t.trip_distance,
    t.fare_amount, 
    t.extra, 
    t.mta_tax, 
    t.tip_amount, 
    t.tolls_amount,
    t.improvement_surcharge, 
    t.total_amount, 
    t.payment_type, 
    t.payment_type_description
from trips_unioned as t
inner join dim_zones as pz
on t.pulocationid = pz.locationid
inner join dim_zones as dz
on t.dolocationid = dz.locationid