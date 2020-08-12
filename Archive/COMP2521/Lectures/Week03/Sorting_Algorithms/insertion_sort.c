// implementation of insertion sort

#include <stdio.h>
#include <stdlib.h>

int main (void) {

    int i = 0;
    int array[10];
    int len = 10;
    int num = 0;
    
    for (i = 0; i < 10; i++) {
        scanf("%d", &num);
        array[i] = num;
        printf("Array[%d] is %d\n", i, array[i]);
    }

// logic of the algorithm 
// we treat the first element of the array as 'sorted'
// we then pick out elements from index 1 to index len-1
// we compare this with the elements before it
// if the element before it is greater, we move that element up one


    i = 0;
    int X = 0;
    int j = 0;
    
    for (i = 1; i < len; i++) {
        X = array[i];
        printf("Current X is %d\n", array[i]);
        for (j = i-1; j>= 0 && array[j] > X; j--) {                         // WHILE the element to the left is larger, shift it so we can find the space
            array[j+1] = array[j];
            printf("Moving %d up one\n", array[j]);
        }
        array[j+1] = X;
    }

    i = 0;
    for (i = 0; i < len; i++) {
        printf("%d\n", array[i]);
    }
  


return 0; 

}
