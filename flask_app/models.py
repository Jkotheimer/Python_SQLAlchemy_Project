from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm, ForeignKey


db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Employee(db.Model):
    SSN = db.Column(db.String(9), primary_key=True)
    Name = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"Employee('{self.Name}', '{self.SSN}')"


class Project(db.Model):
     ID = db.Column(db.Integer, primary_key=True)
     Name = db.Column(db.String(32), nullable=False)

     def __repr__(self):
         return f"Project('{self.ID}', '{self.Name}')"

class Works_on(db.Model):
    SSN = db.Column(db.String(9), ForeignKey('Employee.SSN'), primary_key=True)
    ProjectID = db.Column(db.Integer, ForeignKey('Project.ID'), primary_key=True);
