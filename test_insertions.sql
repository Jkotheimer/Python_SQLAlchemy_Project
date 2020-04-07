USE Company;

INSERT INTO Employee
	(Name, Ssn)
	VALUES
	("Bob Saget", "111223456"),
	("Random Name", "123456789"),
	("Barack Obama", "987654321"),
	("Sister Jean", "019283746");

INSERT INTO Project
	(Name)
	VALUES
	("Public Works"),
	("Financial Aid"),
	("Drawing Pictures");

INSERT INTO Works_on 
	(SSN, ProjectID)
	VALUES
	("019283746", 2),
	("987654321", 2),
	("987654321", 1),
	("111223456", 3),
	("111223456", 2);	
