#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

#define BROJ_MJESTA 7
#define BROJ_DOLAZAKA 10

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t udi_u_brod = PTHREAD_COND_INITIALIZER;
pthread_cond_t brod_kreni = PTHREAD_COND_INITIALIZER;

int random_obala[BROJ_DOLAZAKA*2]; // odabir obale (random)
int br_k = 0, br_m = 0; // broj kanibala, misionara u camcu
int zauzeto_mjesta = 0; // zauzeto mjesta u brodu
int koja_strana = 1;  // 0 je lijevo, 1 je desno

int broji_dolaske = 0; // brojac dolazaka
int lijevo = 0, desno = 0, brojac_brod = 0;
int misionari_cekaju_l = 0, misionari_cekaju_d = 0;
int polje_dolazaka_misionari_lijevo[2*BROJ_DOLAZAKA];
int polje_dolazaka_kanibala_desno[2*BROJ_DOLAZAKA];
int polje_dolazaka_misionari_desno[2*BROJ_DOLAZAKA];
int polje_dolazaka_kanibala_lijevo[2*BROJ_DOLAZAKA];
int polje_misionara[BROJ_MJESTA]; //pamti id misionara u brodu
int polje_kanibala[BROJ_MJESTA]; //pamti id kanibala u brodu


void print_funkcija_polazak() {
    if(koja_strana == 0) {
        printf("C[L]:{");
    } else {
        printf("C[D]:{");
    }

    int br = 0;
    for(int i=0; i<BROJ_MJESTA; i++) {
        if((polje_kanibala[i] != -1) || (polje_misionara[i] != -1)) {
            br++;
        }
    }
    if(br == 0) {
        printf("} ");
    }

    for(int i=0; i<BROJ_MJESTA; i++) {
        if(((polje_misionara[i] != -1) || (polje_kanibala[i] != -1)) && (i < br-1)) {
            if(polje_misionara[i] != -1) {
                printf("M%d ", polje_misionara[i]);
            } else {
                printf("K%d ", polje_kanibala[i]);
            }
        } else if((polje_misionara[i] != -1) || (polje_kanibala[i] != -1)) {
            if(polje_misionara[i] != -1) {
                printf("M%d} ", polje_misionara[i]);
            } else {
                printf("K%d} ", polje_kanibala[i]);
            }
        } else {
            continue;;
        }
    }

    int br1 = 0, br2 = 0;
    for(int i=0; i<2*BROJ_DOLAZAKA; i++) {
        if((polje_dolazaka_misionari_desno[i] != -1)) {
            br1++;
        }
        if(polje_dolazaka_misionari_lijevo[i] != -1) {
            br2++;
        }
        if(polje_dolazaka_kanibala_desno[i] != -1) {
            br1++;
        }
        if(polje_dolazaka_kanibala_lijevo[i] != -1) {
            br2++;
        }
    }

    br = 0;
    printf("LO={");
    for(int i=0; i<2*BROJ_DOLAZAKA; i++) {
        if(((polje_dolazaka_kanibala_lijevo[i] != -1) || (polje_dolazaka_misionari_lijevo[i] != -1)) && (br2 > br+1)) {
            br++;
            if(polje_dolazaka_kanibala_lijevo[i] != -1) {
                printf("K%d ", polje_dolazaka_kanibala_lijevo[i]);
            }
            if(polje_dolazaka_misionari_lijevo[i] != -1) {
                printf("M%d ", polje_dolazaka_misionari_lijevo[i]);
            }
        } else if((polje_dolazaka_kanibala_lijevo[i] != -1) || (polje_dolazaka_misionari_lijevo[i] != -1)) {
            if(polje_dolazaka_misionari_lijevo[i] != -1) {
                printf("M%d} ", polje_dolazaka_misionari_lijevo[i]);
            } else {
                printf("K%d} ", polje_dolazaka_kanibala_lijevo[i]);
            }
        }
    }
    if(br2 == 0) {
        printf("} ");
    }

    br = 0;
    printf("DO={");
    for(int i=0; i<2*BROJ_DOLAZAKA; i++) {
        if(((polje_dolazaka_kanibala_desno[i] != -1) || (polje_dolazaka_misionari_desno[i] != -1)) && (br1 > br+1)) {
            br++;
            if(polje_dolazaka_kanibala_desno[i] != -1) {
                printf("K%d ", polje_dolazaka_kanibala_desno[i]);
            }
            if(polje_dolazaka_misionari_desno[i] != -1) {
                printf("M%d ", polje_dolazaka_misionari_desno[i]);
            }
        } else if((polje_dolazaka_kanibala_desno[i] != -1) || (polje_dolazaka_misionari_desno[i] != -1)) {
            if(polje_dolazaka_misionari_desno[i] != -1) {
                printf("M%d} ", polje_dolazaka_misionari_desno[i]);
            } else {
                printf("K%d} ", polje_dolazaka_kanibala_desno[i]);
            }
        }
    }
    if(br1 == 0) {
        printf("} ");
    }
    printf("\n\n");
}


