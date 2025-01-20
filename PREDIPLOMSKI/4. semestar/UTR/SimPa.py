import sys

polje_redaka = []
for line in sys.stdin:
    polje_redaka.append(line)
#citaj_file = open("utrlab.txt", "r")

#polje_redaka=citaj_file.readlines()
#polje_redaka = ['0|0,2,0|1,2,0\n', 'q1,q2,q3\n', '0,1,2\n', 'J,N,K\n', 'q3\n', 'q1\n', 'K\n', 'q1,0,K->q1,NK\n', 'q1,1,K->q1,JK\n', 'q1,0,N->q1,NN\n', 'q1,1,N->q1,JN\n', 'q1,0,J->q1,NJ\n', 'q1,1,J->q1,JJ\n', 'q1,2,K->q2,K\n', 'q1,2,N->q2,N\n', 'q1,2,J->q2,J\n', 'q2,0,N->q2,$\n', 'q2,1,J->q2,$\n', 'q2,$,K->q3,$']

ulazni_nizovi = polje_redaka[0].strip().split("|")
#ulazni_nizovi = ['0', '0,2,0', '1,2,0']

skup_stanja = polje_redaka[1].strip().split(",")
#skup_stanja = ['q1', 'q2', 'q3']

skup_ulaznih_znakova = polje_redaka[2].strip().split(",")
#skup_ulaznih_znakova = ['0', '1', '2']

skup_znakova_stoga = polje_redaka[3].strip().split(",")
#skup_znakova_stoga = ['J', 'N', 'K']

prihvatljiva_stanja = polje_redaka[4].strip().split(",")
#prihvatljiva_stanja = ['q3']

pocetno_stanje = polje_redaka[5].strip()
#pocetno_stanje = q1

pocetni_znak_stoga = polje_redaka[6].strip()
#pocetni_znak_stoga = K

stog = []
stog.append(pocetni_znak_stoga)
#stog = ['K']

prijelaz = {}
for i in range(7, len(polje_redaka)):
    funk_prijelaza = polje_redaka[i].strip().split("->")
    prijelaz[funk_prijelaza[0]] = funk_prijelaza[1]
#prijelaz = {'q1,0,K': 'q1,NK', 'q1,1,K': 'q1,JK', 'q1,0,N': 'q1,NN', 'q1,1,N': 'q1,JN', 'q1,0,J': 'q1,NJ', 'q1,1,J': 'q1,JJ', 'q1,2,K': 'q2,K', 'q1,2,N': 'q2,N', 'q1,2,J': 'q2,J', 'q2,0,N': 'q2,$', 'q2,1,J': 'q2,$', 'q2,$,K': 'q3,$'}

for ul_nizovi in ulazni_nizovi:
    #ul_nizovi = (1.) 0, (2.) 0,2,0, (3.) 1,2,0

    stog = []
    stog.append(pocetni_znak_stoga)
    #stog = ['K']
    stanje = pocetno_stanje
    #stanje = q1
    
    ispis = pocetno_stanje + "#" + stog[0]

    ul_niz = ul_nizovi.strip().split(",")
    #ul_niz = (1.) ['0'], (2.) ['0', '2', '0'], (3.) ['1', '2', '0']

    zastavica = 0
    #citamo znak po znak
    for znak_niza in ul_niz:
        #print(stog)
        while True:
            if len(stog) != 0:
                kljuc = stanje + "," + znak_niza + "," + stog[0]
                kljuc1 = stanje + ",$," + stog[0]
            else:
                zastavica = 1
                ispis += "|fail|0"
                break
            if kljuc in prijelaz:
                value = prijelaz[kljuc].split(",")
                stog.pop(0)
                stanje = value[0]
                if value[1] != "$":
                    tokens = list(value[1])
                    stog_pom = []
                    for i in tokens:
                        stog_pom.append(i)
                    for i in stog:
                        stog_pom.append(i)
                    stog = stog_pom
                ispis += "|" + value[0] + "#"
                if len(stog) == 0:
                    ispis += "$"
                else:
                    for i in stog:
                        ispis += i
                break

            elif kljuc1 in prijelaz:
                value = prijelaz[kljuc1].split(",")
                stog.pop(0)
                stanje = value[0]
                if value[1] != "$":
                    tokens = list(value[1])
                    stog_pom = []
                    for i in tokens:
                        stog_pom.append(i)
                    for i in stog:
                        stog_pom.append(i)
                    stog = stog_pom
                ispis += "|" + value[0] + "#"
                if len(stog) == 0:
                    ispis += "$"
                else:
                    for i in stog:
                        ispis += i

            else:
                ispis += "|fail|0"
                zastavica = 1
                #print(stog)
                break
            #print(stog)
            #print("******************************************")
        if zastavica == 1:
            break

    if zastavica == 0:
        while True:
            if stanje in prihvatljiva_stanja:
                ispis += "|1"
                break
            else:
                key = stanje + ",$," + stog[0]
                if key in prijelaz:
                    stog.pop(0)
                    value = prijelaz[key].split(",")
                    stanje = value[0]


                    if value[1] != "$":
                        tokens = list(value[1])
                        stog_pom = []
                        for i in tokens:
                            stog_pom.append(i)
                        for i in stog:
                            stog_pom.append(i)
                        stog = stog_pom


                    ispis += "|" + value[0] + "#"
                    if len(stog) == 0:
                        ispis += "$"
                    else:
                        for i in stog:
                            ispis += i
                else:
                    ispis +="|0"
                    break
    print(ispis)
