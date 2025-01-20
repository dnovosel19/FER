import sys

polje_redaka = []
for line in sys.stdin:
    polje_redaka.append(line)

prvi_redak = polje_redaka[0].strip()
razdvojen_prvi = prvi_redak.split("|")

nizovi_rijeci = []
for i in range(len(razdvojen_prvi)):
    razdvojene_rij = razdvojen_prvi[i].split(',')
    nizovi_rijeci.append(razdvojene_rij)

pocetno_stanje = polje_redaka[4].strip()

prijelaz = {}

for i in range(5, len(polje_redaka)):
    funk_prijelaza = polje_redaka[i].strip()
    fp_bez_strelice = funk_prijelaza.split("->")
    prijelaz[fp_bez_strelice[0]] = fp_bez_strelice[1]

for i in range(len(nizovi_rijeci)):
    ulaz = nizovi_rijeci[i]
    aktivno = [pocetno_stanje]
    for sta in aktivno:
        stanje = sta + ",$"
        if stanje in prijelaz:
            usporedi = prijelaz[stanje].split(",")
            for st in range(len(usporedi)):
                if usporedi[st] not in aktivno:
                    aktivno.append(usporedi[st])
    aktivno.sort()

    ispis = (",").join(aktivno)

    for j in range(len(ulaz)):
        znak = ulaz[j]
        pom = aktivno.copy()

        for k in range(len(pom)):
            str_pom = pom[k] + "," + znak
            if str_pom in prijelaz:
                pom_akt = prijelaz[str_pom].split(",")
                aktivno += pom_akt
            aktivno.remove(pom[k])

        aktivno = list(set(aktivno))

        for k in aktivno:
            str_pom1 = k + ",$"
            if str_pom1 in prijelaz:
                pom_prij = prijelaz[str_pom1].split(",")
                for z in range(len(pom_prij)):
                    if pom_prij[z] not in aktivno:
                        aktivno.append(pom_prij[z])
        aktivno.sort()

        if '#' in aktivno:
            aktivno.remove('#')
        ispis += "|" + ((",").join(aktivno), '#')[not aktivno]
    print(ispis)