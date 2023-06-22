from views import not_found


def info_request(request: dict):
    """
    Добавляет информацию в request

    :param request: словарь, который будет передаваться в views
    :return: 'Ok'
    """
    request['secret'] = '112'
    return 'Ok'


def parse_data(data_request: str) -> dict:
    """
    Парсит и переводит параметры пользователя из строки в словарь

    :param data_request: str
        параметры пользователя
    :return: dict
        параметры пользователя
    """
    result = {}
    if data_request:
        list_data_post = data_request.split('&')
        for i in list_data_post:
            k, v = i.split('=')
            result[k] = v
    return result


def check_slash(path: str) -> str:
    """
    Возвращает правильный url-адрес, добавляя слеш в конце если надо

    :param path: url-адрес пользователя
    :return: путь со слешем на конце
    """
    if '/' not in path[-1]:
        path = path + '/'
    return path


def check_path(path: str, route: dict):
    """
    Проверяет налачие точки входа на данный url-адрес

    :param path: url-адрес пользователя
    :param route: словарь адресов, которые обрабатываются
    :return: функция-обработчик
    """
    if path in route:
        func_result = route[path]
    else:
        func_result = not_found
    return func_result


def check_data_post(request_data: dict) -> bytes:
    """
    Проверяет наличие тела (параметров) в запросе пользователя

    :param request_data: запрос пользователя в виде заголовков (словаря)
    :return: тело запроса (параметры пользователя) в байтах
    """
    post_data_len = request_data['CONTENT_LENGTH']
    result = int(post_data_len) if post_data_len else 0
    post_data = b''
    if result > 0:
        post_data = request_data['wsgi.input'].read(result)
    return post_data


def deserialization_data(data_post: bytes) -> dict:
    """
    Десериализует параметры пользователя

    :param data_post: bytes
        параметры пользователя
    :return: dict
        десериализованные параметры пользователя
    """
    result = {}
    if data_post:
        decode_data_post = data_post.decode()
        result = parse_data(decode_data_post)
    return result


class Application:
    """
    Класс Application принимает сообщение от wsgi-сервера, обрабатывает его и возвращает ответ
    """
    def __init__(self, routes, data):
        self.route = routes
        self.data = data

    def __call__(self, environ, start_response):
        path = check_slash(environ['PATH_INFO'])
        func_result = check_path(path, self.route)
        request = {}
        # добавляем environ в request
        for i in environ:
            request[i] = environ[i]
        # добавляем активируем функции из data
        for i in self.data:
            i(request)
        post_data_byte = check_data_post(environ)
        post_data = deserialization_data(post_data_byte)
        get_data = parse_data(environ['QUERY_STRING'])
        request['POST_DATA'] = post_data
        request['GET_DATA'] = get_data
        code, answer = func_result(request)
        start_response(code, [('Content-Type', 'text/html')])
        return answer


data = [info_request, ]