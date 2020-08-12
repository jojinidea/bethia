#include <stdlib.h>
#include <string.h> 
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "textbuffer.h"

#define END_OF_STRING (-1)
#define FALSE 0
#define TRUE 1
#define MODIFY_FIRST 1
#define MODIFY_LAST 2
#define MODIFY_MIDDLE 3
#define MODIFY_EMPTY 4
#define DELETE_WHOLE 5

typedef struct TBNode {
    char *line;
    struct TBNode *next;
    struct TBNode *prev;

} TBNode;


struct textbuffer {
    int nLines;
    TBNode *first;
    TBNode *last;
};

// SECTION 1: FUNCTIONS WRITTEN FOR IMPLEMENTATION OF TB FUNCTIONS
struct textbuffer *createEmptyTB(void);
void trimTB(TB newTB);
struct TBNode *CreateNewNode(char *newline);
void AppendNode(struct TBNode *new, struct textbuffer *newTB);
struct TBNode *returnNthNode(int n, TB tb);
int lengthOfLinesinTB(TB tb, TBNode *from, TBNode *to);
int outOfRange(int lineNum, TB tb);
void deleteTBNodes(TB tb, TBNode *from, TBNode *to);
void appendDeletedTB(int arg, TBNode *before, TBNode *after, TB tb);
char *putCutLinesInArray(TBNode *from, TBNode *to, int lengthLinesTB);
void appendMatchNode(Match matchList, matchNode *new);
matchNode *createNewMatchNode(int lineNumber, int charIndex);

// SECTION 2: TESTING FUNCTIONS
void printTB(TB tb);
void whiteBoxTests();
void testCreateNewTBNode();
void testAppendTBNode();
void testNewTB();
void testSanityOfTBList(TB tb);
void testlengthOfLines(); 
void testDumpTB();
void testlinesTB();
void testReturnNthNode();
void testOutOfRange();
void testAddPrefix();
void printMatch(Match search);
void testMergeTBs();
void testDeleteTBNodes();
void testCutTB();
void testDeleteTB();
void testSearchTB();
void testAppendDeletedTB();
void testPasteTB();
int checkForward(TB tb);
int checkBackward(TB tb);
int checkScanningForwards(TB tb);
int checkScanningBackwards(TB tb);


// FUNCTION 1: NEWTB

/* Allocate a new textbuffer whose contents is initialised with the text given
 * in the array.
 */

TB newTB (char text[]) {
    struct textbuffer *newTB = createEmptyTB();  
    char *tofree;
    char *string; 
    char *newline;
    char *newline1; 
    struct TBNode *new;
    
    tofree = string = strdup(text);
    assert(string != NULL);
    
    if (strcmp(text, "\0") != 0) {
        while ((newline = strsep(&string, "\n")) != NULL) {
            newline1 = strdup(newline);
            new = CreateNewNode(newline1);
            AppendNode(new, newTB);
        }
    trimTB(newTB); 
    }

    free(tofree);
    
	return newTB;
		
}

// SECTION 1: FUNCTIONS WRITTEN FOR NEWTB

// 1.1 Creates an emptyTB

struct textbuffer *createEmptyTB(void) {

    struct textbuffer *newTB = malloc(sizeof(struct textbuffer));
    assert(newTB != NULL);
    newTB->first = NULL;
    newTB->last = NULL;
    newTB->nLines = 0;

return newTB;

}

// 1.2 Creates a newTB node
struct TBNode *CreateNewNode(char *newline) {

    TBNode *new;
    new = malloc(sizeof(TBNode));
    assert(new != NULL); // check memory allocation successful
    new->line = newline; 
    new->prev = new->next = NULL;
    return new;

}

// 1.3. Appends a node to the TB
void AppendNode(struct TBNode *new, struct textbuffer *newTB) {
    
    if (newTB->nLines == 0) {
        newTB->first = newTB->last = new;
        new->prev = NULL;
    } else if (newTB->nLines == 1) {
        newTB->first->next = new;
        new->prev = newTB->first;
        newTB->last = new;
    } else {
        new->prev = newTB->last;
        newTB->last->next = new;
        new->next = NULL;
        newTB->last = new;
    }
    newTB->nLines++;
    
}

// 1.4 Trims the last node containing only a null terminator from the newTB
void trimTB (TB newTB) {
    TBNode *temp;
    temp = newTB->last; 
    newTB->last = newTB->last->prev;
    newTB->last->next = NULL;
    free(temp->line);
    free(temp);
    newTB->nLines--;

}

// END SECTION 1


// FUNCTION 2: RELEASETB 

/* Free the memory occupied by the given textbuffer.  It is an error to access
 * the buffer afterwards.
 */
void releaseTB (TB tb) {
    
    if (tb->nLines == 0) {
        free(tb);
        return;
    } 
    if (tb->nLines == 1) {
        free(tb->first->line);
        free(tb->first);
        free(tb);
        return;
    }
    
    TBNode *curr;
    TBNode *prev;
    curr = tb->first; 
    
    while (curr != NULL) {
        prev = curr;
        curr = curr->next;
        free(prev->line);
        free(prev);
    }
    
    free(tb);
     
}

// FUNCTION 3: DUMPTB 

/* Allocate and return an array containing the text in the given textbuffer.
 * add a prefix corrosponding to line number iff showLineNumbers == TRUE
 */
char *dumpTB (TB tb, int showLineNumbers){

	char *dumpedTB; 
	int maxDigits = log10(tb->nLines) + 1; 
	int lengthLinesTB;
	char *lineNum = malloc(maxDigits+1);; 
	int counter = 1;
	struct TBNode *currNode;
	
	if (tb->nLines != 0) {
	    lengthLinesTB = lengthOfLinesinTB(tb, tb->first, tb->last);
        dumpedTB = malloc(lengthLinesTB + (lengthLinesTB * (strlen(". ") + maxDigits + 1 + strlen("\n"))));
        dumpedTB[0] = '\0';
        currNode = tb->first;
	    for (currNode = tb->first; currNode != NULL; currNode = currNode->next) {
	        if (showLineNumbers == TRUE) {
	            sprintf(lineNum, "%d", counter);
	            if (counter == 0) {
	                strcpy(dumpedTB, lineNum);
	            }  else {
	                strcat(dumpedTB, lineNum);
	            }
	            strcat(dumpedTB, ". ");
	        } 
	        if (showLineNumbers == FALSE && counter == 0) {
	            strcpy(dumpedTB, currNode->line);
	        } 
	        strcat(dumpedTB, currNode->line);   
	        strcat(dumpedTB, "\n");
	        counter++;
	    }
	} else {
	    dumpedTB = malloc(strlen(""));
	    strcpy(dumpedTB, "");
	} 

	return dumpedTB;
}


