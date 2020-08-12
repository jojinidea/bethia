#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <assert.h>

#include "textbuffer.h"

#define TRUE 1
#define FALSE 0

void printMatch(Match search);
void whiteBoxTests();

int main(int argc, char *argv[]) {

    fprintf(stderr, "Performing white box tests\n");
    whiteBoxTests();
    fprintf(stderr, "White box tests PASSED\n");
 
    // 1. TESTING NEWTB
        // Case 1: Regular input 
        char case1[] = "line 01\n"
                 "line 02\n"
                 "line 03\n"
                 "line 04\n"
                 "line 05\n"
                 "line 06\n"
                 "line 07\n"
                 "line 08\n"
                 "line 09\n"
                 "line 10\n";   
        char *dumpcase1;
        TB tb1 = newTB(case1);
        dumpcase1 = dumpTB(tb1, FALSE);  
        fprintf(stderr, "Printing newTB Case 1: Regular input\n");   
        fprintf(stderr, "%s", dumpcase1);
 
        // Case 2: Empty string (create emptyTB) 
        char *empty = "";
        char *dumpcase2; 
        TB tbEmpty = newTB(empty);
        dumpcase2 = dumpTB(tbEmpty, FALSE);
        fprintf(stderr, "Printing newTB Case 2: Empty input\n");   
        fprintf(stderr, "%s", dumpcase2);
               
        // Case 3: Newline char (create TB with 1 empty line) 
        char *newLine = "\n";
        char *dumpcase3; 
        TB tbNewLine = newTB(newLine);
        dumpcase3 = dumpTB(tbNewLine, FALSE);
        fprintf(stderr, "Printing newTB Case 3: Newline input\n");   
        fprintf(stderr, "%s", dumpcase3);      
        
    // 2. TESTING DUMPTB
    
        // Case 1: Textbuffer has no lines (empty string). Expect no output, regardless of showLineNumber's value
        dumpcase2 = dumpTB(tbEmpty, TRUE); 
        fprintf(stderr, "Printing dumpTB Case 1: Empty tb\n");   
        fprintf(stderr, "%s", dumpcase2);
        
        // Case 2: showLineNumbers == TRUE. Expect line numbers appended at start of each line
        dumpcase1 = dumpTB(tb1, TRUE);
        fprintf(stderr, "Printing dumpTB Case 2: showLineNumbers == TRUE and non-empty TB\n");   
        fprintf(stderr, "%s", dumpcase1);
        
        // Case 3: showLineNumbers == FALSE 
        dumpcase1 = dumpTB(tb1, FALSE); 
        fprintf(stderr, "Printing dumpTB Case 2: showLineNumbers == FALSE and non-empty TB\n");   
        fprintf(stderr, "%s", dumpcase1);    
        
    // linesTB
        // Case 1: Textbuffer has no lines
        fprintf(stderr, "LinesTB in emptyTB is %d\n", linesTB(tbEmpty));
        
        // Case 2: Textbuffer has many lines 
        fprintf(stderr, "LinesTB in non-emptyTB is %d\n", linesTB(tb1));
        
    // 3. TESTING ADD PREFIX TB 
        // Case 1: Input string is empty string
            addPrefixTB(tb1, 0, 9, "");
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing addPrefixTB Case 1: empty input string\n");   
            fprintf(stderr, "%s", dumpcase1);      
        
        // Case 2: Input string is null (expect abort) 
            //addPrefixTB(tb1, 0, 9, NULL);
            //dumpcase1 = dumpTB(tb1, FALSE);
            //fprintf(stderr, "Printing addPrefixTB Case 2: input string as NULL\n");   
            //fprintf(stderr, "%s", dumpcase1);  
            
        // Case 3: Add a non-empty prefix to non-empty TB
            addPrefixTB(tb1, 0, 9, "PREFIX ");
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing addPrefixTB Case 3: non-empty prefix and non-empty TB\n");   
            fprintf(stderr, "%s", dumpcase1);   
            tb1 = newTB(case1);
            
        // Case 4: TB is empty 
            addPrefixTB(tbEmpty, 0, 10, "PREFIX ");
            dumpcase1 = dumpTB(tbEmpty, FALSE);
            fprintf(stderr, "Printing addPrefixTB Case 4: emptyTB\n");   
            fprintf(stderr, "%s", dumpcase1);  
    
    // 4. TESTING MERGETB
        // Case 1: Merge tb with itself (should be ignored)
            mergeTB(tb1, 0, tb1);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing MergeTB Case 1: Merge tb with itself\n");   
            fprintf(stderr, "%s", dumpcase1);  
            
        // Case 2: Merge tb with pos == 0. Expect TB2 to be appended to start of TB1
            char *case2 = "Line 01B\nLine 02B\nLine 03B\nLine 04B\nLine 05B\nLine 06B\nLine 07B\nLine 08B\nLine 09B\nLine 10B\n";
            TB tb2 = newTB(case2);
            mergeTB(tb1, 0, tb2); 
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing MergeTB Case 2: Merge tb with pos == 0\n");   
            fprintf(stderr, "%s", dumpcase1);
        
        // Case 3: Merge tb with pos == linesTB(dest)
            tb1 = newTB(case1);
            tb2 = newTB(case2);
            mergeTB(tb1, 10, tb2);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing MergeTB Case 3: Merge tb with pos == nLines tb2\n");   
            fprintf(stderr, "%s", dumpcase1); 
        
        // Case 4: Source empty
            tb1 = newTB(case1);
            tbEmpty = newTB(empty);
            mergeTB(tb1, 0, tbEmpty);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing MergeTB Case 4: Merge tb with empty source\n");   
            fprintf(stderr, "%s", dumpcase1); 
        
        // Case 5: Destination empty **DOES THIS MEAN POS == 0 == LINESTB(DEST)
            // Case 5.1 If pos == 0
            tb1 = newTB(case1);
            mergeTB(tbEmpty, 0, tb1);
            dumpcase1 = dumpTB(tbEmpty, FALSE);
            fprintf(stderr, "Printing MergeTB Case 5.1: Mergetb with empty destination, pos == 0\n");
                
            // Case 5.2 If pos is out of range. Expect abort
            //tb1 = newTB(case1);
            //tbEmpty = newTB(empty);
            //mergeTB(tbEmpty, 1, tb1);
    
    // 5. TESTING PASTETB
        // Case 1: Pos out of bounds (expect error message) 
            //pasteTB(tb1, 11, tb2); 
       
        // Case 2: Pos == 0
            tb1 = newTB(case1);
            tb2 = newTB(case2);
            pasteTB(tb1, 0, tb2);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing PasteTB Case 2\n");   
            fprintf(stderr, "%s", dumpcase1); 
            dumpcase2 = dumpTB(tb2, FALSE);
            fprintf(stderr, "Printing PasteTB Case 2 Source\n");   
            fprintf(stderr, "%s", dumpcase2);            
        
        // Case 3: Pos is between 0 and nLines
            tb1 = newTB(case1);
            pasteTB(tb1, 5, tb2);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing PasteTB Case 3\n");   
            fprintf(stderr, "%s", dumpcase1); 
            dumpcase2 = dumpTB(tb2, FALSE);
            fprintf(stderr, "Printing PasteTB Case 3 Source\n");   
            fprintf(stderr, "%s", dumpcase2); 
        
        // Case 4: Source empty
            tb1 = newTB(case1);
            tb2 = newTB(empty);
            pasteTB(tb1, 5, tb2); 
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing PasteTB Case 4\n");   
            fprintf(stderr, "%s", dumpcase1); 
            dumpcase2 = dumpTB(tb2, FALSE);
            fprintf(stderr, "Printing PasteTB Case 4 Source\n");   
            fprintf(stderr, "%s", dumpcase2); 
            
        // Case 5: Destination empty and pos in range (i.e. pos == 0)
            tb1 = newTB(case1);
            tbEmpty = newTB("");
            pasteTB(tbEmpty, 0, tb1);
            dumpcase1 = dumpTB(tbEmpty, FALSE); 
            fprintf(stderr, "Printing PasteTB Case 5\n"); 
            fprintf(stderr, "%s", dumpcase1);
            dumpcase2 = dumpTB(tb1, FALSE); 
            fprintf(stderr, "Printing PasteTB Case 5 Source\n");   
            fprintf(stderr, "%s", dumpcase2); 
            
    // 6. TESTING CUTTB
        // Case 1: If to < from (expect NULL)
            tb1 = newTB(case1);
            TB cut = cutTB(tb1, 8, 0);
            dumpcase1 = dumpTB(cut, FALSE);
            fprintf(stderr, "Printing CutTB Case 1\n"); 
            fprintf(stderr, "%s", dumpcase1); 
        
        // Case 2: If to == 0 && from == nLines 
            tb1 = newTB(case1);
            cut = cutTB(tb1, 0, 9);
            dumpcase1 = dumpTB(cut, FALSE);
            dumpcase2 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing CutTB Case 2\n"); 
            fprintf(stderr, "%s", dumpcase1);             
            // REMOVE THIS assert(strcmp(dumpcase2, "") == 0);
            
        // Case 3: 0 < to < nLines && to < from < nLines
            tb1 = newTB(case1);
            cut = cutTB(tb1, 3, 8);
            dumpcase1 = dumpTB(cut, FALSE);
            fprintf(stderr, "Printing CutTB Case 3\n");  
            fprintf(stderr, "%s", dumpcase1);
    
    // 7. TESTING DELETETB
        // Case 1: If to < from (expect abort) 
            //tb1 = newTB(case1);
            //deleteTB(tb1, 3, 0);      
        
        // Case 2: If to == 0 && from == nLines
            tb1 = newTB(case1);
            deleteTB(tb1, 0, 9);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing DeleteTB Case2\n");
            fprintf(stderr, "%s", dumpcase1);
        
        // Case 3: 0 < to < nLines && to < from < nLines
            tb1 = newTB(case1);
            deleteTB(tb1, 3, 5);
            dumpcase1 = dumpTB(tb1, FALSE);
            fprintf(stderr, "Printing DeleteTB Case 3 - lines 3-5 deleted\n");
            fprintf(stderr, "%s", dumpcase1);
    
    // 8. TESTING SEARCHTB
        // Case 1: Input string is "" - return NULL
            tb1 = newTB(case1);
            Match searchList = searchTB(tb1, "");
            fprintf(stderr, "Printing SearchTB Case 1: Input string empty\n");
            printMatch(searchList);
        
        // Case 2: Input string is the NULL - expect abort
            //tb1 = newTB(case1);
            //Match searchList = searchTB(tb1, NULL);
        
        // Case 3: Input string not found - return NULL
            tb1 = newTB(case1);
            searchList = searchTB(tb1, "Hello");
            fprintf(stderr, "Printing SearchTB Case 3: Input string not found\n");
            printMatch(searchList);
                
        // Case 4: Input string found 
            tb1 = newTB(case1);
            searchList = searchTB(tb1, "0");
            fprintf(stderr, "Printing SearchTB Case 4: Input string found\n");
            printMatch(searchList);
    
        // Case 5: Consecutive substrings
            tb1 = newTB("My name is Jarred lovelovegood and I love Luna lovegood\n");
            searchList = searchTB(tb1, "love");
            fprintf(stderr, "Printing SearchTB Case 5: Consecutive substrings\n");
            printMatch(searchList);          
    
    // 9. RELEASETB
        releaseTB(tb1);
        releaseTB(tb2);
 
    // 10. FREEING MALLOC'ED MEMORY 
           
        free(dumpcase1);
        free(dumpcase2);
        free(dumpcase3);
        free(cut);
        free(searchList);
    
    return EXIT_SUCCESS;
}
