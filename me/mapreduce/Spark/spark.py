# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 00:11:59 2022

This file helped me to learn about spark and more precisely pyspark. Until now I had never worked on any of the 2.

@author: cypri
"""

# If the spark app is not starting maybe the tmp folder has been removed at system startup ?

#%% Import
print("import ..")
from pyspark.sql import SparkSession

#%% Create app [so this creates both sparkcontext (can be only one) and sparksession (can be multiple)]
print('Create app')
#spark = SparkSession.builder.appName('AutoAccount').getOrCreate()
spark = SparkSession.builder \
        .master("local[1]") \
        .appName('AutoAccount') \
        .getOrCreate()

print("Spark instance (looks like it contains spark context and session)", spark)

#%% Create RDD from parallelize

"""
    RDD: Resilient Distributed Dataset
        fundamental data structure of PySpark that is fault-tolerant, immutable 
        distributed collections of objects, which means once you create an RDD 
        you cannot change it. Each dataset in RDD is divided into logical partitions, 
        which can be computed on different nodes of the cluster.
"""

datalist = [('Java', 2000), ('Python', 1000000), ('Scala', 3000)]
rdd = spark.sparkContext.parallelize(datalist)
print('\n\nRDD count', rdd.count())


#%% Create RDD from textFile

rdd2 = spark.sparkContext.textFile("D:/tmp/tmp.txt")
print('RDD2', rdd2)
print('\n\nRDD2 count', rdd2.count())

#%% Create a standart dataframe

data = [
  ('James','','Smith','1991-04-01','M',3000),
  ('Michael','Rose','','2000-05-19','M',4000),
  ('Robert','','Williams','1978-09-05','M',4000),
  ('Maria','Anne','Jones','1967-12-01','F',4000),
  ('Jen','Mary','Brown','1980-02-17','F',-1)
]

columns = ["firstname", "middlename", "lastname", "dob", "gender", "salary"]
df = spark.createDataFrame(data=data, schema=columns)


df.show()


#%% Use Spark SQL

df.createOrReplaceTempView("PERSON_DATA")
df2 = spark.sql("SELECT * from PERSON_DATA")
df2.printSchema()
df2.show()



#%% Group by

groupDF = spark.sql("SELECT gender, count(*) from PERSON_DATA group by gender")
groupDF.show()


#%% Create DataFrame with schema


from pyspark.sql.types import StructType,StructField, StringType, IntegerType

data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

data3 = [
    ("Emilien","","Delevoye","93000","M",3000),
    ("William","","petitemontage","01000","NB",4000),
    ("Cyprien","Antoine","Ricque","59000","M",4000),
    ("Louise","","Devyncq","96000","F",4000)
   ]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])

df = spark.createDataFrame(data=data2,schema=schema)
df.printSchema()
df.show(truncate=False)

newRows = spark.createDataFrame(data3, schema)
appended = df.union(newRows)
appended.show()