// FUNCTION 4: LINESTB

/* Return the number of lines of the given textbuffer.
 */
int linesTB (TB tb){
	return tb->nLines;
}

// FUNCTION 5: ADDPREFIXTB 
/* Add a given prefix to all lines between pos1 and pos2
 *
 * - The program is to abort() with an error message if line 'pos1' or line
 *   'pos2' is out of range.  The first line of a textbuffer is at position 0.
 */
 
void addPrefixTB (TB tb, int pos1, int pos2, char* prefix){
    
    struct TBNode *curr;
    char *prefixedLine;
    int difference = pos2-pos1;  
    int nLinesChanged;
    
    if (prefix == NULL) {
        fprintf(stderr, "Prefix is NULL. Please enter a non-NULL prefix\n");
        abort();
    }
    if (pos2 >= pos1 && outOfRange(pos2, tb) == FALSE && outOfRange(pos1, tb) == FALSE ) {
        if (tb->first != NULL) {
            curr = returnNthNode(pos1, tb); 
            for (nLinesChanged = 0; nLinesChanged <= difference; nLinesChanged++) {
                prefixedLine = malloc(strlen(prefix) + strlen(curr->line) + 1);
                prefixedLine[0] ='\0';
                strcat(prefixedLine, prefix);
                strcat(prefixedLine, curr->line);
                free(curr->line);
                curr->line = prefixedLine;
                curr = curr->next;
            }
        }
    } else {
        if (tb->first != NULL) {
            if (outOfRange(pos2, tb) == TRUE || outOfRange(pos1, tb) == TRUE) {
                fprintf(stderr, "You entered %d for pos1 and %d for pos2. Please ensure both pos1 & pos2 are in the range 0 to %d\n", pos1, pos2, tb->nLines-1);
            } 
            if (pos2 < pos1) {
                fprintf(stderr, "You entered %d for pos2 and %d for pos1. Please ensure pos2 >= pos1\n", pos2, pos1);
            } 
        abort(); 
        }
    }  
    
}

// FUNCTION 6: MERGETB 
/* Merge 'tb2' into 'tb1' at line 'pos'.
 *
 * - Afterwards line 0 of 'tb2' will be line 'pos' of 'tb1'.
 * - The old line 'pos' of 'tb1' will follow after the last line of 'tb2'.
 * - After this operation 'tb2' can not be used anymore (as if we had used
 *   releaseTB() on it).
 * - The program is to abort() with an error message if 'pos' is out of range.
 */

void mergeTB (TB tb1, int pos, TB tb2) {
    TBNode *posNode;
    TBNode *temp;

    if (pos >= 0 && pos <= tb1->nLines) {
        if (tb1 == tb2) {
            return;
        }
        if (tb1->nLines == 0 || tb2->nLines == 0) {
            if (tb2->nLines == 0) {
                return;
            }      
            tb1->first = tb2->first; 
            tb1->last = tb2->last; 
            tb2->last = tb2->first = NULL;
        } else if (pos == 0) {                                              // modifying head of TB
            if (tb1->nLines == 0) {
                tb1->first = tb2->first; 
                tb1->last = tb2->last;
                tb2->last = tb2->first = NULL;
            } else {
                temp = tb1->first;
                tb1->first = tb2->first;
                tb2->last->next = temp;
                temp->prev = tb2->last;
                tb2->last = tb2->first = NULL;
            }
        } else if (pos == tb1->nLines) {                                    // modifying tail of TB
            tb1->last->next = tb2->first; 
            tb2->first->prev = tb1->last;
            tb1->last = tb2->last;   
            tb2->last = tb2->first = NULL;
         } else {                                                           // modifying linking of middle nodes in TB
            posNode = returnNthNode(pos, tb1); 
            temp = posNode->prev; 
            temp->next = tb2->first;
            tb2->first->prev = temp;
            posNode->prev = tb2->last;
            tb2->last->next = posNode;    
            tb2->last = tb2->first = NULL;
        }
    } else {
        fprintf(stderr, "You entered %d for pos. Please enter a pos in the range 0 - %d\n", pos, tb1->nLines);
        abort();
    }
    
    tb1->nLines = tb1->nLines + tb2->nLines;
    free(tb2);
}

// FUNCTION 7: PASTETB

/* Copy 'tb2' into 'tb1' at line 'pos'.
 *
 * - Afterwards line 0 of 'tb2' will be line 'pos' of 'tb1'.
 * - The old line 'pos' of 'tb1' will follow after the last line of 'tb2'.
 * - After this operation 'tb2' is unmodified and remains usable independent
 *   of 'tb1'.
 * - The program is to abort() with an error message if 'pos' is out of range.
 */
 
void pasteTB (TB tb1, int pos, TB tb2) {
    TBNode *tb1PosBefore;
    TBNode *tb1Pos;
    TBNode *tb2Curr;
    TBNode *tb1Curr; 
    TBNode *new; 
    
    if (pos < 0 || pos > tb1->nLines) {
        fprintf(stderr, "You entered %d for pos. Please ensure that your pos is between 0 and %d\n", pos, tb1->nLines);
        abort();
    }
    if (pos == 0) {
        if (tb1->nLines == 0) {
            tb1->first = tb2->first; 
            tb1->last = tb2->last;
        } else {
            tb1Curr = tb1->first; 
            for (tb2Curr = tb2->last; tb2Curr != NULL; tb2Curr = tb2Curr->prev) {
                new = CreateNewNode(tb2Curr->line);
                tb1Curr->prev = new; 
                new->next = tb1Curr;
                tb1Curr = new; 
            }
        tb1->first = tb1Curr; 
        }
    } else if (pos == tb1->nLines) {
        tb1Curr = tb1->last; 
        for (tb2Curr = tb2->first; tb2Curr != NULL; tb2Curr = tb2Curr->next) {
            new = CreateNewNode(tb2Curr->line);
            tb1Curr->next = new;
            new->prev = tb1Curr;
            tb1Curr = new;
        }
    tb1->last = tb1Curr; 
    } else {
        tb1Pos = returnNthNode(pos, tb1);
        tb1PosBefore = tb1Pos->prev;
        for (tb2Curr = tb2->first; tb2Curr != NULL; tb2Curr = tb2Curr->next) {
            new = CreateNewNode(tb2Curr->line);
            tb1PosBefore->next = new;
            new->prev = tb1PosBefore; 
            new->next = tb1Pos;
            tb1Pos->prev = new; 
            tb1PosBefore = new;
        }
    }
    
    tb1->nLines = tb1->nLines + tb2->nLines;
}

