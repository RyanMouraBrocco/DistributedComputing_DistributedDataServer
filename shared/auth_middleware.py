from werkzeug.wrappers import Request, Response


class authMiddleware():

    def __init__(self, app, authKeys):
        self.app = app
        self.serverAuth = authKeys

    def __call__(self, environ, start_response):
        request = Request(environ)
        authKey = request.headers['auth']

        if authKey in self.serverAuth:
            return self.app(environ, start_response)

        unauthorizedResponse = Response(
            u'Unauthorized', mimetype='text/plain', status=401)
        return unauthorizedResponse(environ, start_response)
