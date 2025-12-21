Secure User Sessions
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/session.py>`_
       | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

   * - Required external dependencies
     - | CPython: `PyJWT <https://pyjwt.readthedocs.io/>`_
       | MicroPython: `jwt.py <https://github.com/micropython/micropython-lib/blob/master/python-ecosys/pyjwt/jwt.py>`_,
                      `hmac.py <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/hmac/hmac.py>`_

   * - Examples
     - | `login.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/sessions/login.py>`_

The session extension provides a secure way for the application to maintain
user sessions. The session data is stored as a signed cookie in the client's
browser, in `JSON Web Token (JWT) <https://en.wikipedia.org/wiki/JSON_Web_Token>`_
format.

To work with user sessions, the application first must configure a secret key
that will be used to sign the session cookies. It is very important that this
key is kept secret, as its name implies. An attacker who is in possession of
this key can generate valid user session cookies with any contents.

To initialize the session extension and configure the secret key, create a
:class:`Session <microdot.session.Session>` object::

    Session(app, secret_key='top-secret')

The :func:`with_session <microdot.session.with_session>` decorator is the
most convenient way to retrieve the session at the start of a request::

    from microdot import Microdot, redirect
    from microdot.session import Session, with_session

    app = Microdot()
    Session(app, secret_key='top-secret')

    @app.route('/', methods=['GET', 'POST'])
    @with_session
    async def index(req, session):
        username = session.get('username')
        if req.method == 'POST':
            username = req.form.get('username')
            session['username'] = username
            session.save()
            return redirect('/')
        if username is None:
            return 'Not logged in'
        else:
            return 'Logged in as ' + username

    @app.post('/logout')
    @with_session
    async def logout(req, session):
        session.delete()
        return redirect('/')

The :func:`save() <microdot.session.SessionDict.save>` and
:func:`delete() <microdot.session.SessionDict.delete>` methods are used to update
and destroy the user session respectively.
