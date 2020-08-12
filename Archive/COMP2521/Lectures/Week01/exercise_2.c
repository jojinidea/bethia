// exercise 2, sequence program

#include <stdio.h>
#include <stdlib.h>

void checkstep(int start, int step, int finish);
void printseq (int start, int step, int finish);

int main (int argc, char *argv[]) {
    int start;
    int finish;
    int step;

    switch (argc) {
    
        case 2:
        start = 1; 
        finish = atoi(argv[1]);
        step = (start < finish) ? 1 : -1;
        // if start is less than finish, step = 1, otherwise it is equal to -1   
        break;
        
        case 3:
        start = atoi(argv[1]);
        finish = atoi(argv[2]);
        step = (start < finish) ? 1 : -1; 
        break;
        
        case 4: 
        start = atoi(argv[1]);
        finish = atoi(argv[3]);
        step = atoi(argv[2]);
        checkstep(start, step, finish);
        break;
        
        default: 
        fprintf(stderr, "Usage: %s [start] [step] finish\n", argv[0]);
        
        exit(EXIT_FAILURE);
        // exit terminates the program - EXIT_SUCCESS results in a successful termination status being returned to the host environment
        // EXIT_FAILURE results in an unsuccessful termination status being returned to the host environment
        break;        
    }
    
    printseq(start, step, finish);
    
return 0;

}

void checkstep(int start, int step, int finish) {
    // start is greater than finish, step has to be negative
    // start is less than finish, step has to be positive 
    
    int ok = 1;
    
    if (step == 0) {
        ok = 0;
        // 0 is TRUE
    } else if (start < finish && step < 0) {
        ok = 0;
    } else if (start > finish && step > 0) {
        ok = 0;
    }
    if (!ok) {
        // !false evaluates to 0 which evaluates to true, which means the condition will be executed
        fprintf (stderr, "Invalid step %d\n", step);
        exit(EXIT_FAILURE);
    }

}

void printseq (int start, int step, int finish) {
    // for(initialisation, condition, incrementation)
    
    int i;
    int seqIncreasing = (start < finish); // statement either evaluates to true or false
    
    // seqIncreasing if true, condition after the ? is considered, otherwise, condition after the : is considered
    
    for (i = start; (seqIncreasing ? i <= finish : i >= finish); i += step) {
        printf ("%d ", i);
    }
 
    printf ("\n");
    
    
}