// FUNCTION 8: CUTTB

/* Cut the lines between and including 'from' and 'to' out of the textbuffer
 * 'tb'.
 *
 * - The result is a new textbuffer (much as one created with newTB()).
 * - The cut lines will be deleted from 'tb'.
 * - The program is to abort() with an error message if 'from' or 'to' is out
 *   of range.
 */
 
 
TB cutTB (TB tb, int from, int to) {
    TBNode *fromNode;
    TBNode *toNode;
    TBNode *beforeNode; 
    TBNode *afterNode; 
    TB cutTB;
    char *cutLines;
    int lengthLinesTB;
    int arg; 
    
    if (outOfRange(from, tb) == TRUE || outOfRange(to, tb) == TRUE) {
        fprintf(stderr, "You entered %d as from and %d as to. Please ensure to and from are between 0 and %d\n", from, to, tb->nLines-1); 
        abort();
    } else if (to < from) {
        cutLines = "\0";
        cutTB = newTB(cutLines);
        return cutTB;
    } else if (tb->nLines == 0) {
        cutLines = "\0";
        cutTB = newTB(cutLines);
        return cutTB; 
    } else {  
        if (from == 0 && to == tb->nLines - 1) {
            arg = DELETE_WHOLE;
        } else if (from == 0) {
            arg = MODIFY_FIRST;
        } else if (to == tb->nLines-1) {
            arg = MODIFY_LAST; 
        } else {
            arg = MODIFY_MIDDLE;
        }
        fromNode = returnNthNode(from, tb);
        toNode = returnNthNode(to, tb);
        beforeNode = fromNode->prev;
        afterNode = toNode->next; 
        lengthLinesTB = lengthOfLinesinTB(tb, fromNode, toNode);
        cutLines = putCutLinesInArray(fromNode, toNode, lengthLinesTB); 
        appendDeletedTB(arg, beforeNode, afterNode, tb);
        cutTB = newTB(cutLines);
        tb->nLines = tb->nLines - (to - from + 1);
    }
    
    return cutTB;

}

// SECTION 8: FUNCTIONS WRITTEN FOR CUTTB

// 8.1 Places the lines from the node 'from' to the node 'to' (inclusive of both nodes) into the char array cutLines
char *putCutLinesInArray(TBNode *from, TBNode *to, int lengthLinesTB) {
    char *cutLines = malloc(lengthLinesTB + (lengthLinesTB * strlen("\n")) + 1);
    cutLines[0] = '\0';
    int isToCopied = FALSE;
    TBNode *curr; 
    
    for (curr = from; isToCopied == FALSE && curr != NULL; curr = curr->next) {
        if (curr == to) {
            isToCopied = TRUE;
        } 
        strcat(cutLines, curr->line);
        strcat(cutLines, "\n");
    }
    
    return cutLines; 
}


// 8.2 Appends the deleted TB with lines deleted from it 

void appendDeletedTB(int arg, TBNode *before, TBNode *after, TB tb) {
    if (arg == DELETE_WHOLE) {
        tb->first = NULL;
        tb->last = NULL;
    }
    if (arg == MODIFY_FIRST) {
        after->prev = NULL;
        tb->first = after; 
    } 
    if (arg == MODIFY_LAST) {
        tb->last = before;
        before->next = NULL;
    }
    if (arg == MODIFY_MIDDLE) {
        before->next = after;
        after->prev = before;
    }

}

// END SECTION 8


// FUNCTION 9: DELETETB 

/* Remove the lines between and including 'from' and 'to' from the textbuffer
 * 'tb'.
 *
 * - The program is to abort() with an error message if 'from' or 'to' is out
 *   of range.
 */
void deleteTB (TB tb, int from, int to) {
    TBNode *beforeNode;
    TBNode *afterNode; 
    TBNode *toNode;
    TBNode *fromNode; 
    int arg;

    if (outOfRange(from, tb) == TRUE || outOfRange(to, tb) == TRUE) {
        fprintf(stderr, "You entered %d as from and %d as to. Please ensure to and from are between 0 and %d\n", from, to, tb->nLines-1); 
        abort();
    } else if (tb->nLines == 0) {
        return;
    } else if (to < from) {
        fprintf(stderr, "You entered %d as from and %d as to. Please ensure to >= from\n", from, to);
        abort();
    } else if (tb->nLines == 0) {
        return; 
    } else {  
        if (from == 0 && to == tb->nLines - 1) {
            arg = DELETE_WHOLE;
        } else if (from == 0) {
            arg = MODIFY_FIRST;
        } else if (to == tb->nLines-1) {
            arg = MODIFY_LAST; 
        } else {
            arg = MODIFY_MIDDLE;
        }
        fromNode = returnNthNode(from, tb);
        toNode = returnNthNode(to, tb);
        beforeNode = fromNode->prev;
        afterNode = toNode->next; 
        deleteTBNodes(tb, fromNode, toNode);
        appendDeletedTB(arg, beforeNode, afterNode, tb);
    }

}

// SECTION 9: FUNCTIONS WRITTEN FOR DELETE TB

// 9.1 Deletes the notes from the node 'from' to the node 'to' (inclusive of both nodes) and frees them
void deleteTBNodes(TB tb, TBNode *from, TBNode *to) {
    
    TBNode *curr = from;
    TBNode *prev;
    int isToDeleted = FALSE;  
    
    while (curr != NULL && isToDeleted == FALSE) {
        prev = curr;
        if (prev == to) {
            isToDeleted = TRUE;
        }
        curr = curr->next;
        free(prev->line);
        free(prev);
        tb->nLines--;
    }
    
   
}

