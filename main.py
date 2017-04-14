#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi


page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        User-Signup
    </h1>
"""

page_footer = """
</body>
</html>
"""


userentry = """

<form method = "post" action = "/">
    <table>
        <tr>
            <td><label for="username">Username</label></td>
            <td><input name="username" type="text" value="%(username)s" required>
            <span class="error">%(username_error)s</span>
            </td>

        </tr>
        <tr>
            <td><label for="password">Password</label></td>
            <td>
                <input name="password" type="password" required>
                <span class="error">%(password_error)s</span>
            </td>
        </tr>
        <tr>
            <td><label for="verify">Verify Password</label></td>
            <td>
                <input name="verify" type="password" required>
                <span class="error">%(verify_error)s</span>
            </td>
        </tr>
        <tr>
            <td><label for="email">Email (optional)</label></td>
            <td>
                <input name="email" type="email" value="%(email)s">
                <span class="error">%(email_error)s</span>
            </td>
        </tr>
    </table>
    <input type="submit">
</form>

"""
wmsg="""
<form method = "get">

  <body>
    <h2>Welcome, %(username)s!</h2>
  </body>
</form>
"""

username_error = ""
password_error = ""
verify_error = ""
email_error = ""
username = ""
email = ""



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):

    def get(self):

        content = page_header + userentry + page_footer
        self.response.write(content%{"email":email, "username":username, "username_error":username_error, "password_error":password_error, "verify_error":verify_error, "email_error":email_error})

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""



        if not valid_username(username):
            username_error = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            password_error = "That wasn't a valid password."
            have_error = True
        if password != verify:
            verify_error = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            email_error = "That's not a valid email."
            have_error = True

        content = page_header + userentry + page_footer
        if have_error:
            self.response.write(content%{"email":email,"username":username, "username_error":username_error, "password_error":password_error, "verify_error":verify_error, "email_error":email_error})
        else:
            self.redirect('/welcome?username='+username)

class Welcome(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')
        self.response.write(wmsg%{"username":username})



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)

], debug=True)
