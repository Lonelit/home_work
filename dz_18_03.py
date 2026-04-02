# задание 1
# class Wolf:
#     def howl(self):
#         print("Yyyy")
# class Dog:
#     def bark(self):
#         print("Гаф")
# class Werewolf(Wolf, Dog):
#     def transform(self):
#         print("Превращение")
# creature1 = Werewolf()
# creature1.howl()
# creature1.bark()
# creature1.transform()
# print(Werewolf.__mro__)

# задание 2
# class EatMixin:
#     def eat(self):
#         print("Сотрудник ест")
# class SleapMixin:
#     def sleep(self):
#         print("Сотрудник спит")
# class Worker(EatMixin, SleapMixin):
#     def __init__(self, name):
#         self.name = name
#     def work(self):
#         print(f"Сотрудник {self.name} работает")
# emp1 = Worker("Zina")
# emp1.eat()
# emp1.sleep()
# emp1.work()

# задание 3

# class A:
#     def show(self):
#         print("Класс А")
# class B:
#     def show(self):
#         print("Класс B")
# # class C(A,B):
# #     def test(self):
# #         self.show()
# # c1 = C()
# # c1.test()
# # был вызван метод Класса А, потому что при множественном наследовании вызывается метод первого
# # класса. в Класс А уже был метод show, поэтому он был вызван
# class C(B,A):
#     def test(self):
#         self.show()
# c2 = C()
# c2.test()
# # был вызван метод Класса B

# задача 4
class PrintMixin:
    def print_doc(self, text):
        print(f"{text}")
class SaveMixin:
    def save_doc(self, text):
        print(f"Сохранено: {text}")
class Documents(PrintMixin,SaveMixin):
    def create(self,content):
        self.print_doc(content)
        self.save_doc(content)
doc1 = Documents()
doc1.create("Важный документ")