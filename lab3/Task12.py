class Employee:

    def __init__(self,name,salary):
        self.name=name
        self.salary=salary

    def total_salary(self):
        return self.salary


class Manager(Employee):

    def __init__(self,name,salary,bonus):
        super().__init__(name,salary)
        self.bonus=bonus

    def total_salary(self):
        return self.salary*(1+self.bonus/100)


class Developer(Employee):

    def __init__(self,name,salary,projects):
        super().__init__(name,salary)
        self.projects=projects

    def total_salary(self):
        return self.salary+self.projects*500


class Intern(Employee):
    pass


data=input().split()

type=data[0]

if type=="Manager":

    obj=Manager(data[1],int(data[2]),int(data[3]))

elif type=="Developer":

    obj=Developer(data[1],int(data[2]),int(data[3]))

else:

    obj=Intern(data[1],int(data[2]))


print(f"Name: {obj.name}, Total: {obj.total_salary():.2f}")
