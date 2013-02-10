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
    email = db.EmailProperty()  #changed from StringProperty()
    first = db.StringProperty()
    last = db.StringProperty()
    calendarID = db.StringProperty()
    type = db.StringProperty()
    
class Teacher(db.Model):
    email = db.EmailProperty()
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
               # teacher_name = self.request.get('teacher_name')
               
            check = db.GqlQuery("SELECT * FROM Teacher WHERE email = '" + user.email() + "'")        
            if check.get() != None:
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
        
class StudentHandler(webapp2.RequestHandler):
    def get(self):
        student_name = self.request.get('student_name')
        user = users.get_current_user()   
        check = db.GqlQuery("SELECT * FROM Student WHERE email = '" + user.email() + "'")
        
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            "calID": "https://www.google.com/calendar/embed?showTitle=0&amp;height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src="+ check.get().calendarID +"%40goup.calendar.google.com&amp;color=%23691426&amp;ctz=America%2FLos_Angeles"
        }

        template = jinja_environment.get_template('student.html')
        self.response.out.write(template.render(template_values))


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
    student.calendarID="vor4323b5pb0vke2a1it4b3sv8@group.calendar.google.com"
    student.put()
    self.response.write(student.email);
    #self.redirect('/?' + urllib.urlencode({'student_name': student_name}))
    self.redirect('/teacher')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/teacher', TeacherHandler),
                               ('/student', StudentHandler),
                               ('/createcal', CreateCal)],
                              debug=True)