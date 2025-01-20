import sys

polje_redaka = []
for line in sys.stdin:
    polje_redaka.append(line)

# citaj_file = open("ppj.txt", "r")
# polje_redaka=citaj_file.readlines()

brojac = 0
zastavica = 0
ispisi_koliko_puta = 0

razmak_lista_naredbi = []
razmak_t = []
razmak_e = []
petlje_broj_razmak = []
l_zagrade = []

u_koliko_sam_petlji = 0
koliko_az_ova = 0
zadnji_je_idn = 0

zbrajamo_po_jedan = 0
pamtim_dubinu = []
pamtim_dubinu.append(1)
pamti_petljice = []
br = 0
dubinica = []
brojac_dubina = []

broj_razmaka = 0
ispis = ''

pocetni_program = []
for i in polje_redaka:
    odvoji_razmake = i.strip().split(" ")
    pocetni_program.append(odvoji_razmake[0])
pocetni_program.append('kraj')

valjda_dobro = []
#valjda_dobro.append(1)
brojim_brojkice = 0
posljednji_znak = ''
pretposljednji_znak = ''
brojcicc = 0
brp = 0
for i in pocetni_program:
    if i == 'OP_PRIDRUZI' or i == 'KR_ZA' or i == 'KR_AZ':
        # print(i)
        # print(posljednji_znak)
        if i == 'KR_ZA' and posljednji_znak == '':
            pamti_petljice.append(0)
            brojac_dubina.append(1)
        if i == 'OP_PRIDRUZI' and posljednji_znak != '':
            if len(brojac_dubina) > 0:
                brojac_dubina[-1] = brojac_dubina[-1] + 1
            # if len(brojac_dubina) > 1:
            #     brojac_dubina[-2] = brojac_dubina[-2] + 1
            if posljednji_znak == 'KR_ZA':
              pamtim_dubinu.append(pamtim_dubinu[-1] + 3)
            else:
              pamtim_dubinu.append(pamtim_dubinu[-1] + 1)
            brojcicc = pamtim_dubinu[-1]
        elif i == 'KR_ZA' and posljednji_znak != '':
            # if len(brojac_dubina) == 0:
            #     brojac_dubina.append(brp+1)
            # else:
            #     brojac_dubina.append(brp + 3)
            pamti_petljice.append(br)
            if posljednji_znak == 'OP_PRIDRUZI' or posljednji_znak == 'KR_AZ':
                pamtim_dubinu.append(pamtim_dubinu[-1] + 1)
                #if posljednji_znak == 'OP_PRIDRUZI':
                    #pamtim_dubinu.append(pamtim_dubinu[-1])
            else:
                pamtim_dubinu.append(pamtim_dubinu[-1] + 3)
            brojcicc = pamtim_dubinu[-1]
            brojac_dubina.append(brojcicc)
        elif i == 'KR_AZ':
            if len(pamti_petljice) > 0:
                if len(brojac_dubina) > 0:
                    brojcicc = brojac_dubina[-1] + 3
                    if posljednji_znak == 'KR_ZA' and pretposljednji_znak == 'KR_ZA':
                        pamtim_dubinu.append(pamtim_dubinu[-1])
                        pamtim_dubinu[-2] = pamtim_dubinu[-2] - 1
                    # if posljednji_znak != 'KR_ZA':
                    #     brojac_dubina[-2] = brojac_dubina[-2] + 1
                    brojac_dubina.pop()
                if posljednji_znak == 'KR_ZA' and len(pamtim_dubinu) > 1:
                    #brojcicc = pamtim_dubinu[pamti_petljice[-1]] + 3
                    pamtim_dubinu.pop()
                    pamtim_dubinu[-1] = pamtim_dubinu[-1] + 1
                else:
                    #brojcicc = pamtim_dubinu[pamti_petljice[-1]] + 4
                    for mama in range(br - pamti_petljice[-1] - 1):
                        if len(pamtim_dubinu) > 0:
                            pamtim_dubinu.pop()
                # print(br)
                # print(pamti_petljice[-1])
                pamti_petljice.pop()
                br = len(pamtim_dubinu) - 1
                if len(brojac_dubina) > 0:
                    brojac_dubina[-1] = brojac_dubina[-1] + 1

        pretposljednji_znak = posljednji_znak
        if i == 'OP_PRIDRUZI':
            posljednji_znak = 'OP_PRIDRUZI'
        elif i == 'KR_ZA':
            posljednji_znak = 'KR_ZA'
        else:
            posljednji_znak = 'KR_AZ'

        br = br + 1
        brp = brp + 1

        if len(valjda_dobro) == 0:
            valjda_dobro.append(1)
            #pamtim_dubinu.append(1)
        if brojcicc != 0:
          valjda_dobro.append(brojcicc)
        
        # print(pamti_petljice)
        # print(pamtim_dubinu)
        # print(valjda_dobro)
        # print(br)
        # print(brojac_dubina)
        # print()
        
