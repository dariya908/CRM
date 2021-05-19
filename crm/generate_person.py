import person
import weapon


person_info_dict = {
    'name':['john','vova','aliya','begimai','erbol'],
    'race':['orc','human','human','elf','human']
}

person_database = []
for index,names in enumerate(person_info_dict['name']):
    new_person = person.Person(name=names, race=person_info_dict['race'][index])
    person_database.append(new_person)

import random
import string


# printing lowercase
letters = string.ascii_lowercase
print ( ''.join(random.choice(letters) for i in range(10)) )

list1 = [random.randint(1,10) for i in range(5)]
print(list1)

"""
Создать класс Armor со всеми характеристиками персонажа для брони: health,power,defense,stamina
1. Создать метод armor_type по примеру в Sword
2. Сгенерировать обьекты мечей и брони
"""