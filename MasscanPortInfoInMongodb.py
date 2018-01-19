#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea
# used masscan scan all port

import os
import sys
from pymongo import MongoClient

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def main():
    scanConfigure = masscanScanConfig()
    if not os.path.exists(scanConfigure.get('masscanPath')):
        sys.exit('Masscan Not Found!!!')
    if not os.path.exists(scanConfigure.get('scanIpFile')):
        sys.exit('Ip File Not Found!!!')
    masscanPar = "%s -p1-65535 -iL %s -oX %s --randomize-hosts --rate=%s" % (
        scanConfigure.get('masscanPath'), scanConfigure.get('scanIpFile'), scanConfigure.get('outLogFile'),
        scanConfigure.get('scanRate'))
    os.system(masscanPar)
    print 'Scanning Complete.'
    portInfo = analysisMasscanXml(scanConfigure.get('outLogFile'))
    if not portInfo:
        sys.exit('Out Log File Not Found!!!')
    mongodbConn = MongodbOperate()
    mongodbConn.InsertInfo(portInfo)
    print 'Insert Mongodb Complete.'


def masscanScanConfig():
    return {
        'masscanPath': '/usr/bin/masscan',
        'scanIpFile': '/tools/ip.txt',
        'outLogFile': '/tools/result.xml',
        'scanRate': '2000'
    }


def convertIpAddress(ipAddress):  # 这里可没有做正确IP检查
    numToIp = lambda x: '.'.join([str(x / (256 ** i) % 256) for i in range(3, -1, -1)])
    ipToNum = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    try:
        return numToIp(int(ipAddress))
    except:
        return ipToNum(ipAddress)


def analysisMasscanXml(xmlPath):
    if not os.path.exists(xmlPath):
        return False
    masscanResult = {
        'count': 0,
        'scanResult': None,
        'startTime': 0,
        'endTime': 0
    }
    tree = ET.ElementTree(file=xmlPath)
    root = tree.getroot()
    hostList = []
    for host in root:
        for address in host:
            if address.tag == 'address':
                tmpIp = '%s' % (convertIpAddress(address.attrib['addr']))  # Mongodb Error: can't have . in field names
                hostList.append(tmpIp)
                # hostList   ['167838072', '167838072', '167838072', '167838072', '167838072']
            '''
            if address.tag == 'finished':
                endTime = address.attrib['time']  # root[-1][0].attrib['time'] 可以替代这里
            '''
    hostList = list(set(hostList))  # 去重
    resultDict = {}.fromkeys(hostList, None)  # 创建结果字典
    masscanResult['count'] = resultDict.__len__()  # 所有主机数量
    masscanResult['startTime'] = root.attrib['start']  # 开始时间
    masscanResult['endTime'] = root[-1][0].attrib['time']  # 结束时间,Masscan version 1.0.3 支持
    '''
    for line in result_dict:    # 这里不重置会有BUG,后面用了try后可以去除
			result_dict[line] = []
    '''
    for host in root:
        ip_str, port_str = '', ''
        for address in host:
            if address.tag == 'address':
                ip_str = '%s' % (convertIpAddress(address.attrib['addr']))
            for port in address:
                port_str = port.attrib['portid']
                try:
                    resultDict[ip_str].append(port_str)
                except:
                    resultDict[ip_str] = []
                    resultDict[ip_str].append(port_str)
    masscanResult['scanResult'] = resultDict
    return masscanResult


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
            print str(e)
        self.db = self.conn[dbName]
        if dbUser and dbPassword:
            self.db.authenticate(dbUser, dbPassword)
        self.collection = self.db[collection]

    def InsertInfo(self, jsonValue):
        return self.collection.insert(jsonValue)


if __name__ == '__main__':
    main()
