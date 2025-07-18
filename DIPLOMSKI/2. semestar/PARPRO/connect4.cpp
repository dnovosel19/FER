#include <mpi.h>
#include <iostream>
#include <cstring>
#include <limits>
#include <cstdlib>
#include <assert.h>

#define ROWS 6
#define COLUMNS 7

int rank, size;

class Board {
	private:
		int height[COLUMNS];

		void Init() {	// inicijaliziraj na pocetno stanje
			for (int c = 0; c < COLUMNS; c++) {
				for (int r = 0; r < ROWS; r++) {
					game[r][c] = 0;
				}
				height[c] = 0;
			}
		}
	public:
		Board() { Init(); }		// poziv inicijalizacije
		int game[ROWS][COLUMNS];
		int last_move;

		int* operator[](const int row) {	// omoguci objektu klase da se ponasa kao 2D polje
			assert(row >= 0 && row < ROWS);
			return game[row];
		}

		bool hasSpace() {	// provjera postoji li slobodnih mjesta
			for (int c = 0; c < COLUMNS; c++) {
				if (game[ROWS - 1][c] == 0) return true;	// provjera samo najviseg retka dovoljna
			}
			return false;
		}

		bool legalMove(int c) {		// postoji li taj stupac i ima li mjesta
			return height[c] < ROWS && c >= 0 && c < COLUMNS;
		}

		void nextMove(int c, int player) {	// napravi potez
			game[height[c]][c] = player;
			height[c]++;
			last_move = player;
		}

		bool isWinningMove(int col) {	// provjeri postoji li 4 u nizu
			int row = height[col] - 1;	// zadnji red gdje smo napravili potez
			int player = game[row][col];	// koji je igrac napravio potez
			if (row < 0) return false;

			// lambda funkcija koja broji koliko je istih elemenata u zadanom smjeru
			auto countDirection = [&](int dRow, int dCol) -> int {
				int r = row + dRow;	// pocetna pozicija je jedan korak u odabranom smjeru od trenutne pozicije
				int c = col + dCol;
				int count = 0;

				while (r >= 0 && r < ROWS && c >= 0 && c < COLUMNS && game[r][c] == player) {	// broji koliko istih elemenata
					count++;
					r += dRow;
					c += dCol;
				}
				return count;
				};

			if (1 + countDirection(-1, 0) >= 4) return true;	// vertikalno
			if (1 + countDirection(0, -1) + countDirection(0, 1) >= 4) return true;		// horizontalno
			if (1 + countDirection(-1, -1) + countDirection(1, 1) >= 4) return true;	// dijagonalno '\'
			if (1 + countDirection(1, -1) + countDirection(-1, 1) >= 4) return true;	// dijagonalno '/'

			return false;
		}

		static Board copyBoard(Board b) {	// kopija trenutnog stanja igre
			Board copy;

			copy.last_move = b.last_move;
			for (int c = 0; c < COLUMNS; c++) {
				for (int r = 0; r < ROWS; r++) {
					copy.game[r][c] = b.game[r][c];
				}
				copy.height[c] = b.height[c];
			}

			return copy;
		}

		void undoMove(int c) {	// ponisti posljednji potez
			height[c]--;
			game[height[c]][c] = 0;
		}
};

struct sendHelp {	// pomocna struktura koja se salje sa MPI_Send
	Board board;
	int prev_move;
};

void printBoard(Board& board) {		// ispis trenutnog stanja ploce
	for (int r = ROWS - 1; r >= 0; r--) {
		for (int c = 0; c < COLUMNS; c++) {
			if (board.game[r][c] == 0) printf(" - ");
			else if (board.game[r][c] == 1) printf(" O ");
			else if (board.game[r][c] == 2) printf(" X ");
		}
		printf("\n");
	}
	for (int c = 0; c < COLUMNS; c++) printf(" %d ", c);
	printf("\n");
	printf("*********************\n\n");
	fflush(stdout);
}

