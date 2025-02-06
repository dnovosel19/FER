#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <math.h>


#define NUM_ITEMS 1000000
#define BUFFER_SIZE NUM_ITEMS

double buffer[BUFFER_SIZE];

double sum = 0.0;
int flag = 0;

void producer() {
    for (int i = 0; i < NUM_ITEMS; i++) {
        buffer[i] = sqrt(sqrt((double)i));
    }
    #pragma omp flush
    #pragma omp atomic write
        flag = 1;   // postavi zastavicu

    #pragma omp flush
}

void consumer() {
    #pragma omp flush
    int myFlag = 0;
    while (!myFlag) {   // cekaj producer()
        #pragma omp flush
        #pragma omp atomic read
            myFlag = flag;
    }
    
    #pragma omp flush
    for (int i = 0; i < NUM_ITEMS; i++) {
        double item = buffer[i];
        sum += item;
    }
}

int main() {

    double t1 = omp_get_wtime();
    
    #pragma omp parallel sections
    {
        #pragma omp section
        producer();
        
        #pragma omp section
        consumer();
    }
    
    double runtime = omp_get_wtime() - t1;

    printf("In %f seconds, The sum is %f \n",runtime,sum);

    return 0;
}