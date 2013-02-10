import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import db
from google.appengine.api import users


class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class Student(db.Model):
    email = db.StringProperty()
    first = db.StringProperty()
    last = db.StringProperty()
    calendarID = db.StringProperty()
    type = db.StringProperty()
    
class Teacher(db.Model):
    email = db.StringProperty()
    first = db.StringProperty()
    last = db.StringProperty()
    calendarID = db.StringProperty()
    type = db.StringProperty()

def student_key(student_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Student', student_name or 'default_student')

def teacher_key(teacher_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Teacher', teacher_name or 'default_teacher')

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
                teacher_name = self.request.get('teacher_name')
        
                check = db.GqlQuery("SELECT * FROM Teacher WHERE email = '" + user.nickname() + "'" ,
                teacher_key(teacher_name))        
                if check:
                    self.redirect('/teacher')
                else:
                    self.redirect('/student')
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        
        
        
class TeacherHandler(webapp2.RequestHandler):
    def get(self):
        teacher_name = self.request.get('teacher_name')
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
        }

        template = jinja_environment.get_template('teacher.html')
        self.response.out.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

class CreateCal(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    student_name = self.request.get('student_name')
    student = Student(parent=student_key(student_name))
    """
    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()
    """
    student.email = self.request.get('email')
    student.first = self.request.get('first')
    student.last = self.request.get('last')
    student.type = "student"
    student.put()
    self.response.write(student.email);
    #self.redirect('/?' + urllib.urlencode({'student_name': student_name}))
    self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook),
                               ('/teacher', TeacherHandler),
                               ('/createcal', CreateCal)],
                              debug=True)