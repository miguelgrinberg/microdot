import logging
import os
import signal
from microdot import *  # noqa: F401, F403
from microdot import Microdot as BaseMicrodot
from microdot import Request


class Microdot(BaseMicrodot):
    def wsgi_app(self, environ, start_response):
        path = environ.get('SCRIPT_NAME', '') + environ.get('PATH_INFO', '')
        if 'QUERY_STRING' in environ and environ['QUERY_STRING']:
            path += '?' + environ['QUERY_STRING']
        headers = {}
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
            stream=environ['wsgi.input'])
        req.environ = environ

        res = self.dispatch_request(req)
        res.complete()

        reason = res.reason or ('OK' if res.status_code == 200 else 'N/A')
        start_response(
            str(res.status_code) + ' ' + reason,
            [(name, value) for name, value in res.headers.items()])
        return res.body_iter()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def shutdown(self):
        pid = os.getpgrp() if hasattr(os, 'getpgrp') else os.getpid()
        os.kill(pid, signal.SIGTERM)

    def run(self, host='0.0.0.0', port=5000, debug=False,
            **options):  # pragma: no cover
        try:
            from waitress import serve
        except ImportError:  # pragma: no cover
            raise RuntimeError('The run() method requires Waitress to be '
                               'installed (i.e. run "pip install waitress").')

        self.debug = debug
        if debug:
            logger = logging.getLogger('waitress')
            logger.setLevel(logging.INFO)

        serve(self, host=host, port=port, **options)
