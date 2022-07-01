import inspect
import types
from datetime import datetime


# datetime.datetime.fromtimestamp(ms/1000.0)
def func_deco(func):
    def wrapper(self, *args, **kwargs):
        self.context[func.__name__] = {
            'start': round(datetime.now().timestamp()*1000)
        }

        result = func(self, *args, **kwargs)

        self.context[func.__name__].update({
            'stop': round(datetime.now().timestamp()*1000)
        })
        return result
    return wrapper


class StageMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, types.FunctionType) and not attr_name.startswith('_'):
                attrs[attr_name] = func_deco(attr_value)

        attrs['context'] = {}

        return super(StageMeta, cls).__new__(cls, name, bases, attrs)


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


class Work1(Stage):
    def job_3(self):
        print('job3')

    def job_1(self):
        print('job1')

    def job_2(self):
        print('job2')


w = Work1()
w.run()
print(w.context)
