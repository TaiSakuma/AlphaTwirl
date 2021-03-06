# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from .mock import MockReader, MockSummarizer

from alphatwirl.collector import ToTupleListWithDatasetColumn

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return ToTupleListWithDatasetColumn(
        summaryColumnNames=('htbin', 'njetbin', 'n', 'nvar'),
        datasetColumnName = 'dataset'
    )

def test_repr(obj):
    repr(obj)

def test_example(obj):
    reader1 = MockReader(
        MockSummarizer(
            [
                (200, 2, 120, 240),
            ]))

    reader2 = MockReader(
        MockSummarizer(
            [
                (300, 2, 490, 980),
                (300, 3, 210, 420),
            ]))

    reader3 = MockReader(
        MockSummarizer(
            [
                (300, 2, 20, 40),
                (300, 3, 15, 30),
            ]))

    reader4 = MockReader(MockSummarizer([]))

    dataset_readers_list = [
        ('QCD', (reader1, reader2)),
        ('TTJets', (reader3, )),
        ('WJets', (reader4, )),
        ('ZJets', ( )),
    ]

    expected = [
        ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
        ('QCD', 200, 2, 120, 240),
        ('QCD', 300, 2, 490, 980),
        ('QCD', 300, 3, 210, 420),
        ('TTJets', 300, 2, 20, 40),
        ('TTJets', 300, 3, 15, 30)
    ]

    actual = obj.combine(dataset_readers_list)

    assert expected == actual

def test_combine_oneReader(obj):

    reader1 = MockReader(
        MockSummarizer(
            [
                (200, 2, 120, 240),
                (300, 2, 310, 620),
            ]))

    dataset_readers_list = [
        ('QCD', (reader1, )),
    ]

    expected = [
        ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
        ('QCD', 200, 2, 120, 240),
        ('QCD', 300, 2, 310, 620),
    ]

    actual = obj.combine(dataset_readers_list)

    assert expected == actual

def test_combine_all_empty_contents(obj):
    reader1 = MockReader(
        MockSummarizer(
            [ ]))

    reader2 = MockReader(
        MockSummarizer(
            [ ]))

    reader3 = MockReader(
        MockSummarizer(
            [ ]))

    dataset_readers_list = [
        ('QCD', (reader1, reader2)),
        ('TTJets', (reader3, )),
    ]

    expected = [
        ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
    ]

    actual = obj.combine(dataset_readers_list)

    assert expected == actual

def test_combine_empty_pairs(obj):
    dataset_readers_list = [ ]

    expected = None

    actual = obj.combine(dataset_readers_list)

    assert expected == actual

##__________________________________________________________________||
