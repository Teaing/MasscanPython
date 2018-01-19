#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import time
import logging
from pymongo import MongoClient

logging.basicConfig(
    level=logging.INFO,  # filename='/tmp/LogNew.log',
    format='[%(levelname)s] %(message)s',
)


def main():
    mongodbConn = MongodbOperate()
    bsonData = mongodbConn.GetLastOne()
    singleData = bsonData[0]
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(singleData['startTime']))))
    for singleLine in singleData['scanResult']:
        ipAddress = convertIpAddress(singleLine)
        portInfo = ','.join(singleData['scanResult'][singleLine])
        print ipAddress, '\t', portInfo


def convertIpAddress(ipAddress):  # 这里可没有做正确IP检查
    numToIp = lambda x: '.'.join([str(x / (256 ** i) % 256) for i in range(3, -1, -1)])
    ipToNum = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    try:
        return numToIp(int(ipAddress))
    except:
        return ipToNum(ipAddress)


class MongodbOperate():
    def __init__(self):
        dbHost = '127.0.0.1'
        dbPort = 17178
        dbName = 'MasscanItem'
        collection = 'PortInfo'
        dbUser = ''
        dbPassword = ''
        try:
            self.conn = MongoClient(dbHost, dbPort)
        except Exception, e:
            logging.info(str(e))
        self.db = self.conn[dbName]
        if dbUser and dbPassword:
            self.db.authenticate(dbUser, dbPassword)
        self.collection = self.db[collection]

    def GetLastOne(self):
        return self.collection.find().sort('_id', -1).limit(1)


if __name__ == '__main__':
    main()
