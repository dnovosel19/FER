# funkcija sortiranja, .sort() mijenja bas tu listu, a sorted() ne mijenja originalnu listu
def sortiraj(lista: list) -> list:
    lista.sort()
    return lista

# ne mijenjaj listu names ali vrati sortirano
def reverse_sort(names :list) -> list:
    return sorted(names, reverse=True)

names = ["Ana", "Petar", "Ana", "Lucija", "Vanja", "Pavao", "Lucija"]
names_desc = reverse_sort(names)

# odaberi elemente: bez prvog i bez zadnjeg, 1 znaci da od indeksa 1, a -1 do zadnjeg ali bez njega
selected_names = names_desc[1:-1]

unique_selected_names = set(selected_names)

# pass_names = [name + " - pass" for name in unique_selected_names]
pass_names = []
for name in unique_selected_names:
    pass_name = name + "- pass"
    pass_names.append(pass_name)

# definiramo dict, smanji vrijednost od value za jedan
person_data = {"Ana" : 1995, "Zoran" : 1978, "Lucija": 2001, "Anja" : 1997}
for key, value in person_data.items():
    value -= 1
    person_data[key] = value

# lista uredenih parova (tuple)
year_age = []
for key, value in person_data.items():
    year_age_tuple = (value, 2022 - value)
    year_age.append(year_age_tuple)

# klasa i unutar nje funkcija
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def increase_age(self):
        self.age += 1

# instanca 
first_person = Person("Marko", 39)
second_person = Person("Ivan", 17)
second_person.increase_age()

# nasljeduje klasu i ima dodatni atribut
class PersonDetail(Person):
    def __init__(self, name, age, address):
        super().__init__(name, age)
        self.address = address

first_person_detail = PersonDetail("Ana", 25, "Unska 3")
first_person_detail.increase_age()

import numpy as np

# Definicija vektora
vector_a = np.array([[1], [3], [5]])
vector_b = np.array([[2], [4], [6]])

# Vanjski umnožak
mat_mul = np.outer(vector_a, vector_b)

# Skalarni produkt
vect_dot = np.dot(vector_a.T, vector_b)

# Potenciranje elemenata matrice mat_mul na drugu potenciju
mat_exp = mat_mul ** 2

# Podmatrica 2x2 koja se nalazi u donjem desnom kutu matrice mat_exp
sub_mat = mat_exp[-2:, -2:]