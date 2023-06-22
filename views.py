from templator import render


def index(request):
    context = {
        'title': 'Index',
        'name_templates': {'index': '/', 'contact': '/contacts/'},
    }
    return '200 OK', [render('index.html', context=context)]


def contacts(request):
    if request['POST_DATA']:
        print(request['POST_DATA'])
    if request['GET_DATA']:
        print(request['GET_DATA'])
    context = {
        'title': 'Contact',
        'name_templates': {'index': '/', 'contact': '/contacts/'},

    }
    return '200 OK', [render('contact.html', context=context)]


def not_found(request):
    return '404 FOUND', [b'Page 404']