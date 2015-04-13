SRC=crossflip_helper.c
OUTPUT=crossflip_helper.so
CC=gcc
CFLAGS=-m64 -O3 -fopenmp -shared -Wl,-soname,crossflip_helper
LIBS= -fPIC
OBJ=${SRC:.c=.o}

genAb: crossflip_helper.o
	$(CC) $(CFLAGS) -o $(OUTPUT) $(LIBS) $(SRC)
	rm -f $(OBJ)
	
clean:
	rm *.so
.PHONY: clean 
