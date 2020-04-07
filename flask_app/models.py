from datetime import datetime
from flask_app import db
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm, ForeignKey

class Employee(db.Model):
	__tablename__ = 'Employee'
	SSN = db.Column(db.String(9), primary_key=True)
	Name = db.Column(db.String(32), nullable=False)

	def __repr__(self):
		return f"Employee('{self.Name}', '{self.SSN}')"


class Project(db.Model):
	__tablename__ = 'Project'
	ID = db.Column(db.Integer, primary_key=True)
	Name = db.Column(db.String(32), nullable=False)

	def __repr__(self):
		return f"Project('{self.ID}', '{self.Name}')"

class Works_on(db.Model):
	__tablename__ = 'Works_on'
	SSN = db.Column(db.String(9), ForeignKey('Employee.SSN'), primary_key=True)
	ProjectID = db.Column(db.Integer, ForeignKey('Project.ID'), primary_key=True);

	def __repr__(self):
		return f"Works_on('{self.ProjectID}', '{self.SSN}')"
