from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import json

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    # render_{METHOD} : string
    def render_GET(self, request):
        if request.path == u"/":
            return self.process(request)
        elif request.path == u"/count":
            return self.getCount(request)
        else:
            request.setHeader(b"content-type", b"html")
            return "404 : Not found"

    def process(self, request):
        request.setHeader(b"content-type", b"html")
        content = open(u"index.html").read()
        self.numberRequests += 1
        return content.encode("utf-8")

    def getCount(self, request):
        request.setHeader(b"content-type", b"json")
        user = request.args['user']
        data = { 'count' : self.numberRequests}
        if user != None:
            data['user'] = user
        return json.dumps(data)

endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(Counter()))
reactor.run()