from threading import local


class UnitOfWork:
    """
    Класс UnitOfWork позволяет отправить несколько запросов как один
    """
    current = local()

    def __init__(self):
        self.MapperRegistry = None
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        for i in self.new_objects:
            self.MapperRegistry.get_mapper(i).insert(i)

    def update_dirty(self):
        for i in self.dirty_objects:
            self.MapperRegistry.get_mapper(i).update(i)

    def delete_removed(self):
        for i in self.removed_objects:
            self.MapperRegistry.get_mapper(i).delete(i)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    """
    Класс DomainObject реализует действия модели
    """
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)