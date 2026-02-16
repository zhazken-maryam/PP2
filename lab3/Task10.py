class Person:
    
    def __init__(self, name):
        self.name = name   # store the person's name


class Student(Person):   # Student inherits from Person
    
    def __init__(self, name, gpa):
        super().__init__(name)   # call Person constructor to set name
        self.gpa = gpa           # store the student's GPA

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")   # print student info


name, gpa = input().split()   # get name and GPA from user

s = Student(name, gpa)        # create Student object

s.display()                   # call display method
