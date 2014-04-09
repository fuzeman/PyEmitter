from threading import Lock
from pyemitter import Emitter


def cb_lock():
    lock = Lock()
    lock.acquire()
    return lock


def test_fires():
    emitter = Emitter()

    @emitter.on('test')
    def callback(fired):
        fired.release()

    # Ensure first emit fires
    fired = cb_lock()
    emitter.emit('test', fired)
    assert fired.acquire(False)

    # Ensure second emit fires
    fired = cb_lock()
    emitter.emit('test', fired)
    assert fired.acquire(False)

def test_fires_once():
    emitter = Emitter()

    @emitter.once('test')
    def callback(fired):
        fired.release()

    # Ensure first emit fires
    fired = cb_lock()
    emitter.emit('test', fired)
    assert fired.acquire(False)

    # Ensure second emit *FAILS*
    fired = cb_lock()
    emitter.emit('test', fired)
    assert not fired.acquire(False)
