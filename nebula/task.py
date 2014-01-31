'''
Created on Feb 16, 2013

@author: cevaris
'''

class Task(object):
    '''
    classdocs
    '''


    def __init__(self):
        pass
        
    def _pre(self):
        raise NotImplementedError()

    def _execute(self):
        raise NotImplementedError()
   
    def _post(self):
        raise NotImplementedError()
    
    def _producer(self):
        raise NotImplementedError()
    
    def _consumer(self):
        raise NotImplementedError()
    
    
    def run(self):
        self._pre()
#        print 'Completed Pre-Execution'
        self._execute()
#        print 'Completed Execution'
        self._post()
#        print 'Completed Post-Execution'
#        print 'Woo-hoo!! Completed the Task'
    
    