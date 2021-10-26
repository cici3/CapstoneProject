import pandas as pd
import re
import string
import pyspark
import nltk
import sklearn

from pyspark.sql.functions import concat, isnull, when, count, col
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col
from sklearn.svm import SVC
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# from sparknlp.base import *
# from textblob import TextBlob

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline  as sklearnpipeline

working_directory = './DataPreparaionandModeling/jars/*'
model_path = './DataPreparaionandModeling/Model/newsclassfier_model.pkl'


#initiate spark session
print("start spark session")
spark = SparkSession \
    .builder \
    .appName("NewsClassifier_Datapreparation") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/Newsarticles_clean.articles") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/Newsarticles_clean.articles") \
    .config('spark.driver.extraClassPath', working_directory) \
    .getOrCreate()

#load data from mongo database, that we have ingested
df = spark.read.format("mongo").load()

#data preprocessing
print("Schema:")
df.printSchema()

print("show top 5 records: ")
df.show(5)

print("Number of records: ",df.count())
print("Columns: ", df.columns)

pysparkDF = df.select(col('category'),  concat(col('headline'), col('short_description'),col('authors')).alias ('text'))
pysparkDF.show(5)

# find null values, if any eliminate them
pysparkDF.select([count(when(isnull(c), c)).alias(c) for c in pysparkDF.columns]).show()
pysparkDF = pysparkDF.replace('?', None).dropna(how='any')

# convert pysparkDF to pandasDF
pandasDF = pysparkDF.toPandas()
print(pandasDF['category'].unique())
print(pandasDF['text'])

#stop spark session as we have converted into pandasDF
spark.stop()
print("spark sesion stopped")

#Preprocessing text by removing unwanted symbols, lemmatize and remove
stop_words_ = set(stopwords.words('english'))
wn = WordNetLemmatizer()
custom_stopwords= ['make', 'amp',  'news','new' ,'time', 'u','s', 'photos',  'get', 'say']
 
def Preprocessing(text):
    clean_text=[]
    clean_text2=[]
    text = re.sub("'","",text) #remove apostrophe
    text = re.sub("(\\d|\\W)+"," ",text)
    clean_text = [wn.lemmatize(word, pos="v") for word in word_tokenize(text) if black_txt(word)]
    clean_text2 = [word for word in clean_text if black_txt(word)]
    return " ".join(clean_text2)

def black_txt(token):
    return  token not in stop_words_ and token not in list(string.punctuation)  and len(token)>2 and token not in custom_stopwords

#Label Encoding
X = pandasDF.drop(['category'],axis=1)
y = pandasDF['category']
print(X)
print (y)


#split the dataset
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
v = dict(zip(list(y), pandasDF['category'].to_list()))

#train the model
sklearn_pipeline = sklearnpipeline([('vect', CountVectorizer(analyzer="word", stop_words="english")),('tfidf', TfidfTransformer(use_idf=True)),('clf', MultinomialNB(alpha=.01))])

print(type(x_train))
sklearn_pipeline.fit(x_train['text'].to_list(), list(y_train))

#test the model
import numpy as np
X_TEST = x_test['text'].to_list()
Y_TEST = list(y_test)
predicted = sklearn_pipeline.predict(X_TEST)

c = 0
for doc, category in zip(X_TEST, predicted):
    if c == 2:break
    print("-"*55)
    print(doc)
    print(v[category])
    print("-"*55)
    c = c + 1 
#print accuracy
acc = np.mean(predicted == Y_TEST)
print("accuracy: ",acc)


docs_new = ['Ten Months After George Floyd’s Death, Minneapolis Residents Are at War Over Policing']

predicted = sklearn_pipeline.predict(docs_new)
v[predicted[0]]

# Saving the Model
import pickle
with open(model_path,'wb') as f:
    pickle.dump(sklearn_pipeline,f)

