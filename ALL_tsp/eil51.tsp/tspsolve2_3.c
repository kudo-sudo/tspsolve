#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "mt19937.h"

int N; // 都市数
int **cost_matrix;

typedef struct {
    int id;
    int x;
    int y;
} City;

// 2点を受け取ってそこの間の移動コストを返す
int cost(int a, int b) {
    if (a == b) {
        return 0;
    }
    int i = (a > b) ? a : b;
    int j = (a > b) ? b : a;

    return cost_matrix[i][j];
}

// tourという巡回路をもらってきて、そこから計算している
int calc_cost(int *tour, int n) {
    int total_cost = 0;

    for (int i = 0; i < n - 1; i++) {
        total_cost += cost(tour[i], tour[i + 1]);
    }

    total_cost += cost(tour[n - 1], tour[0]);

    return total_cost;
}

int makeRandomTour(int *tour, int N) {
    for (int i = 0; i < N; i++) {
        tour[i] = i;
    }

    // tour配列をランダムに入れ替える
    for (int i = N - 1; i > 0; i--) {
        int j = genrand() % (i + 1);

        int temp = tour[i];
        tour[i] = tour[j];
        tour[j] = temp;
    }
}

int printCoords(int current_i, int total_I, int current_cost, int *tour, City *cities, char *instance_name) {
    char filename[30];
    FILE *fp;
    
    sprintf(filename, "random-tour-%d.dat", current_i);
    if ((fp = fopen(filename, "w")) == NULL) {
        fprintf(stderr, "File open error: %s\n", filename);
        exit(1);
    }
    
    fprintf(fp, "# Instance: %s\n", instance_name); // instance_name を使用
    fprintf(fp, "# Repetition: %d / %d\n", current_i, total_I);
    fprintf(fp, "# Cost: %d\n", current_cost);

    for (int i = 0; i < N; i++) {
        fprintf(fp, "%d %d\n", cities[tour[i]].x, cities[tour[i]].y);
    }
    // 輪を閉じるために、最初の都市の座標を最後にもう一度出力する
    fprintf(fp, "%d %d\n", cities[tour[0]].x, cities[tour[0]].y);
    
    fclose(fp);
}

int randomSearch(int I, int *tour, int N, int *tour_temp, City *cities, char *instance_name) {
    makeRandomTour(tour, N);
    int c = calc_cost(tour, N);
    printf("# first_value: %d\n", c);
    printf("0 %d\n", c);

    int interval = 100;

    int i = 1;
    while (i <= I) {
        makeRandomTour(tour_temp, N);
        int c_temp = calc_cost(tour_temp, N);
        if (c_temp < c) {
            memcpy(tour, tour_temp, sizeof(int) * N);
            c = c_temp;
        }
        printf("%d %d\n", i, c);
        if (i % interval == 0) {
            printCoords(i, I, c, tour, cities, instance_name);
        }
        i++;
    }
    return c;
}

int main(int argc, char *argv[]) {
    seed((uint_fast32_t)time(NULL));
    
    if (argc < 3) {
        fprintf(stderr, "Usage: tspsolve <file_path> <iterations>\n");
        exit(1);
    }
    
    int iterations = atoi(argv[2]);
    
    // 問題ファイルの読み込み
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        fprintf(stderr, "File open error: %s\n", argv[1]);
        exit(1);
    }

    // 都市数の読み込み
    do {
        char buf[100];
        fscanf(fp, "%s", buf);
        if (strcmp("DIMENSION", buf) == 0) {
            fscanf(fp, "%s", buf); // ":" をスキップ
            break;
        }
        if (strcmp("DIMENSION:", buf) == 0)
            break;
    } while (1);

    // 都市数を取得
    fscanf(fp, "%d", &N);

    City *cities = (City *)malloc(sizeof(City) * N);

    do {
        char buf[100];
        fscanf(fp, "%s", buf);
        if (strcmp("NODE_COORD_SECTION", buf) == 0) {
            break;
        }
    } while (1);
    
    // 都市ごとのidと座標を保存している
    for (int i = 0; i < N; i++) {
        fscanf(fp, "%d %d %d", &cities[i].id, &cities[i].x, &cities[i].y);
    }
    
    fclose(fp); // ファイルを閉じる
    
    // 移動コストをそれぞれ計算してぶち込んでる（下三角行列）枠を作ってる
    cost_matrix = (int **)malloc(sizeof(int *) * N);
    for (int i = 0; i < N; i++) {
        if (i == 0) {
            cost_matrix[i] = NULL;
        } else {
            cost_matrix[i] = (int *)malloc(sizeof(int) * i);
        }
    }
    
    // 実際に計算してコストを表に入れている
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < i; j++) {
            int dx = cities[i].x - cities[j].x;
            int dy = cities[i].y - cities[j].y;
            cost_matrix[i][j] = (int)round(sqrt(dx * dx + dy * dy));
        }
    }
    
    int *tour = (int *)malloc(sizeof(int) * N);
    int *tour_temp = (int *)malloc(sizeof(int) * N);

    char *instance_name = argv[1];
    char *slash = strrchr(argv[1], '/');
    if (slash == NULL) {
        slash = strrchr(argv[1], '\\');
    }
    if (slash != NULL) {
        instance_name = slash + 1;
    }

    int best_cost = randomSearch(iterations, tour, N, tour_temp, cities, instance_name);
    printf("# Final Best Cost: %d\n", best_cost);

    return 0;
}