import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_app import app, db, bcrypt
from flask_app.forms import AssignForm, RemovalForm
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
	print(work)
	return render_template('home.html', title='Project Management Tool', work=work)

@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/assign", methods=['GET', 'POST'])
def assign_page():
	form = AssignForm()
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
	
@app.route("/employee/<ssn>", methods=['GET', 'POST'])
def employee(ssn):
	form = RemovalForm()
	eName = Employee.query.filter_by(SSN=ssn).first().Name
	if not form.setEmployee(ssn):
		if eName:
			return render_template('employee.html', title=eName)
		else:
			flash('Employee with SSN {} does not exist'.format(ssn), 'danger')
			return redirect(url_for('home'))
	if form.is_submitted():
		projectId = form.Projects.data
		relation = Works_on.query.filter_by(SSN=ssn).filter_by(ProjectID=projectId).first()
		db.session.delete(relation)
		db.session.commit()

		pName = Project.query.filter_by(ID=projectId).first().Name
		flash('{} has been removed from {}'.format(eName, pName), 'success')
		return redirect(url_for('home'))
	return render_template('employee.html', title=eName, form=form)

@app.route("/project/<ID>", methods=['GET', 'POST'])
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
		db.session.delete(relation)
		db.session.commit()
		
		eName = Employee.query.filter_by(SSN=ssn).first().Name
		flash('{} has been removed from {}'.format(eName, pName), 'success')
		return redirect(url_for('home'))
	return render_template('project.html', title=pName, form=form)
