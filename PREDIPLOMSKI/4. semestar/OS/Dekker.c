#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdatomic.h>


int *A;
atomic_int PRAVO = 0;
atomic_int ZASTAVICA[2] = {0};
int Id;

void dekker(int i, int M) {
    for(int j=0; j<M; j++) {
        ZASTAVICA[i] = 1;
        while(ZASTAVICA[1-i]) {
            if(PRAVO == 1 - i) {
                ZASTAVICA[i] = 0;
                while(PRAVO == 1 - i) {} // radno cekanje
                ZASTAVICA[i] = 1;
            }
        }

        (*A)++;
        //printf("Proces %d: %d\n", i, (*A));
        //sleep(1);
        PRAVO = 1-i;
        ZASTAVICA[i] = 0;
    }
}

int main(int argc, char *argv[]) {
    /* zauzimanje zajednicke memorije */
    Id = shmget(IPC_PRIVATE, sizeof(int), 0600); //pretvara kljuc segmenta zajednickog spremnika u njegov id broj
    if(Id == -1) {
        exit(1);
    }
    A = (int *) shmat(Id, NULL, 0); // proces veze segment za svoj adresni prostor
    *A = 0;

    int M;
    if(argc < 2) {
        printf("Greska");
        exit(1);
    }
    M = atoi(argv[1]);
    int pid[2];

    for(int i=0; i<2; i++) {
        pid[i] = fork();
        //printf("pid[%d] = %d\n", i,pid[i]);
        if(pid[i] < 0) {
            printf("Neuspjesno stvaranje procesa\n");
            exit(1);
        }
        if(pid[i] == 0) {
            dekker(i, M);
            exit(0);
        }
    }
    
    (void)wait(NULL);
    (void)wait(NULL);
    
    printf("A=%d\n", *A);
    
    (void) shmdt((char *) A); // otpustanje segmenta
    (void) shmctl(Id, IPC_RMID, NULL); // unistavanje segmenta
    exit(0);

    return 0;
}