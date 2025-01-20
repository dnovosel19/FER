import sys
import math

def entropija_pocetnog_skupa(yes_br, no_br, maybe_br):  # funkcija koja vraca entropiju
    if (no_br == 0) and (maybe_br == 0):
        return 0
    if (yes_br == 0) and (maybe_br == 0):
        return 0
    if (yes_br == 0) and (no_br == 0):
        return 0
    
    if (yes_br == 0):
        broj = (-1) * (no_br / (maybe_br + no_br)) * (math.log(no_br / (maybe_br + no_br), 2)) - (maybe_br / (maybe_br + no_br)) * (math.log(maybe_br / (maybe_br + no_br), 2))
    if (no_br == 0):
        broj = (-1) * (yes_br / (yes_br + maybe_br)) * (math.log(yes_br / (yes_br + maybe_br), 2)) - (maybe_br / (yes_br + maybe_br)) * (math.log(maybe_br / (yes_br + maybe_br), 2))
    if (maybe_br == 0):
        broj = (-1) * (yes_br / (yes_br + no_br)) * (math.log(yes_br / (yes_br + no_br), 2)) - (no_br / (yes_br + no_br)) * (math.log(no_br / (yes_br + no_br), 2))
    if (maybe_br != 0) and (yes_br != 0) and (no_br != 0):
        broj = (-1) * (yes_br / (yes_br + no_br + maybe_br)) * (math.log(yes_br / (yes_br + no_br + maybe_br), 2)) - (no_br / (yes_br + no_br + maybe_br)) * (math.log(no_br / (yes_br + no_br + maybe_br), 2)) - (maybe_br / (yes_br + no_br + maybe_br)) * (math.log(maybe_br / (yes_br + no_br + maybe_br), 2))

    return broj

def IG(entropija, index, podaci):   # funkcija za izracun informacijske dobiti (information gain)
    skupp = set()   # pamti razlicite vrijednosti odredene znacajke
    broj_vrijednosti = []
    nazivnik = 0

    for vrijednost in podaci:   # trazimo razlicite vrijednosti neke znacajke po podacima
        skupp.add(vrijednost[index])
    skup = list(skupp)  # makni bilo kakvu nasumicnost
    skup.sort()
    
    for vrijednost in skup:     # prolaz po razlicitim vrijednostima
        brojac = 0      # koliko je podataka koji sadrze trazenu vrijednost
        yes_br = 0      # brojac 'yes' ili 'True'
        no_br = 0       # brojac 'no' ili 'False'
        maybe_br = 0    # brojac 'maybe' ili 'Unknown'
        for vrij in podaci:     # prebrojimo koliko imamo kojih ciljnih varijabli u trenutnom podskupu podataka
            if vrij[index] == vrijednost:   # provjeravamo vrijednost za dani indeks (znacajku)
                brojac += 1
                if (vrij[-1] == 'yes') or (vrij[-1] == 'True'):
                    yes_br += 1
                elif (vrij[-1] == 'no') or (vrij[-1] == 'False'):
                    no_br += 1
                elif (vrij[-1] == 'maybe') or (vrij[-1] == 'Unknown'):
                    maybe_br += 1
        broj_vrijednosti.append((vrijednost, brojac, yes_br, no_br, maybe_br))  # lista uredenih petorki (vrijednost znacajke, broj 'korisnih' podataka, yes, no, maybe)
    broj = entropija    # entropija trenutnog cvora koju dobijemo u pozivu funkcije

    for i in broj_vrijednosti:  # moze i len(broj_vrijednosti)
        nazivnik += i[1]
    
    for i in broj_vrijednosti:  # formula za izracun informacijske dobiti
        broj -= (i[1] / nazivnik) * entropija_pocetnog_skupa(i[2], i[3], i[4])

    return broj

