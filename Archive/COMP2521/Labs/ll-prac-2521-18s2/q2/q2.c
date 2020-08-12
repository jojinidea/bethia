/*
 * Question 2
 * By Zain Afzal 11/08/2018
 * cs2521 2018 semester 2
 * 
 * isPalindrome is a function that takes in a 
 * doubily linked list where each node stores a single 
 * character, i.e 
 *           
 *                 __head___[L]___tail__	
 *                /                     \
 *               v                       v
 *         X <- 'a' <-> 'b' <-> 'c' <-> 'd' -> X
 *
 * And returns true of the word formed by the characters 
 * is a palindrome and false otherwise. i. 
 * 
 * "aaa" -> TRUE   (aaa == aaa)
 * "aba" -> TRUE   (aba == aba)
 * "abb" -> FALSE  (abb != bba)
 * "a"   -> TRUE   (a == a)
 * ""    -> TRUE   ("" == "") (an empty string is said to be a palindrome)
 * 
 * you can assume each character is only a-z lower case.
 * 
 * The original linked list should _NOT_ be altered in any way. 
 */

#include "q2.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int isPalindrome(List l) {
    // palindromes 
    // first has to match with last, etc. 
    
    struct _node *forward = l->head;
    struct _node *backward = l->tail; 
    
   // int first_test = TRUE; 
   // int second_test = FALSE;
    int is_palindrome = TRUE; 
    
    // could check for size of the list
    struct _node *temp = l->head; 
    int length = 0;
    
    while (temp != NULL) {
        temp = temp->next; 
        length++;
    }
    
    // if both point to null, palindrome
    if (forward == NULL && backward == NULL) {
        is_palindrome = TRUE; 
    } else {
        while (forward != NULL && backward != NULL) {
            if (forward->value != backward->value) {
                is_palindrome = FALSE;
            }
        forward = forward->next;
        backward = backward->prev;
        }
    } 
    
    /*
    else if (length == 2) {
        if (forward->value == backward->value) {
            is_palindrome = TRUE;
        }
    } else {   
        while (forward != NULL && backward != NULL) {
        // while forward is not equal to backwards, check if they match    
            if (forward->value != backward->value) {
                first_test = FALSE; 
            }
        forward = forward->next; 
        backward = backward->prev; 
        }
        if (first_test == TRUE) {
            if (forward->value == backward->value) {
                second_test = TRUE;    
            }
        }
        if (first_test == TRUE && second_test == TRUE) {
            is_palindrome = TRUE; 
        }
    }
    */
    


	return is_palindrome;
}



