'''
Created on Feb 16, 2013

@author: cevaris
'''
import datetime
import types

from pymongo.mongo_client import MongoClient
from data.db.manager import DatabaseManager

TIMESTAMP_CREATED = '_created_timestamp'

class Mongo(DatabaseManager):
    
    def __init__(self,options={}):
        self.config = {
            'HOST':'localhost',
            'PORT':27017,
            'COLLECTION': 'default'
        }
        
        self.config.update(options)
        print self.config 
    
        self.connect()
       

    def connect(self):
        self.client = MongoClient(
            self.config['HOST'],
            self.config['PORT']
        )
        
        self.db = self.client[self.config['COLLECTION']]
        
    
    def iter(self):
        return self.db.collection.find()
    
    def close(self):
        if self.client:
            self.client.close()
    
    def count(self):
        return self.db.collection.count()
        
        
    def put(self,data):
        
        if isinstance(data, types.ListType):
            # For bulk insert, inject timestamp
            for x in data:
                x[TIMESTAMP_CREATED] = datetime.datetime.utcnow()
        else:
            # For single insert, inject timestamp
            data[TIMESTAMP_CREATED] = datetime.datetime.utcnow()
       
        try:
            self.db.collection.insert(data)
            return True
        except Exception as e:
            print e
            return False
        
    
    def update(self):
        pass
    
    def get(self, query=False):
        
        if not query:
            # Get all documents in collection
            return list(self.db.collection.find())
    
    def delete(self):
        pass

    
