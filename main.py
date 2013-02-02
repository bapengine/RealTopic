# -*- coding: utf-8 -*-
#!/usr/bin/env python

import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        import os, jinja2
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
        )
        
        template_values = {}
        template = jinja_environment.get_template('templates/main.html')
        self.response.out.write(template.render(template_values))

class GraphHandler(webapp2.RequestHandler):
    def get(self):
        import os, jinja2
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
        )
        
        template_values = {}
        template = jinja_environment.get_template('templates/graph.html')
        self.response.out.write(template.render(template_values))

class SnsHandler(webapp2.RequestHandler):
    def get(self, service, term, limit = None):
        if limit:
            limit = int(limit)
        else:
            limit = 10

        if not term or type(term) != str:
            self.response.write('')
            return

        if service == 'twitter':
            from apis import twitter
            search = twitter.TwitterSearchApi(limit)
        elif service == 'yozm':
            from apis import yozm
            search = yozm.YozmSearchApi(limit)
        elif service == 'me2day':
            from apis import me2day
            search = me2day.Me2daySearchApi(limit)
        elif service == 'all':
            from apis import twitter
            from apis import yozm
            from apis import me2day
            from apis import sns

            apis = []
            apis.append(twitter.TwitterSearchApi(limit))
            apis.append(yozm.YozmSearchApi(limit))
            apis.append(me2day.Me2daySearchApi(limit))
            sns = sns.SnsApi()
            for api in apis:
                api.search(term)
                api.parse_data()
                sns.append(api.get_object())
            self.response.write(sns.get_json())
            return
        else:
            search = None
        
        if search and term and type(term) == str:
            search.search(term)
            search.parse_data()
            self.response.write(search.get_json())
        else:
            self.response.write('')

class RankHandler(webapp2.RequestHandler):
    def get(self, service):
        if service == 'daum':
            from apis import daum
            rank = daum.DaumRankApi()
        elif service == 'naver':
            from apis import naver
            rank = naver.NaverRankApi()
        elif service == 'nate':
            from apis import nate
            rank = nate.NateRankApi()
        elif service == 'realtopic':
            from apis import daum
            from apis import naver
            from apis import nate
            from apis import rank
            apis = []
            apis.append(daum.DaumRankApi())
            apis.append(naver.NaverRankApi())
            apis.append(nate.NateRankApi())
            rank = rank.RankApi()
            for api in apis:
                if api and api.get_data_from_service():
                    api.parse_rawdata()
                    result = api.get_object()
                    rank.get_data_from_service(result['contents'])
        else:
            rank = None
        
        if rank and rank.get_data_from_service():
            rank.parse_rawdata()
            self.response.write(rank.get_json())
        else:
            self.response.write('')


class TaskHandler(webapp2.RequestHandler):
    def get(self):
        pass

routes = [
        (r'^/sns/([^/]+)/([^/]+)/?(\d*)$', SnsHandler),
        (r'^/rank/([^/]+)$', RankHandler),
        (r'^/task/([^/]+)$', TaskHandler),
        (r'^/graph$', GraphHandler),
        (r'^/$', MainHandler)
    ]
app = webapp2.WSGIApplication(routes, debug=True)