# -*- coding:utf-8 -*-
"""
Parse NAVER search keyword rank data

The result JSON data structure should be follow:

"service":"naver",
"date":"YYYYMMDDhhmmss",
"contents":
    [
        {
        "keyword":"blah",
        "ranking":"1",
        "fluctuation":"",
        "status":""
        },a
        ...
    ]
}

For an input data sample, see /data/nate_rank_sample.xml
"""
class NaverRankApi:
    def __init__(self):
        key = self.load_openapi_key()
        self.url = "http://openapi.naver.com/search?key=%s&query=nexearch&target=rank" % key
        self.rawdata = None
        self.date = None
    
    def load_openapi_key(self):
        from api_config import keys
        return keys["naver_openapi_key"]
    
    def get_data_from_service(self):
        import urllib2
        try:
            fd = urllib2.urlopen(self.url)
            self.rawdata = fd.read()
        except:
            self.rawdata = None
            return False
        return True
    
    def parse_rawdata(self):
        from xml.dom import minidom
        dom = minidom.parseString(self.rawdata)
        
        self.content = []
        for i in range(1, 11):
            try:
                node = dom.getElementsByTagName("R%d" % i)[0]
            except:
                continue
            temp = {}
            temp["ranking"] = i
            try:
                temp["keyword"] = node.getElementsByTagName("K")[0].childNodes[0].data
            except:
                temp["keyword"] = ""
            try:
                temp["status"] = node.getElementsByTagName("S")[0].childNodes[0].data
            except:
                temp["status"] = ""
            try:
                temp["fluctuation"] = node.getElementsByTagName("V")[0].childNodes[0].data
            except:
                temp["fluctuation"] = ""
            
            self.content.append(temp)
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        from datetime import datetime
        output = {}
        output["service"] = "naver"
        output["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
        output["contents"] = self.content
        return output

import unittest
class TestNaverRankApi(unittest.TestCase):
    def setUp(self):
        self.obj = NaverRankApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_parse_json(self):
        testfile = "../data/naver_rank_sample.xml"
        f = open(testfile, "r")
        self.obj.rawdata = f.read()
        self.obj.parse_rawdata()
        result = self.obj.get_json()
        self.assertTrue(type(result) == str)
    
    def test_get_data_from_service(self):
        result = self.obj.get_data_from_service()
        self.assertTrue(result)
    
    def test_load_openapi_key(self):
        key = self.obj.load_openapi_key()
        self.assertTrue(type(key) == str)

if __name__ == '__main__':
    unittest.main()