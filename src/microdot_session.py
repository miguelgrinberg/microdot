import jwt

secret_key = None


def set_session_secret_key(key):
    global secret_key
    secret_key = key


def get_session(request):
    global secret_key
    if not secret_key:
        raise ValueError('The session secret key is not configured')
    session = request.cookies.get('session')
    if session is None:
        return {}
    try:
        session = jwt.decode(session, secret_key, algorithms=['HS256'])
    except jwt.exceptions.PyJWTError:  # pragma: no cover
        raise
        return {}
    return session


def update_session(request, session):
    if not secret_key:
        raise ValueError('The session secret key is not configured')

    encoded_session = jwt.encode(session, secret_key, algorithm='HS256')

    @request.after_request
    def _update_session(request, response):
        response.set_cookie('session', encoded_session, http_only=True)
        return response


def delete_session(request):
    @request.after_request
    def _delete_session(request, response):
        response.set_cookie('session', '', http_only=True,
                            expires='Thu, 01 Jan 1970 00:00:01 GMT')
        return response


def with_session(f):
    def wrapper(request, *args, **kwargs):
        return f(request, get_session(request), *args, **kwargs)

    for attr in ['__name__', '__doc__', '__module__', '__qualname__']:
        try:
            setattr(wrapper, attr, getattr(f, attr))
        except AttributeError:  # pragma: no cover
            pass
    return wrapper
