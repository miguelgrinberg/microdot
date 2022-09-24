from microdot import redirect, urlencode
from microdot_session import get_session, update_session


class LoginAuth:
    def __init__(self, login_url='/login'):
        super().__init__()
        self.login_url = login_url
        self.user_callback = self._accept_user

    def callback(self, f):
        self.user_callback = f

    def login_user(self, request, user_id):
        session = get_session(request)
        session['user_id'] = user_id
        update_session(request, session)
        return session

    def logout_user(self, request):
        session = get_session(request)
        session.pop('user_id', None)
        update_session(request, session)
        return session

    def redirect_to_next(self, request, default_url='/'):
        next_url = request.args.get('next', default_url)
        if not next_url.startswith('/'):
            next_url = default_url
        return redirect(next_url)

    def __call__(self, func):
        def wrapper(request, *args, **kwargs):
            session = get_session(request)
            if 'user_id' not in session:
                return redirect(self.login_url + '?next=' + urlencode(
                    request.url))
            if not self.user_callback(request, session['user_id']):
                return redirect(self.login_url + '?next=' + urlencode(
                    request.url))
            return func(request, *args, **kwargs)

        return wrapper

    def _accept_user(self, request, user_id):
        return True