// END SECTION 9

// FUNCTION 10: SEARCHTB

/*  Return a linked list of Match nodes of all the matches of string search
 *  in tb
 *
 * - The textbuffer 'tb' will remain unmodified.
 * - The user is responsible of freeing the returned list
 */
Match searchTB (TB tb, char* search){
    Match matchList = NULL;
    Match currMatch = NULL;
    matchNode *new;
    struct TBNode *curr;
    int lineNumber = 1; 
    char *strfound;
    char *line;
    int CharIndex;
    int lengthOriginal;
    int lengthSearchString;
    
    if (search == NULL) {
        fprintf(stderr, "You entered null as the input search string. Please enter a different string\n");
        abort();
    } else {
        if (strcmp(search, "") == 0) {
            return NULL;
        }
        if (tb != NULL) {
            curr = tb->first; 
            while (curr != NULL) {
                lengthOriginal = strlen(curr->line);                                    // retain the line's original length 
                line = curr->line;
                while ((strfound = strstr(line, search)) != NULL) {
                    lengthSearchString = strlen(search);
                    CharIndex = lengthOriginal - strlen(strfound);
                    new = createNewMatchNode(lineNumber, CharIndex);                   
                    if (matchList == NULL) {
                        matchList = new;
                        currMatch = matchList; 
                        currMatch->next = NULL;
                    } else {
                        currMatch->next = new;
                        currMatch = currMatch->next;
                        currMatch->next = NULL;
                    }
                    line = strfound + lengthSearchString;

                }
            curr = curr->next; 
            lineNumber++;
            } 
        }       
    } 

    if (matchList == NULL) {                                                        // no matches have been found
        return NULL; 
    } else {
	    return matchList;
	}
}


// SECTION 10: FUNCTIONS WRITTEN FOR SEARCHTB

// 10.1 Dynamically creates new matchnodes 


matchNode *createNewMatchNode(int lineNumber, int charIndex) {
    matchNode *new = malloc(sizeof(matchNode));
    new->lineNumber = lineNumber; 
    new->charIndex = charIndex; 
    new->next = NULL;
    
    return new;
}


// FUNCTION 11: FORMRICHTEXT

/* Search every line of tb for each occurrence of a set of specified subsitituions
 * and alter them accordingly
 *
 * refer to spec for table.
 */
 
 
void formRichText (TB tb){ 

// I actually wrote this function and it was functional but it was too difficult to integrate at 10pm Sunday night :(

}




// SECTION 12: MISCELLANEOUS FUNCTIONS USED FOR MULTIPLE PURPOSES

// 12.1 calculates the length of lines in tb from the node from to to

int lengthOfLinesinTB(TB tb, TBNode *from, TBNode *to) {
    int lengthLines = 0;
    struct TBNode *curr; 
    
    for (curr = from; curr != to->next; curr = curr->next) {
        lengthLines = lengthLines + strlen(curr->line);
    }

return lengthLines;

}


// 12.2 determines whether a line is out of range (either < 0 or greater than the number of lines in a TB)
 
int outOfRange(int lineNum, TB tb) {
    int lineOutOfRange = FALSE; 

    if (tb->nLines == 0) {
        if (lineNum != 0) {
            lineOutOfRange = TRUE;
        }
    } else if (lineNum > tb->nLines - 1 || lineNum < 0) {
        lineOutOfRange = TRUE;
    }
    
    return lineOutOfRange; 
}

// 12.3. Returns Nth node in a tb, with n = 0 corresponding to the first node, n = 1 corresponding to the second node, etc.
struct TBNode *returnNthNode(int n, TB tb) {
    int counter; 
    struct TBNode *curr = tb->first; 
    struct TBNode *nthNode;
    
    for (counter = 0; counter < n; counter++) {
        curr = curr->next; 
    }
    nthNode = curr;
    
return nthNode; 

}



// SECTION 13: WHITEBOX TESTS

void whiteBoxTests() {

    testCreateNewTBNode(); 
    testAppendTBNode();
    testNewTB();
    testlengthOfLines();
    testDumpTB();
    testlinesTB();
    testReturnNthNode();
    testOutOfRange();
    testAddPrefix();
    testMergeTBs(); 
    testDeleteTBNodes();
    testCutTB();
    testAppendDeletedTB();
    testDeleteTB();
    testSearchTB();
    testPasteTB();
    
}

// SECTION 13.1 TESTING CREATENEWTB

// 13.1.1 Test create new node 

void testCreateNewTBNode() {
    char *nonEmptyLine = "Hello";
    char *emptyLine = "\0";
    char *newLine = "\n";
    
    struct TBNode *nonEmptyNode = CreateNewNode(nonEmptyLine);
    struct TBNode *emptyLineNode = CreateNewNode(emptyLine);
    struct TBNode *newLineNode = CreateNewNode(newLine);
    
    assert(strcmp(nonEmptyNode->line, "Hello") == 0);
    assert(strcmp(newLineNode->line, "\n") == 0);
    assert(nonEmptyNode->prev == NULL);
    assert(nonEmptyNode->next == NULL);
    
    fprintf(stderr, "Asserts for testCreateNewTBNode passed\n");
    
    free(nonEmptyNode);
    free(emptyLineNode);
    free(newLineNode);

}

// 13.1.2 Test AppendTBNode 

void testAppendTBNode() {
    struct TBNode *new1 = CreateNewNode("Line1");
    struct TBNode *new2 = CreateNewNode("Line2");
    struct TBNode *new3 = CreateNewNode("Line3");
    struct textbuffer *emptyTB = createEmptyTB();
    
    // Case 1: inserting new node into empty TB
    AppendNode(new1, emptyTB);
    assert(emptyTB->nLines == 1);
    assert(emptyTB->last == emptyTB->first);
    assert(emptyTB->last == new1);
    assert(new1->next == NULL);
    assert(new1->prev == NULL);
    testSanityOfTBList(emptyTB);
    
    // Case 2: inserting new node into 1 element TB (need to modify tail) 
    AppendNode(new2, emptyTB);
    assert(emptyTB->nLines == 2);
    assert(emptyTB->last == new2);
    assert(emptyTB->first == new1);
    assert(emptyTB->last->prev == new1);
    assert(emptyTB->first->next == new2);
    assert(emptyTB->last->next == NULL);
    testSanityOfTBList(emptyTB);

    // Case 3: multiple elements in TB, head & tail needing to be modified
    AppendNode(new3, emptyTB); 
    assert(emptyTB->nLines == 3);
    assert(emptyTB->last == new3);
    assert(emptyTB->last->prev == new2);
    assert((emptyTB->first->next->next) == new3);
    assert(emptyTB->last->next == NULL);
    testSanityOfTBList(emptyTB);
    
    fprintf(stderr, "Asserts for testAppendNewTBNode passed\n");
    
    free(new1);
    free(new2);
    free(new3);

}

