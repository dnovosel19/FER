import sys

def izbaci_tautologiju(redak, klauzule):        # provjera je li neki redak tautologija
    literali = redak.split('v')
    for literal1 in literali:
        literal1 = literal1.strip()
        for literal2 in literali:
            literal2 = literal2.strip()
            if (str(literal1) == '~' + str(literal2)) or ('~' + str(literal1) == str(literal2)):    # pronasli smo tautologiju, ignoriramo redak
                return
    klauzule.append(redak)
    return

def uklanjanje_redundantnih_klauzula(klauzule, negirana_ciljna):    # ukloni redundantne klauzule
    pamti_indekse_koje_izbacujemo = set()       # zapisi indekse koje na kraju izbacujemo
    lista_listi = []
    for klauzula in klauzule:
        lista = set()
        literali = klauzula.split('v')
        for literal in literali:
            literal = literal.strip()
            lista.add(literal)
        lista_listi.append(lista)
    
    for neg_cilj in negirana_ciljna:
        lista = set()
        lista.add(neg_cilj)
        lista_listi.append(lista)
    
    for i, klzl in enumerate(lista_listi):
        for j, klauz in enumerate(lista_listi):
            if i != j:
                if klzl.issubset(klauz):    # provjera sadrzi li jedan skup sve elemente drugoga skupa
                    pamti_indekse_koje_izbacujemo.add(j)
                elif klauz.issubset(klzl):
                    pamti_indekse_koje_izbacujemo.add(i)

    sortirana_lista_indeksa = sorted(pamti_indekse_koje_izbacujemo, reverse=True)   # poredaj silazno

    if len(sortirana_lista_indeksa) > 0:    # uklanjanje redundantnih
        for indeks in sortirana_lista_indeksa:
            if indeks <= len(lista_listi) - len(negirana_ciljna) - 1:
                klauzule.pop(indeks)

def negacija_ciljne_klauzule(ulazna_klauzula):  # negiranje ciljne
    vrati_listu = []
    razdvojeni_literali = ulazna_klauzula.split('v')
    if len(razdvojeni_literali) > 1:
        for literal in razdvojeni_literali:
            literal = literal.strip()
            if literal[0] == '~':
                vrati_listu.append(literal[1])
            else:
                vrati_listu.append('~' + literal)
    else:
        literal = razdvojeni_literali[0]
        if literal[0] == '~':
            vrati_listu.append(literal[1])
        else:
            vrati_listu.append('~' + literal)
    return vrati_listu

def stvori_novonastale(skup_novnastalih_elemenata, klauzula, premise, literal, element):    # punimo skup novonastalih sa svim literalima koji nisu ona dva koja su komplementarno pronadena
    for i in klauzula:
        if (i != literal) and (i != element):
            skup_novnastalih_elemenata.add(i)
    for i in premise:
        if (i != literal) and (i != element):
            skup_novnastalih_elemenata.add(i)

def funkcija_za_pamcenje_puta(pamtim_put, skup_novnastalih_elemenata, biljezi_indeks_puta, prvi, drugi):    # novi skup zapisujemo u pamti_put
    for par in pamtim_put:      # ako vec postoji takav skup onda da ne dupliciramo zapis ignoriramo ga
        i = par[0]
        if i == skup_novnastalih_elemenata:
            return False
    
    for k, el in enumerate(pamtim_put):
        for j, elmnt in enumerate(pamtim_put):
            if k != j:
                skupic = set()
                for a in el[0]:
                    if (a != prvi) and (a != drugi):
                        skupic.add(a)
                for b in elmnt[0]:
                    if (b != prvi) and (b != drugi):
                        skupic.add(b)
                if skupic == skup_novnastalih_elemenata:    # kada napunimo skup provjeravamo jesu li novonastali i ovaj skup identicni jer onda smo nasli prethodnike koji cine trenutni skup
                    pamtim_put.append((skup_novnastalih_elemenata, biljezi_indeks_puta, k, j))
                    return True
    return False

def napuni_new(new, dodaj_u_new):   # punimo new sa dodaj_u_new
    skup_skupova = set()
    for i in new:
        skup_za_provjeru = set()
        for j in i:
            skup_za_provjeru.add(j)
        skup_skupova.add(frozenset(skup_za_provjeru))
    for i in dodaj_u_new:
        if i not in skup_skupova:
            normalan_set = set(i)
            lista = []
            for j in normalan_set:
                lista.append(j)
            new.append(lista)

