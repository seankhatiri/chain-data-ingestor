class CORSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def new_start_response(status, response_headers, exc_info=None):
            response_headers.append(('Access-Control-Allow-Origin', '*'))
            response_headers.append(('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'))
            response_headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
            return start_response(status, response_headers, exc_info)

        return self.app(environ, new_start_response)