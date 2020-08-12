// assuming an adjacency list representation, implement a function to check whether two vertices are directly connected by an edge

bool adjacenct(Graph g, Vertex x, Vertex y) {
    int i = 0;
    if (g->edges[x] == NULL) {
        return FALSE; 
    } else {
        Node curr = g->edges[x];
        for (i = 0; i < g->nV; i++) {
            if (curr->v == y) {
                return TRUE;
            }
            curr = curr->next; 
        }
    
    }

return FALSE;

}


// ADT for adjacency list

typedef struct GraphRep{ 
    Node **edges; // array of pointers to of type node (an array with each element of the array containing an address to a Node)
    int nV;
    int nE;

} GraphRep;

typedef struct Node { 
    Vertex v; // value
    struct Node *next; // address of next node 
} Node;

// initialisation 

Graph newGraph(int V) {
    int i;
    Graph g = malloc(sizeof(GraphRep));
    g->nV = V;
    g->nE = 0;
    
    g->edges = malloc(V*sizeof(Node*)); // malloc enough memory for array of nodes
    for (i = 0; i < V; i++) {
        g->edges[i] = NULL; // set each element in the array's memory address to NULL (points to NULL) 
    }
return g;
}

// for insertion & deletion of edges, use standard linked-list procedures


