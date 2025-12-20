# CSRF Example

This is a small example that demonstrates how the CSRF protection in Microdot
works.

## Running the example

Start by cloning the repostory or copying the two example files *app.py* and
*evil.py* to your computer. The only dependency these examples need to run is `microdot`, so create a virtual environment and run:

    pip install microdot

You need two terminals. On the first one, run:

    python app.py

To see the application open *http://localhost:5000* on your web browser. The
application allows you to make payments through a web form. Each payment that
you make reduces the balance in your account. Type an amount in the form field and press the "Issue Payment" button to see how the balance decreases.

Leave the application running. On the second terminal run:

    python evil.py

Open a second browser tab and navigate to *http://localhost:5001*. This 
application simulates a malicious web site that tries to steal money from your
account. It does this by sending a cross-site form submission to the above
application.

The application presents a form that fools you into thinking you can win some
money. Clicking the button triggers the cross-site request to the form in the
first application, with the payment amount set to $100.

Because the application has CSRF protection enabled, the cross-site request
fails.

If you want to see how the attack can succeed, open *app.py* in your editor and
comment out the line that creates the ``csrf`` object. Restart *app.py* in your
first terminal, then go back to the second browser tab and click the
"Win $100!" button again. You will now see that the form is submitted
successfully and your balance in the first application is decremented by $100.
