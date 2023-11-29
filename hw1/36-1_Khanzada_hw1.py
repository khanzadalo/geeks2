# Класс Person
class Person:
    def __init__(self, fullname, age, is_married):
        self.fullname = fullname
        self.age = age
        self.is_married = is_married

    def introduce_myself(self):
        print(f"Меня зовут {self.fullname}, мне {self.age} лет, я женат/замужем {self.is_married}")

# Класс Student
class Student(Person):
    def __init__(self, fullname, age, is_married, marks):
        super().__init__(fullname, age, is_married)
        self.marks = marks

    def average_mark(self):
        return round(sum(self.marks.values()) / len(self.marks), 2)

# Класс Teacher
class Teacher(Person):
    base_salary = 10000
    def __init__(self, fullname, age, is_married, experience):
        super().__init__(fullname, age, is_married)
        self.experience = experience

    def salary(self):
        bonus = 0
        if self.experience > 3:
            bonus = 0.05 * (self.experience - 3) * self.base_salary
        return self.base_salary + bonus


# Объект учителя
teacher = Teacher("Алексей Цой", 50, True, 20)

teacher.introduce_myself()
print("Зарплата учителя:", teacher.salary())



# Функция create_students
def create_students():
    students = []
    students.append(Student("Ханзада Оморова", 20, False, {"Математика": 5, "Физика": 4, "Java": 5}))
    students.append(Student("Руслан Алашев", 21, False, {"Математика": 5, "Физика": 5, "Java": 5}))
    students.append(Student("Азрет Камалов", 20, True, {"Математика": 3, "Физика": 3, "Java": 4}))
    return students


# Список учеников
students = create_students()

# Вывод информации о каждом ученике
for student in students:
    student.introduce_myself()
    print("Средняя оценка ученика:", student.average_mark())
