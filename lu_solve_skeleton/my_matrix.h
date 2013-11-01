#ifndef MY_MATRIX_H
#define MY_MATRIX_H

#ifndef INT
#define INT int
#endif

struct my_matrix_st {
	INT cols; 
	INT rows; 
	INT LD; 
	double * values; 
	char structure; 
}; 

int my_matrix_read(char *filename, struct my_matrix_st *A); 
int my_matrix_rand(struct my_matrix_st *A, INT rows, INT cols);  
void my_matrix_print(struct my_matrix_st *A); 
void my_matrix_clear(struct my_matrix_st *A); 


double wtime(); 

#endif
