class Person: 

    def initt(self,name):
        self.name=name


class Student(Person):

    def initt(self,name,gpa):
        super().initt(name)
        self.gpa=gpa

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")


name,gpa=input().split()

s=Student(name,gpa)

s.display()
