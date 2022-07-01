import cProfile
import inspect
import types


class StageMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, types.FunctionType) and not attr_name.startswith('_'):
                attrs[attr_name] = cls.deco(attr_value)

        attrs['context'] = {}

        return super(StageMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def deco(cls, func):
        def wrapper(*args, **kwargs):
            print(f'before {func}')
            result = func(*args, **kwargs)
            print(f'after {func}')
            return result
        return wrapper


class Stage(metaclass=StageMeta):
    @classmethod
    def get_jobs(cls):
        jobs = []
        for (name, pointer) in inspect.getmembers(cls, predicate=inspect.isfunction):
            if name.startswith('job'):
                jobs.append(pointer)

        return jobs

    @classmethod
    def run(cls):
        for job in cls.get_jobs():
            job(cls)


class Executor:
    pass


class Work1(Stage):
    def job_3(self):
        print('job3')
        print(self.context)

    def job_1(self):
        print('job1')
        print(self.context)

    def job_2(self):
        print('job2')
        print(self.context)
