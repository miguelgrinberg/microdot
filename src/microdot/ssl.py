import ssl


def create_ssl_context(cert, key, **kwargs):
    """Create an SSL context to wrap sockets with.

    :param cert: The certificate to use. If it is given as a string, it is
                 assumed to be a filename. If it is given as a bytes object, it
                 is assumed to be the certificate data. In both cases the data
                 is expected to be in PEM format for CPython and in DER format
                 for MicroPython.
    :param key: The private key to use. If it is given as a string, it is
                assumed to be a filename. If it is given as a bytes object, it
                is assumed to be the private key data. in both cases the data
                is expected to be in PEM format for CPython and in DER format
                for MicroPython.
    :param kwargs: Additional arguments to pass to the ``ssl.wrap_socket``
                   function.

    Note: This function creates a fairly limited SSL context object to enable
    the use of certificates under MicroPython. It is not intended to be used in
    any other context, and in particular, it is not needed when using CPython
    or any other Python implementation that has native support for
    ``SSLContext`` objects. Once MicroPython implements ``SSLContext``
    natively, this function will be deprecated.
    """
    if hasattr(ssl, 'SSLContext'):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER, **kwargs)
        ctx.load_cert_chain(cert, key)
        return ctx

    if isinstance(cert, str):
        with open(cert, 'rb') as f:
            cert = f.read()
    if isinstance(key, str):
        with open(key, 'rb') as f:
            key = f.read()

    class FakeSSLSocket:
        def __init__(self, sock, **kwargs):
            self.sock = sock
            self.kwargs = kwargs

        def accept(self):
            client, addr = self.sock.accept()
            return (ssl.wrap_socket(client, cert=cert, key=key, **self.kwargs),
                    addr)

        def close(self):
            self.sock.close()

    class FakeSSLContext:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def wrap_socket(self, sock, **kwargs):
            all_kwargs = self.kwargs.copy()
            all_kwargs.update(kwargs)
            return FakeSSLSocket(sock, **all_kwargs)

    return FakeSSLContext(**kwargs)
