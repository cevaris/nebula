import datetime
from consts import ROOT_DIR
import os

def gen_timestamp():
    time = datetime.datetime.now()
    date = datetime.datetime.now()
    return '%d_%d_%d__%d_%d_%d' % (date.month, date.day, date.year, time.hour, time.minute, time.second)


def gen_directory(dir_to_create):
    directory =  dir_to_create
    if not os.path.exists(dir_to_create):
        abs_path = "%s/%s" % (ROOT_DIR,dir_to_create)
        directory = abs_path
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
    
    return directory