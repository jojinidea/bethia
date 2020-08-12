#include <stdio.h>
#include <stdlib.h>

int square(int num);
int reflect(int num);
int alter(int num, int (*fp) (int));

int main(void) {
    
    int num;
    scanf ("%d", &num);
    int (*fp) (int); // declare file pointer - takes in int, returns int
    fp = &reflect;  // gives the file pointer the address of the function
    printf ("%d\n", alter(num, fp));

}

int square(int num) {
    return num*num;

}

int reflect(int num) {
    return num;

}

// the below function alters the num depending on the file pointer we pass into it
// it then returns the result of the function (either square or reflect) (num)
int alter(int num, int (*fp) (int)) {
    return fp(num);

}
