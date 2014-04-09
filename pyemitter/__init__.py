from functools import wraps


class Emitter(object):
    def on(self, event, func=None):
        if func:
            # TODO bind
            return func

        def wrap(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return wrap

    def once(self, event, func=None):
        pass

    def emit(self, event, *args):
        pass
