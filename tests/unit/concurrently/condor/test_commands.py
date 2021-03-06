# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently.condor.commands import split_list_into_chunks, query_status_for, change_job_priority

##__________________________________________________________________||
@pytest.fixture()
def mock_try_executing_until_succeed(monkeypatch):
    ret = mock.MagicMock(name='try_executing_until_succeed')
    module = sys.modules['alphatwirl.concurrently.condor.commands']
    monkeypatch.setattr(module, 'try_executing_until_succeed', ret)
    return ret

def test_query_status_for(mock_try_executing_until_succeed):
    ids = ['3158174', '3158175', '3158176', '3158177', '3158178', '3158179', '3158180', '3158181', '3158182', '3158183', '3158184', '3158185', '3158186', '3158187', '3158188', '3158189']
    n_at_a_time = 5
    query_status_for(ids, n_at_a_time=5)
    expected = [
        mock.call(['condor_q', '3158174', '3158175', '3158176', '3158177', '3158178', '-format', '%d.', 'ClusterId', '-format', '%d ', 'ProcId', '-format', '%-2s\n', 'JobStatus']),
        mock.call(['condor_q', '3158179', '3158180', '3158181', '3158182', '3158183', '-format', '%d.', 'ClusterId', '-format', '%d ', 'ProcId', '-format', '%-2s\n', 'JobStatus']),
        mock.call(['condor_q', '3158184', '3158185', '3158186', '3158187', '3158188', '-format', '%d.', 'ClusterId', '-format', '%d ', 'ProcId', '-format', '%-2s\n', 'JobStatus']),
        mock.call(['condor_q', '3158189', '-format', '%d.', 'ClusterId', '-format', '%d ', 'ProcId', '-format', '%-2s\n', 'JobStatus'])
    ]
    assert expected == mock_try_executing_until_succeed.call_args_list

def test_change_job_priority(mock_try_executing_until_succeed):
    ids = ['3158174', '3158175', '3158176', '3158177', '3158178', '3158179', '3158180', '3158181', '3158182', '3158183', '3158184', '3158185', '3158186', '3158187', '3158188', '3158189']
    n_at_a_time = 5
    change_job_priority(ids, n_at_a_time=5)
    expected = [
        mock.call(['condor_prio', '-p', '10', '3158174', '3158175', '3158176', '3158177', '3158178']),
        mock.call(['condor_prio', '-p', '10', '3158179', '3158180', '3158181', '3158182', '3158183']),
        mock.call(['condor_prio', '-p', '10', '3158184', '3158185', '3158186', '3158187', '3158188']),
        mock.call(['condor_prio', '-p', '10', '3158189'])
    ]
    assert expected == mock_try_executing_until_succeed.call_args_list

def test_split_list_into_chunks():
    ids = ['3158174', '3158175', '3158176', '3158177', '3158178', '3158179', '3158180', '3158181', '3158182', '3158183', '3158184', '3158185', '3158186', '3158187', '3158188', '3158189']
    expected = [['3158174', '3158175', '3158176', '3158177', '3158178'], ['3158179', '3158180', '3158181', '3158182', '3158183'], ['3158184', '3158185', '3158186', '3158187', '3158188'], ['3158189']]
    assert expected == split_list_into_chunks(ids, n=5)

##__________________________________________________________________||
