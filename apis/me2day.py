# -*- coding: utf-8 -*-
class Me2daySearchApi:
    def __init__(self, count = 10):
        self.url = "http://me2day.net/search.json"
        self.count = count
        self.rawdata = None
        self.content = None
        self.blacklist = ['search_now']
        self.term = ""
    
    def search(self, keyword):
        import urllib, urllib2
        self.term = keyword
        try:
            data = {"query":keyword}
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
        
        i = 0
        self.content = []
        for item in data:
            if i >= self.count:
                break

            if item["author"]["id"] in self.blacklist:
                continue
            temp = {}
            try:
                date = datetime.strptime(item["pubDate"].split("+")[0], "%Y-%m-%dT%H:%M:%S")
            except:
                date = datetime.now()
            temp["date"] = date.strftime("%Y%m%d%H%M%S")
            temp["userid"] = item["author"]["id"]
            temp["name"] = item["author"]["nickname"]
            temp["article"] = item["textBody"]
            temp["url"] = item["permalink"]
            self.content.append(temp)
            i += 1
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        from datetime import datetime
        output = {}
        output["service"] = "me2day"
        output["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
        output["contents"] = self.content
        output["keyword"] = self.term
        return output


import unittest
class TestMe2daySearchApi(unittest.TestCase):
    def setUp(self):
        self.obj = Me2daySearchApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_parse_json(self):
        testfile = "../data/me2day_search_sample.json"
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