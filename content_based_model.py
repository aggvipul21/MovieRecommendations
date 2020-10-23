#Import dependencies
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import re

# Set Environment Variables
import os
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk1.8.0_212"
os.environ["SPARK_HOME"] = "C:\software\spark-3.0.0-bin-hadoop2.7"

# Start a SparkSession
#import findspark
#findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
if __name__ == '__main__':
    scSpark = SparkSession \
        .builder \
        .master('local[*]') \
        .config("spark.driver.memory", "7g") \
        .getOrCreate()

from pyspark import SparkFiles
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import CountVectorizer

#movies_df=pd.read_csv("data/updated_movies.csv")
# print(movies_df.columns)
movies_df=scSpark.read\
            .option("inferSchema", "true")\
            .csv("data/updated_movies.csv", header=True, sep=",")\
            .cache()

movies_df.printSchema()

#sample_df=movies_df

print(movies_df.count())

# print(movies_df.columns)

# print(movies_df.loc[0:1,:])

# samples_movie_df=movies_df.copy()

from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import HashingTF, IDF
from pyspark.ml.feature import Normalizer
import pyspark.sql.functions as psf


#tkn = Tokenizer().setInputCol("genres").setOutputCol("combOut")
#tokenized = tkn.transform(sample_df.select("genres"))
#tokenized.show(20, False)
df = movies_df.withColumn("combOut", psf.split(psf.regexp_replace("genres", " ", ""), ','))
df.printSchema()

sample_df = df.sample(fraction=0.01, seed=42)
sample_df.count()

hashingTF = HashingTF(inputCol="combOut", outputCol="tf")
tf = hashingTF.transform(sample_df)

idf = IDF(inputCol="tf", outputCol="feature").fit(tf)
tfidf = idf.transform(tf)


normalizer = Normalizer(inputCol="feature", outputCol="norm")
data = normalizer.transform(tfidf)#.show(20,False)

#data.printSchema()

from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix
mat = IndexedRowMatrix(
    data.select("movieId", "norm")\
        .rdd.map(lambda row: IndexedRow(row.movieId, row.norm.toArray()))).toBlockMatrix()
dot = mat.multiply(mat.transpose())
dot.toLocalMatrix().toArray().show(20,False)

sample_df.rdd.saveAsPickleFile("sample_movies.pckl")
dot.toLocalMatrix().toArray().rdd.saveAsPickleFile("genrepredictor.pckl")


#from sklearn.metrics.pairwise import cosine_similarity

# cv = CountVectorizer()\
#     .setInputCol("combOut")\
#     .setOutputCol("countVec")

# fittedCV = cv.fit(tokenized)
# countVec=fittedCV.transform(tokenized)
# countVec.show(20,False)
#print(countVec)
# #creating a similarity score matrix   
# sim = cosine_similarity(count_matrix)
# print(sim)