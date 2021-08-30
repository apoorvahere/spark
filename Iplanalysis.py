from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.sql.functions as func
spark = SparkSession.builder.getOrCreate()
DF = spark.read.json("hdfs://127.0.0.1:9000/Ipl/ipl_json/1082592.json", multiLine = "true").drop("info","meta")
DF.printSchema()
inningsDF=DF.select(func.col('innings').getItem(0).alias('firstinnings'))
inningsDF.show()
oversDF=inningsDF.select(explode('firstinnings.overs').alias('overs'))
oversDF.show()
deliveryDF=oversDF.select(explode('overs.deliveries').alias('deliveries'))
deliveryDF.show()
runsDF=deliveryDF.select('deliveries.batter','deliveries.bowler',func.col('deliveries.runs.batter').alias("Runs"))
runsDF.show()
totalrunDF=runsDF.groupBy('batter','bowler').agg(func.sum('Runs').alias('Total_Runs'))
totalrunDF.show()
MaxrunsDF=totalrunDF.groupBy('batter').agg(func.max('Total_Runs').alias('Highest_Run'))
MaxrunsDF.show()
ResultDF=MaxrunsDF.join(MaxrunsDF, (MaxrunsDF.Highest_Run==totalrunDF.Total_Runs) & (MaxrunsDF.batter==totalrunDF.batter), how="left").withColumnRenamed("Total_Runs", "Highest_Run")
ResultDF.show()
