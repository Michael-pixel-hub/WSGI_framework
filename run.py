from simple_wsgi import Application, data
from views import routes
from wsgiref.simple_server import make_server

application = Application(routes, data)

if __name__ == '__main__':
    server = make_server('localhost', 8000, application)
    print('Запуск сервера на 8000 порту...')
    server.serve_forever()