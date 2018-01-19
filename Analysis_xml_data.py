#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Tea
#Analysis Xml Data Mode

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def analysis_masscan_xml(xml_data):
	root = ET.fromstring(xml_data)
	host_list = []
	for host in root:
		for address in host:
			if address.tag == 'address':
				tmp_ip_str = address.attrib['addr']
				host_list.append(tmp_ip_str)
	host_list = list(set(host_list))
	masscan_result = {'count': 0,
	                  'scan': None,
	                  'time': ''
	                  }
	result_dict = {}.fromkeys(host_list, None)
	masscan_result['count'] = result_dict.__len__()
	masscan_result['time'] = root.attrib['start']
	for line in result_dict:  # 这里不重置会有BUG
		result_dict[line] = []
	for host in root:
		ip_str, port_str = '', ''
		for address in host:
			if address.tag == 'address':
				ip_str = address.attrib['addr']
			for port in address:
				port_str = int(port.attrib['portid'])
				result_dict[ip_str].append(port_str)
	masscan_result['scan'] = result_dict
	print masscan_result
	return masscan_result
