import sys
import datetime
from pymongo.errors import OperationFailure
from pymongo import MongoClient


def logger(level, log):
    print('[{}] - {} - '.format(level, datetime.datetime.now()) + log)


def connection(user, secret):
    try:
        client = MongoClient('mongodb://%s:%s@localhost:27017' %
                             (user, secret))
        try:
            logger('INFO', '[DB] [CONNECTION] [START]')
            result = client.admin.command("ismaster")
            logger('INFO', '[DB] [CONNECTION] [SUCCESS]')
        except OperationFailure:
            logger('ERROR', '[DB] [CONNECTION] [AUTHENTICATION]')
            logger('INFO', '[PROCESS] [END] [-1]')
            sys.exit()
    except Exception as e:
        logger('ERROR', '[DB] [CONNECTION] [{}]'.format(e))
        logger('INFO', '[PROCESS] [END] [-1]')
        sys.exit()
    return client