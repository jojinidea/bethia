// if one argument, print from 1 to the number
// could be positive (count upwards) or negative (count down)
// if two arguments, print from the first number to the second
// the first could be larger (count down), or the first could be smaller (count up) 
// if three arguments, print from the first to the third number, incrementing by the second argument
// if the middle value is positive, the first has to be smaller than the third
// if the middle is negative, the first has to be larger than the third
// OR ERROR 

int main (int argc, char *argv[]) {

// for (initialisation, condition, increment)

   for (i = start; i <= end; i = i + step) {
        printf ("%d ", i);
   }

}

// in line conditional statement

// x > 5 ? y = y + 3: y = y + 5
// If x > 5, y = y + 3, otherwise y = y + 5
// If first statement true, y = y + 3, if first statement false, y = y + 5

switch (argc) {
case 2:
    start = 1;
    finish = getValue(argv, 1, "finish"); // essentailly atoi(argv[1]) - but we need to check that the input is valid - if the value isn't valid, prints error message
    step = (start < finish) ? 1 : -1;
    break;

case 3: // two command line arguments
    start = getValue(argv, 1, "start");


}

int getValue (char *argv[], int which, char *name) {
   
    // sscanf - reads from a string
    
    int value; 
    if (sscanf(argv[which], "%d", &value) != 1) {
        fprintf(stderr, "INvalid %s\n", name);
        exit(EXIT_FAILURE);
    }
    return value;
    
    default // prints message that is default 
    // got valid start, step finish

}


void seq (int start, int step, int finish) {
   
    int i;
    
    int seqIncreasing = (start < finish); // evaluates to 0 or 1 depending on whether true or false
    
    for (i = start; seqIncreasing ? i <= finish : i>= finish; i = i + step) {
        printf ("%d ", );
    }
    printf ("\n");

}

void checkStep (int start, int step, int finish) {


}