def tautologija(dodaj_u_new):   # provjera ako je neki od novonastalih skupova tautologija da ga izbacimo
    izbaci_indeks = set()
    lista_dodaj = list(dodaj_u_new) # pretvorba u listu
    for ind, i in enumerate(lista_dodaj):
        zastavica = 0
        for element in i:
            for drugi_el in i:
                if (element == '~' + drugi_el) or (drugi_el == '~' + element):
                    zastavica = 1
                    izbaci_indeks.add(ind)
                    break
            if zastavica == 1:
                break
    sortirana = sorted(izbaci_indeks, reverse=True)
    for i in sortirana:
        lista_dodaj.pop(i)
    return set(lista_dodaj)

def redundiraj(new, dodajem):   # makni sve 'viskove' iz novonastaloga skupa kako bismo u new dodali sto je moguce manje elemenata
    koji_mi_ne_trebaju = []
    for i in new:
        klauzula = set(i)
        for j in dodajem:
            if klauzula.issubset(j):    # ako vec imamo neki manji skup unutar new koji je podskup novonastaloga onda novonastali ignoriramo
                koji_mi_ne_trebaju.append(j)
    for ind, i in enumerate(dodajem):
        for inx, j in enumerate(dodajem):
            if ind != inx:
                if i.issubset(j):
                    koji_mi_ne_trebaju.append(j)
    vrati = set()
    for i in dodajem:
        if i not in koji_mi_ne_trebaju:
            vrati.add(i)
    return vrati

