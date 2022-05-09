from werkzeug.wrappers import Request, Response


class authMiddleware():

    def __init__(self, app):
        self.app = app
        self.serverAuth = [
            "SNDFISFNEI82FH28FN392HFBR3289FH32FN2FJ3290",
            "PDIOFNSUIDCN298904Y3FBSBV87DW0GCSUB78GW178",
            "FASNOFSI81D01BUABCS7Q8S087ACGSABCS7AC80AGC"
        ]

    def __call__(self, environ, start_response):
        request = Request(environ)
        authKey = request.headers['auth']

        if authKey in self.serverAuth:
            return self.app(environ, start_response)

        unauthorizedResponse = Response(u'Unauthorized', mimetype= 'text/plain', status=401)
        return unauthorizedResponse(environ, start_response)
