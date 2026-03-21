#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark
from pyspark.sql import SparkSession


# In[2]:


spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()


# In[21]:


df_green = spark.read.parquet("data/pq/green/*/*")


# In[22]:


df_green.show()


# In[23]:


print(df_green.count())


# In[24]:


df_yellow = spark.read.parquet("data/pq/yellow/*/*")


# In[25]:


df_yellow.show()


# In[26]:


df_yellow.printSchema()


# In[27]:


df_green.printSchema()


# In[28]:


df_green.columns


# In[29]:


df_yellow.columns


# In[ ]:





# In[39]:


df_green = df_green \
    .withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime')


# In[40]:


df_yellow = df_yellow \
    .withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime')


# In[50]:


set(df_yellow.columns) & set(df_green.columns)


# In[ ]:





# In[43]:


common_columns = []

yellow_columns = set(df_yellow.columns)

for col in df_green.columns:
    if col in yellow_columns:
        common_columns.append(col)


# In[54]:


common_columns


# In[55]:


from pyspark.sql import functions as f


# In[57]:


df_green_sel = df_green \
    .select(common_columns) \
    .withColumn('service_type', f.lit('green'))


# In[58]:


df_green_sel.show()


# In[59]:


df_yellow_sel = df_yellow \
    .select(common_columns) \
    .withColumn('service_type', f.lit('yellow'))


# In[60]:


df_trips_data = df_green_sel.unionAll(df_yellow_sel)


# In[61]:


df_trips_data.groupBy('service_type').count().show()


# In[62]:


df_trips_data.registerTempTable('trips_data')


# In[66]:


spark.sql("""
SELECT count(1),
service_type
FROM
    trips_data
GROUP BY 
    service_type;
""").show()


# In[77]:


df_result = spark.sql("""
SELECT 
    -- Revenue grouping 
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month, 
    service_type, 

    -- Revenue calculation 
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,

    -- Additional calculations
    AVG(passenger_count) AS avg_monthly_passenger_count,
    AVG(trip_distance) AS avg_monthly_trip_distance

FROM 
    trips_data
GROUP BY
    1,2,3
""")


# In[78]:


df_result.show()


# In[79]:


df_result.write.parquet('data/report/revenue/')


# In[76]:


df_result.coalesce(1).write.parquet('data/report/revenue/', mode = 'overwrite')


# In[ ]:




