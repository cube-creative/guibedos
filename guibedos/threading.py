from Qt import QtCore


class Threadable(QtCore.QObject):
    """
    Implement loop_kick() or exec_()

    To be used with move_to_new_thread()
    """
    DEFAULT_SLEEP_MS = 100
    finished = QtCore.Signal()
    stopped = QtCore.Signal()

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self._running = False

    def stop(self):
        self._running = False
        self.stopped.emit()

    def loop_kick(self):
        QtCore.QThread.msleep(self.DEFAULT_SLEEP)

    def exec_(self):
        self._running = True
        while self._running:
            self.loop_kick()

        self.finished.emit()


def move_to_new_thread(threadable, signals=list()):
    """
    Creates a new `QThread`. Attaches the given instance of `Threadable` to it

    Give a list of (source, target) signals to be connected if needed

    Returns the new `QThread` instance
    """
    thread = QtCore.QThread()
    thread.started.connect(threadable.exec_)

    for source, target in signals:
        source.connect(target)

    threadable.stopped.connect(thread.quit)
    threadable.stopped.connect(thread.wait)
    threadable.finished.connect(thread.quit)
    threadable.finished.connect(thread.wait)

    threadable.moveToThread(thread)

    return thread
