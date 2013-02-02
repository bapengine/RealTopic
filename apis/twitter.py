# -*- coding:utf-8 -*-
class TwitterSearchApi:
    def __init__(self, count = 10):
        self.url = "http://search.twitter.com/search.json"
        """
        page=   : page number to return
        rpp=    : number of tweets to return per a page, up to 100, maximum
        lang=ko : tweet language code
        """
        self.count = count
        self.rawdata = None
        self.content = None
        self.blacklist = ['daumtrend', 'pdragonman', 'navertrend', 'june2good', 'keyword_now']
        self.term = ""
    
    def search(self, keyword):
        import urllib, urllib2
        self.term = keyword
        try:
            data = {"rpp":self.count + 20, "q":keyword}
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
        for item in data["results"]:
            if len(self.content) > self.count:
                break
            if item['from_user'] in self.blacklist:
                continue
            temp = {}
            try:
                date = datetime.strptime(item["created_at"].split("+")[0].strip(), "%a, %d %b %Y %H:%M:%S")
            except:
                date = datetime.now()
            temp["date"] = date.strftime("%Y%m%d%H%M%S")
            temp["userid"] = item["from_user"]
            temp["name"] = item["from_user"]
            temp["article"] = item["text"]
            temp["url"] = "http://twitter.com/#!/%s/status/%s" % (item["from_user"], item["id_str"])
            self.content.append(temp)
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        from datetime import datetime
        output = {}
        output["service"] = "twitter"
        output["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
        output["contents"] = self.content
        output["keyword"] = self.term
        return output

import unittest
class TestTwitterSearchApi(unittest.TestCase):
    def setUp(self):
        self.obj = TwitterSearchApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_parse_json(self):
        testfile = "../data/twitter_search_sample.json"
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