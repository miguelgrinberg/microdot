import os
import signal
from microdot import *  # noqa: F401, F403
from microdot import Microdot as BaseMicrodot, Request, NoCaseDict


class Microdot(BaseMicrodot):
    def __init__(self):
        super().__init__()
        self.embedded_server = False

    def wsgi_app(self, environ, start_response):
        """A WSGI application callable."""
        path = environ.get('SCRIPT_NAME', '') + environ.get('PATH_INFO', '')
        if 'QUERY_STRING' in environ and environ['QUERY_STRING']:
            path += '?' + environ['QUERY_STRING']
        headers = NoCaseDict()
        for k, v in environ.items():
            if k.startswith('HTTP_'):
                h = '-'.join([p.title() for p in k[5:].split('_')])
                headers[h] = v
        req = Request(
            self,
            (environ['REMOTE_ADDR'], int(environ.get('REMOTE_PORT', '0'))),
            environ['REQUEST_METHOD'],
            path,
            environ['SERVER_PROTOCOL'],
            headers,
            stream=environ['wsgi.input'],
            sock=environ.get('gunicorn.socket'))
        req.environ = environ

        res = self.dispatch_request(req)
        res.complete()

        reason = res.reason or ('OK' if res.status_code == 200 else 'N/A')
        header_list = []
        for name, value in res.headers.items():
            if not isinstance(value, list):
                header_list.append((name, value))
            else:
                for v in value:
                    header_list.append((name, v))
        start_response(str(res.status_code) + ' ' + reason, header_list)
        return res.body_iter()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def shutdown(self):
        if self.embedded_server:  # pragma: no cover
            super().shutdown()
        else:
            pid = os.getpgrp() if hasattr(os, 'getpgrp') else os.getpid()
            os.kill(pid, signal.SIGTERM)

    def run(self, host='0.0.0.0', port=5000, debug=False,
            **options):  # pragma: no cover
        """Normally you would not start the server by invoking this method.
        Instead, start your chosen WSGI web server and pass the ``Microdot``
        instance as the WSGI callable.
        """
        self.embedded_server = True
        super().run(host=host, port=port, debug=debug, **options)
