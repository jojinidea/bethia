// ARRAYS to POINTERS
// a pointer needs a certain amount of SPACE in memory to store the thing it will store
// char * pointer needs enough memory to store a char! 
// if we have a variable that is an array of pointers

List *chain // chain is a variable that is an array of lists
// a list is a pointer to something with a first rep and a last rep
// each field of the array stores a list (a pointer/memory address)

// if we want to declare a new array of lists
// each element of the array needs to store a list
sizeof(List); // this would just create one list, but we want to create many lists, so, use
num_indices*sizeof(List)

