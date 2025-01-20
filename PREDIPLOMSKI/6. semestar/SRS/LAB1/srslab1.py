import sys
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password

    def initt(self):
        salt = get_random_bytes(16)     # a (byte) string to use for better protection from dictionary attacks
        key = PBKDF2(self.master_password, salt, 32, count=100000, hmac_hash_module=SHA512) # a byte string of length dkLen used as key material
        
        nonce = get_random_bytes(16)    # value that must never be reused
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)    # AES alg = (secret key (16, 24, 32 bytes long), mode, iv - initialization vector, nonce - 16 bytes long)
        
        data = get_random_bytes(16)
        ciphertext, tag = cipher.encrypt_and_digest(data)   # sifriranje podataka (rezultat sifriranja je ciphertext), generiranje autenticnosti (provjera integriteta pri desifriranju, tag)
        
        # spremi u svaku zasebnu datoteku binarni zapis podataka
        with open("salt.txt", "wb") as file1:
            file1.write(salt)
        with open("nonce.txt", "wb") as file2:
            file2.write(nonce)
        with open("tag.txt", "wb") as file3:
            file3.write(tag)
        with open("ciphertext.txt", "wb") as file4:
            file4.write(ciphertext)
        
        print("Password manager initialized.")

    def put(self, par_adresa_zaporka):
        adresa = par_adresa_zaporka[0].encode()     # adresa u nizu bajtova
        zaporka = par_adresa_zaporka[1].encode()    # zaporka u nizu bajtova

        # procitaj i zapisi zadnje pohranjene vrijednosti od salt, nonce, tag i ciphertext
        with open("salt.txt", "rb") as file1:
            salt = file1.read()
        with open("nonce.txt", "rb") as file2:
            nonce = file2.read()
        with open("tag.txt", "rb") as file3:
            tag = file3.read()
        with open("ciphertext.txt", "rb") as file4:
            ciphertext = file4.read()
        
        key = PBKDF2(self.master_password, salt, 32, count=100000, hmac_hash_module=SHA512)     # ako je master password dobar onda se generira dobar kljuc
        
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)    # ako je key dobar, dobar je i cipher
        
        # probaj desifrirati i provjeri autenticnost 
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext=ciphertext, received_mac_tag=tag)
        except (KeyError, ValueError):
            print("Master password incorrect or integrity check failed.")
            return
        
        # ako adresa postoji onda promjeni zaporku
        lista_redaka = plaintext.split(b'\n')
        plaintext = b""
        promjena = 0
        for i in lista_redaka:
            if i.split(b" ")[0] == adresa:
                i = adresa + b" " + zaporka
                promjena = 1
            plaintext += i + b'\n'

        # ako adresa nije pronadena onda je potrebno i adresu i zaporku zapisati
        if promjena == 0:
            # lista_redaka.append(adresa + b" " + zaporka)
            plaintext += adresa + b" " + zaporka + b'\n'

        # generiramo novu salt, nonce, tag, ciphertext kako bi bilo napadacu sto teze probiti u nas sustav
        salt = get_random_bytes(16)
        key = PBKDF2(self.master_password, salt, 32, count=100000, hmac_hash_module=SHA512)
        
        nonce = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # zapisi nove vrijednosti u txt filove
        with open("salt.txt", "wb") as file1:
            file1.write(salt)
        with open("nonce.txt", "wb") as file2:
            file2.write(nonce)
        with open("tag.txt", "wb") as file3:
            file3.write(tag)
        with open("ciphertext.txt", "wb") as file4:
            file4.write(ciphertext)
        
        print("Stored password for " + adresa.decode())

    def get(self, adresa):
        # procitaj i zapisi posljednje vrijednosti salt, nonce, tag i ciphertext
        with open("salt.txt", "rb") as file1:
            salt = file1.read()
        with open("nonce.txt", "rb") as file2:
            nonce = file2.read()
        with open("tag.txt", "rb") as file3:
            tag = file3.read()
        with open("ciphertext.txt", "rb") as file4:
            ciphertext = file4.read()
        
        key = PBKDF2(self.master_password, salt, 32, count=100000, hmac_hash_module=SHA512)     # ako je master password dobar onda se generira dobar kljuc
        
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)    # ako je key dobar, dobar je i cipher
        
        # probaj desifrirati i provjeri autenticnost
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext=ciphertext, received_mac_tag=tag)
        except (KeyError, ValueError):
            print("Master password incorrect or integrity check failed.")
            return
        
        # trazi adresu, ako postoji procitaj sifru
        lista_redaka = plaintext.split(b'\n')
        adresa_postoji = 0
        for i in lista_redaka:
            if i.split(b' ')[0] == adresa:
                password = i.split(b' ')[1]
                adresa_postoji = 1

        # ako ne postoji, prekini
        if adresa_postoji == 0:
            #print("Address not found.")
            print("Master password incorrect or integrity check failed.")
            return
        
        # generiraj nove vrijednosti
        salt = get_random_bytes(16)
        key = PBKDF2(self.master_password, salt, 32, count=100000, hmac_hash_module=SHA512)
        
        nonce = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # zapisi nove vrijednosti salt, nonce, tag, ciphertext
        with open("salt.txt", "wb") as file1:
            file1.write(salt)
        with open("nonce.txt", "wb") as file2:
            file2.write(nonce)
        with open("tag.txt", "wb") as file3:
            file3.write(tag)
        with open("ciphertext.txt", "wb") as file4:
            file4.write(ciphertext)
        
        print("Password for " + adresa.decode() + " is: " + password.decode())

unos = sys.argv                         # ucitavanje s komandne linije
command = unos[1]                       # init / put / get
master_password = unos[2]
password_manager = PasswordManager(master_password)

if command == 'init':
    # if (len(master_password) > 8): # mozda jos neki uvjeti kako bi sifra bila sto jaca, "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$" - regex oblik ideje
    password_manager.initt()
elif command == 'put':
    par_adresa_zaporka = (unos[3], unos[4]) # (adresa, zaporka)
    password_manager.put(par_adresa_zaporka)
elif command == 'get':
    password_manager.get(unos[3].encode()) # (adresa), niz bajtova