def ig_lista(podaci_odvojeni_zarezom, header):  # funkcija koja vraca sve informacijske dobiti kao trojke (ig, znacajka, index znacajke)
    yes_brojac = 0
    no_brojac = 0
    maybe_brojac = 0
    
    for i in podaci_odvojeni_zarezom:   # koliko je yes / no / maybe unutar odredenog skupa podataka
        if (i[-1] == 'yes') or (i[-1] == 'True'):
            yes_brojac += 1
        elif (i[-1] == 'no') or (i[-1] == 'False'):
            no_brojac += 1
        elif (i[-1] == 'maybe') or (i[-1] == 'Unknown'):
            maybe_brojac += 1
        else:
            continue

    poc_ent = entropija_pocetnog_skupa(yes_brojac, no_brojac, maybe_brojac) # entropija od koje oduzimamo kako bismo dobili informacijsku dobit neke vrijednosti znacajke

    ig_lista = []
    for ind, i in enumerate(header):    # idi kroz header te zapisi (infor. dobit, naziv znacajke, koji je indeks te znacajke u headeru)
        ig_lista.append((round(IG(poc_ent, ind, podaci_odvojeni_zarezom), 4), i, ind))

    sortirana = sorted(ig_lista, key=lambda x: (-x[0], x[1]))   # sortiraj, padajuce prema ig, a ako je to isto onda prema nazivu znacajke ali uzlazno
    printam = ''
    for i in sortirana:     # zapis od IG koji se prikaze nakon izvodenja programa
        printam += f"IG({i[1]})={i[0]:.4f}  "
    prvi = sortirana[0]     # izdvoji trazenu trojku, ona koja ima najvecu IG
    if prvi[0] != float(0):     # ako je IG veci od 0 onda ga mozda ispisi
        if len(razdvoji_unos) == 3:     # ako nema ogranicenja dubine, onda ispis
            print(printam)
        elif (len(razdvoji_unos) == 4) and (duljina_headera - int(razdvoji_unos[3])) < len(sortirana):      # imamo ogranicenje u dubinu, necemo ispisivati ig od cvorova koji se nalaze dublje od zadane dubine
            print(printam)
    return list(sortirana)

def pronadi_vrijednosti(znacajka, podaci):  # funkcija koja vraca listu svih razlicitih vrijednosti znacajke
    skup = set()
    for i in podaci:
        skup.add(i[znacajka])
    return (list(skup))

def id3(makni_indeks, lista_podataka, header, grana, zapis):    # funkcija ID3
    pomocni = zapis     # pocetni zapis, pamti ga kako bi mogao imati razlicite zapise za isti korijen, ako se grana temperatura na nisku i visoku, onda imamo zapis sto je bilo prije toga
    vrijednosti_znacajke = pronadi_vrijednosti(makni_indeks, lista_podataka)
    vrijednosti_znacajke.sort()     # poslozi ih abecedno, podudarnost ispisa
    for vrijednost in vrijednosti_znacajke:     # cloudy, rainy, sunny
        zapis += vrijednost + ' '
        
        pomocna_lista = []  # lista listi koja sadrzi samo ona pravila koja moramo gledati za trenutnu vrijednost
        for pravila in lista_podataka:
            if pravila[makni_indeks] == vrijednost:     # imamo indeks koji je na redu tako da gledamo samo na mjestu toga indeksa unutar pravila
                helpic = []     # ako bi koristili pop() onda se brise u svim rekurzijama ta vrijednost, a nama treba da se u svakoj rekurziji samo dogodi da neku varijablu 'ne vidimo'
                for indeksic, pravilo in enumerate(pravila):
                    if indeksic != makni_indeks:
                        helpic.append(pravilo)
                pomocna_lista.append(helpic)    # ne sadrzi vrijednost trenutno pozvane (id3) znacajke

        h2 = []     # novi header koji ne sadrzava vec obradeni element
        for inde, j in enumerate(header):
            if inde != makni_indeks:
                h2.append(j)
        
        if len(h2) != 0:    # header jos nije prazan, listove jos trazimo
            pocet = ig_lista(pomocna_lista, h2)     # pronadi unutar novog headera i nove liste pravila IG od ostalih znacajki
            znac = pocet[0]     # prva je ona koja nama treba jer se vraca sortirana lista prema IG i stringu

            if znac[0] == float(0):     # ako je vrijednost najvece IG == 0, onda smo stigli do lista
                element = pomocna_lista[0]  # nije bitno koje pravilo odaberemo kada svi vracaju istu vrijednost ciljne varijable
                zapis += element[-1]
                rjesenje.append(zapis)
                zapis = pomocni

            else:   # jos uvijek nismo dosli do listova
                zapis +=str(grana+1) + ':' + znac[1] + '='
                id3(znac[2], pomocna_lista, h2, grana+1, zapis)     # rekurzivni poziv
                zapis = pomocni
        
        else:   # header je prazan znaci da postoji samo taj jedan primjer sa takvim vrijednostima te se preko njega ne moze zakljuciti nista novo, zapisi ono sto je vec bilo u pocetnim podacima za ucenje
            pronadi = []    # znamo da se prethodni koraci nalaze u varijabli zapis pa na temelju nje trazimo ekvivalent u pocetnim podacima
            pom_string = zapis.split()
            for pom in pom_string:
                nov = pom.split("=")
                pronadi.append(nov[1])
            for z in podaci_odvojeni_zarezom:
                if pronadi == z[:len(pronadi)]: # imamo sve osim ciljne vrijednosti, zato usporedujemo sve osim te varijable unutar z
                    zapis += str(z[-1])
                    break
            rjesenje.append(zapis)
            zapis = pomocni

