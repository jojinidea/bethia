#include <stdio.h>
#include <stdlib.h>

int main (void) {

    int A[10];
    int num = 0;
    
    for (int i = 0; i < 10; i++) {
        scanf("%d", &num);
        A[i] = num;
    }

// logic of algorithm
// compare A[i] and A[i+1], if A[i] > A[i+1], swap these two elements
// increment i by 1
// do this until we get to the last element 
// do this until the whole array is sorted

    int len = 10;
    int i = 0;
    
    
    for (int sorted = 10; sorted > 0; sorted--) {
        for (i = 0; i < sorted - 1; i++) {
            if (A[i] > A[i + 1]) {
                int temp = A[i + 1];
                A[i + 1] = A[i];
                A[i] = temp;
            }
        }
    i = 0;
    }

    i = 0;
    for (i = 0; i < len; i++) {
        printf("%d\n", A[i]);
    }
    
    


}
