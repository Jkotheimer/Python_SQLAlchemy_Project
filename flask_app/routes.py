import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_app import app, db, bcrypt
from flask_app.forms import AssignForm
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
	print("FUCK")
	if form.validate_on_submit():
		print("HEREEEEE")
		ssn = form.Employee.data
		pid = form.Project.data
		confirmation = Works_on.query.filter_by(SSN=ssn).filter_by(ProjectID=pid).all()
		if confirmation:
			print("Exists")
			flash('The specified employee is alread working on this project', 'danger')
			return render_template('assign.html', title='Assign', form=form)
		assignment = Works_on(SSN = ssn, ProjectID = pid)
		db.session.add(assignment)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('assign.html', title='Assign', form=form)
	
@app.route("/employee/<ssn>")
def employee(ssn):
	results = Works_on.query.filter_by(SSN=ssn) \
		.order_by(Works_on.ProjectID.asc()) \
		.join(Project, Project.ID == Works_on.ProjectID) \
		.add_columns(Project.Name) \
		.join(Employee, Employee.SSN == ssn) \
		.add_columns(Employee.Name).all()
	# Convert the SQL query results into a usable data structure
	
	projects = dict()
	for result in results:
		projects[result.Works_on.ProjectID] = result[1]	
	return render_template('employee.html', title='Project Management Tool', projects=projects, employee=result[2])

@app.route("/project/<ID>")
def project(ID):
	results = Works_on.query.filter_by(ProjectID=ID) \
		.join(Project, Project.ID == ID) \
		.add_columns(Project.Name) \
		.join(Employee, Employee.SSN == Works_on.SSN) \
		.add_columns(Employee.Name).all()
	# Convert the SQL query results into a usable data structure
	
	employees = dict()
	for result in results:
		employees[result.Works_on.SSN] = result[2]	
	return render_template('project.html', title='Project Management Tool', employees=employees, project=result[1])


'''
@app.route("/login")
def login():
	if current_user.is_authenticated:
        return 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_dept():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new department!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='New Department',
                           form=form, legend='New Department')


@app.route("/dept/<dnumber>")
@login_required
def dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())


@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
@login_required
def update_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    currentDept = dept.dname

    form = DeptUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.dnumber.data = dept.dnumber
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('create_dept.html', title='Update Department',
                           form=form, legend='Update Department')




@app.route("/dept/<dnumber>/delete", methods=['POST'])
@login_required
def delete_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    db.session.delete(dept)
    db.session.commit()
    flash('The department has been deleted!', 'success')
    return redirect(url_for('home'))
'''
