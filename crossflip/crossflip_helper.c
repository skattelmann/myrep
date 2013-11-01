#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define BIT_SET(a,b) ((a) |= (1ULL<<(63-b)))
#define BIT_CHECK(a,b) ((a) & (1ULL<<(63-b)))
#define BIT_CLEAR(a,b) ((a) &= ~(1ULL<<(63-b)))

// DEBUGGING
// void printbits(unsigned long long num) {
// 	int i; 
// 	for(i = 63; i >= 0; i--) putchar('0' + ((num >> i) & 1));
// 	printf("\n");
// }


void genAb(void *boardIn, const int n1, const int n2, void *MIn){
  
	int *board = (int *) boardIn;
	unsigned long long *M = (unsigned long long *) MIn;
	
	int i,j,k;
	int Mcols = (n1*n2 + 1) / 64; if( (n1*n2 + 1) % 64 != 0 ) Mcols++;
	int bPos = n1*n2;
	int currentElem;
	for(i=0; i<n1;i++){
	  for(j=0;j<n2;j++){

	      currentElem = i*n2+j;  

	      if( board[i*n2+j] < 2 ){
		      BIT_SET( M[ currentElem*Mcols + currentElem / 64 ] , currentElem % 64 );
		      
		      if( board[currentElem] == 1){
			      BIT_SET( M[ currentElem*Mcols + bPos / 64 ] , bPos % 64 );
		      }
	      }
	      else{
		      continue;
	      }
	      
	      
	      for(k=j-1;k>=0;k--){
		      if(board[i*n2+k] < 2){
			      BIT_SET( M[currentElem*Mcols + (i*n2+k) / 64] , (i*n2+k) % 64 );
		      }
		      else{ 
			      break;
		      }
	      }
		      
	      for(k=j+1;k<n2;k++){
		      if(board[i*n2+k] < 2){
			      BIT_SET( M[currentElem*Mcols + (i*n2+k) / 64] , (i*n2+k) % 64 );
		      }
		      else{ 
			      break;
		      }
	      }
	      
	      for(k=i-1;k>=0;k--){
		      if(board[k*n2+j] < 2){
			      BIT_SET( M[currentElem*Mcols + (k*n2+j) / 64] , (k*n2+j) % 64 );
		      }
		      else{ 
			      break;
		      }
	      }
			      
	      for(k=i+1;k<n1;k++){
		      if(board[k*n2+j] < 2){
			      BIT_SET( M[currentElem*Mcols + (k*n2+j) / 64] , (k*n2+j) % 64 );
		      }
		      else{ 
			      break;
		      }
	      }
	      
	  }
	}
	
}

void binGauss(void *MIn, void *xIn, const int n){

	unsigned long long *M = (unsigned long long *) MIn;
	int *x = (int *) xIn;
	
	int Mcols = (n + 1) / 64; if( (n + 1) % 64 != 0 ) Mcols++;
	
	int i,j,k;
	unsigned long long *temp;
	int currRow = 0, found, varCounter = 0, sum;
	int *considered = (int *) malloc(sizeof(int) * n);
	
	//build array of pointer for the rows -> easy row swapping
	unsigned long long **rows = (unsigned long long **) malloc( sizeof(unsigned long long *) * n);
	for(i=0;i<n;i++){
	    rows[i] = M + i*Mcols;
	}

	//naive Gaussian Elimination with pivoting
	for(i=0; i<n;i++){
		 
		//find pivot and switch rows
		if( BIT_CHECK( *(rows[currRow] + i/64) , i % 64) == 0ULL ){
		    found = 0;
		    for(j=1;j<n-currRow;j++){
		      if( BIT_CHECK( *(rows[currRow+j] + i/64) , i % 64) > 0ULL ){
			  temp = rows[currRow];
			  rows[currRow] = rows[currRow+j];
			  rows[currRow+j] = temp;
			  found = 1; 		//a pivot has been found!
			  break;
		      }
		    }
		    
		    //couldn't find a pivot? -> declare coloumn as as 'not to be considered', don't increment currCol and move on
		    if( found == 0 ){
			  considered[i] = 0;
			  continue;
		    }  
		}
		    
		considered[i] = 1;

		
		//the elimination step
		#pragma omp parallel for
		for(j=1; j<n-currRow;j++){
			if( BIT_CHECK( *(rows[currRow+j] + i/64) , i % 64) > 0ULL ){
			    for(k=i/64;k<Mcols;k++){
				  *(rows[currRow+j]+k) = *(rows[currRow]+k) ^ *(rows[currRow+j]+k);
			    }
			    
			}
		}
		
		//increment currRow for the next step
		currRow++;
		
	}

	//backward substitution
	currRow--;
	for(i=n-1;i>=0;i--){
		if( considered[i] == 1 ){

		    if( BIT_CHECK( *(rows[currRow] + n/64) , n % 64) > 0ULL ) 	sum = 1;
		    else 							sum = 0;
		    
		    j=0;
		    for(k=0;k<n;k++){
		      
			if(j>=varCounter) break;
		      
			if(considered[n-1-k] == 1){
			    if( BIT_CHECK( *(rows[currRow] + (n-1-k)/64) , (n-1-k) % 64) > 0ULL && x[n-1-k] == 1 ) sum ^= 1;
			    j++;
			}

		    }
		    
		    x[i] = sum;
		    varCounter++;
		    currRow--;
		    
		  
		}
	}
	
}


void starter(void *boardIn, const int n1, const int n2, void *MIn, void *xIn, const int n ){
  
	genAb(boardIn, n1, n2, MIn);
	binGauss(MIn, xIn, n);
  
}









