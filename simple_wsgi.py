from wsgiref.simple_server import make_server
from urls import routes
from views import not_found


def info_request(request):
    request['secret'] = '112'


data = [info_request, ]


class Application:
    def __init__(self, routes, data):
        self.route = routes
        self.data = data

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if '/' not in path[-1]:
            path = path + '/'
        if path in self.route:
            func_result = self.route[path]
        else:
            func_result = not_found
        request = {}
        for i in environ:
            request[i] = environ[i]
        for i in self.data:
            i(request)
        code, answer = func_result(request)
        start_response(code, [('Content-Type', 'text/html')])
        return answer


application = Application(routes, data)

if __name__ == '__main__':
    server = make_server('localhost', 8000, application)
    print('Запуск сервера на 8000 порту...')
    server.serve_forever()
