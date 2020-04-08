import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_app import app, db, bcrypt
from flask_app.forms import AssignForm, RemovalForm, EmployeeForm, ProjectForm
from flask_app.models import Employee, Project, Works_on
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
	results = Works_on.query \
		.order_by(Works_on.ProjectID.asc()) \
		.join(Project, Project.ID == Works_on.ProjectID) \
		.add_columns(Project.Name) \
		.join(Employee, Employee.SSN == Works_on.SSN) \
		.add_columns(Employee.Name).all()
	# Convert the SQL query results into a usable data structure
	work = dict()
	lastID = -1 
	for result in results:
		if result.Works_on.ProjectID != lastID:
			lastID = result.Works_on.ProjectID
			work[lastID] = dict()
			work[lastID]['Name'] = result[1]
			work[lastID]['Employees'] = list()
		next_employee = (result.Works_on.SSN, result[2])
		work[lastID]['Employees'].append(next_employee)
	return render_template('home.html', title='Project Management Tool', work=work)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/assign", methods=['GET', 'POST'])
def assign_page():
	form = AssignForm()
	form.set()
	# if the form has been submitted, confirm the entry and commit it to the database
	if form.validate_on_submit():
		ssn = form.Employee.data
		pid = form.Project.data
		confirmation = Works_on.query.filter_by(SSN=ssn).filter_by(ProjectID=pid).all()
		if confirmation:
			flash('The specified employee is alread working on this project', 'danger')
			return render_template('assign.html', title='Assign', form=form)
		assignment = Works_on(SSN = ssn, ProjectID = pid)
		db.session.add(assignment)
		db.session.commit()
		return redirect(url_for('home'))
	# else just return the form page
	return render_template('assign.html', title='Assign Project', form=form)

@app.route("/employees", methods=['GET', 'POST'])
def employees():
	form = EmployeeForm()
	employees = Employee.query.order_by(Employee.SSN.asc()).all()
	if form.validate_on_submit():
		print("Submitted")
		Name = form.Name.data
		SSN = form.SSN.data
		result = Employee.query.filter_by(SSN=SSN).all()
		if result:
				flash('Employee with SSN: {} already exists'.format(SSN), 'danger')
		else:
			Emp = Employee(SSN=SSN, Name=Name)
			db.session.add(Emp)
			db.session.commit()
			flash('Employee successfully added!', 'success')
			return redirect(url_for('employees'))
	return render_template('entity.html', title='Add an employee', form=form, entities=employees, entity_type='employee')

@app.route("/employees/<ssn>", methods=['GET', 'POST'])
def employee(ssn):
	form = RemovalForm()
	eName = Employee.query.filter_by(SSN=ssn).first()
	if not eName:
		flash('Employee with SSN {} does not exist'.format(ssn), 'danger')
		return redirect(url_for('home'))
	eName = eName.Name
	if not form.setEmployee(ssn):
		return render_template('employee.html', title=eName)
	if form.is_submitted():
		projectId = form.Projects.data
		relation = Works_on.query.filter_by(SSN=ssn).filter_by(ProjectID=projectId).first()
		if relation:
			db.session.delete(relation)
			db.session.commit()
			pName = Project.query.filter_by(ID=projectId).first().Name
			flash('{} has been removed from {}'.format(eName, pName), 'success')
		else:
			flash('Relationship not found', 'danger')
		return redirect(url_for('employee', ssn=ssn))
	return render_template('employee.html', title=eName, form=form)

@app.route("/projects", methods=['GET', 'POST'])
def projects():
	form = ProjectForm()
	projects = Project.query.order_by(Project.ID.asc()).all()
	if form.validate_on_submit():
		Name = form.Name.data
		results = Project.query.filter_by(Name=Name).first()
		'''
		If a project with this name already exists, start counting from 2 and check for
		any other projects with the same name, but a number after it. If the count is free,
		make that the new name of the project
		'''
		if results:
			count = 2
			tempName = Name
			while results:
				tempName = Name + ' ' + str(count)
				results = Project.query.filter_by(Name=tempName).first()
				count += 1
			Name = tempName
		Proj = Project(Name=Name)
		db.session.add(Proj)
		db.session.commit()
		flash('Project added', 'success')
		return redirect(url_for('projects'))
	return render_template('entity.html', title='Add a project', form=form, entities=projects, entity_type="project")

@app.route("/projects/<ID>", methods=['GET', 'POST'])
def project(ID):
	form = RemovalForm()
	pName = Project.query.filter_by(ID=ID).first().Name
	if not form.setProject(ID):
		if pName:
			return render_template('project.html', title=pName)
		else:
			flash('Project with ID: {} does not exist'.format(ID), 'danger')
			return redirect(url_for('home'))
	if form.is_submitted():
		ssn = form.Employees.data
		relation = Works_on.query.filter_by(SSN=ssn).filter_by(ProjectID=ID).first()
		if relation:
			db.session.delete(relation)
			db.session.commit()
			eName = Employee.query.filter_by(SSN=ssn).first().Name
			flash('{} has been removed from {}'.format(eName, pName), 'success')
		else:
			flash('Relationship not found', 'danger')
		return redirect(url_for('project', ID=ID))	
	return render_template('project.html', title=pName, form=form)
