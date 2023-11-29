class Computer:
    def __init__(self, cpu, memory):
        self.__cpu = cpu
        self.__memory = memory

    @property
    def cpu(self):
        return self.__cpu

    @cpu.setter
    def cpu(self, value):
        self.__cpu = value

    @property
    def memory(self):
        return self.__memory

    @memory.setter
    def memory(self, value):
        self.__memory = value


    def make_computations(self):
        return self.__cpu + self.__memory

    def __str__(self):
        return f'Device: Computer cpu:{self.__cpu} memory:{self.__memory}'

    def __lt__(self, other):
        return self.memory < other.memory

    def __eq__(self, other):
        return self.memory == other.memory

    def __gt__(self, other):
        return self.memory > other.memory

    def __le__(self, other):
        return self.memory <= other.memory

    def __ge__(self, other):
        return self.memory >= other.memory

    def __ne__(self, other):
        return self.__memory != other.memory



class Phone:
    def __init__(self, sim_cards_list):
        self.__sim_cards_list = sim_cards_list

    @property
    def sim_cards_list(self):
        return self.__sim_cards_list

    @sim_cards_list.setter
    def sim_cards_list(self, value):
        self.__sim_cards_list = value

    def call(self, sim_card_number, call_to_number):
        print(f'There is a call to the number {call_to_number} '
              f'from sim card {sim_card_number} {self.__sim_cards_list[sim_card_number]}')

    def __str__(self):
        return f"Sim cards: {self.sim_cards_list} "




class SmartPhone(Computer, Phone):
    def __init__(self, location, cpu, memory, sim_cards_list):
        Computer.__init__(self, cpu, memory)
        Phone.__init__(self, sim_cards_list)
        self.location = location

    def use_gps(self, location):
        print(f'{location} to "Bishkek"')


    def __str__(self):
        return f'Your location: {self.location}'



# Объект компьютера
computer = Computer(cpu=2.5, memory=16)

computer.make_computations()

phone = Phone(["MegaCom", "O!", "Beeline"])


# Объект смартфонов
smartphone_1 = SmartPhone(cpu=3.0, memory=32, sim_cards_list=["MegaCom", "O!", "Beeline"], location=' geektech')
smartphone_2 = SmartPhone(cpu=4.0, memory=64, sim_cards_list=["MegaCom", "O!", "Beeline"], location=' geekstudio')

# Распечатываем информацию об объектах
print(computer)
print(phone)
print(smartphone_1)
print(smartphone_2)

# Опробуем методы
computer.make_computations()
phone.call(1, "+996 707 45 55 41")
phone.call(2, "+996 777 77 88 99")

smartphone_1.use_gps("Talas")
smartphone_2.use_gps("Osh")


# Сравнение объектов
print(computer < smartphone_1)
print(smartphone_1 == smartphone_2)
print(smartphone_2 > computer)
print(smartphone_1 <= smartphone_2)
print(smartphone_2 >= computer)
