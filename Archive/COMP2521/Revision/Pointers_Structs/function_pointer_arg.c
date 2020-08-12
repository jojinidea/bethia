int my_function(int *a) // takes in a variable that points to some address

int input;
int a = my_function(&input) // pass in the address of a variable that is declared in a program (a pointer is a variable that holds an address) 
// we want the pointer to hold the address of a local variable in main, but when the function is called, the value IN the address changes

// any changes made by the function using the pointer (using the address) needs to be permanently made at the address of the passed variable

// a pointer is just something that stores a memory address
//declare a variable - e.g. input
int input
//if the function uses a pointer all it is saying is it needs a memory address
pass in &input // IF we passed in *input, this wouldn't necessarily make sense because it's not pointing anywhere

// if we are given a pointer, if we want to access its value, dereference it
int *p
print p // prints address stored in p
print *p // prints value stored at address

// we want to pass in the memory address of a variable if a function requires a pointer (address), not a pointer itself as where is the pointer POINTING TO (what address does the variable contain)?  
