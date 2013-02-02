# -*- coding:utf-8 -*-
"""
Parse NATE search keyword rank data

The result JSON data structure should be follow:

"service":"nate",
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
class NateRankApi:
    def __init__(self):
        self.url = "http://rkwd.nate.com/rank/search_rk.xml"
        self.rawdata = None
        self.date = None
    
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
        
        try:
            self.date = dom.getElementsByTagName("CONFIG")[0].getElementsByTagName("NOW_TIME")[0].childNodes[0].data + "00"
        except:
            self.date = None
        
        self.content = []
        i = 1
        for item in dom.getElementsByTagName("R"):
            if i >= 10:
                break
            temp = {}
            try:
                temp["keyword"] = item.getElementsByTagName("K")[0].childNodes[0].data
            except:
                temp["keyword"] = ""
            temp["ranking"] = i
            try:
                temp["fluctuation"] = item.getElementsByTagName("C")[0].childNodes[0].data
            except:
                temp["fluctuation"] = "0"
            try:
                temp["status"] = item.getElementsByTagName("M")[0].childNodes[0].data
            except:
                temp["status"] = ""
            
            self.content.append(temp)
            i += 1
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        output = {}
        output["service"] = "nate"
        if self.date:
            output["date"] = self.date
        else:
            from datetime import datetime
            output["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
        output["contents"] = self.content
        return output

import unittest
class TestNateRankApi(unittest.TestCase):
    def setUp(self):
        self.obj = NateRankApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_parse_json(self):
        testfile = "../data/nate_rank_sample.xml"
        f = open(testfile, "r")
        self.obj.rawdata = f.read()
        self.obj.parse_rawdata()
        result = self.obj.get_json()
        self.assertTrue(type(result) == str)
    
    def test_get_data_from_service(self):
        result = self.obj.get_data_from_service()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()