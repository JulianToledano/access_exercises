import sys
from datetime import datetime, timedelta
from utils import utils
from pymongo import MongoClient

client = utils.connection('clarity', 'clarity#demo')
db = client["clarity-data"]
collection = db["hosts"]

current_timestamp = datetime.now()
one_hour_before_ts = current_timestamp - timedelta(hours=1)
destination_host = sys.argv[1]
source_host = sys.argv[2]


def get_hosts_connected_to(dst_host):
    results = collection.find({
        'timestamp': {
            '$gte': one_hour_before_ts,
            '$lt': current_timestamp
        },
        'dst': dst_host
    })
    hostnames = []
    for result in results:
        hostnames.append(result['src'])
    utils.logger(
        'INFO',
        'List of hosts connected to {}: {}'.format(destination_host,
                                                   hostnames))


def get_hosts_receiving_from(src_host):
    results = collection.find({
        'timestamp': {
            '$gte': one_hour_before_ts,
            '$lt': current_timestamp
        },
        'src': src_host
    })
    hostnames = []
    for result in results:
        hostnames.append(result['dst'])
    utils.logger(
        'INFO',
        'List of hosts connected from {}: {}'.format(src_host, hostnames))


def get_max_connections_hostname():
    results = collection.aggregate([{
        '$match': {
            'timestamp': {
                '$gte': one_hour_before_ts,
                '$lt': current_timestamp
            }
        }
    }, {
        '$group': {
            '_id': '$src',
            'total': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'total': -1
        }
    }, {
        '$limit': 1
    }])
    for result in results:
        utils.logger(
            'INFO',
            'Host generating the most connections: {}'.format(result['_id']))


utils.logger('INFO',
             '[OPERATION] [CONNECTED TO] [{}]'.format(destination_host))
get_hosts_connected_to(destination_host)
utils.logger('INFO', '[OPERATION] [CONNECTED FROM] [{}]'.format(source_host))
get_hosts_receiving_from(source_host)
utils.logger('INFO', '[OPERATION] [GENERATOR] []')
get_max_connections_hostname()
