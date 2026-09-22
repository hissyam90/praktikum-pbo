class Hero:

    jumlahhero = 0

    def __init__(self, name, health, attack, armor):
        self.name = name
        self.health = health
        self.attack = attack
        self.armor = armor
        Hero.jumlahHero += 1

        sniper = Hero("sniper", 100, 15, 4)
        print(sniper.__dict__)
        print(sniper.name)

        


    # def attack(self, other_hero):
    #     other_hero.health -= self.attack_power
    #     print(f"{self.name} attacks {other_hero.name} for {self.attack_power} damage!")

    # def serang(self, lawan):
    #     print(f"{self.name} menyerang {lawan.name}!")
    # def diserang(self, lawan):
    #     print(f"{self.name} diserang {lawan.name}!")

# classmethod


# def totalHero(cls):
#     # return cls.jumlahHero
#     print(f"Total hero: {cls.jumlahHero}")

# balmon = Hero("Balmon", 100, 40, 10)
# Hero.jumlah_hero()

# balmon = Hero("Balmon", 100, 40, 10)
# roger = Hero("roger", 100, 20, 10)


# print(hero._dict_)
# balmon.serang(roger)

# print(balmon)

# axe = Hero("Axe", 100, 15, 4)
# print(axe.name)
# roger = Hero("Roger", 100, 20, 10)