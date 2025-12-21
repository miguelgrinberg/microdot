User Logins
~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `login.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/auth.py>`_
       | `session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/session.py>`_
       | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_
   * - Required external dependencies
     - | CPython: `PyJWT <https://pyjwt.readthedocs.io/>`_
       | MicroPython: `jwt.py <https://github.com/micropython/micropython-lib/blob/master/python-ecosys/pyjwt/jwt.py>`_,
                      `hmac.py <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/hmac/hmac.py>`_
   * - Examples
     - | `login.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/login/login.py>`_

The login extension provides user login functionality. The logged in state of
the user is stored in the user session cookie, and an optional "remember me"
cookie can also be added to keep the user logged in across browser sessions.

To use this extension, create instances of the
:class:`Session <microdot.session.Session>` and :class:`Login <microdot.login.Login>`
class::

    Session(app, secret_key='top-secret!')
    login = Login()

The ``Login`` class accept an optional argument with the URL of the login page.
The default for this URL is */login*.

The application must represent users as objects with an ``id`` attribute. A
function decorated with ``@login.user_loader`` is used to load a user object::

    @login.user_loader
    async def get_user(user_id):
        return database.get_user(user_id)

The application must implement the login form. At the point in which the user
credentials have been received and verified, a call to the
:func:`login_user() <microdot.login.Login.login_user>` function must be made to
record the user in the user session::

    @app.route('/login', methods=['GET', 'POST'])
    async def login(request):
        # ...
        if user.check_password(password):
            return await login.login_user(request, user, remember=remember_me)
        return redirect('/login')

The optional ``remember`` argument is used to add a remember me cookie that
will log the user in automatically in future sessions. A value of ``True`` will
keep the log in active for 30 days. Alternatively, an integer number of days
can be passed in this argument.

Any routes that require the user to be logged in must be decorated with
:func:`@login <microdot.login.Login.__call__>`::

    @app.route('/')
    @login
    async def index(request):
        # ...

Routes that are of a sensitive nature can be decorated with
:func:`@login.fresh <microdot.login.Login.fresh>`
instead. This decorator requires that the user has logged in during the current
session, and will ask the user to logged in again if the session was
authenticated through a remember me cookie::

    @app.get('/fresh')
    @login.fresh
    async def fresh(request):
        # ...

To log out a user, the :func:`logout_user() <microdot.auth.Login.logout_user>`
is used::

    @app.post('/logout')
    @login
    async def logout(request):
        await login.logout_user(request)
        return redirect('/')
