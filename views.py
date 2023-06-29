from templator import render
from patterns.generating_patterns import Engine, Logger, routes_decorator


engine = Engine()
logger = Logger('new')
routes = {}


@routes_decorator('/', routes)
def index(request):
    context = {
        'title': 'Index',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'create_categories': '/create_categories/'
        },
    }
    return '200 OK', [render('index.html', context=context)]


@routes_decorator('/contacts/', routes)
def contacts(request):
    if request['POST_DATA']:
        print(request['POST_DATA'])
    if request['GET_DATA']:
        print(request['GET_DATA'])
    context = {
        'title': 'Contact',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'create_categories': '/create_categories/'
        },

    }
    return '200 OK', [render('contact.html', context=context)]


@routes_decorator('/categories/', routes)
def categories_view(request):
    context = {
        'title': 'Categories create',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'create_categories': '/create_categories/',
            'courses': '/courses/'
        },
        'list_category': engine.categories
    }
    return '200 OK', [render('view_categories.html', context=context)]


@routes_decorator('/create_categories/', routes)
def categories_create(request):
    context = {
        'title': 'Categories create',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'create_categories': '/create_categories/'
        },
    }
    if request['POST_DATA']:
        name_cat = engine.create_category(request['POST_DATA']['name_category'])
        engine.categories.append(name_cat)
        context['list_category'] = engine.categories
        logger.logger('Категория создана')
        return '302 FOUND', [render('index.html', context=context)]
    return '200 OK', [render('create_categories.html', context=context)]


@routes_decorator('/courses/', routes)
def courses_view(request):
    context = {
        'title': 'Courses',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'create_courses': '/create_course/'
        },
        'list_courses': engine.courses
    }
    return '200 OK', [render('view_courses.html', context=context)]


@routes_decorator('/create_course/', routes)
def courses_create(request):
    context = {
        'title': 'Categories create',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'create_categories': '/create_categories/'
        },
    }
    if request['POST_DATA']:
        course = engine.create_course(request['POST_DATA']['type'], request['POST_DATA']['name_course'], request['POST_DATA']['name_category'])
        engine.courses.append(course)
        context['list_courses'] = engine.courses
        logger.logger('Курс создан')
        return '302 FOUND', [render('index.html', context=context)]
    return '200 OK', [render('create_courses.html', context=context)]


def not_found(request):
    return '404 FOUND', [b'Page 404']