#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea
# used masscan scan all port

import os
import sys

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
    analysisMasscanXml(scanConfigure.get('outLogFile'))


def masscanScanConfig():
    return {
        'masscanPath': '/usr/bin/masscan',
        'scanIpFile': '/tools/tmp.txt',
        'outLogFile': '/tools/result.xml',
        'scanRate': '2000'
    }


def analysisMasscanXml(xmlPath):
    if not os.path.exists(xmlPath):
        return False
    masscanResult = {
        'count': 0,
        'scanResult': None,
        'time': ''
    }
    tree = ET.ElementTree(file=xmlPath)
    root = tree.getroot()
    hostList = []
    for host in root:
        for address in host:
            if address.tag == 'address':
                tmpIp = address.attrib['addr']
                hostList.append(tmpIp)
                # hostList   ['10.1.1.120', '10.1.1.120', '10.1.1.120', '10.1.1.120', '10.1.1.120']
    hostList = list(set(hostList))  # 去重
    resultDict = {}.fromkeys(hostList, None)  # 创建结果字典
    masscanResult['count'] = resultDict.__len__()  # 所有主机数量
    masscanResult['time'] = root.attrib['start']  # 开始时间
    '''
    for line in result_dict:    # 这里不重置会有BUG,后面用了try后可以去除
			result_dict[line] = []
    '''
    for host in root:
        ip_str, port_str = '', ''
        for address in host:
            if address.tag == 'address':
                ip_str = address.attrib['addr']
            for port in address:
                port_str = port.attrib['portid']
                try:
                    resultDict[ip_str].append(port_str)
                except:
                    resultDict[ip_str] = []
                    resultDict[ip_str].append(port_str)
    masscanResult['scanResult'] = resultDict
    return masscanResult


if __name__ == '__main__':
    main()
