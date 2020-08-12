// if we are removing nodes from the END of a list
    // a. Make sure L->last points to L->last->prev
    // b. MAKE SURE L->LAST->NEXT IS SET TO NULL 
    
// if we are removing nodes from the beginning of a list
    // a. Make sure L->first points to L->first->next; 
    // b. Make sure L->first->prev is set to NULL 

// if we are removing nodes from the middle of a list
    // a. Make sure we store curr->next as AFTER
    // b. Make sure we store curr->prev as BEFORE
    // c. AFTER->prev = BEFORE
    // d. BEFORE->next = AFTER
    // e. Change the current pointer
    // f. Free
