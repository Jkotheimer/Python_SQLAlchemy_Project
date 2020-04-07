from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_app import db
from flask_app.models import Employee, Project, Works_on

class AssignForm(FlaskForm):
	results = Employee.query.order_by(Employee.Name.asc()).all()
	employees = list()
	for result in results:
		employees.append((str(result.SSN), str(result.Name)))
	results = Project.query.order_by(Project.Name.asc()).all()
	projects = list()
	for result in results:
		projects.append((str(result.ID), str(result.Name)))

	Employee = SelectField('Employee', choices=employees)  # myChoices defined at top
	Project = SelectField('Project', choices=projects)
	Submit = SubmitField('Assign')