void* misionar(void *start_routine) {
    int obala;
    pthread_mutex_lock(&mutex);
    
    int id = *(int*)start_routine + 1;

    if(random_obala[id-1] == 0) {
        obala = 0;
        polje_dolazaka_misionari_lijevo[broji_dolaske] = id;
        printf("M%d: došao na lijevu obalu\n", id);
        print_funkcija_polazak();
        misionari_cekaju_l++;
    } else {
        obala = 1;
        polje_dolazaka_misionari_desno[broji_dolaske] = id;
        printf("M%d: došao na desnu obalu\n", id);
        print_funkcija_polazak();
        misionari_cekaju_d++;
    }
    broji_dolaske++;

    pthread_mutex_unlock(&mutex);

    int index = -1;
    pthread_mutex_lock(&mutex);
    while(1) {
        //pthread_mutex_lock(&mutex);
        if(index == -1) {
            index = broji_dolaske - 1;
        }
        if(obala){
            if(koja_strana == obala && zauzeto_mjesta < BROJ_MJESTA && (br_k<=br_m || br_k == 1 || (misionari_cekaju_d + br_m >= br_k && BROJ_MJESTA <= misionari_cekaju_d+br_k+br_m))) {
                printf("M%d: ušao u čamac\n", id);
                misionari_cekaju_d--;
                if(obala) {
                    polje_dolazaka_misionari_desno[index] = -1;
                } else {
                    polje_dolazaka_misionari_lijevo[index] = -1;
                }
                polje_misionara[brojac_brod] = id;
                br_m++;
                brojac_brod++;

                print_funkcija_polazak();
                zauzeto_mjesta++;

                pthread_cond_broadcast(&udi_u_brod);
                //zauzeto_mjesta++;
                pthread_cond_signal(&brod_kreni);
                //pthread_mutex_unlock(&mutex);
                break;
            } else {
                //pthread_cond_broadcast(&udi_u_brod); //DODANO
                pthread_cond_wait(&udi_u_brod, &mutex);
                //pthread_mutex_unlock(&mutex);
            }
        } else {
            if(koja_strana == obala && zauzeto_mjesta < BROJ_MJESTA && (br_k<=br_m || br_k == 1 || (misionari_cekaju_l + br_m >= br_k && BROJ_MJESTA <= misionari_cekaju_l+br_k+br_m))) {
                printf("M%d: ušao u čamac\n", id);
                misionari_cekaju_l--;

                if(obala) {
                    polje_dolazaka_misionari_desno[index] = -1;
                } else {
                    polje_dolazaka_misionari_lijevo[index] = -1;
                }
                polje_misionara[brojac_brod] = id;
                br_m++;
                brojac_brod++;

                print_funkcija_polazak();
                zauzeto_mjesta++;

                pthread_cond_broadcast(&udi_u_brod);
                //zauzeto_mjesta++;
                pthread_cond_signal(&brod_kreni);
                //pthread_mutex_unlock(&mutex);
                break;
            } else {
                //pthread_cond_broadcast(&udi_u_brod); //DODANO
                pthread_cond_wait(&udi_u_brod, &mutex);
                //pthread_mutex_unlock(&mutex);
            }
        }
    }
    pthread_mutex_unlock(&mutex);
}