// 13.1.3 TestnewTB

void testNewTB() {

    // Case 1: Regular input
    char *regularInput = "Hello\nMy name is\nBethia\n";
    TB regularTB = newTB(regularInput);
    assert(regularTB->nLines == 3);
    TBNode *curr = regularTB->first; 
    assert(strcmp("Hello", curr->line) == 0);
    assert(strcmp("My name is", curr->next->line) == 0);
    assert(strcmp("Bethia", curr->next->next->line) == 0);
    free(regularTB);
    fprintf(stderr, "Test 1 passed\n");
    
    // Case 2: Empty string input. Expect a newTB with no items
    char *emptyString = "";
    TB emptyTB = newTB(emptyString);
    assert(emptyTB->nLines == 0);
    assert(emptyTB->first == NULL);
    assert(emptyTB->last == NULL);
    free(emptyTB);
    fprintf(stderr, "Test 2 passed\n");
    
    // Case 3: Input with 1 newline. 
    char *newLine = "\n";
    TB newLineTB = newTB(newLine);
    assert(newLineTB->nLines == 1);
    assert(strcmp("", newLineTB->first->line) == 0);
    free(newLineTB);
    
    // Case 4: Input with multiple newlines 
    char *newLines = "\n\n\n\n\n\n";
    TB newLinesTB = newTB(newLines);
    assert(newLinesTB->nLines == 6);
    assert(strcmp("\0", newLinesTB->last->line) == 0);
    assert(strcmp("\0", newLinesTB->first->line) == 0);
    free(newLinesTB);
    
    // Case 5: Input with multiple newlines & word input
    char *newLinesChars = "Hello\n\nMy name is\nBethia\n\n";
    TB newLinesCharsTB = newTB(newLinesChars);
    assert(newLinesCharsTB->nLines == 5);
    assert(strcmp("\0", newLinesCharsTB->first->next->line) == 0);
    free(newLinesCharsTB);
    
    fprintf(stderr, "Asserts for testNewTB passed\n");
}

void testlengthOfLines() {
    char *input = "Hello\nMy name is\nBethia\n"; 
    TB newTB1 = newTB(input);
    assert(lengthOfLinesinTB(newTB1, newTB1->first, newTB1->last) == 21);
    
    free(newTB1);
    fprintf(stderr, "Asserts for testlengthOfLines passed\n");
}


// 13.2 TESTING DUMPTB


void testDumpTB() {   
    char *input = "Hello\nMy name is\nBethia\nThis is a textbuffer\n";
    TB newTB1 = newTB(input);
    char *empty = "\0";
    TB emptyTB1 = newTB(empty);
    
    // Case 1: when showLineNumbers is false
    // Don't append each line
    char *dumpFalse = dumpTB(newTB1, FALSE); 
    fprintf(stderr, "Printing dumpTB %s\n", dumpFalse);
    
    
    // Case 2: when showLineNumbers is true
    // Append to each line before returning the line number
    char *dump = dumpTB(newTB1, TRUE);
    fprintf(stderr, "Printing dump TB %s\n", dump);
    
    // Case 3: tb empty, expect empty string
    char *emptyTB = dumpTB(emptyTB1, TRUE);
    assert(strcmp(emptyTB, "\0") == 0);
    emptyTB = dumpTB(emptyTB1, FALSE);
    assert(strcmp(emptyTB, "\0") == 0);
    

fprintf(stderr, "Asserts for dumpTB passed\n");

}

// 13.3 TESTING LINESTB

void testlinesTB() {
    // Case 1: Regular input
    char *input = "Hello\nMy name is\nBethia\nThis is a textbuffer\n";
    TB newTB1 = newTB(input);
    
    // Case 2: Empty input
    char *empty = "\0";
    TB emptyTB1 = newTB(empty);
    
    // Case 3: Input with only 1 new line
    char *newLine = "\n";
    TB newLineTB = newTB(newLine);    
    
    // Case 4: Input with multiple new lines
    char *newLines = "\n\n\n\n";
    TB newLinesTB = newTB(newLines);
    
    assert(linesTB(newTB1) == 4);
    assert(linesTB(emptyTB1) == 0);
    assert(linesTB(newLineTB) == 1);
    assert(linesTB(newLinesTB) == 4);  
    
    free(newTB1);
    free(emptyTB1);
    free(newLineTB);
    free(newLinesTB);
    
    fprintf(stderr, "Asserts for testlinesTB passed\n");  
    
}

// 13.4 TESTING APPENDPREFIX TB

void testAddPrefix() {
    char *input = "Hello\nMy name is\nBethia\nThis is a long\ntextbuffer\n";
    TB inputTB = newTB(input);
    char *empty = "\0";
    TB emptyTB = newTB(empty);
    char *newLines = "\n\n\n";
    TB newLinesTB = newTB(newLines);
    
    // Case 1: Pos2 is less than pos1 but are otherwise valid (i.e. in range)
    // expect abort 
    //fprintf(stderr, "Testing add prefix with pos2 < pos1\n");
    //addPrefixTB(inputTB, 3, 1, "PREFIX ");
    
    // Case 2: Pos 2 is out of range
    // expect abort
    //fprintf(stderr, "Testing add prefix with invalid pos2\n"); 
    //addPrefixTB(inputTB, 0, 10, "PREFIX ");
    
    // Case 3: Pos 1 is out of range
    // expect abort
    //fprintf(stderr, "Testing add prefix with invalid pos1\n");
    //addPrefixTB(inputTB, -1, 3, "PREFIX ");
     
    // Case 4: Both pos2 and pos1 out of range
    // expect abort
    //fprintf(stderr, "Testing add prefix with invalid pos2 & pos1\n");
    //addPrefixTB(inputTB, -3, 10, "PREFIX ");
     
    // Case 5: tb is empty 
    // expect no changes
    addPrefixTB(emptyTB, 0, 0, "PREFIX ");
    assert(emptyTB->first == NULL);

    // Case 6: Regular tb
    addPrefixTB(inputTB, 1, 3, "PREFIX ");
    assert(strcmp(inputTB->first->next->line, "PREFIX My name is") == 0);
    assert(strcmp(inputTB->first->next->next->line, "PREFIX Bethia") == 0);
    assert(strcmp(inputTB->last->prev->line, "PREFIX This is a long") == 0);
    testSanityOfTBList(inputTB);


// Case 7: When pos1 == pos2 
    addPrefixTB(inputTB, 0, 0, "PREFIX AGAIN ");
    assert(strcmp(inputTB->first->line, "PREFIX AGAIN Hello") == 0);
    testSanityOfTBList(inputTB);
    
// Case 8: When the TB is not empty but the nodes are empty
    addPrefixTB(newLinesTB, 0,2, "PREFIX");
    assert(strcmp(newLinesTB->first->line, "PREFIX") == 0);
    testSanityOfTBList(newLinesTB);

    
    free(inputTB);
    free(emptyTB);
    free(newLinesTB);

}