def plResolution(F, G):     # algoritam rezolucije opovrgavanjem
    koje_sam_vec_medusobno_provjerio = set()
    new = []        # new = [['water'], ['heater'], ['tea_bag'], ['~water', '~heater', 'hot_water'], ['~coffee_powder', '~hot_water', 'coffee'], ['~hot_water', '~tea_bag', 'tea'], ['~coffee'], ['~tea']]
    pamtim_put = [] # ({}, indeks_skupa, prvi_prethodnik, drugi_prethodnik)
    biljezi_indeks_puta = 0     # pamti indeks skupa

    for i in F:
        razdvojeni = i.split(' v ')
        skup = set()
        for j in razdvojeni:
            skup.add(j)
        new.append(razdvojeni)
        pamtim_put.append((skup, biljezi_indeks_puta, -1, -1))
        biljezi_indeks_puta += 1
    
    koliko_je_pocetnih = len(new)   # barem jedna roditeljska klauzula uvijek dolazi iz SoS
    
    for i in G:
        skup = set()
        skup.add(i)
        lista = []
        lista.append(i)
        new.append(lista)
        pamtim_put.append((skup, biljezi_indeks_puta, -1, -1))
        biljezi_indeks_puta += 1

    # pamtim_put = [({'water'}, 0, -1, -1), ({'heater'}, 1, -1, -1), ({'tea_bag'}, 2, -1, -1), ({'hot_water', '~heater', '~water'}, 3, -1, -1), ({'coffee', '~hot_water', '~coffee_powder'}, 4, -1, -1), ({'tea', '~tea_bag', '~hot_water'}, 5, -1, -1), ({'~coffee'}, 6, -1, -1), ({'~tea'}, 7, -1, -1)]

    NIL = False
    while True:
        pocetna_duljina = len(new)  # s njom se usporeduje novonastali len(new) za prekid petlje
        dodaj_u_new = set()     # skup koji sadrzi potencijalne skupove koje treba dodati u new
        for i, klauzula in enumerate(new):  # idemo listu po listu unutar new, primjer: ['water'], ..., ['~coffee_powder', '~hot_water', 'coffee'], ..., ['~tea']
            if i < koliko_je_pocetnih:  # preskace pocetne premise
                continue
            else:
                for j, premise in enumerate(new):   # idemo listu po listu unutar new, primjer: ['water'], ..., ['~coffee_powder', '~hot_water', 'coffee'], ..., ['~tea']
                    if i != j:  # nema smisla dvije iste klauzule usporedivati
                        if (i, j) not in koje_sam_vec_medusobno_provjerio:  # ne kombiniraj klauzule koje si vec kombinirao ili pokusao kombinirati
                            koje_sam_vec_medusobno_provjerio.add((i, j))    # usporedujemo ih pa to biljezimo
                            koje_sam_vec_medusobno_provjerio.add((j, i))
                            for literal in klauzula:    # element po element unutar klauzule idemo
                                for element in premise: # element po element unutar klauzule
                                    if (literal == '~' + element) or (element == '~' + literal):    # pronasli smo dva komplementarna literala
                                        skup_novnastalih_elemenata = set()  # skup koji nastaje kada se 'spoje' dvije klauzule koje imaju komplementarne literale
                                        stvori_novonastale(skup_novnastalih_elemenata, klauzula, premise, literal, element) # napuni skup novonastalih elemenata
                                        if funkcija_za_pamcenje_puta(pamtim_put, skup_novnastalih_elemenata, biljezi_indeks_puta, literal, element):
                                            biljezi_indeks_puta += 1    # ako smo uspjesno dodali skup onda za iduci skup povecamo indeks
                                        dodaj_u_new.add(frozenset(skup_novnastalih_elemenata))  # skup skupova, da nemoramo provjeravati nalazili se vec unutra ili ne
                                        if len(skup_novnastalih_elemenata) == 0:    # slucaj kada smo naisli da su dvije klauzule imale samo jedan element i ti su elementi medusobno komplementarni pa dobivamo NIL
                                            NIL = True
                                            break
                                if NIL: break
                    if NIL: break
                if NIL: break
        if len(dodaj_u_new) > 0:    # ako postoji nesto 'novo'
            dodajem = tautologija(dodaj_u_new)  # makni tautologije iz novoga skupa
            dodaj_bez_red = redundiraj(new, dodajem)    # ako je neki od clanova novonastalog skupa nadskup vec nekog postojeceg, ukloni ga
            napuni_new(new, dodaj_bez_red)  # dodajemo sve koji su ostali od dodaj_u_new u new

        if pocetna_duljina >= len(new): # ako nema promjena onda smo dosli do kraja
            break
        if NIL: break

    if NIL: # ako je uspjesno onda moramo ispisati put
        pamti_indekse = []
        sve = set()
        zadnji_pamtim_put = pamtim_put[-1]  # zadnji nam sluzi da pronademo sve prethodnike
        trebam_prvi_broj = zadnji_pamtim_put[2]     # prvi prethodnik
        trebam_drugi_broj = zadnji_pamtim_put[3]    # drugi prethodnik
        pamti_indekse.append(trebam_drugi_broj)
        pamti_indekse.append(trebam_prvi_broj)
        sve.add(trebam_prvi_broj)
        sve.add(trebam_drugi_broj)
        put = [(zadnji_pamtim_put[1], 'NIL', trebam_prvi_broj, trebam_drugi_broj)]
        while True:
            sve_br = len(sve)
            novo = []
            for j in pamti_indekse:
                a = pamtim_put[j]
                koliko_v = len(a[0]) - 1
                string = ''
                for k in a[0]:
                    string += str(k)
                    if koliko_v > 0:
                        string += ' v '
                        koliko_v += -1
                broj_jedan = a[2]
                broj_dva = a[3]
                put.append((a[1], string, broj_jedan, broj_dva))    # uredena cetvorka, (indeks, string, prethodnik1, prethodnik2) za lakse sortiranje
                novo.append(broj_jedan)
                novo.append(broj_dva)
            pamti_indekse = []
            for j in novo:
                if j != -1:
                    if j not in sve:
                        pamti_indekse.append(j)
                        sve.add(j)
            if len(sve) == sve_br:
                break
        put.sort()

        for i in G:     # ako neko negirano ciljno nismo koristili, svejedno ga treba ispisati zato trazimo indeks gdje cemo ga umetnuti
            imam_ga = 0
            brojac = 0
            for j in put:
                if j[2] == -1:
                    brojac += 1
                if (j[1]) == (i):
                    imam_ga = 1
            if imam_ga == 0:
                put.insert(brojac, (-2, i, -1, -1))

        indeksi = 1
        parovi_zamjene = []
        proden = set()
        proden.add(-1)
        for i in put:   # zamjenjujemo stvarne indekse sa onima puno manjima da zapis bude 'uredniji i citljiviji'
            if i[0] not in proden:
                parovi_zamjene.append((i[0], indeksi))
                indeksi += 1
                proden.add(i[0])
            if i[2] not in proden:
                parovi_zamjene.append((i[2], indeksi))
                indeksi += 1
                proden.add(i[2])
            if i[3] not in proden:
                parovi_zamjene.append((i[3], indeksi))
                indeksi += 1
                proden.add(i[3])

        crtice = 1
        ispis = ''
        for i in put:   # petlja za ispis
            for j in parovi_zamjene:
                if (crtice == 1) and (i[2] != -1):
                    crtice = 0
                    ispis += '===============\n'
                if i[0] == j[0]:
                    ispis += str(j[1]) + '. ' + i[1]
                    break
            if i[2] != -1:
                for k in parovi_zamjene:
                    if i[2] == k[0]:
                        ispis += ' (' + str(k[1]) + ', '
                        break
                for k in parovi_zamjene:
                    if i[3] == k[0]:
                        ispis += str(k[1]) + ')\n'
            else:
                ispis += '\n'
        ispis += '==============='
        print(ispis)

    return NIL

def makni_iz_clauses(klauzule, maknuti):    # funkcija za uklanjanje nakon znaka '-'
    ukloni = ''
    makni_indeks = -10
    for ind, i in enumerate(maknuti):
        ukloni += i.lower()
        if ind < len(maknuti) - 1:
            ukloni += ' '
    for ind, i in enumerate(klauzule):
        if i == ukloni:
            makni_indeks = ind
            break
    if makni_indeks != -10:
        klauzule.pop(ind)
        return ind


