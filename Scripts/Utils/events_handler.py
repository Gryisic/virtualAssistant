handlers = {}


def register_handler(event: str, func: callable):
    functions = handlers.get(event)

    if functions is None:
        handlers[event] = [func]
    else:
        functions.append(func)


def dispatch_event(event: str, *args, **kwargs):
    functions = handlers.get(event)

    if functions is None:
        raise ValueError(f'Unknown Event {event}')

    for function in functions:
        function(*args, **kwargs)
