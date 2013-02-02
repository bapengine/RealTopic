# -*- coding: utf-8 -*-
"""
Parse DAUM search keyword rank data

The result JSON data structure should be follow:

{
"service":"daum",
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

For an input data example, see /data/daum_rank_sample.json
"""
class DaumRankApi:
    def __init__(self):
        self.url = "http://stimg.search.daum-img.net/SearchTrend/section_total_rt_list.xml"
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
            nodes = dom.getElementsByTagName("word")
        except:
            return False
        
        try:
            self.date = dom.getElementsByTagName("realtime")[0].attributes.values()[0].value
        except:
            from datetime import datetime
            self.date = datetime.now().strftime("%Y%m%d%H%M%S")
        self.content = []
        for node in nodes:
            temp = {}
            temp["keyword"] = node.getElementsByTagName("keyword")[0].childNodes[0].data
            temp["ranking"] = node.getElementsByTagName("rank")[0].childNodes[0].data
            try:
                temp["fluctuation"] = node.getElementsByTagName("varinum")[0].childNodes[0].data
            except:
                temp["fluctuation"] = ""
            status = node.getElementsByTagName("vari")[0].childNodes[0].data
            if status == "1":
                temp["status"] = "+"
            elif status == "2":
                temp["status"] = "n"
            else:
                temp["status"] = "-"
            
            self.content.append(temp)
        return True
        
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        output = {}
        output["service"] = "daum"
        output["date"] = self.date
        output["contents"] = self.content
        return output

import unittest
class TestDaumRankApi(unittest.TestCase):
    def setUp(self):
        self.obj = DaumRankApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_parse_json(self):
        testfile = "../data/daum_rank_sample.xml"
        f = open(testfile, "r")
        self.obj.rawdata = f.read()
        self.assertTrue(self.obj.parse_rawdata())
        result = self.obj.get_json()
        self.assertTrue(type(result) == str)
    
    def test_get_data_from_service(self):
        result = self.obj.get_data_from_service()
        self.assertTrue(result)
    
    def test_all(self):
        result = self.obj.get_data_from_service()
        self.assertTrue(result)
        self.obj.parse_rawdata()
        result = self.obj.get_json()
        self.assertTrue(type(result) == str)

if __name__ == '__main__':
    unittest.main()