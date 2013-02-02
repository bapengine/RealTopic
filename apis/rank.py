# -*- coding:utf-8 -*-
class Rank():
    def __init__(self):
        self.dataset = []

    """
    Create New Rank

    1. if KEYWORD is duplicated:
        weight +5
    2. if first word in KEYWORD is duplicated:
        weight +2
    3. if any word in KEYWORD is duplicated:
        weight +0.2
    """
    def push(self, rankdata):
        self.dataset.append(rankdata)

    def calc(self):
        import operator
        dic = {}        # dictionary of all words
        first_dic = {}    # dictionary of first words
        rank_dic = {}   # dictionary of keyword

        for serv in self.dataset:
            for row in serv:
                keyword = row['keyword']
                words = keyword.split()
                first = words[0]

                if rank_dic.has_key(keyword):   # exact all match
                    rank_dic[keyword] += 5
                elif first_dic.has_key(first):  # match only first word
                    orig = keyword
                    orig_cnt = len(orig.split())
                    for i in first_dic[first]:
                        cnt = len(i.split())
                        if cnt > orig_cnt:
                            orig = i
                            orig_cnt = cnt
                        try:
                            rank_dic[i] += 2
                        except:
                            continue
                    first_dic[first].append(keyword)
                    rank_dic[keyword] = len(first_dic[first]) * 2
                    if len(words) > 1:
                        w = orig.split()
                        w = w + [x for x in words if x not in w]
                        k = " ".join(w)
                        first_dic[first].append(k)
                        rank_dic[k] = len(first_dic[first]) * 2
                else:
                    point = 0
                    if row['status'] == '+':
                        point += 1
                    rank_dic[keyword] = point
                    first_dic[first] = [keyword]
            
                for w in words:
                    if dic.has_key(w):
                        if keyword not in dic[w]:
                            dic[w].append(keyword)
                        for i in dic[w]:
                            rank_dic[i] += 0.5
                    else:
                        dic[w] = [keyword]

        # sort
        rank = sorted(rank_dic.iteritems(), key=operator.itemgetter(1), reverse=True)

        return rank

class RankApi:
    def __init__(self):
        import datetime
        self.rank = Rank()
        self.content = []
        self.date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    def get_data_from_service(self, data = None):
        if not data:
            if len(self.rank.dataset) > 0:
                return True
            else:
                return False
        self.rank.push(data)
        return True
    
    def parse_rawdata(self):
        ranking = self.rank.calc()
        idx = 1
        for i in ranking:
            temp = {}
            temp["keyword"] = i[0]
            temp["ranking"] = idx
            temp["fluctuation"] = i[1]
            temp["status"] = ""
            self.content.append(temp)
            idx += 1
    
    def get_json(self):
        import json
        return json.dumps(self.get_object())

    def get_object(self):
        output = {}
        output["service"] = "rank"
        output["date"] = self.date
        output["contents"] = self.content
        return output

import unittest
class TestRankApi(unittest.TestCase):
    def setUp(self):
        self.obj = RankApi()
    
    def tearDown(self):
        self.obj = None
    
    def test_get_object(self):
        
        import json
        testfile = "../data/output_nate_sample.json"
        f = open(testfile, "r")
        r = json.loads(f.read())
        self.obj.rank.push(r['contents'])
        testfile = "../data/output_daum_sample.json"
        f = open(testfile, "r")
        r = json.loads(f.read())
        self.obj.rank.push(r['contents'])
        testfile = "../data/output_naver_sample.json"
        f = open(testfile, "r")
        r = json.loads(f.read())
        self.obj.rank.push(r['contents'])
        self.obj.parse_rawdata()
        """
        import daum
        import naver
        import nate
        apis = []
        apis.append(daum.DaumRankApi())
        apis.append(naver.NaverRankApi())
        apis.append(nate.NateRankApi())

        for api in apis:
            if api and api.get_data_from_service():
                api.parse_rawdata()
                result = api.get_object()
                self.obj.get_data_from_service(result['contents'])
        """
        self.obj.parse_rawdata()
        result = self.obj.get_object()
        self.assertTrue(type(result) == dict)
        if type(result) == dict:
            self.assertTrue(result.has_key("service"))
            self.assertTrue(result.has_key("date"))
            self.assertTrue(result.has_key("contents"))

class TestRank(unittest.TestCase):
    def setUp(self):
        self.obj = Rank()
    
    def tearDown(self):
        self.obj = None
    
    def test_calc(self):
        import json
        testfile = "../data/output_nate_sample.json"
        f = open(testfile, "r")
        r = json.loads(f.read())
        self.obj.push(r['contents'])
        testfile = "../data/output_daum_sample.json"
        f = open(testfile, "r")
        r = json.loads(f.read())
        self.obj.push(r['contents'])
        testfile = "../data/output_naver_sample.json"
        f = open(testfile, "r")
        r = json.loads(f.read())
        self.obj.push(r['contents'])
        
        self.assertTrue(len(self.obj.dataset) == 3)
        result = self.obj.calc()
        
        self.assertTrue(type(result) == list)
        
        if type(result) == list:
            for i in result:
                self.assertTrue(type(i) == tuple)
                self.assertTrue(len(i) == 2)

if __name__ == '__main__':
    unittest.main()