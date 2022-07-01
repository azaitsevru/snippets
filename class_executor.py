import inspect
import types
from datetime import datetime
from typing import Any

from json2object import json_2_object


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

    @classmethod
    def set_value(cls, name: str, data: Any):
        cls.context[inspect.stack()[1][3]].update({
            name: data
        })

    @classmethod
    def get_context(cls):
        return json_2_object(cls.context)


class Work1(Stage):
    def job_3(self):
        print(self.get_context().job_2.do_build)

    def job_1(self):
        pass

    def job_2(self):
        self.set_value('do_build', True)


w = Work1()
w.run()
# print(w.context)
