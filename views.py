from templator import render
from patterns.generating_patterns import Engine, Logger, routes_decorator, EmailNotifier


engine = Engine()
logger = Logger('new')
routes = {}
email_observer = EmailNotifier()


@routes_decorator('/', routes)
def index(request):
    context = {
        'title': 'Index',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'students': '/students/',
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
            'students': '/students/',
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
            'students': '/students/',
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
            'students': '/students/',
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
            'students': '/students/',
            'create_courses': '/create_course/',
            'update_courses': '/update_course/'
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
            'students': '/students/',
            'create_categories': '/create_categories/'
        },
    }
    if request['POST_DATA']:
        course = engine.create_course(request['POST_DATA']['type'], request['POST_DATA']['name_course'], request['POST_DATA']['name_category'])
        course.append_observers(email_observer)
        engine.courses.append(course)
        context['list_courses'] = engine.courses
        logger.logger('Курс создан')
        return '302 FOUND', [render('index.html', context=context)]
    return '200 OK', [render('create_courses.html', context=context)]


@routes_decorator('/update_course/', routes)
def courses_update(request):
    context = {
        'title': 'Categories create',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'students': '/students/',
        },
        'course': engine.get_course(request['GET_DATA']['name'])
    }
    if request['POST_DATA']:
        course = engine.update_course(request['GET_DATA']['name'], request['POST_DATA']['type'], request['POST_DATA']['name_course'], request['POST_DATA']['name_category'])
        course.append_observers(email_observer)
        course.notification_observers()
        context['list_courses'] = engine.courses
        logger.logger('Курс изменен')
        return '302 FOUND', [render('index.html', context=context)]
    return '200 OK', [render('update_courses.html', context=context)]


@routes_decorator('/students/', routes)
def students_view(request):
    context = {
        'title': 'Students view',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'students': '/students/',
            'create_student': '/create_student/',
            'add_student': '/add_student/'
        },
        'list_students': engine.student
    }
    return '200 OK', [render('view_students.html', context=context)]


@routes_decorator('/create_student/', routes)
def students_create(request):
    context = {
        'title': 'Students view',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'students': '/students/',
        },
    }
    if request['POST_DATA']:
        student = engine.create_student(request['POST_DATA']['first_name'], request['POST_DATA']['last_name'])
        engine.student.append(student)
        context['list_students'] = engine.student
        logger.logger('Студент создан')
        return '302 FOUND', [render('index.html', context=context)]
    return '200 OK', [render('create_student.html', context=context)]


@routes_decorator('/add_student/', routes)
def student_add_course(request):
    context = {
        'title': 'Students view',
        'name_templates': {
            'index': '/',
            'contact': '/contacts/',
            'categories': '/categories/',
            'students': '/students/',
        },
        'list_courses': engine.courses,
        'list_students': engine.student
    }
    if request['POST_DATA']:
        course = engine.get_course(request['POST_DATA']['course'])
        student = engine.get_student(request['POST_DATA']['student'])
        if course:
            course.add_student(student)
        context['list_students'] = engine.student
        logger.logger('Студент создан')
        return '302 FOUND', [render('view_students.html', context=context)]
    return '200 OK', [render('add_student_in_course.html', context=context)]


def not_found(request):
    return '404 FOUND', [b'Page 404']