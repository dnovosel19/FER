import numpy as np
import random
import sys

class Sloj:
    def __init__(self, ulaz_u_neuron, koliko_neurona):   # konstruktor
        self.ulaz_u_neuron = ulaz_u_neuron
        self.koliko_neurona = koliko_neurona
        self.matrix = np.random.normal(0, 0.01, (koliko_neurona, ulaz_u_neuron))    # matrica 'koliko_neurona' x 'ulaz_u_neuron', nasumicne vrijednosti distribuirane normalnom razdiobom
        self.bias_w0 = np.random.normal(0, 0.01, koliko_neurona)    # vektor nasumicnih brojeva distribuiranih normalnom razdiobom
        
    @classmethod
    def stvori_novi_sloj(cls, prvi, drugi):    # krizanje
        novi_sloj = cls(drugi.ulaz_u_neuron, drugi.koliko_neurona)   # iste dimenzije, moze i 'prvi'
        novi_sloj.matrix = (prvi.matrix + drugi.matrix) / 2    # srednja vrijednost matrica
        novi_sloj.bias_w0 = (prvi.bias_w0 + drugi.bias_w0) / 2     # srednja vrijednost biasa
        return novi_sloj
            
    def izlaz_sloja(self, vektor_x, sigmoida):  # funkcija izlaza
        izlaz = np.dot(self.matrix, vektor_x) + self.bias_w0    # matricno mnozenje, zbroji bias
        if sigmoida:    # potrebno je koristiti funkciju sigmoide
            return 1 / (1 + np.exp(-izlaz))
        else:
            return izlaz
        

class NeuronskaMreza:
    def __init__(self, konf_slojeva, koliko_ulaza):   # konstruktor
        self.konf_slojeva = konf_slojeva
        self.koliko_ulaza = koliko_ulaza
        self.slojevi = []

        for i, konfiguracija in enumerate(konf_slojeva):  # stvori slojeve
            if i == 0:
                pocetno_ulaza = koliko_ulaza
            else:
                pocetno_ulaza = sloj.koliko_neurona   # svaki sloj ima ulaza koliko je prethodni imao neurona
            
            sloj = Sloj(pocetno_ulaza, konfiguracija)
            self.slojevi.append(sloj)

    @classmethod
    def stvori_dijete(cls, parent, roditelj):
        dijete = cls(roditelj.konf_slojeva, roditelj.koliko_ulaza)    # moze i parent
        dijete_slojevi = []
        neur_m1_slojevi = parent.slojevi
        neur_m2_slojevi = roditelj.slojevi

        for i in range(len(neur_m1_slojevi)):   # idi po slojevim neuronskih mreza i stvori nove
            novi_sloj = Sloj.stvori_novi_sloj(neur_m1_slojevi[i], neur_m2_slojevi[i])
            dijete_slojevi.append(novi_sloj)
        dijete.slojevi = dijete_slojevi
        return dijete
    
    def mutation(self, sd, vjerojatnost):
        for sloj in self.slojevi:   # idi kroz sve slojeve mreze
            for neuron in range(sloj.koliko_neurona):  # idi kroz sve neurone trenutnog sloja
                if random.random() <= vjerojatnost:     # mutiraj bias, za svaki neuron!
                    sloj.bias_w0[neuron] += random.gauss(0, sd)
                for ulaz in range(sloj.ulaz_u_neuron):    # prolaz kroz sve ulaze u neuron
                    if random.random() <= vjerojatnost:     # mutiraj element matrice ako je uvjet zadovoljen
                        sloj.matrix[neuron, ulaz] += random.gauss(0, sd)
        
    def izlaz_neuronske(self, ulazni_retci):
        izlaz = []
        for redak in ulazni_retci:
            pomoc = []
            for vrijednost in redak[:-1]:
                pomoc.append([vrijednost])
            stupcasti = np.array(pomoc)    # stupcasti vektor
            for i, sloj in enumerate(self.slojevi):     # prolazak slojevima
                zadnji = (i != len(self.slojevi) - 1)   # trenutni sloj je zadnji?
                stupcasti = sloj.izlaz_sloja(stupcasti, zadnji)   # izlaz trenutnog sloja
            izlaz.append(stupcasti[0, 0])
        return izlaz
    
    def izracunaj_error(self, ulazni_retci, izlaz_neuronske):   # formula u uputama
        sum_error = 0
        for i in range(len(ulazni_retci)):
            redak = ulazni_retci[i]     # trenutni redak
            izlaz = izlaz_neuronske[i]  # trenutni izlaz
            error = (redak[-1] - izlaz) ** 2    # ciljna i stvarna
            sum_error += error
        self.error = sum_error / len(izlaz_neuronske)   # srednje kvadratno odstupanje
        return self.error
    
    def fitness(self):  # selekcija proporcionalna dobroti
        return 1 / (self.error + 1)


razdvoji_unos = sys.argv

