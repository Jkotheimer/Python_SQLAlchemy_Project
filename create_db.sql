DROP DATABASE IF EXISTS Company;
CREATE DATABASE Company;
USE Company;

CREATE TABLE Student (
	StudentID		NUMERIC NOT NULL,
	StudentName		VARCHAR(25),
	CONSTRAINT Student_PK
	PRIMARY KEY (StudentID)
);

CREATE TABLE Faculty (
	FacultyID		NUMERIC NOT NULL,
	FacultyName		VARCHAR(25),
	CONSTRAINT Faculty_PK
	PRIMARY KEY (FacultyID)
);

CREATE TABLE Course (
	CourseID		CHAR(8) NOT NULL,
	CourseName		VARCHAR(15),
	CONSTRAINT Course_PK
	PRIMARY KEY (CourseID)
);

CREATE TABLE Section (
	SectionNo		NUMERIC(18,0) NOT NULL,
	Semester 		CHAR(7) NOT NULL,
	CourseID 		CHAR(8) NOT NULL,
	CONSTRAINT Section2_PK
	PRIMARY KEY (SectionNo, Semester, CourseID),
	CONSTRAINT Section_FK
	FOREIGN KEY (CourseID)
	REFERENCES Course(CourseID)
);

CREATE TABLE Qualified (
	FacultyID		NUMERIC NOT NULL ,
	CourseID		CHAR(8) NOT NULL,
	DateQualified   DATE,
	CONSTRAINT IsQualified_PK
	PRIMARY KEY (FacultyID,CourseID),
	CONSTRAINT QualifiedFaculty_FK
	FOREIGN KEY (FacultyID)
	REFERENCES Faculty (FacultyID),
	CONSTRAINT QualifiedCourse_FK
	FOREIGN KEY (CourseID)
	REFERENCES Course (CourseID)
);

CREATE TABLE Registration (
	StudentID		NUMERIC NOT NULL,
	SectionNo		NUMERIC(18,0) NOT NULL,
	Semester		CHAR(7) NOT NULL,
	CourseID		CHAR(8) NOT NULL,
	CONSTRAINT Registration_PK
	PRIMARY KEY (StudentID, SectionNo, Semester),
	CONSTRAINT Registration_FK
	FOREIGN KEY (SectionNo, Semester, CourseID)
	REFERENCES Section(SectionNo, Semester, CourseID)
);


INSERT INTO Student
	(StudentID, StudentName)
	VALUES
	(38214,'Letersky'),
	(54907,'Altvater'),
	(66324,'Aiken'),
	(70542,'Maara');

INSERT INTO Faculty
	(FacultyID, FacultyName)
	VALUES
	(2143,'Birkin'),
	(3467,'Berndt'),
	(4756,'Collins');

INSERT INTO Course
	(CourseID,CourseName)
	VALUES
	('ISM 3113','Syst Analysis'),
	('ISM 3112','Syst Design'),
	('ISM 4212','Database'),
	('ISM 4930','Networking');

INSERT INTO Qualified
	(FacultyID, CourseID, DateQualified)
	VAlUES
	(2143,'ISM 3112','1988-09-01'),
	(2143,'ISM 3113','1988-09-01'),
	(3467,'ISM 4212','1995-09-01'),
	(3467,'ISM 4930','1996-09-01'),
	(4756,'ISM 3113','1991-09-01'),
	(4756,'ISM 3112','1991-09-01');

INSERT INTO Section
	(SectionNo, Semester, CourseID)
	VALUES
	(2712,'I-2008','ISM 3113'),
	(2713,'I-2008','ISM 3113'),
	(2714,'I-2008','ISM 4212'),
	(2715,'I-2008','ISM 4930');

INSERT INTO Registration
	(StudentID, SectionNo, Semester, CourseID)
	VALUES
	(38214,'2714','I-2008','ISM 4212'),
	(54907,'2714','I-2008','ISM 4212'),
	(54907,'2715','I-2008','ISM 4930'),
	(66324,'2713','I-2008','ISM 3113');
