#include <stdio.h>
#include <time.h>
#include <signal.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>

int K_Z[3] = {0};
int T_P = 0;
int stog[3] = {0};
int prioritet_signala;

void obrada(int sig);

struct timespec t0; /* vrijeme pocetka programa */

/* postavlja trenutno vrijeme u t0 */
void postavi_pocetno_vrijeme() {
    clock_gettime(CLOCK_REALTIME, &t0);
}

/* dohvaca vrijeme proteklo od pokretanja programa */
void vrijeme(void) {
    struct timespec t;

    clock_gettime(CLOCK_REALTIME, &t);

    t.tv_sec -= t0.tv_sec;
    t.tv_nsec -= t0.tv_nsec;
    if(t.tv_nsec < 0) {
        t.tv_nsec += 1000000000;
        t.tv_sec--;
    }

    printf("%03ld.%03ld:\t", t.tv_sec, t.tv_nsec/1000000);
}

/* ispis kao i printf uz dodatak trenutnog vremena na pocetku */
#define PRINTF(format, ...)         \
do {                                \
    vrijeme();                      \
    printf(format, ##__VA_ARGS__);  \
}                                   \
while(0)

void inicijalizacija() {
    struct sigaction act;
    act.sa_handler = obrada;
    sigemptyset(&act.sa_mask);
    sigaction(SIGUSR1, &act, NULL);
    act.sa_flags = SA_NODEFER;

    act.sa_handler = obrada;
    sigemptyset(&act.sa_mask);
    sigaction(SIGTERM, &act, NULL);
    act.sa_flags = SA_NODEFER;

    act.sa_handler = obrada;
    sigemptyset(&act.sa_mask);
    sigaction(SIGINT, &act, NULL);
    act.sa_flags = SA_NODEFER;

    postavi_pocetno_vrijeme();
}

void postavi_stog() {
    int brojac = 0;
    for(int i=0; i<2; i++) {
        if(stog[i]) {
            brojac++;
        }
    }
    
    if(brojac == 0) {
        printf("0, reg[0]\n");
    } else if(brojac == 1) {
        for(int i=0; i<2; i++) {
            if(stog[i]) {
                printf("%d, reg[%d], 0, reg[0]\n", i+1, i+1);
            }
        }
    } else if(brojac == 2) {
        int br = 0;
        for(int i=1; i>=0; --i) {
            if(br == 0 && stog[i]) {
                br++;
                printf("%d, reg[%d], ", i+1, i+1);
            } else if(br == 1 && stog[i]) {
                printf("%d, reg[%d], 0, reg[0]\n", i+1, i+1);
            }
        }
    }

    printf("\n");
}

void obraduj_signal() {
    for(int i=0; i<20; i++) {
        sleep(1);
    }
}

int main() {
    inicijalizacija();

    PRINTF("Program s PID=%ld krenuo s radom\n", (long) getpid());
    PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
    printf("\n");

    while(1) {
        sleep(1);
    }
    
    return 0;
}

void obrada(int sig) {
    if(sig == 2) {
        if(T_P != 3) {
            K_Z[2] = 1;
            prioritet_signala = 3;
        } else {
            return;
        }
    } else if(sig == 10) {
        if(T_P != 2) {
            K_Z[1] = 1;
            prioritet_signala = 2;
        } else {
            return;
        }
    } else if(sig == 15) {
        if(T_P != 1) {
            K_Z[0] = 1;
            prioritet_signala = 1;
        } else {
            return;
        }
    }

    while((T_P != 0) || (K_Z[0] || K_Z[1] || K_Z[2])) {
        /* signal razine 3 */
        if(prioritet_signala == 3 && K_Z[2]) {
            PRINTF("SKLOP: Dogodio se prekid razine 3 i prosljeduje se procesoru\n");

            /* nije bilo tekuceg prekida */
            if(T_P == 0) {
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
                printf("\n");

                PRINTF("Pocela obrada prekida razine 3\n");
                K_Z[2] = 0;
                T_P = 3;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                obraduj_signal();
                T_P = 0;
                PRINTF("Zavrsila obrada prekida razine 3\n");
                PRINTF("Nastavlja se izvodenje glavnog programa\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
                printf("\n");
            } else if(T_P == 1) {   /* tekuci prekid razine 1 se zaustavlja da se obardi signal razine 3 */
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                PRINTF("Pocela obrada prekida razine 3\n");
                K_Z[2] = 0;
                T_P = 3;
                stog[0] = 1;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                obraduj_signal();
                PRINTF("Zavrsila obrada prekida razine 3\n");

                if(K_Z[1] || stog[1]) {
                    stog[0] = 1;
                    T_P = 2;
                } else {
                    PRINTF("Nastavlja se obrada prekida razine 1\n");
                    T_P = 1;
                    stog[0] = 0;
                    PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                    postavi_stog();
                    return;
                }
            } else if(T_P == 2) {   /* tekuci prekid razine 2 se zaustavlja da se obradi signal razine 2  */
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                PRINTF("Pocela obrada prekida razine 3\n");
                K_Z[2] = 0;
                T_P = 3;
                stog[1] = 1;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                obraduj_signal();
                PRINTF("Zavrsila obrada prekida razine 3\n");
                PRINTF("Nastavlja se obrada prekida razine 2\n");
                T_P = 2;
                stog[1] = 0;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                return;
            }
        }

        /* signal razine 2 */
        if(prioritet_signala == 2 || K_Z[1]) {
            if(T_P == 0) {  /* nije bilo aktivnog signala */
                PRINTF("SKLOP: Dogodio se prekid razine 2 i prosljeduje se procesoru\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
                printf("\n");
                PRINTF("Pocela obrada prekida razine 2\n");
                
                K_Z[1] = 0;
                T_P = 2;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                obraduj_signal();
                T_P = 0;
                PRINTF("Zavrsila obrada prekida razine 2\n");
                PRINTF("Nastavlja se izvodenje glavnog programa\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
                printf("\n");
            } else if(T_P == 1) {   /* prekida signal razine 1 */
                PRINTF("SKLOP: Dogodio se prekid razine 2 i prosljeduje se procesoru\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                PRINTF("Pocela obrada prekida razine 2\n");
                stog[0] = 1;
                K_Z[1] = 0;
                T_P = 2;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                obraduj_signal();
                T_P = 1;
                stog[0] = 0;
                PRINTF("Zavrsila obrada prekida razine 2\n");
                PRINTF("Nastavlja se obrada prekida razine 1\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                return;
            } else if(T_P == 3 && prioritet_signala!=1) {   /* pojava signala razine 2, ali aktivan signal razine 3 */
                PRINTF("SKLOP: Dogodio se prekid razine 2, ali se on pamti i ne prosljeduje procesoru\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                break;
            } else if(T_P == 2 && stog[0]) {
                T_P = 3;
                PRINTF("SKLOP: Dogodio se prekid razine 2 i prosljeduje se procesoru\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                PRINTF("Pocela obrada prekida razine 2\n");
                
                K_Z[1] = 0;
                T_P = 2;
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                stog[0] = 0;

                obraduj_signal();
                T_P = 1;
                PRINTF("Zavrsila obrada prekida razine 2\n");
                PRINTF("Nastavlja se obrada prekida razine 1\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                return;
            }
        }

        /* signal razine 1 */
        if(prioritet_signala == 1 || K_Z[0]) {
            if(T_P == 0) {  /* nema tekuceg prekida pa signal razine 1 se obraduje */
                PRINTF("SKLOP: Dogodio se prekid razine 1 i prosljeduje se pocesoru\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
                printf("\n");
                K_Z[0] = 0;
                T_P = 1;
                PRINTF("Pocela obrada prekida razine 1\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();

                obraduj_signal();
                T_P = 0;
                PRINTF("Zavrsila obrada prekida razine 1\n");
                PRINTF("Nastavlja se izvodenje glavnog programa\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: -\n", K_Z[0], K_Z[1], K_Z[2], T_P);
                printf("\n");
            } else {    /* signali razine 3 i 2 ce se obraditi prije prekida razine 1 */
                PRINTF("SKLOP: Dogodio se prekid razine 1, ali se on pamti i ne prosljeduje procesoru\n");
                PRINTF("K_Z=%d%d%d, T_P=%d, stog: ", K_Z[0], K_Z[1], K_Z[2], T_P);
                postavi_stog();
                break;
            }
        }
    }
}