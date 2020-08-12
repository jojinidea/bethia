# COMP2521 ass1

CC=gcc
CFLAGS=-Wall -Werror -std=gnu99 -gdwarf-2
BINS=testwhitebox

all: $(BINS)

testwhitebox : testwhitebox.o textbuffer.o
	$(CC) -o testwhitebox testwhitebox.o textbuffer.o -lm

textbuffer.o : textbuffer.c textbuffer.h -lm

clean:
	rm -f $(BINS) *.o core
