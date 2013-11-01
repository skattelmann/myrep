/** Some Helpers */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "mmio.h"
#include "my_matrix.h"


/**
 * returns the time in seconds since EPOCH (1.1.1970 00:00). 
 * used to implement an easy tic-toc time measurement. 
 **/
double wtime() {
	struct timeval tv;                                                                                                       
	gettimeofday (&tv, NULL);                                                                                                
	return tv.tv_sec + tv.tv_usec / 1e6;                                                                                     
}


/*
 * Read a dense matrix from a given file. It returns
 * 0 if it was successful. Otherwise it returns a negative value.
 */
int my_matrix_read(char *filename, struct my_matrix_st *A){
	FILE *fp; 
	MM_typecode type; 
	INT i,j; 
	double v; 

	if ( !(fp = fopen(filename,"r"))){
		fprintf(stderr, "Error opening:%s\n", filename); 
		return -1; 
	}

	if ( mm_read_banner(fp, &type) ) {
		fprintf(stderr, "Can not read matrix market header:%s\n", filename); 
		fclose(fp); 
		return -2; 
	}

	if ( !mm_is_real(type)){
		fprintf(stderr, "Only real matrices allowed.\n"); 
		fclose(fp); 
		return -3; 
	}
	if ( !mm_is_general(type)){
		fprintf(stderr, "Only unsymmetric matrices allowed.\n"); 
		fclose(fp); 
		return -4; 
	}
	if ( !mm_is_dense(type)) {
		fprintf(stderr, "Only dense matrices allowed.\n"); 
		fclose(fp); 
		return -5; 
	}
	if ( mm_read_mtx_array_size(fp, &(A->rows), &(A->cols))){
		fprintf(stderr,"Can not read the size information\n"); 
		fclose(fp); 
		return -6; 
	}
	
	A->values = (double *) malloc(sizeof(double) * A->rows * A->cols); 
	if ( !A->values){
		fprintf(stderr,"Can not allocate the matrix\n"); 
		fclose(fp); 
		return -7; 

	}
	A->LD = A->rows; 
	A->structure = 'U'; 
	for ( j = 0; j < A->cols; j++) {
		for ( i = 0 ; i < A->rows; i++){
			if ( fscanf(fp,"%lg",&v) != 1){
				fprintf(stderr,"Error while reading entry (%d,%d)\n", i,j); 
				fclose(fp); 
				return -8; 
			}
			A->values[A->LD*j+i] = v; 
		}
	}
	fclose(fp); 
	return 0; 
}

/*
 * Create a random rows-by-cols matrix. It returns 0 on success otherwise a 
 * non zero value.
 */
int my_matrix_rand(struct my_matrix_st *A, INT rows, INT cols) {
	INT i, j; 
	srand(time(NULL)); 
	A->rows = rows; 
	A->cols = cols; 
	A->LD = rows; 
	A->values = (double *) malloc(sizeof(double) * A->rows * A->cols); 
	if ( !A->values){
		fprintf(stderr,"Can not allocate the matrix\n"); 
		return -1; 
	}
	for ( j = 0; j < A->cols; j++) {
		for ( i = 0 ; i < A->rows; i++){
			A->values[A->LD*j+i] =rand()/(double)RAND_MAX; 
		}
	}
	return 0; 
}

void my_matrix_print(struct my_matrix_st *A) {
	INT i,j; 
	
	for ( i=0; i< A->rows; i++ ) {

		for ( j=0; j< A->cols; j++ ) {
			printf("%15.10e ", A->values[A->LD*j+i]); 
		}
		printf("\n"); 
	}
}


/*
 * Deallocate a matrix
 */
void my_matrix_clear(struct my_matrix_st *A) {
	if ( A->values) free(A->values); 
}




