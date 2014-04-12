import logging
import traceback

log = logging.getLogger(__name__)


class Emitter(object):
    __constructed = False
    __callbacks = None

    def ensure_constructed(self):
        if self.__constructed:
            return

        self.__callbacks = {}
        self.__constructed = True

    def __wrap(self, callback, *args, **kwargs):
        def wrap(func):
            callback(func=func, *args, **kwargs)
            return func

        return wrap

    def on(self, event, func=None):
        if not func:
            # assume decorator, wrap
            return self.__wrap(self.on, event)

        log.debug('on(event: %s, func: %s)', repr(event), repr(func))

        self.ensure_constructed()

        if event not in self.__callbacks:
            self.__callbacks[event] = []

        # Bind callback to event
        self.__callbacks[event].append(func)

        return self

    def once(self, event, func=None):
        if not func:
            # assume decorator, wrap
            return self.__wrap(self.once, event)

        log.debug('once(event: %s, func: %s)', repr(event), repr(func))

        def once_callback(*args, **kwargs):
            self.off(event, once_callback)
            func(*args, **kwargs)

        self.on(event, once_callback)

        return self

    def off(self, event=None, func=None):
        log.debug('off(event: %s, func: %s)', repr(event), repr(func))

        self.ensure_constructed()

        if event and event not in self.__callbacks:
            return self

        if func and func not in self.__callbacks[event]:
            return self

        if event and func:
            self.__callbacks[event].remove(func)
        elif event:
            self.__callbacks[event] = []
        elif func:
            raise ValueError('"event" is required if "func" is specified')
        else:
            self.__callbacks = {}

        return self

    def emit(self, event, *args, **kwargs):
        log.debug('emit(event: %s, args: %s, kwargs: %s)', repr(event), repr(args), repr(kwargs))

        self.ensure_constructed()

        if event not in self.__callbacks:
            return

        for callback in self.__callbacks[event]:
            try:
                callback(*args, **kwargs)
            except Exception, e:
                log.warn('Exception raised in callback for "%s" %s', event, traceback.format_exc())

        return self


def on(emitter, event, func=None):
    return emitter.on(event, func)


def once(emitter, event, func=None):
    return emitter.once(event, func)


def off(emitter, event, func=None):
    return emitter.off(event, func)


def emit(emitter, event, *args, **kwargs):
    return emitter.emit(event, *args, **kwargs)
