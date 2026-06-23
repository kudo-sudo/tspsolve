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
//2点を受け取ってそこの間の移動コストを返す
int cost(int a,int b){
    if(a == b){
        return 0;
    }
    int i = (a > b) ? a : b;
    int j = (a > b) ? b : a;

    return cost_matrix[i][j];
}
//tourという巡回路をもらってきて、そこから計算している
int calc_cost(int *tour,int n){
    int total_cost = 0;

    for(int i=0;i<n-1;i++){
        total_cost += cost(tour[i],tour[i+1]);

    }

    total_cost += cost(tour[n-1],tour[0]);

    return total_cost;
}

int makeRandomTour(int *tour,int N){
    for(int i = 0;i<N;i++){
        tour[i] = i;
    }

    //tour配列をランダムに入れ替える
    for(int i  = N -1;i>0;i--){
        int j = genrand() % (i+1);

        int temp = tour[i];
        tour[i] = tour[j];
        tour[j] = temp;
    }
}

int main(int argc, char *argv[]) {
    seed((uint_fast32_t)time(NULL));
    // `$ tspsolve <file path>` の形式でファイルへのパスが渡されることを想定
    if (argc < 2) {
        fprintf(stderr, "Usage: tspsolve <file_path>\n");
        exit(1);
    }

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
        // "DIMENSION" までスキップ
        if (strcmp("DIMENSION", buf) == 0) {
            fscanf(fp, "%s", buf); // ":" をスキップ
            break;                 // ループを抜ける
        }
        // "DIMENSION:" までスキップ
        if (strcmp("DIMENSION:", buf) == 0)
            break; // ループを抜ける
    } while (1);

    // 都市数を取得
    fscanf(fp, "%d", &N);

    // 動作確認のため都市数を表示
    //printf("dimension: %d\n", N);

    City *cities = (City *)malloc(sizeof(City) * N);

    do{
        char buf[100];
        fscanf(fp, "%s",buf);
        //NODE_COORD_SECTIONまでスキップ
        if(strcmp("NODE_COORD_SECTION", buf) == 0){
            break;
        }
    }while(1);
    //都市ごとのidと座標を保存している
    for(int i=0;i<N;i++){
        int ID,x,y;
        fscanf(fp, "%d %d %d",&cities[i].id,&cities[i].x,&cities[i].y);
        //printf("%d %d %d\n",cities[i].id,cities[i].x,cities[i].y);
    }
    
    fclose(fp); // ファイルを閉じる
    //移動コストをそれぞれ計算してぶち込んでる（下三角行列）枠を作ってる
    cost_matrix = (int **)malloc(sizeof(int *) * N);
    for(int i=0;i<N;i++){
        if(i == 0){
            cost_matrix[i] = NULL;
        }else{
            cost_matrix[i] = (int *)malloc(sizeof(int)*i);
        }
        

    }
    //実際に計算してコストを表に入れている
    for(int i=0;i<N;i++){
        for(int j=0;j<i;j++){
            int dx = cities[i].x - cities[j].x;
            int dy = cities[i].y - cities[j].y;
            cost_matrix[i][j] = (int)round(sqrt(dx*dx + dy*dy));
            }
        }
    //巡回路を昇順で行うためにtourに昇順で1から入れている
    int *tour = (int *)malloc(sizeof(int)*N);
    
    makeRandomTour(tour,N);

    int total = calc_cost(tour,N);
    printf("%d\n", total);

    return 0;
}   