def provjeri(grana):    # vracamo skup svih (znacajka, vrijednost) neke grane osim zadnje znacajke jer je tamo ciljna varijabla
    vrati = set()
    for pravilo in grana[:-1]:
        pomoc = pravilo.split(":")
        pom = pomoc[1].split("=")
        vrati.add((pom[0], pom[1]))     # ('weather', 'sunny')
    return vrati

def predict(ispis, testovi, stablo_odluke, head_test, novi_acc):    # prediction funkcija
    testni = []     # lista skupova u koju se spremaju primjeri za koje treba napraviti prediction
    for test in testovi:
        tst = set()
        for ind, pom in enumerate(test):
            tst.add((head_test[ind], pom))
        testni.append(tst)

    for test in testni:     # za svaki primjer koji zelimo predvidjeti
        zastavica = 0   # oznacava da smo u stablu odluke pronasli (ili nismo) neku granu koja moze napraviti predikciju
        for grane in stablo_odluke:     # prolazak kroz stablo odluke
            grana = grane.split()
            if (provjeri(grana)).issubset(test):    # ako se sve vrijednosti znacajke unutar neke grane poklapaju sa danim primjerom
                novi_acc.append(grana[-1])  # lista za accuracy podzadatak
                ispis += ' ' + grana[-1]
                zastavica = 1
                break
        
        if zastavica == 0:  # nismo nasli kompatibilnu granu, stoga uzimamo od trenutnog cvora podatke i pronalazimo one koji imaju najvise istih zakljucaka, ili ako imaju jednak broj onda uzimamo abecedno
            yes_brojac = 0
            no_brojac = 0
            maybe_brojac = 0
            yess = ''
            no = ''
            mybi = ''
            
            for i in podaci_odvojeni_zarezom:
                if (i[-1] == 'yes') or (i[-1] == 'True'):
                    yes_brojac += 1
                    yess = i[-1]
                elif (i[-1] == 'no') or (i[-1] == 'False'):
                    no_brojac += 1
                    no = i[-1]
                elif (i[-1] == 'maybe') or (i[-1] == 'Unknown'):
                    maybe_brojac += 1
                    mybi = i[-1]
                else:
                    continue

            if (yes_brojac == no_brojac) and (maybe_brojac == 0):
                ispis += ' ' + min(yess, no)
                novi_acc.append(min(yess, no))
            elif (yes_brojac == no_brojac) and (maybe_brojac == yes_brojac):
                ispis += ' ' + min(yess, no, mybi)
                novi_acc.append(min(yess, no, mybi))
            else:
                if max(yes_brojac, no_brojac, maybe_brojac) == yes_brojac:
                    ispis += ' ' + yess
                    novi_acc.append(yess)
                elif max(yes_brojac, no_brojac, maybe_brojac) == no_brojac:
                    ispis += ' ' + no
                    novi_acc.append(no)
                else:
                    ispis += ' ' + mybi
                    novi_acc.append(mybi)

    print(ispis)
    return

