'''
Created on Feb 16, 2013

@author: cevaris
'''

class DatabaseManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        pass

        
    def connect(self):
        raise NotImplementedError()
    
    def close(self):
        raise NotImplementedError()
    
    
    def put(self):
        raise NotImplementedError()
    
    def update(self):
        raise NotImplementedError()
    
    def get(self):
        raise NotImplementedError()
    
    def delete(self):
        raise NotImplementedError()
    
    
    