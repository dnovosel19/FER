#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<omp.h>

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
    // provjera radi li OMP_NUM_THREADS
    // int num_thr = omp_get_max_threads();
    // printf("%d\n", num_thr);

    int N = atoi(argv[1]);  // numeric string u integer value
    float E = 0.0;
    float E_kv = 0.0;
    float start = omp_get_wtime();  // zapocni mjerenje vremena

    #pragma omp parallel 
    {
        unsigned int seed = time(NULL) ^ omp_get_thread_num();  // osiguravamo razlicite rezultate, XOR
        float local_E = 0.0;
        float local_E_kv = 0.0;
        
        #pragma omp for
            for(int i=0; i<N; i++) {
                float x = a + (b - a) * ((float)rand_r(&seed) / RAND_MAX);
                float f = integral_funkcije(x);
                // printf("%d. dretva sa rjesenjem %f\n", omp_get_thread_num(), x);
                local_E += f;
                local_E_kv += f*f;
            }
        #pragma omp atomic
            E += local_E;  // zapisi u sumu da se ne izgubi podatak
            E_kv += local_E_kv;
    }
    float I = ((b-a)/N) * E; // metoda Monte Carlo

    // izracun greske
    float stdev = sqrt((b-a) * ((E_kv/N) - (E/N) * (E/N)));
    float V = stdev / sqrt(N);

    float end = omp_get_wtime();
    float vrijeme = ((float) (end-start));
    
    printf("%.6f\n", I);
    printf("%.6f\n", V);
    printf("%.6f\n", vrijeme);
    
    return 0;
}