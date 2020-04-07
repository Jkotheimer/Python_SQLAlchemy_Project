USE Company;

-- Get the names of all employees that work on a project
SELECT Name FROM Employee
	JOIN Works_on ON Employee.SSN=Works_on.SSN
	WHERE Works_on.ProjectID=2;

SELECT (""); -- This is here as a spacer for bash output

-- Get the names of all the projects that the given employee name is working on
Select Project.Name from Works_on
	JOIN Project ON Works_on.ProjectID=Project.ID 
	JOIN Employee ON Works_on.SSN=Employee.SSN
	WHERE Employee.Name="Barack Obama";
