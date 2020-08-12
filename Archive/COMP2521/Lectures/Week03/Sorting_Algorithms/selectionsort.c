// simple implementation of selection sort

#include <stdio.h>
#include <stdlib.h>

#define MAX_LEN 100000

int main (void) {
    
    int num = 0;
    int array[MAX_LEN];
    int i = 0;
    
    // scans input into array 
    
    while (scanf(%d, &num) == 1) {
        array[i] = num;
        i++;
    }   

    int counter = 0; // counter to keep track of which elements are sorted vs which are unsorted
    
    while (counter < len) {
    
    }
    


}

// finds smallest element in the array, returns index

int find_smallest(int len, int counter) {
       
    int i = 0;
    int min = array[0];
    
    while (i < len) {
        if (array[i] < min) {
            min = array[i]; break;
        }
    i++;
    }

return i;

}
