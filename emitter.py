class Emitter:
    def __init__(self):
        self._handlers = {}

    def on(self, event, handler):
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def off(self, event, handler=None):
        if event in self._handlers:
            if handler is None:
                del self._handlers[event]
            else:
                self._handlers[event] = [h for h in self._handlers[event] if h != handler]
                if not self._handlers[event]:
                    del self._handlers[event]

    def emit(self, event, data=None):
        if event in self._handlers:
            for handler in self._handlers[event]:
                if data is not None:
                    handler(data)
                else:
                    handler()
