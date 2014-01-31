
import csv

class CSVWriter(object):

    def __init__(self,output_file_name):
        self.output_path = output_file_name
        
        
    def write(self, data):
        with open(self.output_path, 'w+') as output:
            report = csv.writer(output, delimiter=',')
            
            for line in data:
                report.writerow(line)