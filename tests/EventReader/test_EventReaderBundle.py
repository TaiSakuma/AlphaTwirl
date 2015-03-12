from AlphaTwirl.EventReader import EventReaderBundle, EventLoopRunner, EventLoop
import unittest


##____________________________________________________________________________||
class MockEvent(object):
    def __init__(self, id):
        self.id = id

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##____________________________________________________________________________||
class MockReaderPackage(object):
    def __init__(self):
        self._readers = [ ]
        self.collected = False

    def make(self, name):
        reader = MockReader(name)
        self._readers.append(reader)
        return reader

    def collect(self):
        self.collected = True

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self._events = None

##____________________________________________________________________________||
class MockEventLoopRunner(object):
    def __init__(self):
        self.began = False
        self.ended = False
        self.eventLoop = None

    def begin(self):
        self.began = True

    def run(self, eventLoop):
        self.eventLoop = eventLoop

    def end(self):
        self.ended = True

##____________________________________________________________________________||
class TestEventReaderEventReaderBundle(unittest.TestCase):

    def setUp(self):
        self.eventBuilder = MockEventBuilder()
        self.eventLoopRunner = MockEventLoopRunner()
        self.bundle = EventReaderBundle(self.eventBuilder, self.eventLoopRunner)

    def test_addReaderPackage(self):
        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

    def test_begin_end(self):

        self.assertFalse(self.eventLoopRunner.began)
        self.assertFalse(self.eventLoopRunner.ended)
        self.bundle.begin()
        self.assertTrue(self.eventLoopRunner.began)
        self.assertFalse(self.eventLoopRunner.ended)
        self.bundle.end()
        self.assertTrue(self.eventLoopRunner.began)
        self.assertTrue(self.eventLoopRunner.ended)

    def test_read(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        self.bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"

        self.assertIsNone(self.eventLoopRunner.eventLoop)
        self.bundle.read(component1)
        self.assertIsInstance(self.eventLoopRunner.eventLoop, EventLoop)
        self.assertIs(self.eventBuilder, self.eventLoopRunner.eventLoop.eventBuilder)
        self.assertIs(component1, self.eventLoopRunner.eventLoop.component)
        self.assertIs("compName1", self.eventLoopRunner.eventLoop.component.name)
        self.assertEqual(package1._readers, self.eventLoopRunner.eventLoop.readers)

##____________________________________________________________________________||