for i in range(len(razdvoji_unos)):     # ucitavanje podataka
    if razdvoji_unos[i] == "--train":
        datoteka_skupa_podataka = razdvoji_unos[i + 1]
        try:
            with open(datoteka_skupa_podataka, 'r', encoding='utf-8') as file:
                retci_file = file.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")
    
    elif razdvoji_unos[i] == "--test":
        testna_datoteka = razdvoji_unos[i + 1]
        try:
            with open(testna_datoteka, 'r', encoding='utf-8') as file:
                testni_retci = file.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")

    elif razdvoji_unos[i] == "--nn":
        arhitektura_neuronske_mreze = razdvoji_unos[i + 1]
    elif razdvoji_unos[i] == "--popsize":
        velicina_populacije = int(razdvoji_unos[i + 1])
    elif razdvoji_unos[i] == "--elitism":
        elitizam = int(razdvoji_unos[i + 1])
    elif razdvoji_unos[i] == "--p":
        vjerojatnost_mutacije = float(razdvoji_unos[i + 1])
    elif razdvoji_unos[i] == "--K":
        standardna_dev = float(razdvoji_unos[i + 1])
    elif razdvoji_unos[i] == "--iter":
        broj_iteracija = int(razdvoji_unos[i + 1])

slojevi = []    # polje za pamcenje konfiguracije neuronske mreze
pomoc = arhitektura_neuronske_mreze.split('s')
for sloj in pomoc[:-1]:     # ignoriramo zadnji (prazni) element
    slojevi.append(int(sloj))
slojevi.append(1)

podaci_odvojeni_zarezom = []    # lista listi, vrijednosti ulaznih podataka
retci_file.pop(0)   # makni header
for redak in retci_file:
    redak = redak.strip().split(',')
    pomoc = []
    for vrijednost in redak:
        pomoc.append(float(vrijednost))
    podaci_odvojeni_zarezom.append(pomoc)

testovi = []    # lista listi
testni_retci.pop(0)     # makni header
for redak in testni_retci:
    redak = redak.strip().split(',')
    pomoc = []
    for vrijednost in redak:
        pomoc.append(float(vrijednost))
    testovi.append(pomoc)

population = []
for i in range(velicina_populacije):    # stvori neuronske mreze
    neuronska_mreza = NeuronskaMreza(slojevi, len(podaci_odvojeni_zarezom[0]) - 1)  # konfiguracije_slojeva, dimenzija_ulaznih_podataka
    neuronska_mreza.izracunaj_error(podaci_odvojeni_zarezom, neuronska_mreza.izlaz_neuronske(podaci_odvojeni_zarezom))
    population.append(neuronska_mreza)

for i in range(broj_iteracija):
    neuronske_pamtim = []
    population.sort(key=lambda x: x.fitness(), reverse=True)    # sortiraj padajuce po fitness vrijednosti
    neuronske_pamtim.extend(population[:elitizam]) # uzmi samo prvih 'elitizam' najboljih jedinki za iducu generaciju

    ukup_fit = 0     # ukupan fitness neuronskih mreza
    for nm in population:
        ukup_fit += nm.fitness()

    while len(neuronske_pamtim) < velicina_populacije:    # dok nema zadanu velicinu
        neur_mre_pomoc = []     # pamti dvije neuronske mreze za stvaranje djeteta
        while(len(neur_mre_pomoc) < 2):     # dvije neuronske
            vjer = random.random()
            prob_sel = 0    # proporcionalna selekcija
            for nm in population:   # prolaz kroz sve neuronske mreze
                prob_sel += nm.fitness() / ukup_fit
                if vjer <= prob_sel:
                    neur_mre_pomoc.append(nm)
                    break
        
        if len(neur_mre_pomoc) < 2:     # garancija da smo uzeli dvije mreze, nikada nebi trebalo doci do ispunjenja ovog if uvjeta
            neur_mre_pomoc = random.sample(population, 2)

        child = NeuronskaMreza.stvori_dijete(neur_mre_pomoc[0], neur_mre_pomoc[1])  # stvori novo dijete
        child.mutation(standardna_dev, vjerojatnost_mutacije)   # uvodimo slucajne promjene
        neuronske_pamtim.append(child)
    
    population = neuronske_pamtim

    lista_error = []
    for nm in population:   # izracunaj error za svaku populaciju
        err = nm.izracunaj_error(podaci_odvojeni_zarezom, nm.izlaz_neuronske(podaci_odvojeni_zarezom))
        lista_error.append(err)
    error = min(lista_error)    # uzmi najmanji
    
    if (i+1) % 2000 == 0:   # ispis svakih 2000 iteracija
        print(f"[Train error @{i+1}]: {error:.6f}")

lista_error = []
for nm in population:   # prolaz kroz sve neuronske mreze
    err = nm.izracunaj_error(testovi, nm.izlaz_neuronske(testovi))
    lista_error.append(err)
test_error = min(lista_error)   # minimalna pogreska na testnim primjerima
print(f"[Test error]: {test_error:.6f}")