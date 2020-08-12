#include <stdio.h>

struct person {
    int age;
    double height; 
    char *name;

}; 

typedef struct person person_t;

int main (void) {

    person_t Bob;
    Bob.age = 10;
    Bob.height = 198.7;
    Bob.name = "Bob";
    
    printf ("Age is %d, height is %lf, name is %s\n", Bob.age, Bob.height, Bob.name);

return 0;

}
