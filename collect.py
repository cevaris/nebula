'''
Created on Mar 5, 2013

@author: cevaris
'''
from tasks.twitter.tasks import TweetStream
from optparse import OptionParser
import sys
import json

def parse_input(parser, config_file):
    
    print '\nReading configuration from, ',config_file
    data = None
    try:
        data = open(config_file, 'r').read()
    except IOError as e:
        parser.error('file not found')
    
    if len(data) == 0:
        parser.error('file is empty')
        
    data = json.loads(data)
    
    if options.database_name:
        data['db_name'] = options.database_name
    
    print 'Preparing Task, ', data
    task = TweetStream(config=data)
    task.run()
    
    

if __name__=="__main__":
    
    parser = OptionParser("usage: %prog configuration_file")
    parser.add_option("-a", "--action", dest="config_file",  type='string', help='Provide an action to do')
    parser.add_option("-c", "--config", dest="config_file",  type='string', help='Provide a JSON configuration file')
    parser.add_option("-n", "--name", dest="database_name",  type='string', help='Provide name database where the data is to be stored')

    (options, args) = parser.parse_args(sys.argv)
    if len(args) != 1:
        parser.error('incorrect number of arguments')
    
    config_file = options.config_file
    
    parse_input(parser,config_file)
    
        
        
    
    
    
        
    
        
    
    

#    task = StreamTweet()
#    task.run()
    
    
