// tutorial wk 7 
// Q4
// write a function that takes a Graph as a parameter and returns an array containing all the edges in the Graph along with a count of the number of edges


Edge *edges(Graph g, int *nE) {
    Edge *new = malloc(g->nE*sizeof(Edge)); // an array that holds g->nE edges
    Node *curr; 
    
    for (v = 0; v < g->nV; v++) {
        for (curr = g->edges[v]; c!= NULL; c = c->next) {
            int val = c->v;
            new[n++] = makeEdge(val, v);
        }
    
    }


}

Edge *edges(Graph g, int *nE) {
// assuming adjacency list representation
    for (v = 0; v < g->nV; v++) {
        Node *curr;
        Edge *new = malloc(g->nE*sizeof(Edge)); // an array that holds edges
        for (c = g->edges[v]; c != NULL; c = c->next) {
            w = c->v;
            new[n++] = mkEdge(v, w);
        }
    
    }

}

Edge *es;
int n;
es = edges(g, &n) 

// for an adjacency matrix representation

Edge *edges(Graph g, int *nE) {
    int i;
    int j;
    for (i = 0; i < g->nV; i++) {
        for (j = 0; j < g->nV; j++) {
            if (g->edges[i][j] != 0) {
                new[n++] = makeEdge(i, j);
            }
        }
    
    }    

}


typedef struct GraphRep {
    int **edges; // adjacency matrix (2x2 matrix)
    int nV;
    int nE;

} GraphRep;
