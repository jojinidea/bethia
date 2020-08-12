// structs group different data types together 

#include <stdio.h>

struct person {
    int age;
    double height;
    char *name;

};

// if we want to declare a struct person within the declaration, we can do the following

/* struct person {
    int age;
    double height;
    char *name;
} example, example_2, example_3, example_4; // declares 4 types of struct persons

// typedefs - similar to a hash-define, old type after typedef and person_t - every time struct person exists in the code, we can make it person_t

typedef struct person person_t;



*/ 

int main (void) {

    struct person example;
    // struct person is a type, example is the name
    example.age = 18;
    example.height = 179.1;
    example.name = "Robert";
    
    // can create a pointer to a struct
    
    struct person *sp;
    sp = %example;
    // variable called sp that points to a struct person
    // need to give this an address 

    (*sp).age // dereferences the struct. alternatively, we can use sp->age
    

}