// 13.5 TESTING MERGETB

void testMergeTBs() {
    char *sourceInput = "Line 1 Source\nLine 2 Source\nLine 3 Source\nLine 4 Source\n";
    char *destinationInput = "Line 1 Dest\nLine 2 Dest\nLine 3 Dest\nLine 4 Dest\nLine 5 Dest\n";
    TB source = newTB(sourceInput);
    TB destination = newTB(destinationInput);
    
    // Case 1: Pos = 0 (insert src before start of dest)
    // expect src appended before dest
    mergeTB(destination, 0, source);
    testSanityOfTBList(destination);
    printTB(destination);
    fprintf(stderr, "Finished printing Case1\n");
    free(destination);
    
    // Case 2: Pos = linesTB(dest) - 1 
    // expect src appended before last line of dest
    destination = newTB(destinationInput);
    source = newTB(sourceInput);
    mergeTB(destination, 4, source);
    testSanityOfTBList(destination);
    printTB(destination);
    fprintf(stderr, "Finished printing Case2\n");
    free(destination);
    
    // Case 3: Pos = linesTB(dest) 
    // expect src appended at the end of dest)
    destination = newTB(destinationInput);
    source = newTB(sourceInput);
    mergeTB(destination, 5, source);
    testSanityOfTBList(destination);
    printTB(destination);
    fprintf(stderr, "Finished printing Case3\n");
    free(destination);

    // Case 4: Destination is empty (source should be appended to the end of the empty TB if pos is in range) 
    destination = newTB("\0");
    source = newTB(sourceInput); 
    mergeTB(destination, 0, source);
    printTB(destination);
    fprintf(stderr, "Finished printing Case4\n");
    free(destination);

    // Case 5: Src is empty (nothing should happen unless pos is out of range - in which case we expect the program to abort) 
    destination = newTB(destinationInput);
    source = newTB("\0");
    mergeTB(destination, 3, source); 
    printTB(destination);
    fprintf(stderr, "Finished printing Case5\n");
    free(destination);
    
}

// 13.6 TEST PASTETB

void testPasteTB() {

    // Case 1: TB2 is empty
    TB tb2Empty = newTB("");
    TB tb1 = newTB("Line 1 tb1\nLine 2 tb1\nLine 3 tb1\nLine 4 tb1");
    pasteTB(tb1, 0, tb2Empty);
    fprintf(stderr, "Printing TB1 case1 PASTE\n");
    printTB(tb1);
    fprintf(stderr, "Printing TB2 case1 PASTE\n");
    printTB(tb2Empty);
    
    // Case 2: Pos = 0
    TB tb2NonEmpty = newTB("Line 1 tb2\nLine 2 tb2\nLine 3 tb2\n");
    pasteTB(tb1, 0, tb2NonEmpty);
    fprintf(stderr, "Printing TB1 case2 PASTE\n");
    printTB(tb1);
    fprintf(stderr, "Printing TB2 case2 PASTE\n");
    printTB(tb2NonEmpty);
    
    // Case 3: Pos = linesTB(dest) - 1
    tb1 = newTB("Line 1 tb1\nLine 2 tb1\nLine 3 tb1\nLine 4 tb1");
    pasteTB(tb1, 2, tb2NonEmpty); 
    fprintf(stderr, "Printing TB1 case3 PASTE\n");
    printTB(tb1);
    fprintf(stderr, "Printing TB2 case3 PASTE\n");
    printTB(tb2NonEmpty);
    
    // Case 4: Pos = linesTB(dest)
    tb1 = newTB("Line 1 tb1\nLine 2 tb1\nLine 3 tb1\nLine 4 tb1");
    pasteTB(tb1, 3, tb2NonEmpty);
    fprintf(stderr, "Printing TB1 case4 PASTE\n");
    printTB(tb1);
    fprintf(stderr, "Printing TB2 case4 PASTE\n");
    printTB(tb2NonEmpty);
    
    // Case 5: Destination is empty 
    tb1 = newTB("");
    pasteTB(tb1, 0, tb2NonEmpty); 
    fprintf(stderr, "Printing TB1 case5 PASTE\n");
    fprintf(stderr, "DUMPING TB1\n");
    assert(tb1->first != NULL);
    fprintf(stderr, "Tb1->first is %s\n", tb1->first->line);
    //char *h = dumpTB(tb1, TRUE);
    //fprintf(stderr, "%s", h);
    printTB(tb1);
    fprintf(stderr, "Printing TB2 case5 PASTE\n");
    printTB(tb2NonEmpty);
    
    // Case 6: Pos is out of bounds
    // expect abort()
    //tb1 = newTB("Line 1 tb1\nLine 2 tb1\nLine 3 tb1\nLine 4 tb1");
    //pasteTB(tb1, 9, tb2NonEmpty);


}


// 13.7 TEST CUTTB


