# class Hero:

#     jumlahhero = 0

#     def __init__(self, name):
#         self.name = name

#     @property
#     def name(self):
#         return self.__name

#     @name.setter
#     def name(self, namaBaru):
#         self.__name = namaBaru
        

# miya = Hero("Miya")
# print(miya.name)

class C1: 
    def __init__(self, nama, nim):
        self.nama = nama
        self.__nim = nim #private attribute

    @property
    def nim(self):
        return self.__nim
        
antung = C1("Antung", 92)
print(antung.nama)

