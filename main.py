from abc import ABC,abstractmethod

class Absclass(ABC):
    def printMethod(self,x):
        print("Passed value: ",x)

    @abstractmethod
    def task(self):
        print("We are in Absclass")

class test_class(Absclass):
    def task(self):
        print("We are inside test_class")

class example_class(Absclass):
    def task(self):
        print("We are inside example_class")

test_obj = test_class()
test_obj.task()
test_obj.printMethod(100)

example_obj = example_class()
example_obj.task()
example_obj.printMethod(200)

print("test_obj is instance of Absclass? ", isinstance(test_obj, Absclass))
print("example_obj is instance of Absclass? ", isinstance(example_obj, Absclass))
