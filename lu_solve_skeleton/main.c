#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <math.h>
#include "my_matrix.h"
#include "timer.h"


int numthreads = 0;

// BLAS functions
void dtrsm_(char *SIDE, char *UPLO, char *TRANS, char *DIAG, INT *M, INT *N, double *alpha, double *A, INT *LDA, double *RHS, INT *LDB);

// Scale a Column 
void scale_col(double s, struct my_matrix_st A, int i, int j, int col){
	int k; 
	for (k=i; k<j; k++){
		A.values[A.LD*col+k]*=s; 
	}
}

// Rank-1 Update 
void r1_update(struct my_matrix_st A, int i, int end, double s, double *v, int incv, 
	       double *w, int incw) {
	int j,k; 
	for (j = i ; j < end; j++){
		for ( k = i; k < end; k++){
			A.values[k+j*A.LD] += s * v[(k-i)*incv] * w[(j-i)*incw]; 
		}
	}
}


void innerUpdate( struct my_matrix_st A, int pos, int blockSize ){
	
	int i,j,k;
  
	#pragma omp parallel for shared(A, pos, blockSize) private(i,j,k) num_threads(numthreads)
	for(i=pos+blockSize; i<A.LD; i++){
	    for(j=pos+blockSize; j<A.LD; j++){
		
		for(k=0; k<blockSize; k++){
		  
		    A.values[i+j*A.LD] -= A.values[i + (pos+k)*A.LD] * A.values[ pos + k + j*A.LD ];
		    		  
		}
	      
	    } 
	}
	
	
}


void LU(struct my_matrix_st A, int pos, int blockSize){
        int k;
        for(k = pos; k < pos+blockSize; k++){
                scale_col(1/A.values[k + k*A.LD], A, k+1, pos+blockSize, k);
                r1_update(A, k+1, pos+blockSize, -1, &A.values[k+1 + k*A.LD], 1, &A.values[k + (k+1)*A.LD], A.LD);
        }
}


void BlOP_LU(struct my_matrix_st A, int blockSize){

	char SIDE;
	char UPLO;
	char TRANS = 'N';
	char DIAG;
	double alpha = 1;
	
	int m;
	int n;
	
	int pos;
	for(pos=0; pos<A.LD-blockSize; pos+=blockSize){
	    
	    LU(A, pos, blockSize);
	    
	    m = A.LD-(pos+blockSize);
	    n = A.LD-(pos+blockSize);
	    
	    // L
	    SIDE = 'R';
	    UPLO = 'U';
	    DIAG = 'N';
	    dtrsm_(&SIDE, &UPLO, &TRANS, &DIAG, &blockSize , &n, &alpha, &A.values[pos + pos*A.LD], &A.LD, &A.values[pos + blockSize + pos*A.LD], &A.LD);
	

	    //U
	    SIDE = 'L';
	    UPLO = 'L';
	    DIAG = 'U';
	    dtrsm_(&SIDE, &UPLO, &TRANS, &DIAG, &m, &blockSize , &alpha, &A.values[pos + pos*A.LD], &A.LD, &A.values[pos + (blockSize + pos)*A.LD], &A.LD);
	      
	     //inner rank-k update
	    innerUpdate( A, pos, blockSize );
	    
	}

	LU(A, pos, blockSize);
  
}


int main (int argc , char **argv ){
	int n = atoi(argv[1]);
	int blockSize = atoi(argv[2]);
	int T = atoi(argv[3]);
	
	// Build matrix
	struct my_matrix_st A;
	my_matrix_rand(&A,n,n);
	
	double tic,toc;

	 int i;
	 for(i=1;i<T;i++){
	    numthreads = i;
	    tic = walltime();
	    BlOP_LU(A,blockSize);
	    toc = walltime();
	    printf("Laufzeit für \t %d Threads: \t %f\n", i, toc-tic);
	 }
	
	// Cleanup
	my_matrix_clear(&A); 
	return 0; 

}
