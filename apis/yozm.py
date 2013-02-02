# -*- coding:utf-8 -*-
class YozmSearchApi:
    def __init__(self, count = 10):
        self.url = "https://apis.daum.net/yozm/v1_0/search/timeline.json"
        self.count = count
        self.rawdata = None
        self.content = None
        self.term = ""
    
    def search(self, keyword):
        import urllib, urllib2
        self.term = keyword
        try:
            data = {"count":self.count, "q":keyword}
            data = urllib.urlencode(data)
            fd = urllib2.urlopen(self.url, data)
            self.rawdata = fd.read()
        except:
            self.rawdata = None
    
    def parse_data(self):
        import json
        from datetime import datetime
        try:
            data = json.loads(self.rawdata)
        except:
            return None
        
        self.content = []
        if type(data) != dict or not data.has_key("msg_list"):
            return
        
        for item in data["msg_list"]:
            temp = {}
            try:
                date = datetime.strptime(item["pub_date"], "%a, %d %b %Y %H:%M:%S KST")
            except:
                date = datetime.now()
            temp["date"] = date.strftime("%Y%m%d%H%M%S")
            temp["userid"] = item["user"]["url_name"]
            temp["name"] = item["user"]["nickname"]
            temp["article"] = item["plain_text"]
            temp["url"] = item["permanent_url"]
            self.content.append(temp)
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        from datetime import datetime
        output = {}
        output["service"] = "yozm"
        output["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
        output["contents"] = self.content
        output["keyword"] = self.term
        return output

import unittest
class TestYozmSearchApi(unittest.TestCase):
    def setUp(self):
        self.obj = YozmSearchApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_parse_json(self):
        testfile = "../data/yozm_search_sample.json"
        f = open(testfile, "r")
        self.obj.rawdata = f.read()
        self.obj.term = "선거"
        self.obj.parse_data()
        result = self.obj.get_json()
        self.assertTrue(type(result) == str)
    
    def test_search(self):
        term = "선거"
        self.obj.search(term)
        self.assertEquals(term, self.obj.term)
        self.assertTrue(type(self.obj.rawdata) == str)

if __name__ == '__main__':
    unittest.main()