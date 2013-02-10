#!/usr/bin/env python

from google.appengine.ext import db

class Student(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.StringProperty()
    calendars = db.StringListProperty()
        
    