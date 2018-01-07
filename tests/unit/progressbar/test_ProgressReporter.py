# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import time

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReporter

##__________________________________________________________________||
@pytest.fixture()
def queue():
    return mock.MagicMock()

@pytest.fixture()
def mocktime():
    return mock.MagicMock(return_value = 1000.0)

@pytest.fixture()
def reporter(queue, mocktime, monkeypatch):
    monkeypatch.setattr(time, 'time', mocktime)
    ret = ProgressReporter(queue)
    return ret

@pytest.fixture()
def report():
    return mock.MagicMock(**{'last.return_value': False, 'first.return_value': False})

@pytest.fixture()
def report_last():
    return mock.MagicMock(**{'last.return_value': True, 'first.return_value': False})

@pytest.fixture()
def report_first():
    return mock.MagicMock(**{'last.return_value': False, 'first.return_value': True})

##__________________________________________________________________||
def test_repr(reporter):
    repr(reporter)

def test_report(reporter, queue, mocktime, report):

    assert 1000.0 == reporter.lastTime

    mocktime.return_value = 1000.2
    reporter._report(report)

    assert [mock.call(report)] == queue.put.call_args_list

    assert 1000.2 == reporter.lastTime

def test_needToReport(reporter, queue, mocktime, report, report_last,
                      report_first):

    interval = reporter.interval
    assert 0.1 == interval

    assert 1000.0 == reporter.lastTime

    # before the interval passes
    mocktime.return_value += 0.1*interval
    assert not reporter._needToReport(report)

    # the first report before the interval passes
    assert reporter._needToReport(report_first)

    # the last report before the interval passes
    assert reporter._needToReport(report_last)

    # after the interval passes
    mocktime.return_value += 1.2*interval
    assert reporter._needToReport(report)

    assert 1000.0 == reporter.lastTime

##__________________________________________________________________||
