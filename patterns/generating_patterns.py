import copy


class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class AutoInstructor(User):
    pass


class Client(User):
    pass


class UserFactory:
    types = {
        'instructor': AutoInstructor,
        'client': Client
    }

    @classmethod
    def create_user(cls, type, first_name, last_name):
        return cls.types[type](first_name, last_name)


class PrototypeCourse:
    def clone(self):
        return copy.deepcopy(self)


class Course(PrototypeCourse):
    def __init__(self, name, category):
        self.name = name
        self.category = category


class OnlineFormat(Course):
    pass


class OfflineFormat(Course):
    pass


class FactoryCourse:
    types = {
        'offline': OfflineFormat,
        'online': OnlineFormat
    }

    @classmethod
    def create_course(cls, type, name, category):
        return cls.types[type](name, category)


class CategoryCourse:
    id = 0

    def __init__(self, name):
        self.id = CategoryCourse.id + 1
        self.name = name
        self.list_course = []


class Engine:
    def __init__(self):
        self.courses = []
        self.categories = []
        self.auto_instructor = []
        self.client = []

    @staticmethod
    def create_category(name):
        category = CategoryCourse(name)
        return category

    @staticmethod
    def create_course(type, name, category):
        course = FactoryCourse.create_course(type, name, category)
        return course


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __ceil__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name not in cls.__instance:
            cls.__instance[name] = super().__call__(*args, **kwargs)
        return cls.__instance[name]


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def logger(text):
        print('log >> ', text)