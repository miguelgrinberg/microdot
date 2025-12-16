def patch(imp, return_value=None):
    """A very simple mock.patch implementation for MicroPython"""
    target = None
    mod = imp
    while mod:
        try:
            target = __import__(mod)
        except ImportError:
            mod, _ = mod.rsplit('.', 1)
            continue
        break
    items = imp.split('.')[1:]
    for item in items[:-1]:
        target = getattr(target, item)

    class Mock:
        def _mock(self, *args, **kwargs):
            return return_value

        def start(self):
            self._mocked = getattr(target, items[-1])
            setattr(target, items[-1], self._mock)

        def stop(self):
            setattr(target, items[-1], self._mocked)

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.stop()

    return Mock()
