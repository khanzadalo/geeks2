from enum import Enum
from random import choice, randint


class SuperAbility(Enum):
    CRITICAL_DAMAGE = 1
    BOOST = 2
    BLOCK_DAMAGE_AND_REVERT = 3
    HEAL = 4
    INCREASE_ATTACK = 5
    STUN_BOSS = 6
    REVIVE = 7
    PLAY_DEAD = 8
    KAMIKAZE = 9
    TIME_WARP = 10


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.__stunned = False

    @property
    def defence(self):
        return self.__defence

    @property
    def stunned(self):
        return self.__stunned

    @stunned.setter
    def stunned(self, value):
        self.__stunned = value

    def choose_defence(self, heroes):
        if self.__stunned:
            self.__defence = None
            self.__stunned = False
        else:
            random_hero = choice(heroes)
            self.__defence = random_hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if hero.ability == SuperAbility.BLOCK_DAMAGE_AND_REVERT and self.__defence != SuperAbility.BLOCK_DAMAGE_AND_REVERT:
                    hero.blocked_damage = int(self.damage / 5)
                    hero.health -= (self.damage - hero.blocked_damage)
                elif hero.ability == SuperAbility.STUN_BOSS:
                    self.__stunned = True
                    continue
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        if type(ability) == SuperAbility:
            self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss, heroes):
        coeff = randint(2, 6)
        boss.health -= self.damage * coeff
        print(f'Warrior {self.name} hit critically {self.damage * coeff}')



class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points

'''1. Magic должен увеличивать атаку каждого героя после каждого раунда на n-ное количество'''
class Magic(Hero):
    def __init__(self, name, health, damage, increase_amount):
        super().__init__(name, health, damage, SuperAbility.BOOST)
        self.__increase_amount = increase_amount

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0:
                hero.damage += self.__increase_amount



'''2. Thor, удар по боссу имеет шанс оглушить босса на 1 раунд,
вследствие чего босс пропускает 1 раунд и не наносит урон героям'''
class Thor(Hero):
    def __init__(self, name, health, damage, stun_chance):
        super().__init__(name, health, damage, SuperAbility.STUN_BOSS)
        self.__stun_chance = stun_chance

    def apply_super_power(self, boss, heroes):
        if self.__stun_chance >= randint(1, 100):
            print(f'Thor {self.name} stunned the boss!')
            boss.stunned = True



'''3. Witcher, не наносит урон боссу, но получает урон от босса. 
Имеет 1 шанс оживить первого погибшего героя, отдав ему свою жизнь, при этом погибает сам.'''
class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.REVIVE)

    def apply_super_power(self, boss, heroes):
        revive_hero = None
        for hero in heroes:
            if hero.health <= 0:
                revive_hero = hero
                break

        if revive_hero:
            revive_hero.health = self.health
            self.health = 0
            print(f'Witcher {self.name} revived {revive_hero.name} by sacrificing themselves.')


'''8. Tricky,  способность которого будет состоять в том, чтобы притвориться мертвым 
в определенном раунде(из случайного выбора), но в следующем раунде он снова вступает в бой. 
При этом он не получает урон и не бьет босса когда притворился мертвым'''
class Tricky(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.PLAY_DEAD)
        self.__played_dead = False
        self.__round_to_play_dead = randint(2, 7)

    def apply_super_power(self, boss, heroes):
        if not self.__played_dead and round_number == self.__round_to_play_dead:
            self.__played_dead = True
            self.__round_to_play_dead += randint(2, 7)
            print(f'{self.name} is playing dead.')
        elif self.__played_dead:
            self.__played_dead = False
            print(f'{self.name} is back in action!')


'''11. Герой Kamikadze  без урона но хорошое здоровье, его способность  жертвовать собой. 
Но он должен попасть точно в цель, иначе нанесет урон только на 50% из своего остатка жизни.'''
class Kamikaze(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.KAMIKAZE)

    def apply_super_power(self, boss, heroes):
        damage = self.health
        if boss.defence != SuperAbility.BLOCK_DAMAGE_AND_REVERT:
            boss.health -= damage
            print(f'{self.name} has sacrificed themselves and dealt {damage} damage to {boss.name}.')
        else:
            damage //= 2
            boss.health -= damage
            print(f'{self.name} has sacrificed themselves and dealt {damage} damage to {boss.name}.')
        self.health = 0

'''
У моего героя Chronos есть способность "Time Warp" (Искривление времени).
Когда Chronos активирует способность, он увеличивает урон всех героев в команде на 5, кроме себя.
В следующем раунде после активации Chronos восстанавливает стандартный урон всех героев 
и его способность Time Warp становится неактивной.
'''
class Chronos(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.TIME_WARP)
        self.__time_warp_active = False

    def apply_super_power(self, boss, heroes):
        if self.__time_warp_active and not self.__time_warp_applied:
            self.__time_warp_applied = True
            for hero in heroes:
                if hero != self:
                    hero.damage += 5
            print(f'{self.name} has activated Time Warp, increasing damage of all heroes (except {self.name}) by 5.')

    def restore_defaults(self, heroes):
        for hero in heroes:
            if hero != self:
                hero.damage -= 5
        self.__time_warp_active = False
        print(f'{self.name} has restored the default damage of all heroes and Time Warp ability is now inactive.')




round_number = 0


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True

    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
    return all_heroes_dead


def show_stats(boss, heroes):
    print(f'ROUND {round_number} ---------------------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0:
            if boss.defence != hero.ability:
                if hero.ability != SuperAbility.PLAY_DEAD:
                    hero.attack(boss)
                hero.apply_super_power(boss, heroes)
            elif hero.ability == SuperAbility.REVIVE:
                hero.apply_super_power(boss, heroes)
    show_stats(boss, heroes)


def start_game():
    boss = Boss('Balmond', 1000, 50)

    warrior_1 = Warrior('Grid', 280, 10)
    warrior_2 = Warrior('Tigril', 270, 15)
    magic = Magic('Potter', 260, 20, 5)
    thor = Thor('Thor', 250, 10, 30)
    witcher = Witcher('Geralt', 240, 5)
    medic = Medic('Stown', 240, 5, 15)
    assistant = Medic('Astes', 300, 5, 5)
    tricky = Tricky('Joker', 200, 10)
    kamikaze = Kamikaze('Kazuma', 450, 2)
    chronos = Chronos('Areon', 240, 10)

    heroes_list = [warrior_1, warrior_2, magic, thor, witcher, medic, assistant, tricky, kamikaze, chronos]

    show_stats(boss, heroes_list)

    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()


