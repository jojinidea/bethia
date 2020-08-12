// HashTable.c ... implementation of HashTable library

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "List.h"
#include "HashTable.h"

typedef struct _hash_table_rep {
   int nslots;    // size of chains[] array
   int nvals;     // # keys stored in table
   List *chains;  // array of hash chains 
} HashTableRep;

// hash function (int -> [0..nslots-1])
static int hash(int val, int nslots)
{
   return (val%nslots);
}

// create an empty hash table
HashTable newHashTable(int N)
{
   HashTable new;
   int i;
   new = malloc(sizeof(HashTableRep));
   assert(new != NULL);
   new->nslots = N;
   new->nvals = 0;
   new->chains = malloc(N*sizeof(List));
   assert(new->chains != NULL);
   for (i = 0; i < N; i++)
      new->chains[i] = newList();
   return new;
}

// free memory for a hash table
void dropHashTable(HashTable ht)
{
   assert(ht != NULL);
   int i;
   for (i = 0; i < ht->nslots; i++)
      dropList(ht->chains[i]);
   free(ht->chains);
   free(ht);
}

// display a hash table on stdout
void showHashTable(HashTable ht)
{
   assert(ht != NULL);
   int i;
   for (i = 0; i < ht->nslots; i++) {
      printf("[%2d] ",i);
      showList(ht->chains[i]);
   }
}

// add a new value into a HashTable
void insertHashTable(HashTable ht, int val)
{
   void expand(HashTable);
   assert(ht != NULL);
   if (ht->nvals > 2*ht->nslots) expand(ht);
   int h = hash(val,ht->nslots);
   appendList(ht->chains[h],val);
   ht->nvals++;
}

// double the number of slots/chains in a hash table
void expand(HashTable ht)
{

    int i = 0;
    int dim;
    
    List *new = malloc(2*ht->nslots*sizeof(List));
    // sizeof(List) is the size of one block of memory and we need ht->nslots * 2 blocks
    for (i = 0; i < ht->nslots * 2; i++) {
        new[i] = newList();
    }
    int j = 0;
    for (j = 0; j < ht->nslots; j++) {
        int *vals = valuesFromList(ht->chains[j], &dim);
        // for each value in the array, apply the hash function and insert it into the new list
        for (i = 0; i < dim; i++) {
            int hashVal = hash(vals[i], ht->nslots*2);
            fprintf(stderr, "Hash val is %d, val is %d\n", hashVal, vals[i]);
            // insert this value into appropriate position
            appendList(new[hashVal], vals[i]);
        }
    i = 0;
    }
    // free old list
    for (i = 0; i < ht->nslots; i++) {
        dropList(ht->chains[i]);
    }
    free(ht->chains);
    ht->chains = new;
    ht->nslots = ht->nslots * 2;
    
    // BE SUPER CAREFUL WITH ADTs, if we're ever given one with stuff like nElements, nValues, if we change this, make sure we modify accordingly otherwise the function will NOT WORK when tested!!

    
   return; //TODO
}
