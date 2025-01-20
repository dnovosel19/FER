#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdatomic.h>
#include <unistd.h>

int A = 0;
int N, M;
atomic_int* ULAZ;
atomic_int* BROJ;

void udi_u_ko(int i) {
    ULAZ[i] = 1;
    int max = 0;

    for(int j=0; j<N; j++) {
        if(BROJ[j] > max) {
            max = BROJ[j];
        }
    }

    BROJ[i] = max+1;
    ULAZ[i] = 0;

    for(int j=0; j<N; j++) {
        if(j != i) {
            while(ULAZ[j] != 0);
            while(BROJ[j] != 0 && (BROJ[j] < BROJ[i] || (BROJ[j] == BROJ[i] && j<i)));
        }
    }
}

void izadi_iz_ko(int i) {
    BROJ[i] = 0;
}

void* lamport(void* start_routine) {
    //int id = *(int*)start_routine;
    for(int i=0; i<M; i++) {
        udi_u_ko(i);
        A++;
        printf("A = %d, dretva = %d\n", A, i);
        izadi_iz_ko(i);
    }
    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {
    if(argc != 3) {
        printf("Greska.\n");
        return 1;
    }

    N = atoi(argv[1]);
    M = atoi(argv[2]);

    if(N <= 0 || M <= 0) {
        printf("Greska.\n");
        return 1;
    }

    ULAZ = (atomic_int*)calloc(N, sizeof(atomic_int));
    BROJ = (atomic_int*)calloc(N, sizeof(atomic_int));

    pthread_t dretve[N];
    //int dretve_id[N];

    for(int i=0; i<N; i++) {
        //dretve_id[i] = i;
        pthread_create(&dretve[i], NULL, lamport, NULL); //(void*)&dretve_id[i]);
    }
    for(int i=0; i<N; i++) {
        pthread_join(dretve[i], NULL);
    }

    //printf("ZAVRSNI: ");
    printf("A = %d\n", A);
    
    free(ULAZ);
    free(BROJ);

    return 0;
}