def id3_limited_depth(makni_indeks, lista_podataka, header, grana, zapis, depth): # ID3 funkcija sa ogranicenjem dubine
    if depth == 0:
        return
    
    pomocni = zapis     # pocetni zapis, pamti ga kako bi mogao imati razlicite zapise za isti korijen, ako se grana temp na nisku i visoku, onda imamo zapis sto je bilo prije toga
    vrijednosti_znacajke = pronadi_vrijednosti(makni_indeks, lista_podataka)
    vrijednosti_znacajke.sort()     # poslozi ih abecedno, podudarnost ispisa
    for vrijednost in vrijednosti_znacajke:     # cloudy, rainy, sunny
        zapis += vrijednost + ' '

        pomocna_lista = []      # lista listi koja sadrzi samo ona pravila koja moramo gledati za trenutnu vrijednost
        for pravila in lista_podataka:
            if pravila[makni_indeks] == vrijednost:     # imamo indeks koji je na redu tako da gledamo samo na mjestu toga indeksa unutar pravila
                helpic = []     # ako bi koristili pop() onda se brise u svim rekurzijama ta vrijednost, a nama treba da se u svakoj rekurziji samo dogodi da neku varijablu 'ne vidimo'
                for indeksic, pravilo in enumerate(pravila):
                    if indeksic != makni_indeks:
                        helpic.append(pravilo)
                pomocna_lista.append(helpic)    # ne sadrzi vrijednost trenutno pozvane (id3_limited_depth) znacajke
        
        h2 = []     # novi header koji ne sadrzava vec obradeni element
        for inde, j in enumerate(header):
            if inde != makni_indeks:
                h2.append(j)

        if len(h2) != 0:    # header jos nije prazan, trazimo listove i dalje
            pocet = ig_lista(pomocna_lista, h2)     # pronadi unutar novog headera i nove liste pravila IG od svih preostalih znacajki
            znac = pocet[0]     # prva je ona koja nama treba jer se vraca sortirana lista prema IG i stringu
            
            if znac[0] == float(0):     # ako je vrijednost najvece IG == 0 onda smo stigli do lista
                element = pomocna_lista[0]  # nije bitno koje pravilo odaberemo kada svi vracaju istu vrijednost ciljne varijable
                zapis += element[-1]
                rjesenje.append(zapis)
                zapis = pomocni
            
            else:   # jos uvijek nismo dosli do listova
                if depth-1 != 0:
                    zapis +=str(grana+1) + ':' + znac[1] + '='
                else:   # iduci poziv funkcije ce biti zadnji jer imamo ogranicenje na dubinu
                    zapis += najcesci(pomocna_lista)    # na temelju trenutnog cvora i pravila odredimo kojeg zakljucka ima najvise (ako je jednako, onda na temelju stringa)
                    rjesenje.append(zapis)
                
                id3_limited_depth(znac[2], pomocna_lista, h2, grana+1, zapis, depth-1)  # rekurzivni poziv
                zapis = pomocni

        else:   # header je prazan znaci da postoji samo taj jedan primjer sa takvim vrijednostima te se preko njega ne moze zakljuciti nista novo, zapisi ono sto je vec bilo u pocetnim podacima za ucenje
            pronadi = []    # znamo da se prethodni koraci nalaze u varijabli zapis pa na temelju nje trazimo ekvivalent u pocetnim podacima
            pom_string = zapis.split()
            for pom in pom_string:
                nov = pom.split("=")
                pronadi.append(nov[1])
            for z in podaci_odvojeni_zarezom:
                if pronadi == z[:len(pronadi)]:     # imamo sve osim ciljne vrijednosti, zato usporedujemo sve osim te varijable unutar z
                    zapis += str(z[-1])
                    break
            rjesenje.append(zapis)
            zapis = pomocni

def najcesci(skup_podataka):    # funkcija koja racuna sto ce se zakljuciti iz danog skupa pravila, ali gdje se ne dolazi do listova nego se prekine zbog nove znacajke
    yes_brojac = 0
    no_brojac = 0
    maybe_brojac = 0
    yess = ''
    no = ''
    mybi = ''

    for i in skup_podataka:
        if (i[-1] == 'yes') or (i[-1] == 'True'):
            yes_brojac += 1
            yess = i[-1]
        elif (i[-1] == 'no') or (i[-1] == 'False'):
            no_brojac += 1
            no = i[-1]
        elif (i[-1] == 'maybe') or (i[-1] == 'Unknown'):
            maybe_brojac += 1
            mybi = i[-1]
        else:
            continue

    if (yes_brojac == no_brojac) and (maybe_brojac == 0):
        return min(yess, no)
    elif (yes_brojac == no_brojac) and (maybe_brojac == yes_brojac):
        return min(yess, no, mybi)
    elif (yes_brojac == no_brojac) and (maybe_brojac < yes_brojac):
        return min(yess, no)
    else:
        if max(yes_brojac, no_brojac, maybe_brojac) == yes_brojac:
            return yess
        elif max(yes_brojac, no_brojac, maybe_brojac) == no_brojac:
            return no
        else:
            return mybi


