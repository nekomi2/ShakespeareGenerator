from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer

spark = SparkSession.builder.appName("Hamlet Tokenization").getOrCreate()

df = spark.read.text("hamlet.txt").withColumnRenamed("value", "sentence")

tokenizer = Tokenizer(inputCol="sentence", outputCol="words")

tokenized = tokenizer.transform(df)

tokenized.select("sentence", "words").show(truncate=False, n=20)

spark.stop()
