# -*- coding:utf-8 -*-
class SnsApi:
    def __init__(self):
        self.data = []
    
    def append(self, snsdata):
        self.data.append(snsdata)
    
    def get_object(self):
        import operator
        from datetime import datetime

        posts = []

        for l in self.data:
            service = l['service']
            for i in l['contents']:
                temp = {}
                temp['service'] = service
                temp['date'] = i['date']
                temp['userid'] = i['userid']
                temp['name'] = i['name']
                temp['article'] = i['article']
                temp['url'] = i['url']
                posts.append((i['date'], temp))

        result = sorted(posts, key=operator.itemgetter(1))

        output = {}
        output["service"] = "sns"
        output["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
        output["contents"] = []
        output["keyword"] = ""
        for i in result:
            output["contents"].append(i[1])
        return output
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

import unittest
class TestSnsApi(unittest.TestCase):
    def setUp(self):
        self.obj = SnsApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_get_json(self):
        import json
        testfile = "../data/output_twitter_sample.json"
        f = open(testfile, "r")
        self.obj.append(json.loads(f.read()))
        testfile = "../data/output_yozm_sample.json"
        f = open(testfile, "r")
        self.obj.append(json.loads(f.read()))
        testfile = "../data/output_me2day_sample.json"
        f = open(testfile, "r")
        self.obj.append(json.loads(f.read()))

        result = self.obj.get_object()
        self.assertTrue(type(result) == dict)
        if type(result) == dict:
            self.assertTrue(result.has_key('service'))
            self.assertTrue(result.has_key('date'))
            self.assertTrue(result.has_key('contents'))
            self.assertTrue(result.has_key('keyword'))
            self.assertTrue(result.has_key('contents'))
        
        result = self.obj.get_json()
        self.assertTrue(type(result) == str)

if __name__ == '__main__':
    unittest.main()