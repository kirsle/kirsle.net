# Simple CAS Protocol

[Central Authentication Service](https://apereo.github.io/cas/5.1.x/protocol/CAS-Protocol-Specification.html)
is a very simple Single Sign On protocol. Here's a quick tl;dr. how it works.

CAS involves three parties:

* A **client web browser** that wants to log in to your web application.
* A **web application** that wants to authenticate the client browser by using CAS.
* The **CAS server** that provides the single sign-on for users (stores their email
  address and password in a database).

## How it looks to the Web Application

1. Client web browser visits your web application and clicks a "Log In" button.
2. The web application issues an HTTP redirect to send the user to the CAS server's
   `/login` URL, including a query string parameter of the URL that CAS should
   send the user back to after they authenticate with CAS (a "service URL").
   * e.g.: `https://accounts.cas.com/login?service=https://your-application.com/login-complete`
3. CAS server presents the user with a login screen to enter their email and
   password. Upon successful login with CAS, CAS redirects the user to your
   service's URL along with a `ticket` query string parameter.
4. The web application's back-end code sends the `ticket` and its `service` URL
   to the CAS server to verify, by making an HTTP request to the `/validate`
   URL on CAS.
   * e.g.: `https://accounts.cas.com/verify?service=https://your-application.com/login-complete&ticket=1A2B3C`
5. Assuming the login with CAS was successful and the ticket is valid and correct,
   the CAS `/verify` URL returns a simple plain text response:
   `yes\nname@example.com` -- it says "yes" or "no" on the first line indicating
   if the ticket was correct, and the user's email address on the second line if
   the login was successful.

The web application now has the user's verified e-mail address confirmed through
CAS and could set session cookies to mark them "logged in" on the application,
create a web application account using their e-mail address, etc.

Example web app code in Python/Flask:

```python
from flask import Flask, redirect, url_for, session
import requests

app = Flask(__name__)

# Config variables.
CAS_SERVER = "https://accounts.cas.com"
CAS_LOGIN_URL = CAS_SERVER + "/login"
CAS_VERIFY_URL = CAS_SERVER + "/validate"

# The service URL that CAS will send the user back to, on our
# web application, after they authenticate with CAS.
SERVICE_URL = "https://your-application.com/login-complete"
# (Python/Flask could determine this URL dynamically as follows):
# SERVICE_URL = url_for("login_complete", _external=True)

@app.route("/")
def index_page():
    return """
      <a href="/login">Sign in to this web application</a>
    """

@app.route("/login")
def login_begin():
    # Start of the login process: redirect the user to CAS to authenticate.
    # URL is like: https://accounts.cas.com/login?service=https://your-application.com/login-complete
    return redirect(
        CAS_LOGIN_URL + "?service=" + CAS_VERIFY_URL
    )

@app.route("/login-complete")
def login_complete():
    # This HTTP request includes a "ticket" query parameter.
    ticket = request.args.get("ticket")

    # Call the CAS server to verify the ticket.
    r = requests.get(
        CAS_VERIFY_URL,
        params={
            "ticket": ticket,
            "service": SERVICE_URL,
        }
    )
    # omitted: handle http errors, check if `r.ok` or r.status_code is 200, etc.

    # Read the response from CAS validate url.
    data = r.text   # looks like "yes\nname@example.com" or "no\n"
    lines = data.split("\n")

    # Successful?
    if lines[0] == "yes":
        email = lines[1]

        # User is authenticated, mark them logged in or whatever.
        session["logged_in"] = True
        session["user_email"] = email
        return "Login successful, welcome %s!" % email

    return "Login failed."
```

## How it looks to CAS Server

The CAS Server itself is just a simple web application that has user accounts
and session cookies to log users in and remember them.

Suppose the CAS server has a database with these tables:

* Users table
  * Email
  * Password (hashed of course!)
* Tickets table
  * Service URL
  * Ticket
  * Email
  * Expires (datetime)

The logic of the CAS endpoints works as follows:

* **/login**
  * Query parameters:
      * `service`: the URL to redirect the user back to after login (this is a URL
        on the web application that is wanting to authenticate the user)
  * Present a login page with an email and password box. The login form POSTs
    to the CAS server to check the password is correct (either POST to same
    /login URL or other one, not important).
  * The POST handler verifies the email address and password is valid.
      * Query the Users table by the email address given.
      * Verify the submitted password hashes to the same one in the database.
  * On successful password login:
      * Generate a "ticket" (a completely random string, a UUID or whatever).
      * Insert the ticket into the Tickets table:
          * Service URL = the `service` parameter originally given to "/login"
          * Ticket = the randomly generated ticket string
          * Email = the email the user just entered the correct password for
          * Expires = a date/time shortly in the future (say 1 hour or so)
      * Redirect user to the `service` URL with the `ticket` query parameter.
* **/verify**
  * The web application will call this to verify the ticket parameter given to
    its service URL.
  * Query parameters:
      * `service`: the very same service URL originally given to `/login` above.
      * `ticket`: the ticket string given to the service URL.
  * CAS queries the Tickets table to find the ticket string.
      * If the ticket is not found, error: return `no\n`
      * If the ticket has expired (current date/time > Expires time in DB): error,
      return `no\n`
      * If the `service` query parameter does NOT match the Service URL in the
      Tickets table for that ticket: error, return `no\n`
      * If the ticket exists in DB, the service URL matches, and the ticket is
      NOT expired, success! Return `yes\n` and the email address from the
      Tickets table.
  * Delete the row from the Tickets table so the ticket can only be verified
    one time (prevent replay attacks).
