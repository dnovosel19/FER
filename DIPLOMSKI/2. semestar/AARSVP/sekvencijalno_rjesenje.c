#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>

#define WIDTH 3840
#define HEIGHT 2160
#define FRAME_SIZE (WIDTH * HEIGHT)
#define NUM_FRAMES 60


// rgb -> yuv
void rgb_to_yuv_convert(uint8_t *RGB, uint8_t *Y, uint8_t *U, uint8_t *V) {
    uint8_t *R = RGB;
    uint8_t *G = RGB + FRAME_SIZE;
    uint8_t *B = RGB + 2 * FRAME_SIZE;

    for (int i = 0; i < FRAME_SIZE; i++) {
        Y[i] = (uint8_t)(0.257 * R[i] + 0.504 * G[i] + 0.098 * B[i] + 16);
        U[i] = (uint8_t)(-0.148 * R[i] - 0.291 * G[i] + 0.439 * B[i] + 128);
        V[i] = (uint8_t)(0.439 * R[i] - 0.368 * G[i] - 0.071 * B[i] + 128);
    }
}

void poduzorkovanje(uint8_t *U444, uint8_t *V444, uint8_t *U420, uint8_t *V420) {
    for (int i = 0; i < HEIGHT; i += 2) {
        for (int j = 0; j < WIDTH; j += 2) {
            int output_index = (i / 2) * (WIDTH / 2) + (j / 2);
            int top_left = i * WIDTH + j;
            int top_right = i * WIDTH + (j + 1);
            int bottom_left = (i + 1) * WIDTH + j;
            int bottom_right = (i + 1) * WIDTH + (j + 1);

            U420[output_index] = (U444[top_left] + U444[top_right] + U444[bottom_left] + U444[bottom_right]) / 4;
            V420[output_index] = (V444[top_left] + V444[top_right] + V444[bottom_left] + V444[bottom_right]) / 4;
        }
    }
}

void naduzorkovanje(uint8_t *U420, uint8_t *V420, uint8_t *U444, uint8_t *V444) {
    for (int i = 0; i < HEIGHT; ++i) {
        for (int j = 0; j < WIDTH; ++j) {
            int position420 = (i / 2) * (WIDTH / 2) + (j / 2);
            int position444 = i * WIDTH + j;
            U444[position444] = U420[position420];
            V444[position444] = V420[position420];
        }
    }
}

// spremi u YUV 4:4:4 format
void write_yuv444(FILE *fout, uint8_t *Y, uint8_t *U, uint8_t *V) {
    fwrite(Y, 1, FRAME_SIZE, fout);
    fwrite(U, 1, FRAME_SIZE, fout);
    fwrite(V, 1, FRAME_SIZE, fout);
}

// spremi u YUV 4:2:0 format
void write_yuv420(FILE *fout, uint8_t *Y, uint8_t *U420, uint8_t *V420) {
    fwrite(Y, 1, FRAME_SIZE, fout);
    fwrite(U420, 1, FRAME_SIZE / 4, fout);
    fwrite(V420, 1, FRAME_SIZE / 4, fout);
}

int main() {
    FILE *fin = fopen("raw_video.yuv", "rb");
    FILE *rgb_yuv = fopen("rgb_to_yuv.yuv", "wb");
    FILE *poduzork = fopen("poduzorkovanje.yuv", "wb");
    FILE *naduzork = fopen("naduzorkovanje.yuv", "wb");

    if (!fin || !rgb_yuv || !poduzork || !naduzork) {
        perror("Pogreska pri citanju");
        return 1;
    }

    uint8_t *RGB = malloc(3 * FRAME_SIZE);
    uint8_t *Y = malloc(FRAME_SIZE);
    uint8_t *U = malloc(FRAME_SIZE);
    uint8_t *V = malloc(FRAME_SIZE);
    uint8_t *U420 = malloc(FRAME_SIZE / 4);
    uint8_t *V420 = malloc(FRAME_SIZE / 4);
    uint8_t *U_upsampled = malloc(FRAME_SIZE);
    uint8_t *V_upsampled = malloc(FRAME_SIZE);

    double start = omp_get_wtime();
    for (int f = 0; f < NUM_FRAMES; f++) {
        fread(RGB, 1, 3 * FRAME_SIZE, fin);     // citaj jedan frame

        rgb_to_yuv_convert(RGB, Y, U, V);
        write_yuv444(rgb_yuv, Y, U, V);

        poduzorkovanje(U, V, U420, V420);
        write_yuv420(poduzork, Y, U420, V420);

        naduzorkovanje(U420, V420, U_upsampled, V_upsampled);
        write_yuv444(naduzork, Y, U_upsampled, V_upsampled);

        // printf("Obradeni frame: %d\n", f);
    }
    double end = omp_get_wtime();

    printf("Vrijeme trajanja s taskovima: %.6f s\n", end - start);

    fclose(fin);
    fclose(rgb_yuv);
    fclose(poduzork);
    fclose(naduzork);

    free(RGB);
    free(Y);
    free(U);
    free(V);
    free(U420);
    free(V420);
    free(U_upsampled);
    free(V_upsampled);

    return 0;
}
