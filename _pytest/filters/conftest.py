import copy
import pytest
from functools import reduce
from dataclasses import dataclass


TESTS_TO_RUN = ['0001', '0002']


@dataclass
class Test:
    test: any
    is_run: bool


def check_test_to_delete(test: any):
    checks = map(lambda x: x in test.originalname, TESTS_TO_RUN)
    return Test(test=test, is_run=reduce(lambda x, y: x or y, checks))


def pytest_collection_finish(session):
    tests_for_delete = []
    for test in session.items:
        tests_for_delete.append(check_test_to_delete(test=test))

    for test in tests_for_delete:
        if not test.is_run:
            session.items.remove(test.test)

# def pytest_report_teststatus(report, config):
#     return ('HELLO+', 'OK+', 'foo')