valjda_dobro.append(pamtim_dubinu[-1] + 1)

# print(valjda_dobro)

stog = []
stog.append('#')
stog.append('<program>')

ispis += stog[-1]
ispis += '\n'

if (stog[-1] == '<program>') and ((pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'KR_ZA') or (pocetni_program[0] == 'kraj')):
    stog[-1] = '<lista_naredbi>'
    while True:
        if stog[-1] == '<lista_naredbi>':
            if (pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'KR_ZA'):
                # elif u_koliko_sam_petlji > koliko_az_ova:
                #     razmak_lista_naredbi.append(razmak_lista_naredbi[-1] + 3)
                # else:
                #     razmak_lista_naredbi.append(razmak_lista_naredbi[-1] + 1)
                for i in range(valjda_dobro[0]):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                ispisi_koliko_puta = ispisi_koliko_puta + 1
                broj_razmaka = valjda_dobro[0] + 1
                stog.append('<naredba>')
                valjda_dobro.pop(0)
            elif (pocetni_program[0] == 'KR_AZ') or (pocetni_program[0] == 'kraj'):
                for i in range(valjda_dobro[0]):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                stog.pop()
                for i in range(valjda_dobro[0] + 1):
                    ispis += ' '
                ispis += '$'
                ispis += '\n'
                valjda_dobro.pop(0)
                #broj_razmaka = broj_razmaka - 1
            else:
                zastavica = 1
                break
        
        if stog[-1] == '<naredba>':
            if pocetni_program[0] == 'IDN':
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                broj_razmaka = broj_razmaka + 1
                stog[-1] = '<naredba_pridruzivanja>'
            elif pocetni_program[0] == 'KR_ZA':
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                broj_razmaka = broj_razmaka + 1
                stog[-1] = '<za_petlja>'
            else:
                zastavica = 1
                break

        if stog[-1] == '<naredba_pridruzivanja>':
            if pocetni_program[0] == 'IDN':
                #razmak_lista_naredbi.append(razmak_lista_naredbi[-1] + 3)
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                broj_razmaka = broj_razmaka + 1
                ispis += '\n'
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                stog[-1] = '<E>'
                stog.append('OP_PRIDRUZI')
                pocetni_program.pop(0)
            else:
                zastavica = 1
                break

        if stog[-1] == '<za_petlja>':
            if pocetni_program[0] == 'KR_ZA':
                u_koliko_sam_petlji = u_koliko_sam_petlji + 1
                #razmak_lista_naredbi.append(razmak_lista_naredbi[-1] + 3)
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                broj_razmaka = broj_razmaka + 1
                petlje_broj_razmak.append(broj_razmaka)
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                stog[-1] = 'KR_AZ'
                stog.append('<lista_naredbi>')
                stog.append('<E>')
                stog.append('KR_DO')
                stog.append('<E>')
                stog.append('KR_OD')
                stog.append('IDN')
                pocetni_program.pop(0)
            else:
                zastavica = 1
                break

        if stog[-1] == '<E>':
            if (pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'BROJ') or (pocetni_program[0] == 'OP_PLUS') or (pocetni_program[0] == 'OP_MINUS') or (pocetni_program[0] == 'L_ZAGRADA'):
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                broj_razmaka = broj_razmaka + 1
                razmak_e.append(broj_razmaka)
                stog[-1] = '<E_lista>'
                stog.append('<T>')
            else:
                zastavica = 1
                break

        if stog[-1] == '<E_lista>':
            if (pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'D_ZAGRADA') or (pocetni_program[0] == 'KR_ZA') or (pocetni_program[0] == 'KR_DO') or (pocetni_program[0] == 'KR_AZ') or (pocetni_program[0] == 'kraj'):
                for i in range(razmak_e[-1]):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                stog.pop()
                for i in range(razmak_e[-1] + 1):
                    ispis += ' '
                ispis += '$'
                ispis += '\n'
                razmak_e.pop()
                broj_razmaka = broj_razmaka - 1
            elif (pocetni_program[0] == 'OP_PLUS') or (pocetni_program[0] == 'OP_MINUS'):
                for i in range(razmak_e[-1]):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                stog[-1] = '<E>'
                broj_razmaka = razmak_e[-1] + 1
                for i in range(razmak_e[-1] + 1):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                pocetni_program.pop(0)
                razmak_e.pop()
            else:
                zastavica = 1
                break

        if stog[-1] == '<T>':
            if (pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'BROJ') or (pocetni_program[0] == 'OP_PLUS') or (pocetni_program[0] == 'OP_MINUS') or (pocetni_program[0] == 'L_ZAGRADA'):
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                broj_razmaka = broj_razmaka + 1
                razmak_t.append(broj_razmaka)
                stog[-1] = '<T_lista>'
                stog.append('<P>')
            else:
                zastavica = 1
                break

        if stog[-1] == '<T_lista>':
            if (pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'OP_PLUS') or (pocetni_program[0] == 'OP_MINUS') or (pocetni_program[0] == 'D_ZAGRADA') or (pocetni_program[0] == 'KR_ZA') or (pocetni_program[0] == 'KR_DO') or (pocetni_program[0] == 'KR_AZ') or (pocetni_program[0] == 'kraj'):
                for i in range(razmak_t[-1]):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                stog.pop()
                for i in range(razmak_t[-1] + 1):
                    ispis += ' '
                ispis += '$'
                ispis += '\n'
                razmak_t.pop()
                broj_razmaka = broj_razmaka - 2
            elif (pocetni_program[0] == 'OP_PUTA') or (pocetni_program[0] == 'OP_DIJELI'):
                for i in range(razmak_t[-1]):
                    ispis += ' '
                ispis += stog[-1]
                ispis += '\n'
                stog[-1] = '<T>'
                broj_razmaka = razmak_t[-1] + 1
                for i in range(razmak_t[-1] + 1):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                razmak_t.pop()
                brojac = brojac + 1
                pocetni_program.pop(0)
            else:
                zastavica = 1
                break

        if stog[-1] == '<P>':
            if (pocetni_program[0] == 'IDN') or (pocetni_program[0] == 'BROJ'):
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                broj_razmaka = broj_razmaka + 1
                ispis += '\n'
                stog.pop()
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                pocetni_program.pop(0)
            elif (pocetni_program[0] == 'OP_PLUS') or (pocetni_program[0] == 'OP_MINUS'):
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                broj_razmaka = broj_razmaka + 1
                ispis += '\n'
                stog[-1] = '<P>'
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                #broj_razmaka = broj_razmaka - 1
                brojac = brojac + 1
                pocetni_program.pop(0)
            elif (pocetni_program[0] == 'L_ZAGRADA'):
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += stog[-1]
                broj_razmaka = broj_razmaka + 1
                ispis += '\n'
                stog[-1] = 'D_ZAGRADA'
                stog.append('<E>')
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                l_zagrade.append(broj_razmaka)
                ispis += '\n'
                brojac = brojac + 1
                pocetni_program.pop(0)
            else:
                zastavica = 1
                break

        if stog[-1] == 'IDN':
            if pocetni_program[0] == 'IDN':
                #razmak_lista_naredbi.pop()
                if len(petlje_broj_razmak) != 0:
                    broj_razmaka = petlje_broj_razmak[-1]
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                #broj_razmaka = broj_razmaka + 1
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
            else:
                zastavica = 1
                break

        if stog[-1] == 'OP_PRIDRUZI':
            if pocetni_program[0] == 'OP_PRIDRUZI':
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
            else:
                zastavica = 1
                break
        
        if stog[-1] == 'KR_OD':
            if pocetni_program[0] == 'KR_OD':
                broj_razmaka = petlje_broj_razmak[-1]
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                #broj_razmaka = broj_razmaka + 1
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
            else:
                zastavica = 1
                break

        if stog[-1] == 'KR_DO':
            if pocetni_program[0] == 'KR_DO':
                broj_razmaka = petlje_broj_razmak[-1]
                for i in range(broj_razmaka):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                #broj_razmaka = broj_razmaka + 1
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
            else:
                zastavica = 1
                break

        if stog[-1] == 'KR_AZ':
            if pocetni_program[0] == 'KR_AZ':
                koliko_az_ova = koliko_az_ova + 1
                for i in range(petlje_broj_razmak[-1]):
                    ispis += ' '
                petlje_broj_razmak.pop()
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
            else:
                zastavica = 1
                break

        if stog[-1] == 'D_ZAGRADA':
            if pocetni_program[0] == 'D_ZAGRADA':
                for i in range(l_zagrade[-1]):
                    ispis += ' '
                ispis += polje_redaka[brojac].strip()
                ispis += '\n'
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
                l_zagrade.pop()
            else:
                zastavica = 1
                break

        if stog[-1] == '#':
            if pocetni_program[0] == 'kraj':
                brojac = brojac + 1
                pocetni_program.pop(0)
                stog.pop()
            else:
                zastavica = 1
                break

        if len(pocetni_program) == 0:
            break

if len(pocetni_program) > 0:
    if pocetni_program[0] == 'OP_PRIDRUZI':
        zastavica = 1

if zastavica == 0:
    print(ispis)
else:
    ispis = ''
    ispis += 'err '
    if len(polje_redaka) <= brojac:
        ispis += 'kraj'
    else:
        ispis += polje_redaka[brojac].strip()
    print(ispis)