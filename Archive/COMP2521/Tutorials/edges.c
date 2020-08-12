void edges(Graph g) {
    // for the matrix
    
    int inner_counter = 0;
    int outer_counter = 0;
    
    while (outer_counter < Graph->nE) {
        while (inner_counter < Graph->nE) {
            if (edges[outer_counter][inner_counter] == 1) {
                printf ("%d is connected to %d\n", outer_counter, inner_counter);
            }
        inner_counter++;
        }
    inner_counter = 0;
    outer_counter++;
    }
    // for inner_counter = outer_counter + 1
    // then we don't print twice - only go down diagonal
    
    // for the list
    
    typedef struct vnode{
        int v;
        vNode *next;
    } vNode;
    typedef vNode *List;
    
    int edge = 0;
    while (edge < Graph->nE) {
        while (List->next != NULL) {
            printf ("%d is connected to %d\n", List->v, List->next->v); 
        List = List->next;   
        }
    edge++;
    }
    // if (i<= curr->v) printf



}
