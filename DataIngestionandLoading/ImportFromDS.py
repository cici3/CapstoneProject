import json
from pymongo import MongoClient 

  
# Making Connection
myclient = MongoClient("mongodb://localhost:27017/") 
dbName= "Newsarticles_clean"
collectionName = "articles" 

# dataset below is from kagle
jsonfileName = '.\DataPreparation\Category_Dataset_v2.json'  
   
# database 
db = myclient[dbName]
   
# get collection 
Collection = db[collectionName]
  
# open json file
with open(jsonfileName) as file:
    file_data = json.load(file)
      
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)  
else:
    Collection.insert_one(file_data)