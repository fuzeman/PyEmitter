from pyemitter import Emitter
import logging
import time


class One(Emitter):
    def test(self):
        time.sleep(3)  # (do something)
        return self.emit_on('tested', 5, string='string')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    one = One()

    @one.test()
    def on_tested(number, string):
        print 'on_tested', number, string
