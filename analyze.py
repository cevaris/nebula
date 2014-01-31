'''
Created on Mar 5, 2013

@author: cevaris
'''

import sys

from optparse import OptionParser

from tasks.twitter.tasks import AnalyzeTweets

def parse_input(options):
    
    if options.database_name:
        database_name = options.database_name
        config = { 'name': database_name }
        
        if options.result_dir:
            config['result_dir'] = options.result_dir
        
        print 'Preparing Task, '
        task = AnalyzeTweets(config)
        task.run()
        
        
if __name__=="__main__":
    
    parser = OptionParser("usage: %prog -n configuration_file")
    parser.add_option("-n", "--name", dest="database_name",  type='string', help='Provide name database where the data is to be stored')
    parser.add_option("-o", "--result-dir", dest="result_dir",  type='string', help='Provide directory path where to output the results')

    (options, args) = parser.parse_args(sys.argv)
    if len(args) != 1:
        parser.error('incorrect number of arguments')
    
    parse_input(options)
    
        
    