razdvoji_unos = sys.argv

datoteka_skupa_podataka = razdvoji_unos[1]  # datoteka za treniranje
testna_datoteka = razdvoji_unos[2]          # datoteka za testiranje

try:
    with open(datoteka_skupa_podataka, 'r', encoding='utf-8') as file:
        retci_file = file.readlines()
except FileNotFoundError:
    print("Greska prilikom otvaranja datoteke.")

try:
    with open(testna_datoteka, 'r', encoding='utf-8') as file:
        testni_retci = file.readlines()
except FileNotFoundError:
    print("Greska prilikom otvaranja datoteke.")

podaci_odvojeni_zarezom = []    # radimo listu listi od podataka za treniranje
for i in retci_file:
    i = i.strip()
    lista = i.split(',')
    podaci_odvojeni_zarezom.append(lista)

# radimo listu listi od podataka za testiranje, zadnji clan svake liste se ignorira jer je to 'prava' vrijednost koju nemamo te ju spremamo u accuracy kako bismo usporedili dobivene i stvarne vrijednosti
accuracy = []
testiram = []
for i in testni_retci:
    i = i.strip()
    lista = i.split(',')
    accuracy.append(lista.pop())
    testiram.append(lista)
accuracy.pop(0)

rjesenje = []   # lista u koju spremamo stablo odluke

header = podaci_odvojeni_zarezom.pop(0)     # nazivi znacajki
header.pop()    # makni zadnju vrijednost, jer je to zakljucak koji nam nece trebati za potrebe buducih iteracija
duljina_headera = len(header)
pocetno = ig_lista(podaci_odvojeni_zarezom, header) # pocetna lista IG-eva
znacajka = pocetno[0]   # korijen stabla
grane = 1   # broj kojim se prati broj dubine, koristan za ispis
zapis = ''  # string koji pohranjuje izgled grana
zapis += str(grane) + ':' + znacajka[1] + '='   # pocetno

if len(razdvoji_unos) == 3:     # nemamo dubinu, znaci da se treba doci do svih listova stabla
    id3(znacajka[2], podaci_odvojeni_zarezom, header, grane, zapis)
else:
    id3_limited_depth(znacajka[2], podaci_odvojeni_zarezom, header, grane, zapis, int(razdvoji_unos[3]))

print("[BRANCHES]:")
for i in rjesenje:  # printamo sve grane koje se pohranjuju u rjesenje
    print(i)

prediction = '[PREDICTIONS]:'
head_testiranja = testiram.pop(0)

novi_accuracy = []  # lista koja pamti nasa predvidanja temeljena na stablu odluke
predict(prediction, testiram, rjesenje, head_testiranja, novi_accuracy)

tocno = 0   # koliko se zakljucaka podudara sa stvarnim rjesenjem
for ind, i in enumerate(accuracy):
    if novi_accuracy[ind] == i:
        tocno += 1

print("[ACCURACY]: " + f"{(tocno / len(accuracy)):.5f}")

razlicite_vrijednosti = set()   # koliko je razlicitih vrijednosti ciljnih varijabli
for i in podaci_odvojeni_zarezom:
    razlicite_vrijednosti.add(i[-1])
sorted_list = (list(razlicite_vrijednosti))
sorted_list.sort()  # sortiramo da se matrica obilazi pravilnim redoslijedom

print("[CONFUSION_MATRIX]:")
for i in sorted_list:
    ispis = ''
    for j in sorted_list:
        broj_u_matrici = 0
        for ind, k in enumerate(accuracy):
            if (novi_accuracy[ind] == j) and (k == i):
                broj_u_matrici += 1
        ispis += str(broj_u_matrici) + ' '
    print(ispis)