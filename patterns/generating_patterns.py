import copy
from patterns.architectural_system_patterns import DomainObject
from sqlite3 import connect


# поведенческие паттерны

class Subject:
    def __init__(self):
        self.observers = []

    def append_observers(self, obs):
        self.observers.append(obs)

    def delete_observers(self, obs):
        self.observers.remove(obs)

    def notification_observers(self):
        for i in self.observers:
            i.update()


class Observer:
    def update(self):
        pass


class SmsNotifier(Observer):
    def update(self):
        print(f'Курс изменен')


class EmailNotifier(Observer):
    def update(self):
        print(f'Курс изменен')


# порождающие паттерны

class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.courses = []


class AutoInstructor(User):
    pass


class Student(User, DomainObject):
    pass


class UserFactory:
    types = {
        'instructor': AutoInstructor,
        'student': Student
    }

    @classmethod
    def create_user(cls, type, first_name, last_name):
        return cls.types[type](first_name, last_name)


class PrototypeCourse:
    def clone(self):
        return copy.deepcopy(self)


class Course(PrototypeCourse, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.students = []
        super().__init__()

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)


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
        self.student = []

    @staticmethod
    def create_category(name):
        category = CategoryCourse(name)
        return category

    @staticmethod
    def create_course(type, name, category):
        course = FactoryCourse.create_course(type, name, category)
        return course

    @staticmethod
    def create_student(first_name, last_name):
        student = UserFactory.create_user('student', first_name, last_name)
        return student

    def update_course(self, course, type_course, name_course, category_course):
        count = 0
        for i in self.courses:
            if i.name == course:
                del self.courses[count]
                course = FactoryCourse.create_course(type_course, name_course, category_course)
                self.courses.append(course)
                return course
            else:
                count += 1

    def get_course(self, course):
        for i in self.courses:
            if i.name == course:
                return i
            else:
                return None

    def get_student(self, student):
        for i in self.student:
            if i.first_name == student:
                return i
            else:
                return None


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


# структурные паттерны

def routes_decorator(path, routes):
    def decorator_(func):
        def inner():
            func()

        routes[path] = func
        return inner
    return decorator_

# архитектурные системные паттерны


connection = connect('patterns.sqlite')


class StudentMapper:
    """
    Класс StudentMapper передает данные между обьектом студента и базой данных
    """
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        students = self.cursor.fetchall()
        result = []
        for i in students:
            id, first_name, last_name = i
            student = Student(first_name, last_name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id_person):
        statement = f'SELECT id, first_name, last_name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id_person,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise Exception(f'{id_person} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (first_name, last_name) VALUES (?, ?)'
        self.cursor.execute(statement, (obj['first_name'], obj['last_name'],))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception('failed to add values to table')

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET first_name=? WHERE id=?'
        self.cursor.execute(statement, (obj.first_name, obj.id))
        statement = f'UPDATE {self.tablename} SET last_name=? WHERE id=?'
        self.cursor.execute(statement, (obj.last_name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception('the values in the table could not be changed')

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception('failed to delete the object')


class MapperRegistry:
    """
    Класс MapperRegistry представляет из себя реестр с мапперами, которые можно получить
    """
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)