import getpass
import sys
import bcrypt

# provjera je li lozinka sadrzi malo i veliko slovo, barem jedan broj, neki poseban znak te duljinu barem 8 znakova
def provjera_ispravnosti_lozinke(lozinka):
    veliko = False
    malo = False
    broj = False
    poseban_znak = False
    if len(lozinka) < 8:
        duljina = False
    else:
        duljina = True

    for i in lozinka:
        if i.isdigit():
            broj = True
        if i.isupper():
            veliko = True
        if i.islower():
            malo = True
        if not i.isalnum():
            poseban_znak = True
    return veliko and malo and broj and poseban_znak and duljina

unos = sys.argv
korisnicko_ime = unos[1]

with open("userbase.txt", "r") as file:
    users = file.readlines()

zapis = ''
promjena = 0
prekid = True
broj_pogresaka = 0
nema_imena = 0

while prekid:
    zapis = ''
    # ako smo tri puta krivu lozinku utipkali onda prekini program
    if broj_pogresaka == 3:
        exit()

    password = getpass.getpass(prompt="Password:")
    for ind, i in enumerate(users):
        user = i.split()
        if user[0] == korisnicko_ime:
            nema_imena = 1
            salt = user[1].encode()
            bytes_password = password.encode('utf-8')
            hash = bcrypt.hashpw(bytes_password, salt)

            # ako nema zahtjeva za novom lozinkom
            if user[3] == '0':
                if hash.decode() == user[2]:
                    zapis += users[ind]
                    prekid = False
                    promjena = 1
                else:
                    print("Username or password incorrect.")
                    broj_pogresaka += 1
            
            # postoji zahtjev za novom lozinkom
            else:
                if hash.decode() != user[2]:
                    print("Username or password incorrect.")
                    broj_pogresaka += 1
                    break
                new_password = getpass.getpass(prompt="New password:")
                
                while True:
                    if provjera_ispravnosti_lozinke(new_password):
                        if password == new_password:
                            print("Cannot change the password to the same password")
                            new_password = getpass.getpass(prompt="New password:")
                        else:
                            break
                    else:
                        print("New password isn't strong enough.")
                        new_password = getpass.getpass(prompt="New password:")

                repeat_new_password = getpass.getpass(prompt="Repeat new password:")

                # generiraj nove hasheve
                new_salt = bcrypt.gensalt()
                new_bytes_password = new_password.encode('utf-8')
                new_hash = bcrypt.hashpw(new_bytes_password, new_salt)

                if new_password == repeat_new_password:
                    zapis += korisnicko_ime + ' ' + new_salt.decode() + ' ' + new_hash.decode() + ' 0\n'
                    promjena = 1
                    prekid = False
                
                else:
                    print("Password change failed. Password mismatch.")
                    exit()

        else:
            zapis += users[ind]
    
    # ako taj user ne postoji
    if nema_imena == 0:
        print("Username or password incorrect.")
        break

if promjena:
    with open("userbase.txt", "w") as file:
        file.write(zapis)
    print("bash$")