import subprocess


from pymining import itemmining, assocrules
from pattern.text.en.parser import sentiment
from nltk.stem.snowball import EnglishStemmer

from consts import ROOT_DIR
from data.util import gen_directory
from nebula.task import Task
from data.report.csv import CSVWriter

    
class DefaultTextAnalysis(Task):
    def __init__(self, name=None):
        self.name = name
        self.sentiment = []
        
        if not self.name:
            raise Exception('No name was provided from database')
        
    def generate_report(self, result_dir):
        
        directory = gen_directory(result_dir)
                
        result_file = "%s/%s" % (directory, 'sentiment.txt')
        
        with open(result_file, 'w+') as writer:
            for line in self.sentiment:
                writer.write("%s\n" % str(line))
                     
    def _execute(self):
        
        corpus = mongoExtractText(self.name)
        stemmer = EnglishStemmer()
        for item in corpus:
            line = item.replace(',', ' ')
            stemmed_line = stemmer.stem(line)
            self.sentiment.append((sentiment.sentiment(stemmed_line), stemmed_line))

#    def analyze_text_sentiment(self,corpus):
#        results = []
#        for item in corpus:
#            string = ' '.join(item)
#            results.append((sentiment.sentiment(string), string))
#        return results

    def _pre(self):
        # Set up directories
        pass
    
    
    def _post(self):
        # Write Report
        pass


class DefaultLocation(Task):
    def __init__(self, name=None):
        self.name = name
        self.tweet_locations = []
        
        if not self.name:
            raise Exception('No name was provided from database')
        
    def generate_report(self, result_dir):
        
        directory = gen_directory(result_dir)
        result_file = "%s/%s" % (directory, 'tweet-locations.txt')
        
        with open(result_file, 'w+') as writer:
            for line in self.tweet_locations:
                writer.write("%s\n" % str(line))
                     
    def _execute(self):
        
        self.tweet_locations = mongoTweetLongLat(self.name)
        pass

    def _pre(self):
        # Set up directories
        pass
    
    
    def _post(self):
        # Write Report
        pass

        
    
class DefaultFrequentItemSets(Task):
    
    def __init__(self, name=None):
        self.transactions = []
        self.item_sets = []
        self.rules = []
        self.name = name
        self.min_support = 5
        self.min_confidence = 0.6
        
        if not self.name:
            raise Exception('No name given')
        
    def _execute(self):
        
        self.transactions = mongoComputeHashTagItemSets(self.name)
        relim_input = itemmining.get_relim_input(self.transactions)
        self.item_sets = itemmining.relim(relim_input, self.min_support)
        self.rules = assocrules.mine_assoc_rules(self.item_sets, self.min_support, self.min_confidence)
        
    def _pre(self):
        # Set up directories
        pass
    
    def _post(self):
        # Write Report
        pass

    def generate_report(self, result_dir):
        
        directory = gen_directory(result_dir)
        
        result_file = "%s/%s" % (directory, 'transactions.txt')
        with open(result_file, 'w+') as writer:
            for line in self.transactions:
                writer.write("%s\n" % ','.join(line))
        
        result_file = "%s/%s" % (directory, 'freq-itemsets.txt')
        with open(result_file, 'w+') as writer:
            for line in self.item_sets:
                writer.write("%s\n" % str(line))
                
        result_file = "%s/%s" % (directory, 'association-rules.txt')
        with open(result_file, 'w+') as writer:
            for line in self.rules:
                writer.write("%s\n" % str(line))
        
        result_file = "%s/%s" % (directory, 'bag-of-words.txt')
        if not mongoExtractText(self.name, result_file):
            raise Exception('Error executing Mongo query "text.js"')
                
        
def mongoComputeHashTagItemSets(name):
    """
    Example Command
    mongo --quiet --host localhost immigration_3_27_2013__20_17_41  resources/queries/hashtag-itemsets.js
    """
    
    if len(name) == 0:
        raise Exception('Invalid database name')
    
    command = ['mongo', '--quiet', '--host', 'localhost', name, 'resources/queries/hashtag-itemsets.js']
    results = subprocess.check_output(command).splitlines()

    transacations = [r.split(',') for r in results]
    return transacations

def mongoTweetLongLat(name, file_path=None):
    """
    Example Command
    mongo --quiet --host localhost immigration_3_27_2013__20_17_41  resources/queries/tweet-long-lat.js
    """
    
    if len(name) == 0:
        raise Exception('Invalid database name')
    
    command = ['mongo', '--quiet', '--host', 'localhost', name, 'resources/queries/tweet-long-lat.js']

    if file_path:
        ouput = open(file_path, "w+")
        try:
            subprocess.call(command, stdout=ouput)
            return True
        except Exception as e:
            print e
            return False
    else:
        return subprocess.check_output(command).splitlines()

def mongoExtractText(name, file_path=None):
    """
    Example Command
    mongo --quiet --host localhost immigration_3_27_2013__20_17_41 resources/queries/text.js
    """
    if len(name) == 0:
        raise Exception('Invalid database name')
    
    command = ['mongo', '--quiet', '--host', 'localhost', name, 'resources/queries/text.js']
       
    if file_path:

        ouput = open(file_path, "w+")
        
        try:
            subprocess.call(command, stdout=ouput)
            return True
        except Exception as e:
            print e
            return False
    else:
        return subprocess.check_output(command).splitlines()
        


                
        
            



