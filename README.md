## Masscan_Python
Analysis Masscan Xml Report   
Output:    
**{'count': 9, 'time': '1472196894', 'scan': {'192.168.19.30': ['80'], '192.168.19.202': ['21'], '192.168.19.180': ['80', '8080'], '192.168.19.158': ['22', '23', '80'], '192.168.19.185': ['80'],
'192.168.19.186': ['8080'], '192.168.19.162': ['8080', '80'], '192.168.19.170': ['21', '80'], '192.168.19.178': ['8080', '80']}}**


**Analysis_xml_data.py**  
**Analysis_xml_path.py**  
两个不同数据源的格式化扫描数据脚本


**Call_Masscan_Scan.py** 直接调用扫描器  
**MasscanPortInfoInMongodb.py** 调用扫描器扫描并将结果存入Mongodb  
**GetPortInfoFromMongodb.py**  从Mongodb中取出最新的扫描结果  