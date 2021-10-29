# Import some necessary modules
from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Connect to MongoDB and newarticles database
try:
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.Newsarticles_raw
    print("Connected successfully!")
except:  
    print("Error connecting to MongoDB")
    
# connect kafka consumer to kafka topic news-articles
consumer = KafkaConsumer('news-articles',bootstrap_servers=['192.168.0.212:9092'])

#print(type(consumer),consumer.topics(),consumer.assignment())

# Parse received data from Kafka consumer
for msg in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key,  msg.value))
  
    record = json.loads(msg.value)
   
    # ingest data into MongoDB
    try:
        rec_id = db.articles.insert_one(record)
        print("Data inserted with record ids", rec_id)
    except:
        print("Could not insert into MongoDB")