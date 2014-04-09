from functools import wraps


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

        def once_callback(*args, **kwargs):
            self.off(event, once_callback)
            func(*args, **kwargs)

        self.on(event, once_callback)

        return self

    def off(self, event=None, func=None):
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
        if event not in self.__callbacks:
            return

        for callback in self.__callbacks[event]:
            callback(*args, **kwargs)

        return self