void* kanibal(void *start_routine) {
    int obala;
    pthread_mutex_lock(&mutex);
    
    int id = *(int*)start_routine + 1;

    if(random_obala[BROJ_DOLAZAKA+(id-1)] == 0) {
        obala = 0;
        polje_dolazaka_kanibala_lijevo[broji_dolaske] = id;
        printf("K%d: došao na lijevu obalu\n", id);
        print_funkcija_polazak();
    } else {
        obala = 1;
        polje_dolazaka_kanibala_desno[broji_dolaske] = id;
        printf("K%d: došao na desnu obalu\n", id);
        print_funkcija_polazak();
    }
    broji_dolaske++;

    pthread_mutex_unlock(&mutex);

    int index = -1;
    pthread_mutex_lock(&mutex);
    while(1) {
        //pthread_mutex_lock(&mutex);
        if(index == -1) {
            index = broji_dolaske-1;
        }
        if(koja_strana == obala && zauzeto_mjesta < BROJ_MJESTA && (br_k<br_m || br_m == 0)) {
            printf("K%d: ušao u čamac\n", id);

            if(obala) {
                polje_dolazaka_kanibala_desno[index] = -1;
            } else {
                polje_dolazaka_kanibala_lijevo[index] = -1;
            }
            polje_kanibala[brojac_brod] = id;
            br_k++;
            brojac_brod++;

            print_funkcija_polazak();
            zauzeto_mjesta++;

            pthread_cond_broadcast(&udi_u_brod);
            //zauzeto_mjesta++;
            pthread_cond_signal(&brod_kreni);
            //pthread_mutex_unlock(&mutex);
            break;
        } else {
            //pthread_cond_broadcast(&udi_u_brod); //DODANO
            pthread_cond_wait(&udi_u_brod, &mutex);
            //pthread_mutex_unlock(&mutex);
        }
    }
    pthread_mutex_unlock(&mutex);
}

void* brod() {
    while(1) {
        pthread_mutex_lock(&mutex);
        if(koja_strana) {
            printf("C: prazan na desnoj obali\n");
        } else {
            printf("C: prazan na lijevoj obali\n");
        }
        print_funkcija_polazak();

        while(zauzeto_mjesta < 3) {
            pthread_cond_wait(&brod_kreni, &mutex);
        }
        pthread_mutex_unlock(&mutex);
        printf("C: tri putnika ukrcana, polazim za jednu sekundu\n");
        print_funkcija_polazak();
        sleep(1);
        pthread_mutex_lock(&mutex);
        pthread_cond_broadcast(&udi_u_brod);
        pthread_mutex_unlock(&mutex);

        int pamti_obalu = 1 - koja_strana;
        if(koja_strana) {
            printf("Prevozim putnike s desne na lijevu stranu: ");
        } else {
            printf("Prevozim putnike s lijeve na desnu stranu: ");
        }
        for(int i=0; i<BROJ_MJESTA; i++) {
            if((polje_kanibala[i] != -1) || (polje_misionara[i] != -1)) {
                if(polje_kanibala[i] != -1) {
                    printf("K%d ", polje_kanibala[i]);
                } else {
                    printf("M%d ", polje_misionara[i]);
                }
            }
        }
        printf("\n");
        //print_funkcija_polazak();

        koja_strana = -1;   // brod plovi
        sleep(2);

        for(int i=0; i<BROJ_MJESTA; i++) {
            polje_kanibala[i] = -1;
            polje_misionara[i] = -1;
        }
        br_k = 0;
        br_m = 0;
        zauzeto_mjesta = 0;
        koja_strana = pamti_obalu;
        brojac_brod = 0;

        pthread_mutex_lock(&mutex);
        pthread_cond_broadcast(&udi_u_brod);
        pthread_mutex_unlock(&mutex);
    }
}

int main() {
    //srand((int)time(NULL));
    srand(1000);

    for(int i=0; i<2*BROJ_DOLAZAKA; i++) {
        polje_dolazaka_misionari_lijevo[i] = -1;
        polje_dolazaka_kanibala_desno[i] = -1;
        polje_dolazaka_misionari_desno[i] = -1;
        polje_dolazaka_kanibala_lijevo[i] = -1;
    }

    for(int i=0; i<BROJ_MJESTA; i++) {
        polje_kanibala[i] = -1;
        polje_misionara[i] = -1;
    }

    pthread_t boat;
    pthread_t misionari[BROJ_DOLAZAKA];
    pthread_t kanibali[BROJ_DOLAZAKA];

    if(pthread_create(&boat, NULL, brod, NULL)) {
        printf("Error\n");
        return 1;
    }
    sleep(1);

    for(int i=0; i<BROJ_DOLAZAKA; i++) {
        random_obala[i] = rand()%2;
        pthread_create(&misionari[i], NULL, misionar, (void*)&i);
        sleep(2);
        random_obala[BROJ_DOLAZAKA+i] = rand()%2;
        pthread_create(&kanibali[i], NULL, kanibal, (void*)&i);
        sleep(1);
    }

    pthread_join(boat, NULL);
    for(int i=0; i<BROJ_DOLAZAKA; i++) {
        pthread_join(misionari[i], NULL);
    }
    for(int i=0; i<BROJ_DOLAZAKA; i++) {
        pthread_join(kanibali[i], NULL);
    }

    return 0;
}