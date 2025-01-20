#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <semaphore.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>

#define BROJ_DOLAZAKA 20

sem_t *stolica_slobodna;
sem_t *broj_klijenata;
int ID, ID2;
int *waiting_clients, *is_open, *koji_id, *num_of_chairs;
int Id, Id1, Id2, Id3;

int *shared_array;
int shmid;


void frizerka() {
    printf("Frizerka: Otvaram salon\n");
    printf("Frizerka: Postavljam znak OTVORENO\n");
    (*is_open) = 1;

    while(1) {
        if((*is_open) == 0 && (*waiting_clients) == 0) {
            printf("Frizerka: Postavljam znak ZATVORENO\n");
            printf("Frizerka: Zatvaram salon\n");
            break;
        } else if((*waiting_clients) > 0) {
            //provjeri sa petljom koji je klijent
            for(int i=0; i<BROJ_DOLAZAKA; i++) {
                if(shared_array[i] == 1) {
                    shared_array[i] = 0;
                    *koji_id = i+1;
                    break;
                }
            }
            printf("Frizerka: idem raditi na klijentu %d\n", *koji_id);
            (*waiting_clients)--;
            printf("\tKlijent (%d): frizerka mi radi frizuru\n", *koji_id);
            sleep(5); //rad na frizuri
            printf("Frizerka: Klijent %d je gotov\n", *koji_id);
            (*koji_id)++;
            sem_post(stolica_slobodna);
        } else if((*waiting_clients) == 0 && (*is_open) == 1) {
            printf("Frizerka: Spavam dok klijenti ne dođu\n");
            sem_wait(broj_klijenata);
        } else {
            (*is_open) = 0;
            printf("Salon je zatvoren i nema klijenata u čekaonici\n");
            break;
        }
    }
}

void klijent(int id) {
    printf("\tKlijent (%d): Želim na frizuru\n", id);
    if(*is_open == 1 && (*waiting_clients) < (*num_of_chairs)) {
        shared_array[id-1] = 1;
        (*waiting_clients)++;
        printf("\tKlijent (%d): Ulazim u čekaonicu (%d)\n", id, *waiting_clients);
        sem_post(broj_klijenata); //klijent dosao i to javio semaforom
        sem_wait(stolica_slobodna); //ako je stolica slobodna onda je zauzmi i to javi, inace cekaj
    } else if((*is_open) == 1 && (*waiting_clients) == (*num_of_chairs)){
        printf("\tKlijent (%d): Nema mjesta u čekaoni, vratit ću se sutra\n", id);
    } else {
        printf("\tKlijent (%d): Salon je zatvoren, vratit ću se sutra\n", id);
    }
}

int main() {
    shmid = shmget(IPC_PRIVATE, BROJ_DOLAZAKA*sizeof(int), IPC_CREAT | 0666);
    if(shmid < 0) {
        exit(1);
    }
    shared_array = shmat(shmid, NULL, 0);
    for(int i=0; i<BROJ_DOLAZAKA; i++) {
        shared_array[i] = 0;
    }


    Id = shmget(IPC_PRIVATE, sizeof(int), 0600); //pretvara kljuc segmenta zajednickog spremnika u njegov id broj
    if(Id == -1) {
        exit(1);
    }
    koji_id = (int *) shmat(Id, NULL, 0); // proces veze segment za svoj adresni prostor
    *koji_id = 1; //id prvog klijenta je 1

    Id1 = shmget(IPC_PRIVATE, sizeof(int), 0600); //pretvara kljuc segmenta zajednickog spremnika u njegov id broj
    if(Id1 == -1) {
        exit(1);
    }
    waiting_clients = (int *) shmat(Id1, NULL, 0); // proces veze segment za svoj adresni prostor
    *waiting_clients = 0; //nula klijenata ceka

    Id2 = shmget(IPC_PRIVATE, sizeof(int), 0600); //pretvara kljuc segmenta zajednickog spremnika u njegov id broj
    if(Id2 == -1) {
        exit(1);
    }
    is_open = (int *) shmat(Id2, NULL, 0); // proces veze segment za svoj adresni prostor
    *is_open = 0; //pocetno je salon zatvoren

    Id3 = shmget(IPC_PRIVATE, sizeof(int), 0600); //pretvara kljuc segmenta zajednickog spremnika u njegov id broj
    if(Id3 == -1) {
        exit(1);
    }
    num_of_chairs = (int *) shmat(Id3, NULL, 0); // proces veze segment za svoj adresni prostor
    *num_of_chairs = 10; //10 stolaca

    ID = shmget(IPC_PRIVATE, sizeof(sem_t), 0600);
    stolica_slobodna = shmat(ID, NULL, 0);
    shmctl(ID, IPC_RMID, NULL);
    sem_init(stolica_slobodna, 1, 1); //u pocetku je stolica slobodna 

    ID2 = shmget(IPC_PRIVATE, sizeof(sem_t), 0600);
    broj_klijenata = shmat(ID, NULL, 0);
    shmctl(ID, IPC_RMID, NULL);
    sem_init(broj_klijenata, 1, 0); //na pocetku je 0 klijenata

    if(fork() == 0) {
        frizerka();
        exit(0);
    }
    //wait(NULL);

    for(int i=0; i<BROJ_DOLAZAKA; i++) {
        sleep((int)rand()%3);
        if(fork() == 0) {
            klijent(i+1);
            exit(0);
        }
        if(i == BROJ_DOLAZAKA - 1)
            *is_open = 0;
    }

    wait(NULL);

    for(int i=0; i<BROJ_DOLAZAKA; i++)
        wait(NULL);

    sem_destroy(broj_klijenata);
    shmdt(broj_klijenata);
    sem_destroy(stolica_slobodna);
    shmdt(stolica_slobodna);
    return 0;
}