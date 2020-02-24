import sys
import datetime
import time
from utils import utils
from pymongo import MongoClient

client = utils.connection('clarity', 'clarity#demo')
db = client["clarity-data"]
collection = db["hosts"]

documents = []
start = time.time()
for line in sys.stdin:
    parsed_line = line.strip().split(" ")
    try:
        documents.append({
            'timestamp':
            datetime.datetime.fromtimestamp(int(parsed_line[0]) / 1e3),
            'src':
            parsed_line[1],
            'dst':
            parsed_line[2]
        })
    except IndexError:
        utils.logger('ERROR', 'Line index out of range {}'.format(parsed_line))
    if len(documents) >= 3000 or (time.time() - start) > 3.0:
        try:
            collection.insert_many(documents)
            utils.logger('INFO', '[DB] [INSERT] [{}]'.format(len(documents)))
            documents = []
            start = time.time()
        except Exception as e:
            utils.logger('ERROR', '[DB] [INSERTION] [{}]'.format(e))

try:
    collection.insert_many(documents)
    utils.logger('INFO', '[DB] [INSERT] [{}]'.format(len(documents)))
except Exception as e:
    utils.logger('ERROR', '[DB] [INSERTION] [{}]'.format(e))

utils.logger('INFO', '[PROCESS] [END] [1]')
