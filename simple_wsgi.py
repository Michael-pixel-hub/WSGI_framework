from views import not_found


def info_request(request):
    request['secret'] = '112'


data = [info_request, ]


def deserializer_data(data_request: str) -> dict:
    result = {}
    if data_request:
        list_data_post = data_request.split('&')
        for i in list_data_post:
            k, v = i.split('=')
            result[k] = v
    return result


def check_slash(path: str) -> str:
    if '/' not in path[-1]:
        path = path + '/'
    return path


def check_path(path: str, route: dict):
    if path in route:
        func_result = route[path]
    else:
        func_result = not_found
    return func_result


def check_data_post(request_data: dict) -> bytes:
    post_data_len = request_data['CONTENT_LENGTH']
    result = int(post_data_len) if post_data_len else 0
    post_data = b''
    if result > 0:
        post_data = request_data['wsgi.input'].read(result)
    return post_data


def decode_data_post(data_post: bytes) -> dict:
    result = {}
    if data_post:
        decode_data_post = data_post.decode()
        result = deserializer_data(decode_data_post)
    return result


class Application:
    def __init__(self, routes, data):
        self.route = routes
        self.data = data

    def __call__(self, environ, start_response):
        path = check_slash(environ['PATH_INFO'])
        func_result = check_path(path, self.route)
        request = {}
        for i in environ:
            request[i] = environ[i]
        for i in self.data:
            i(request)
        post_data_byte = check_data_post(environ)
        post_data = decode_data_post(post_data_byte)
        get_data = deserializer_data(environ['QUERY_STRING'])
        request['POST_DATA'] = post_data
        request['GET_DATA'] = get_data
        code, answer = func_result(request)
        start_response(code, [('Content-Type', 'text/html')])
        return answer
