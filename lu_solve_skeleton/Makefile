SRC=main.c mmio.c helper.c timer.c
OUTPUT=lu_solve
CC=gcc
CFLAGS= -fopenmp -O2 
LIBS= -lblas -lgfortran -lm 
OBJ=${SRC:.c=.o}

$(OUTPUT): $(OBJ)
	$(CC) -o $(OUTPUT) $(CFLAGS) $(OBJ) $(LIBS) 

.SUFFIXES: .c .o
.c.o:
	$(CC) -c -o $@ $(CFLAGS) $<
clean:
	rm -f $(OBJ)
.PHONY: clean 