double evaluate(Board b, int player, int last_move, int depth, bool isPar) {	// daje vrijednost potencijalnog poteza
	if (b.isWinningMove(last_move)) return player == 1 ? 1 : -1;
	int num_moves = 0, nextPlayer = player == 1 ? 2 : 1;
	double best_value = 0;
	bool lose = true, win = true;	// prati ako su svi potezi lose/win

	if (depth > 0) {	// cilj je doci do zadane dubine
		for (int c = 0; c < COLUMNS; c++) {	// provjeri sve legalne poteze
			if (b.legalMove(c)) {
				num_moves++;
				b.nextMove(c, nextPlayer);
				double value = evaluate(Board::copyBoard(b), nextPlayer, c, depth - 1, isPar);	// pamti vrijednost poteza
				b.undoMove(c);

				if (value != 1) win = false;
				if (value > -1) lose = false;
				if (value == -1 && nextPlayer == 2) return -1;
				if (value == 1 && nextPlayer == 1) return 1;

				best_value += value;
			}
		}
	}
	else if (isPar && depth == 0) {		// raspodijeli posao procesima 
		bool valid[COLUMNS];
		for (int c = 0; c < COLUMNS; c++) {
			if (b.legalMove(c)) {
				valid[c] = true;
				num_moves++;
				b.nextMove(c, nextPlayer);
				sendHelp pom;
				pom.board = Board::copyBoard(b);
				pom.prev_move = c;
				MPI_Send(&pom, sizeof(pom), MPI_BYTE, (c % (size - 1) + 1), 0, MPI_COMM_WORLD);	// koristi sve slave (bez master) i tako ciklicno
				b.undoMove(c);
			}
			else {
				valid[c] = false;
			}
		}

		for (int c = 0; c < COLUMNS; c++) {	// za sve dozvoljene poteze cekaj vrijednost slave-ova
			if (valid[c]) {
				double val;
				MPI_Recv(&val, sizeof(val), MPI_BYTE, (c % (size - 1) + 1), 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
				if (val > -1) lose = false;
				if (val != 1) win = false;
				best_value += val;
			}
		}
	}

	if (win) return 1;
	if (lose) return -1;
	return best_value / num_moves;	// vrati aritmeticku sredinu
}

int minimax(Board b, int depth, bool isSerial) {	// funkcija za pronalazak najboljeg poteza
	double best_value;
	int best_move = -1;

	for (int c = 0; c < COLUMNS; c++) {
		if (b.legalMove(c)) {	// ovdje 'ne postavljamo' novo stanje igre, nego probavamo sve poteze
			b.nextMove(c, 1);
			double value = evaluate(b, 1, c, depth, !isSerial);
			b.undoMove(c);
			if (best_move == -1 || value > best_value) {
				best_move = c;
				best_value = value;
			}
		}
	}

	return best_move;
}

// COMPUTER = 1, HUMAN = 2
void master_function(int master_depth, int slave_depth) {	// connect 4
	Board board;
	bool finish = false;
	int num_moves = 0;

	printBoard(board);
	
	while (board.hasSpace()) {	// ako ploca nije popunjena
		int chosen_column;
		printf("Choose your move (0 - 6): ");
		fflush(stdout);
		scanf_s("%d", &chosen_column);

		if (board.legalMove(chosen_column)) {
			board.nextMove(chosen_column, 2);	// zapisi covjekov odabrani potez
			printBoard(board);

			if (board.isWinningMove(chosen_column)) {	// provjera pobjede
				finish = true;
				printf("Winner winner chicken dinner\n");
				fflush(stdout);
				break;
			}

			clock_t start = clock();
			bool serial = (master_depth == 0 || size == 1) ? true : false;
			int computer_move = minimax(Board::copyBoard(board), master_depth, serial);
			clock_t end = clock();
			
			num_moves++;
			double time = (double)(end - start) / CLOCKS_PER_SEC;
			printf("Time needed to calculate the best move: %f s\n", time);
			printf("Computer played %d\n", computer_move);
			board.nextMove(computer_move, 1);	// racunalo radi svoj najbolji moguci potez
			printBoard(board);
			if (board.isWinningMove(computer_move)) {	// provjera pobjede
				finish = true;
				printf("Better luck next time\n");
				fflush(stdout);
				break;
			}
		}
	}

	if (!board.hasSpace() || !finish) {	// prostora nema, pobjednika nema
		printf("It's a tie\n");
		fflush(stdout);
	}

	for (int i = 1; i < size; i++) {	// ugasi procese
		sendHelp pom;
		pom.board = board;
		pom.prev_move = -1;
		MPI_Send(&pom, sizeof(sendHelp), MPI_BYTE, i, 0, MPI_COMM_WORLD);
	}

    double averageTime = totalTime / numberOfMoves;
    printf("Average time per computer move: %f seconds\n", averageTime);
    fflush(stdout);
}

void slave_function(int depth) {	// slave-ovi cekaju podatke od mastera i vracaju vrijednosti
	while (true) {
		sendHelp recive;
		MPI_Recv(&recive, sizeof(sendHelp), MPI_BYTE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

		if (recive.prev_move == -1) return;
		double val = evaluate(recive.board, recive.board.last_move, recive.prev_move, depth, false);
		MPI_Send(&val, sizeof(val), MPI_BYTE, 0, 1, MPI_COMM_WORLD);
	}
}


int main(int argc, char** argv) {
	MPI_Init(&argc, &argv);

	MPI_Comm_size(MPI_COMM_WORLD, &size);	// broj procesa
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);	// indeks procesa

	int master_depth = atoi(argv[1]);
	int slave_depth = atoi(argv[2]);

	if (rank == 0) {	// proces 0 je master
		master_function(master_depth, slave_depth);
	}
	else {
		slave_function(slave_depth);
	}

	MPI_Finalize();
	return 0;
}