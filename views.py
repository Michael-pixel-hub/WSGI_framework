from templator import render


def index(request):
    context = [{'title': 'Dark'}]
    return '200 OK', [render('templates/index.html', context=context)]


def contacts(request):
    context = [{'title': 'Dark'}]
    return '200 OK', [render('templates/contact.html', context=context)]


def not_found(request):
    return '404 FOUND', [b'Page 404']