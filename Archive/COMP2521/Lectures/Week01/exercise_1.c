#include <stdio.h>
#include <stdlib.h>
char *monthName (int month);

int main (int argc, char *argv[]) {

    
    if (argc == 2) {
        int month = atoi(argv[1]);
        if (month < 1 || month > 3) {
            fprintf (stderr, "Invalid month\n");        
        } else {
            printf ("%s\n", monthName(month));
        }
    } else {
        fprintf (stderr, "Invalid number of command line arguments\n");
    }

}

char *monthName (int month) {
    char *monthName;
    
    switch(month) {
        case 1:
        monthName = "January"; break;
        case 2: 
        monthName = "Feb"; break;
        case 3:
        monthName = "March"; break;
    }

return monthName;

}
