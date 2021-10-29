from kafka import KafkaProducer
import requests
import json
import random
import time

#import logging
#logging.basicConfig(level=logging.DEBUG)


url = "https://free-news.p.rapidapi.com/v1/search"


def generateNews():
    headers = {
        'x-rapidapi-host': "free-news.p.rapidapi.com",
        'x-rapidapi-key': "ce68fb8002msh0e8901c9f3c6e79p1f60e2jsndfe1fb607635"
        }
    key_words = []
    querystring = {"q":"entertainment","lang":"en"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    global artcles_list
    res = response.json()
    
    #save articles in list
    artcles_list = res["articles"]



def produce_msgs(artcles_list,hostname='192.168.0.212', port='9092', 
                 topic_name='news-articles',         
                 nr_messages=2,                     
                 max_waiting_time_in_sec=60):
    
    # Function for Kafka Producer with settings related to the Kafka's Server
    producer = KafkaProducer(
        bootstrap_servers=hostname+":"+port,api_version=(0,10),
        value_serializer=lambda v: json.dumps(v).encode('ascii'),
        key_serializer=lambda v: json.dumps(v).encode('ascii')
    )
 
    j=0
    j=len(artcles_list)
    for i in artcles_list:
        print("Sending: {}".format(i))
     
        producer.send(topic_name,i)
        
        # Sleeping time
        sleep_time = random.randint(0, max_waiting_time_in_sec * 10)/10
        print("Sleeping for..."+str(sleep_time)+'s')
        time.sleep(sleep_time)

         # Force flushing of all messages
        if (j % 100) == 0:
             producer.flush()
        j = j + 1        
    
    producer.close()
    
generateNews()        
produce_msgs(artcles_list)