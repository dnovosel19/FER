#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <stdbool.h>
#include <time.h>

#define TAG_FORK_SEND 1     // slanje vilice
#define TAG_FORK_RECIVE 0   // zahtjev za vilicu


void think(int size, int rank, bool prljava, bool* left_fork, bool* right_fork, int* req_left, int* req_right, int left_phil, int right_phil) {
    int think_duration = (rand() % 10) + 1;
    int flag, buf;
    MPI_Status status;

    printf("%*sFilozof %d misli %d sekundi.\n", rank * 4, "", rank, think_duration);
    fflush(stdout);

    for (int i = 0; i < think_duration; i++) {
        MPI_Iprobe(MPI_ANY_SOURCE, TAG_FORK_RECIVE, MPI_COMM_WORLD, &flag, &status);    // postoji li zahtjev za vilicom
        if (flag) {     // postoji zahtjev
            printf("%*sFilozof %d primio zahtjev od %d\n", rank * 4, "", rank, status.MPI_SOURCE);
            int request;
            MPI_Recv(&request, 1, MPI_INT, status.MPI_SOURCE, TAG_FORK_RECIVE, MPI_COMM_WORLD, &status);    // primi i obradi zahtjev za vilicom

            if (prljava) {  // daj vilicu
                printf("%*sFilozof %d salje vilicu filozofu %d\n", rank * 4, "", rank, status.MPI_SOURCE);
                fflush(stdout);
                if (size != 2) {
                    if (status.MPI_SOURCE == left_phil) *left_fork = false;
                    if (status.MPI_SOURCE == right_phil) *right_fork = false;
                }
                else if (size == 2) {
                    if (*left_fork && !(*right_fork)) {
                        *left_fork = false;
                    }
                    else if (!(*left_fork) && *right_fork) {
                        *right_fork = false;
                    }
                    else {
                        *left_fork = false;
                    }
                }

                MPI_Send(&buf, 1, MPI_INT, status.MPI_SOURCE, TAG_FORK_SEND, MPI_COMM_WORLD);   // slanje vilice
            }
            else {  // pamti zahtjev
                printf("%*sFilozof %d pamti zahtjev filozofa %d za vilicom\n", rank * 4, "", rank, status.MPI_SOURCE);
                fflush(stdout);

                if (status.MPI_SOURCE == left_phil) *req_left = 1;
                if (status.MPI_SOURCE == right_phil) *req_right = 1;
            }
        }

        Sleep(1000);
    }
}