void testCutTB() {
    // Case 1: If two is < from (expect NULL to be returned)
    char *input = "Hello\nThis is a textbuffer\nA long textbuffer\nA really long one\n";
    TB new1 = newTB(input);
    TB cut;
    cut = cutTB(new1, 2, 1);
    assert(cut->first == NULL);
    assert(cut->last == NULL);
    assert(cut->nLines == 0);
    testSanityOfTBList(cut);
    printTB(cut);
    fprintf(stderr, "Finished printing case1 cut\n");
    printTB(new1);
    fprintf(stderr, "Finished printing case1 new1\n");
    testSanityOfTBList(new1);
    
    // Case 2: If to/from are out of bounds
    //cut = cutTB(new1, 3, 5);
    
    
    // Case 3: If to == from (expect only one line to be deleted)
    cut = cutTB(new1, 1, 1);
    assert(cut->nLines == 1);
    assert(new1->nLines == 3);
    printTB(cut);
    fprintf(stderr, "Finished printing case3 cut\n");
    printTB(new1);
    fprintf(stderr, "Finished printing case3 new1\n");
    testSanityOfTBList(cut);
    testSanityOfTBList(new1);
    
    // Case 4: If to == first && from == last (expect whole tb to be empty) 
    new1 = newTB(input);
    cut = cutTB(new1, 0, 3);
    assert(cut->nLines == 4);
    printTB(cut);
    fprintf(stderr, "Finished printing case4 cut\n");
    printTB(new1);
    fprintf(stderr, "Finished printing case4 new1\n");
    assert(new1->first == NULL);
    fprintf(stderr, "new1->nLines is %d\n", new1->nLines);
    assert(new1->nLines == 0); 
    testSanityOfTBList(cut);
    testSanityOfTBList(new1);
    
    // Case 5: If to == first && from != last (need to modify first)
    new1 = newTB(input);
    cut = cutTB(new1, 0, 2);
    assert(cut->nLines == 3);
    assert(new1->nLines == 1);
    printTB(cut);
    fprintf(stderr, "Finished printing case4 cut\n");
    printTB(new1);
    fprintf(stderr, "Finished printing case4 new1\n");
    testSanityOfTBList(cut);
    testSanityOfTBList(new1);
    
    // Case 6: If to != first && from == last (need to modify last) 
    new1 = newTB(input);
    cut = cutTB(new1, 2, 3);
    assert(cut->nLines == 2);
    assert(new1->nLines == 2);
    printTB(cut);
    fprintf(stderr, "Finished printing case5 cut\n");
    printTB(new1);
    fprintf(stderr, "Finished printing case5 new1\n");
    testSanityOfTBList(cut);
    testSanityOfTBList(new1);


}

// 13.7.1 Testing Append Deleted TB (function written for CutTB)



void testAppendDeletedTB() {
    char *input = "Hello\nThis is a textbuffer\nA long textbuffer\nA really long one\n";
    TB new1 = newTB(input);
    TBNode *before = returnNthNode(0, new1)->prev;
    TBNode *after = returnNthNode(3, new1)->next;
    appendDeletedTB(DELETE_WHOLE, before, after, new1);
    assert(new1->first == NULL);
    assert(new1->last == NULL);
    
    new1 = newTB(input);
    before = returnNthNode(0, new1)->prev; 
    after = returnNthNode(2, new1)->next; 
    appendDeletedTB(MODIFY_FIRST, before, after, new1); 
    assert(new1->first != NULL);
    assert(new1->first == after);
    
    new1 = newTB(input);
    before = returnNthNode(1, new1)->prev; 
    after = returnNthNode(3, new1)->next; 
    appendDeletedTB(MODIFY_LAST, before, after, new1); 
    assert(new1->last != NULL);
    assert(new1->last == before);
    
    new1 = newTB(input);
    before = returnNthNode(1, new1)->prev; 
    after = returnNthNode(2, new1)->next; 
    appendDeletedTB(MODIFY_MIDDLE, before, after, new1); 
    assert(new1->first->next != NULL);
    assert(new1->first->next == after);    
    
}

// 13.8 TEST DELETE TB

void testDeleteTB() {
    // Case 1: If TB is empty (expect empty TB) 
    char *empty = "\0";
    TB emptyTB = newTB(empty);
    deleteTB(emptyTB, 0, 0);
    assert(emptyTB->first == NULL);
    assert(emptyTB->last == NULL);
    assert(emptyTB->nLines == 0);
    testSanityOfTBList(emptyTB);
    free(emptyTB);
    
    // Case 2: If to || from out of range (expect abort with signal)
    //char *line = "Hello\nHello\n";
    //TB lineTB = newTB(line);
    //deleteTB(onelineTB, 1, 10); // expect abort;
    
    
    // Case 3: If to < from (abort)
    //deleteTB(lineTB, 1, 0); // expect abort; 
    
    // Case 4: Regular input (expect lines to be deleted) 
    char *modifyfirst = "Modify\nFirst\nTB\n";
    char *modifylast = "Modify\nLast\nTB\n";
    char *modifymiddle = "Modify\nMiddle\nTB\n";
    char *deleteall = "Delete\nAll\nTB\n";
    TB modfirstTB = newTB(modifyfirst);
    TB modifylastTB = newTB(modifylast);
    TB modifymiddleTB = newTB(modifymiddle);
    TB deleteAll = newTB(deleteall);
    
        // Case 1: Modify first
    deleteTB(modfirstTB, 0, 1);
    printTB(modfirstTB);
    fprintf(stderr, "Finished printing case 1\n");
    testSanityOfTBList(modfirstTB);
    
        
        // Case 2: Modify last
    deleteTB(modifylastTB, 1, 2);
    printTB(modifylastTB);
    fprintf(stderr, "Finished printing case 2\n");
    testSanityOfTBList(modifylastTB);
    
        // Case 3: Delete all
    deleteTB(deleteAll, 0, 2);
    printTB(deleteAll);
    assert(deleteAll->first == NULL);
    fprintf(stderr, "Finished printing case 3\n");
    testSanityOfTBList(deleteAll); 
        
        // Case 4: Modify middle
    deleteTB(modifymiddleTB, 1, 1);
    printTB(modifymiddleTB);
    fprintf(stderr, "Finished printing case 4\n");
    testSanityOfTBList(modifymiddleTB); 

}


// 13.8.1 Test Delete TB Nodes (function written for DeleteTB)

