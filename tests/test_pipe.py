from pyemitter import Emitter

e_one = Emitter()
e_two = Emitter()
e_three = Emitter()


def test_pipe():
    # One -> Two
    @e_two.on('two')
    def two():
        print 'two'

    e_one.pipe(['two'], e_two)
    e_one.emit('two')

    # One -> Three
    e_one.pipe('three', e_three)

    @e_three.on('three')
    def three():
        print 'three'

    e_one.emit('three')


if __name__ == '__main__':
    test_pipe()
