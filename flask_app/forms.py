from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_app import db
from flask_app.models import Employee, Project, Works_on

class AssignForm(FlaskForm):
	Employee = SelectField('Employee')
	Project = SelectField('Project')
	Submit = SubmitField('Assign')

	def set(self):
		results = db.session.query(Employee).order_by(Employee.Name.asc()).all()
		employees = list()
		for result in results:
			employees.append((str(result.SSN), str(result.Name)))
		results = db.session.query(Project).order_by(Project.Name.asc()).all()
		projects = list()
		for result in results:
			projects.append((str(result.ID), str(result.Name)))
		self.Employee.choices = employees
		self.Project.choices = projects
		

class RemovalForm(FlaskForm):
	Employees = RadioField(validators=[DataRequired()])
	Projects = RadioField(validators=[DataRequired()])
	Submit = SubmitField('Remove')

	def setEmployee(self, ssn):
		results = Works_on.query.filter_by(SSN=ssn) \
			.order_by(Project.ID.asc()) \
			.join(Project, Project.ID == Works_on.ProjectID) \
			.add_columns(Project.Name) \
			.join(Employee, Employee.SSN == Works_on.SSN) \
			.add_columns(Employee.Name).all()
		if results:
			# Convert the SQL query results into a usable data structure
			choices = list()
			for result in results:
				choices.append((result.Works_on.ProjectID, 'Project {}: {}'.format(result.Works_on.ProjectID, result[1])))
			self.EmployeeName = result[2]
			self.Projects.choices = choices
			self.Submit.label.text = 'Remove project from this employee'
			return True
		else:
			return False
	
	def setProject(self, Id):
		results = Works_on.query.filter_by(ProjectID=Id) \
			.order_by(Employee.Name.asc()) \
			.join(Project, Project.ID == Works_on.ProjectID) \
			.add_columns(Project.Name) \
			.join(Employee, Employee.SSN == Works_on.SSN) \
			.add_columns(Employee.Name).all()
		if results:
			# Convert the SQL query results into a usable data structure
			choices = list()
			for result in results:
				choices.append((result.Works_on.SSN, result[2]))
			self.ProjectName = result[1]
			self.Employees.choices = choices
			self.Submit.label.text = 'Remove employee from this project'
			return True
		else:
			return False

class EmployeeForm(FlaskForm):
	Name = StringField('Employee Name', validators=[DataRequired(), Length(min=2, max=32)])
	SSN = StringField('Employee SSN', validators=[DataRequired(), Length(min=9, max=9)])
	Submit = SubmitField('Add Employee')

class ProjectForm(FlaskForm):
	Name = StringField('New Project Name', validators=[DataRequired(), Length(min=2, max=32)])
	Submit = SubmitField('Add Project')
