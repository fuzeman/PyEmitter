from pyemitter import Emitter

emitter = Emitter()


def test_call():
    def cb_one():
        print 'cb_one'
    emitter.on('cb_one', cb_one)

    callbacks = emitter._Emitter__callbacks

    assert 'cb_one' in callbacks
    assert cb_one in callbacks['cb_one']


def test_decorator():
    @emitter.on('cb_two')
    def cb_two():
        print 'cb_two'

    callbacks = emitter._Emitter__callbacks

    assert 'cb_two' in callbacks
    assert cb_two in callbacks['cb_two']