void eat(int rank) {
    int eating = (rand() % 5) + 1;
    printf("%*sFilozof %d jede %d sekundi.\n", rank * 4, "", rank, eating);
    fflush(stdout);
    Sleep(eating * 1000);
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int size, rank;
    MPI_Comm_size(MPI_COMM_WORLD, &size);   // upisuje ukupan broj procesa u grupi u parametar size (n)
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);   // upisuje indeks procesa pozivatelja u parametar rank

    int left_phil, right_phil, req_left = 0, req_right = 0, must_req_left = 1, must_req_right = 1;
    bool left_fork, right_fork, prljava;
    MPI_Status status;

    if (rank == 0) {
        left_fork = true;
        right_fork = true;
        left_phil = rank + 1;
        right_phil = size - 1;
        prljava = true;
    }
    else if (rank == size - 1) {
        left_fork = false;
        right_fork = false;
        left_phil = 0;
        right_phil = rank - 1;
        prljava = true;
    }
    else {
        left_fork = true;
        right_fork = false;
        left_phil = rank + 1;
        right_phil = rank - 1;
        prljava = true;
    }

    /*printf("Filozof %d: vilice (%s, %s), lijevi: %d, desni: %d, prljava: %s\n", rank, left_fork ? "DA" : "NE", right_fork ? "DA" : "NE", left_phil, right_phil, prljava ? "DA" : "NE");
    fflush(stdout);*/

    srand((unsigned)time(NULL) + rank);

    while (true) {
        think(size, rank, prljava, &left_fork, &right_fork, &req_left, &req_right, left_phil, right_phil);

        printf("%*sFilozof %d je razmislio te zeli jesti\n", rank * 4, "", rank);
        fflush(stdout);

        if (!left_fork) {   // ako nema lijevu vilicu salje zahtjev
            int buf;
            printf("%*sFilozof %d trazi lijevu vilicu od filozofa %d\n", rank * 4, "", rank, left_phil);
            fflush(stdout);

            MPI_Send(&buf, 1, MPI_INT, left_phil, TAG_FORK_RECIVE, MPI_COMM_WORLD);     // salji zahtjev za vilicom
        }

        if (!right_fork) {  // ako nema desnu vilicu salje zahtjev
            int buf;
            printf("%*sFilozof %d trazi desnu vilicu od filozofa %d\n", rank * 4, "", rank, right_phil);
            fflush(stdout);

            MPI_Send(&buf, 1, MPI_INT, right_phil, TAG_FORK_RECIVE, MPI_COMM_WORLD);    // salji zahtjev za vilicom
        }

        while (!left_fork || !right_fork) { // dok nemam obje vilice
            int buf;
            MPI_Recv(&buf, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);   // cekaj neku poruku

            if (status.MPI_TAG == TAG_FORK_SEND) {  // dobio je neku vilicu
                
                if (size != 2) {    // ako je vise od 2 filozofa
                    if (status.MPI_SOURCE == left_phil) left_fork = true;
                    if (status.MPI_SOURCE == right_phil) right_fork = true;
                }
                else if (size == 2) {   // poseban slucaj za 2 filozofa jer samo njih dvoje komuniciraju
                    if (!left_fork && right_fork) {
                        left_fork = true;
                    }
                    else if (!right_fork && left_fork) {
                        right_fork = true;
                    }
                    else {
                        right_fork = true;
                    }
                }
                prljava = false;
                printf("%*sFilozof %d dobio vilicu od filozofa %d\n", rank * 4, "",  rank, status.MPI_SOURCE);
                fflush(stdout);
            }
            else if (status.MPI_TAG == TAG_FORK_RECIVE) {    // zahtjev za vilicom
                if (prljava) {  // ako je prljava onda je moze dati
                    printf("%*sFilozof %d daje vilicu filozofu %d\n", rank * 4, "", rank, status.MPI_SOURCE);
                    fflush(stdout);
                    MPI_Send(&buf, 1, MPI_INT, status.MPI_SOURCE, TAG_FORK_SEND, MPI_COMM_WORLD);   // salji vilicu

                    if (status.MPI_SOURCE == left_phil) {
                        left_fork = false;

                        int buf;
                        printf("%*sFilozof %d trazi lijevu vilicu od filozofa %d\n", rank * 4, "", rank, left_phil);
                        fflush(stdout);
                        MPI_Send(&buf, 1, MPI_INT, left_phil, TAG_FORK_RECIVE, MPI_COMM_WORLD); // ponovi zahtjev za vilicom koju si dao (nece se odma ispuniti zbog cistoce)
                    }
                    if (status.MPI_SOURCE == right_phil) {
                        right_fork = false;

                        int buf;
                        printf("%*sFilozof %d trazi desnu vilicu od filozofa %d", rank * 4, "", rank, right_phil);
                        fflush(stdout);
                        MPI_Send(&buf, 1, MPI_INT, right_phil, TAG_FORK_RECIVE, MPI_COMM_WORLD);    // ponovi zahtjev
                    }

                    prljava = true;
                }
                else {  // vilica je cista, samo pamti zahtjev
                    if (status.MPI_SOURCE == left_phil) req_left = 1;
                    if (status.MPI_SOURCE == right_phil) req_right = 1;
                    prljava = false;
                }
            }

        }

        eat(rank);
        prljava = true; // ako su bile ciste sada ce se zaprljati

        if (req_left) {     // postoji zahtjev za lijevom vilicom koji se zapamtio, moramo ga ispuniti
            int buf;
            printf("%*sFilozof %d odgovara na dobiveni zahtjev i salje lijevu vilicu filozofu %d\n", rank * 4, "", rank, left_phil);
            MPI_Send(&buf, 1, MPI_INT, left_phil, TAG_FORK_SEND, MPI_COMM_WORLD);
            left_fork = false;
            req_left = 0;
        }

        if (req_right) {    // postoji zahtjev za vilicom koji se zapamtio, moramo ga ispuniti
            int buf;
            printf("%*sFilozof %d odgovara na dobiveni zahtjev i salje desnu vilicu filozofu %d\n", rank * 4, "", rank, right_phil);
            MPI_Send(&buf, 1, MPI_INT, right_phil, TAG_FORK_SEND, MPI_COMM_WORLD);
            right_fork = false;
            req_right = 0;
        }
    }

    MPI_Finalize();
    return 0;
}