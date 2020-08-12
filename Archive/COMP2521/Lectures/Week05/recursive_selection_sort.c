// write a recursive selection sort algorithm 

#include <stdio.h>
#include <stdlib.h>

void selection_sort(int array[10], int L); 
void print_array(int array[10]);

int main (void) {

    int num; 
    int array[10];    
    
    for (int i = 0; i < 10; i++) {
            scanf("%d", &num);
            array[i] = num;
    }
    selection_sort(array, 0);
    print_array(array);

}

void selection_sort(int array[10], int L) {
// selection sort is where we find the smallest element in the array

    int size = 10;
    
    // this means the array does not need any more sorting
    if (L == size-2) {
        return;
    }
    
    // we want to compare the elements from L to size-1 to find the current min
    // we want to put the current min at L
    
    int i;
    int min_index = 0;
    
    for(i = L; i < size-1; i++) {
        int curr_min = array[L];
        if (array[i] < curr_min) {
            curr_min = array[i];
            min_index = i;
        }
    }
    // insert curr_min at L's place
    int temp = array[L];
    array[L] = array[min_index];
    array[min_index] = temp;
    
    selection_sort(array, L+1);
     
}

void print_array(int array[10]) {
    int size = 10;
    for (int i= 0; i < size; i++) {
        printf("Hi %d\n", array[i]);
    } 

}
