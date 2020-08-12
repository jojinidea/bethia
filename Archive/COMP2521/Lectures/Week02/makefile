# Makefile for Set ADT

CC = gcc
CFLAGS = -Wall -Werror -g

all : ts slab
// make sure ts or slab are up to date

ts : testSet.o Set.o   // creates executable out of testSet.o and Set.o
	$(CC) -o ts testSet.o Set.o

slab : SetLab.o Set.o
	$(CC) -o slab SetLab.o Set.o

testSet.o : testSet.c Set.h 
	$(CC) $(CFLAGS) -c testSet.c

SetLab.o : SetLab.c Set.h
	$(CC) $(CFLAGS) -c SetLab.c

Set.o : Set.c Set.h Bool.h
// we don't care weather set.o is about a linked list/array

clean : // remove all object files to recreate everything
	rm -f *.o slab ts core