void testDeleteTBNodes() {
// pass in TB, tb node from, tb node to, char array 
    char *input = "Hello\nThis is a textbuffer\nA long textbuffer\nA really long one\n";
    TB new1 = newTB(input);
    TBNode *from = returnNthNode(1, new1);
    TBNode *to = returnNthNode(2, new1);
    deleteTBNodes(new1, from, to);
    fprintf(stderr, "We have %d new lines\n", new1->nLines);
    assert(new1->nLines == 2);
    //fprintf(stderr, "The array is %s\n", array);
    free(new1);

}


// 13.9 TEST SEARCHTB

void testSearchTB() {
    // Case 1: Regular input, with search substring present
    //char *input = "My name is Jared lovegood and I love cats\nI also love luna lovegood\n";
    //TB inputTB = newTB(input);
    //Match search = searchTB(inputTB, "love");
    //printMatch(search);

    char *input1 = "Hello my name is\n Jarred lovegood\n and I love cats\n";
    struct textbuffer *newTB1 = newTB(input1);
    Match matchListTB1 = searchTB(newTB1, "love");
    fprintf(stderr, "TESTING SEARCH TB\n");
    printMatch(matchListTB1);
    
    // Case 2: Regular input, with search substring as empty string - expect empty list
    //Match emptyMatchList = searchTB(newTB1, ""); 
    //assert(emptyMatchList == NULL);
    //printMatch(emptyMatchList);
    
    // Case 3: Empty input string - expect abort
    //Match nullInputMatchList = searchTB(newTB1, "");
    
    free(newTB1);
    free(matchListTB1);
    //free(emptyMatchList);
    
    // Case 4: tb as empty: expect empty Match list
    char *empty = "\0";
    struct textbuffer *emptyTB = newTB(empty);
    Match emptyMatchList2 = searchTB(emptyTB, "love");
    assert(emptyMatchList2 == NULL);

}



// 13.10 TESTING MISCELLANEOUS FUNCTIONS 

// 13.10.1 Test Return NthNode

void testReturnNthNode() {

    char *input = "Hello\nMy name is\nBethia\nThis is a textbuffer\n";
    TB newTB1 = newTB(input);
    assert(strcmp(returnNthNode(0, newTB1)->line, "Hello") == 0);
    assert(strcmp(returnNthNode(3, newTB1)->line, "This is a textbuffer") == 0);
    
    fprintf(stderr, "Asserts for returnNthNode passed\n"); 
    
}

// 13.10.2 Test Out of Range

void testOutOfRange() {
    char *empty = "\0";
    char *input = "Hello\nMy name is\n";
    TB emptyTB = newTB(empty);
    TB inputTB = newTB(input);
    assert(outOfRange(1, emptyTB) == TRUE);
    assert(outOfRange(0, emptyTB) == FALSE);
    assert(outOfRange(1, inputTB) == FALSE);
    
    free(emptyTB);
    free(inputTB);
    
    fprintf(stderr, "Asserts for testOutOfRange passed\n");

}

// 13.11 PRINT FUNCTIONS USED FOR TESTING

// 13.11.1 Function written to print out nodes in the Match ADT 

void printMatch(Match search) {
    Match temp = search;
    while (temp != NULL) {
        fprintf(stderr, "temp char index is %d, line index is %d -->NEXT\n", temp->charIndex, temp->lineNumber);
        temp = temp->next;
    }

}

//13.11.2 Function written to print out lines in nodes of TB

void printTB(struct textbuffer *TB) {
    TBNode *curr;
    if (TB->first != NULL) {
        curr = TB->first;
        while (curr != NULL) {
            fprintf(stderr, "%s\n", curr->line);
            curr = curr->next; 
        }
    }

}


// OTHER FUNCTIONS FOR TESTING THE SANITY OF THE TBLIST. 

void testSanityOfTBList(TB tb) {
    if (tb == NULL) {
        // list is empty, nItems should be 0, first, last & curr should be NULL
        assert(tb->nLines == 0);
        assert(tb->first == NULL);
        assert(tb->last == NULL);
    } 
    if (tb->first == NULL) {
        assert(tb->last == NULL);
    } else {
        // list not empty, L->last, L->first && L->curr cannot be null
        assert(tb->last != NULL && tb->first != NULL);
        // check links backward and forward into list 
        assert(checkBackward(tb) == TRUE && checkForward(tb) == TRUE);
        assert(checkScanningBackwards(tb) == TRUE && checkScanningForwards(tb) == TRUE);
    }

}

int checkForward(TB tb) {
    TBNode *curr; 
    int count = 0;
    int areForwardLinksValid = TRUE;
    
    for (curr = tb->first; curr != NULL; curr = curr->next) {
        if (curr->prev != NULL && curr->prev->next != curr) {
            fprintf(stderr, "Invalid forward link into node\n");
            areForwardLinksValid = FALSE;
        }
    count++;
    }
    
    assert(count == tb->nLines);
    
    return areForwardLinksValid;
}

int checkBackward(TB tb) {
    TBNode *curr; 
    int count = 0;
    int arePrevLinksValid = TRUE;

    for (curr = tb->first; curr != NULL; curr = curr->next) {
        if (curr->next != NULL && curr->next->prev != curr) {
            fprintf(stderr, "Invalid prev link into node\n");
            arePrevLinksValid = FALSE;
        }
    count++;
    }
    
    assert(count == tb->nLines);
    
    return arePrevLinksValid;
}

int checkScanningForwards(TB tb) {
    int forwardsValid = TRUE;
    TBNode *curr; 
    int count = 0;
    
    for (curr = tb->first; curr != NULL; curr = curr->next) {
        //fprintf(stderr, "Curr is %s\n", curr->line);
        count++;
    }
    if (count != tb->nLines) {
        fprintf(stderr, "FORWARDS Count is %d, nlines is %d\n", count, tb->nLines);
        forwardsValid = FALSE;
    }
    
    return forwardsValid;
    
}

int checkScanningBackwards(TB tb) {
    int backwardsValid = TRUE;
    TBNode *curr; 
    int count = 0;
    
    for (curr = tb->last; curr != NULL; curr = curr->prev) {
        //fprintf(stderr, "Curr is %s\n", curr->line);
        count++;
    }
    if (count != tb->nLines) {
        fprintf(stderr, "BACKWARDS Count is %d, nlines is %d\n", count, tb->nLines);
        backwardsValid = FALSE;
    }
    
    return backwardsValid;
    
}

