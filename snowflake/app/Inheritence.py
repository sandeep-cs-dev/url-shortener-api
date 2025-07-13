class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_name(self):
        print(self.name)


class Employee(Person):

    def __init__(self, name, age, salary):
        super().__init__(name, age)
        self.salary = salary


e = Employee("Sandeep", 33, 345000);

e.print_name()
