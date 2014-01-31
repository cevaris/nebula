from Queue import Queue
from time import sleep
import threading
import os

import sys
import time

from tweetstream.streamclasses import FilterStream


from consts import TWITTER_USERNAME
from consts import TWITTER_PASSWORD
from data.db.mongo import Mongo
from data.mining import DefaultFrequentItemSets, DefaultLocation
from data.mining import DefaultTextAnalysis
from data.util import gen_timestamp
from nebula.task import Task
from util import spinning_cursor


class TweetStream(Task):
    tweet_queue = Queue()
    tags = []
    locations = []
            
    def __init__(self,config={}):
        self.config = {
            'name':'default',
            'db_name':None,
            'tags':[],
            'locations': [],
        }
        
        self.config.update(config)
        
    def _pre(self):
        
        if not self.config['db_name']:
            self.config['db_name'] = "%s_%s" % (self.config['name'],  gen_timestamp())
            print 'Creating Database', self.config['db_name']
        
        print 'Configuration', self.config, self.config['db_name']
        
        TweetStream.mongoDb = Mongo({
            'COLLECTION' : self.config['db_name']
        })
        
        TweetStream.tags = self.config['tags']
        TweetStream.locations =  self.config['locations']
        

    class Producer(threading.Thread):
        def run(self):
            tweet_queue = TweetStream.tweet_queue
            tags = TweetStream.tags
            locations = TweetStream.locations
            print 'Producing with ',tags
            
            print 'Starting Producer'
            with FilterStream(TWITTER_USERNAME, TWITTER_PASSWORD, track=tags,locations=locations) as stream:
                for tweet in stream:
                    tweet_queue.put(tweet)
                    
    class Consumer(threading.Thread):
        
        def run(self):
            tweet_queue = TweetStream.tweet_queue
            mongoDB = TweetStream.mongoDb
            
            print 'Starting Consumer'
            while True:
                
                if tweet_queue.qsize() < 15:
                    sleep(0.1) # Shh...go to sleep...
                
                if tweet_queue.empty():
                    pass
                    #print 'Nothing to do'
                else:
                    tweet = tweet_queue.get()
                    mongoDB.put(tweet)
                    
                    print 'Inserting Tweet, ', tweet['text'], '...',                    
                    print 'Done'
    
    class SpinWheel(threading.Thread):
        
        def run(self):
            tweet_queue = TweetStream.tweet_queue
            
            while True:
                for c in spinning_cursor():
                    if tweet_queue.empty():
                        sys.stdout.write(c)
                        sys.stdout.flush()
                        time.sleep(0.08)
                        sys.stdout.write('\b')
                
    
    def _execute(self):
        
        th_producer = TweetStream.Producer()
        th_consumer = TweetStream.Consumer()
        spin_wheel  = TweetStream.SpinWheel()
        
        th_producer.start()
        th_consumer.start()
        spin_wheel.start()
        
        th_consumer.join()
        th_producer.join()
        spin_wheel.join()
           
    def _post(self):
        
        TweetStream.mongoDb.close()
            

   
   

class AnalyzeTweets(Task):
    
    def __init__(self,config={}):
        self.config = {
            'name':None,
            'text_output':None
        }
        self.config.update(config)
        
        if self.config['text_output']:
            self.create_directory(os.path.dirname(self.config['text_output']))
            
        print "Configuration ", self.config
    
    def _pre(self):
        self.mongoDb = Mongo({
            'COLLECTION' : self.config['name']
        })
    
    def _execute(self):
        
        itemset_report = DefaultFrequentItemSets(self.config['name'])
        itemset_report.run()
        
        sent_report = DefaultTextAnalysis(name=self.config['name'])
        sent_report.run()
        
        location_report = DefaultLocation(name=self.config['name'])
        location_report.run()
            
        if self.config['result_dir']:            
            itemset_report.generate_report(self.config['result_dir'])
            sent_report.generate_report(self.config['result_dir'])
            location_report.generate_report(self.config['result_dir'])
            
#        for tweet in self.mongoDb.iter():
#            print tweet['text']
           
    def _post(self):
        pass
    
    def create_directory(self,directory):
        if not os.path.exists(directory):
            print 'Creating directory', directory
            os.makedirs(directory)

    
    
    
    