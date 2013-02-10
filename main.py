#!/usr/bin/env python
#
# Copyright 2012 Google Inc.
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

"""Starting template for Google App Engine applications.

Use this project as a starting point if you are just beginning to build a Google
App Engine project. Remember to download the OAuth 2.0 client secrets which can
be obtained from the Developer Console <https://code.google.com/apis/console/>
and save them as 'client_secrets.json' in the project directory.
"""

import httplib2
import json
import logging
import os
import pickle

import student

from apiclient.discovery import build
from oauth2client.appengine import oauth2decorator_from_clientsecrets
from oauth2client.client import AccessTokenRefreshError
from google.appengine.api import memcache
# from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret.
# You can see the Client ID and Client secret on the API Access tab on the
# Google APIs Console <https://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<code>%s</code>
<p>You can find the Client ID and Client secret values
on the API Access tab in the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>

""" % CLIENT_SECRETS


http = httplib2.Http(memcache)
service = build("calendar", "v3", http=http)


# Set up an OAuth2Decorator object to be used for authentication.  Add one or
# more of the following scopes in the scopes parameter below. PLEASE ONLY ADD
# THE SCOPES YOU NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
decorator = oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope=[
      'https://www.googleapis.com/auth/calendar.readonly',
      'https://www.googleapis.com/auth/calendar',
    ],
    message=MISSING_CLIENT_SECRETS_MESSAGE)

class MainHandler(webapp.RequestHandler):

  @decorator.oauth_required
  def get(self):
    # self.response.out.write("<html><p>Hello world!</p><html>")
    # Get the authorized Http object created by the decorator.
    http = decorator.http()
    # Call the service using the authorized Http object.
    # request = service.events().list(calendarId='primary')
    # response = request.execute(http=http)
    
    student = False
    
    if student:
        self.redirect("/student")
    else:
        self.redirect("/teacher")
    
    # self.response.out.write("<html>")
    # Parse every item
    # for event in response["items"]:
    #    self.response.out.write("<p>" + event["summary"] + "</p>")
    
    # self.response.out.write("</html>")
    
class StudentHandler(webapp.RequestHandler):
    
    @decorator.oauth_required
    def get(self):
        student_db = db.Key.from_path('Data', 'student_table')
        
        user = student.Student(student_db)
        
        user.first_name = "Stuff"
        user.last_name = "Thing"
        user.email = "thisisanemail@whatever.com"
        user.calendars = ["test text for now"]
        
        user.put()
        
        template_values = {'first': user.first_name, 
                           'last': user.last_name, 
                           'calendars': user.calendars}
        
        path = os.path.join(os.path.dirname(__file__), 'student.html')
        self.response.out.write(template.render(path, template_values))
        
class Teacher(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.StringProperty()
    calendars = db.StringListProperty()        
        
class TeacherHandler(webapp.RequestHandler):
    
    @decorator.oauth_required
    def get(self):
        teacher_db = db.Key.from_path('Data', 'teacher_table')
        
        user = Teacher(teacher_db)
        
        user.first_name = "Stuff2"
        user.last_name = "Thing2"
        user.email = "thisisanemail2@whatever.com"
        user.calendars = ["test text for now 2"]
        
        user.put()
        
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), 'teacher.html')
        self.response.out.write(template.render(path, template_values))
        
class EventHandler(webapp.RequestHandler):
    
    def get(self):
        self.response.out.write("<html><p>Hello World!</p></html>")
        
class CreateCalHandler(webapp.RequestHandler):
    
    def get(self):
        self.response.out.write("<html><p>Hello World!</p></html>")

def main():
  application = webapp.WSGIApplication(
      [
       ('/', MainHandler),
       ('/student', StudentHandler),
       ('/teacher', TeacherHandler),
       ('/event', EventHandler),
       ('/createcal', CreateCalHandler),
       (decorator.callback_path, decorator.callback_handler()),
      ],
      debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