razdvoji_unos = sys.argv
trazim_resolution = 0       # pamti jel trazen cooking ili resolution

for i in range(len(razdvoji_unos)):     # ucitavanje ulaznih podataka

    if razdvoji_unos[i] == "resolution":
        ime_txt_file = razdvoji_unos[i + 1]
        try:
            with open(ime_txt_file, 'r', encoding='utf-8') as file:
                retci_file = file.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")
        trazim_resolution = 1
    
    if razdvoji_unos[i] == "cooking":
        ime_txt_file = razdvoji_unos[i + 1]
        korisnicke_naredbe = razdvoji_unos[i + 2]
        try:
            with open(ime_txt_file, 'r', encoding='utf-8') as file:
                retci_file = file.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")
        try:
            with open(korisnicke_naredbe, 'r', encoding='utf-8') as file1:
                naredbe = file1.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")

if trazim_resolution:
    klauzule = []
    for line in  retci_file:
        if line[0] != '#':
            line = line.lower().strip()
            izbaci_tautologiju(line, klauzule)  # ako je neki redak tautologija, ignoriramo ga

    ciljna_klauzula = klauzule.pop()    # izvuci zadnji clan - to je ciljno stanje
    negirana_ciljna_klauzula = negacija_ciljne_klauzule(ciljna_klauzula)    # negiramo ciljno jer radimo strategijom opovrgavanjem
    uklanjanje_redundantnih_klauzula(klauzule, negirana_ciljna_klauzula)    # uklanjamo redundantne klauzule

    SoS = []    # strategija skupa potpore
    for klauzula in negirana_ciljna_klauzula:
        SoS.append(klauzula)

    rjesenje = plResolution(klauzule, SoS)  # rezolucija opovrgavanjem
    if rjesenje:
        print("[CONCLUSION]: " + ciljna_klauzula + " is true")
    else:
        print("[CONCLUSION]: " + ciljna_klauzula + " is unknown")

else:
    ispis = 'Constructed with knowledge:\n'
    klauzule = []
    for line in retci_file:
        if line[0] != '#':
            line = line.lower().strip()
            izbaci_tautologiju(line, klauzule)
    for i in klauzule:
        ispis += i + '\n'
    print(ispis, end='\n')
    zapamti_indeks = -1
    
    for i in naredbe:   # redak po redak za naredbe
        ispis = ''
        razdvoji_cilj_naredba = i.split()
        duljina = len(razdvoji_cilj_naredba)
        
        if razdvoji_cilj_naredba[-1] == '+':    # umetni klauzulu ako ona vec ne postoji
            if duljina != 2:
                razdvoji_cilj_naredba.pop()
                umecem = ''
                for brojacic, umetni in enumerate(razdvoji_cilj_naredba):
                    umecem += str(umetni.lower())
                    if brojacic < duljina - 2:
                        umecem += ' '
            else:
                umecem = razdvoji_cilj_naredba[0].lower()
            
            if zapamti_indeks != -1:
                if umecem not in klauzule:
                    klauzule.insert(zapamti_indeks, umecem)
                    zapamti_indeks = -1
            else:
                if umecem not in klauzule:
                    klauzule.append(umecem)
            
            ispis += 'User\'s command: ' + i.strip().lower() + '\n'
            ispis += 'Added ' + str(umecem)
            print(ispis)
        
        elif razdvoji_cilj_naredba[-1] == '-':  # uklanjanje
            micem = ''
            razdvoji_cilj_naredba.pop()
            for broji, micemm in enumerate(razdvoji_cilj_naredba):
                micem += micemm.lower()
                if broji < len(razdvoji_cilj_naredba) - 1:
                    micem += ' '
            zapamti_indeks = makni_iz_clauses(klauzule, razdvoji_cilj_naredba)
            ispis += 'User\'s command: ' + i.strip().lower() + '\n'
            ispis += 'Removed ' + str(micem)
            print(ispis)
        
        elif razdvoji_cilj_naredba[-1] == '?':
            pomoc = klauzule.copy()
            print('User\'s command: ' + i.strip().lower())
            negirana_ciljna_kau = negacija_ciljne_klauzule(razdvoji_cilj_naredba[0].lower())
            uklanjanje_redundantnih_klauzula(klauzule, negirana_ciljna_kau)

            SoS = []
            for klauzula in negirana_ciljna_kau:
                SoS.append(klauzula)

            rjesenje = plResolution(klauzule, SoS)
            klauzule = pomoc
            if rjesenje:
                print("[CONCLUSION]: " + str(razdvoji_cilj_naredba[0].lower()) + " is true")
            else:
                print("[CONCLUSION]: " + str(razdvoji_cilj_naredba[0].lower()) + " is unknown")
        print()