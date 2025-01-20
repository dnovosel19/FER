#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

#define a 0.0
#define b 10.0

float integral_funkcije(float x) {  // funkcija za izracun 
    float rez;
    if (x != 0.0) {
        rez = sin(x) / x;
    } else {
        rez = 1.0; // sprijeci dijeljenje s 0, pogledaj na grafu koja je vrijednost u x = 0
    }
    return rez;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Pogresan broj ulaznih parametara.\n");
        return 1;
    }

    int N = atoi(argv[1]);  // numeric string u integer value
    unsigned int seed = time(NULL); // uvijek drugaciji seed
    float E = 0.0;
    float E_kv = 0.0;
    clock_t start, end; // kada pocinje i zavrsava izracun vrijednosti integrala

    start = clock();    // zapocinje mjerenje vremena
    for(int i=0; i<N; i++) {
        float x = a + (b - a) * ((float)rand_r(&seed) / RAND_MAX);
        float f = integral_funkcije(x);
        //printf("%f\n", x);
        E += f;
        E_kv += f*f;
    }
    float I = ((b-a)/N) * E; // metoda Monte Carlo

    // izracun greske
    float stdev = sqrt((b-a) * ((E_kv/N) - (E/N) * (E/N)));
    float V = stdev / sqrt(N);
    end = clock();  // zavrsava mjerenje vremena

    float vrijeme = ((float) (end-start)) / CLOCKS_PER_SEC;
    
    printf("%.6f\n", I);
    printf("%.6f\n", V);
    printf("%.6f\n", vrijeme);
    
    return 0;
}