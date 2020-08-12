// write an algorithm to output all edges of the graph

int i = 0;
int j = 0;

for (i = 0; i < g->nV; i++) {
    for (j = 0; j < g->nV; j++) {
        printf("%d", g->edges[i][j]);
    } 

}

// assuming an adjacency matrix representation, implement a function to check whether two vertices are connected by an edge

bool adjacenct(Graph g, Vertex x, Vertex y) {
    if (g->edges[x][y] == 1) {
        return TRUE;
    }
return FALSE;
}


// graph ADT

typedef struct GraphRep {
    int **edges; // adjacency matrix (2x2 matrix)
    int nV;
    int nE;

} GraphRep;

// initialisation 

Graph newGraph(int V) {
    Graph g = malloc(sizeof(GraphRep));
    g->nV = V;
    g->nE = 0;
    
    g->edges = malloc(V*sizeof(int*)); // number of vertices * size of int*
    
    for (i = 0; i < V; i++) {
        g->edges[i] = calloc(V, sizeof(int)); // calloc allocates a memory block of size nelems * bytes and sets all bytes to 0
    }
    
    return g;
}

// insert edge

void insertEdge(Graph g, Edge e) {
    if (g->edges[e.v][e.u] == 0 && g->edges[e.u][e.v] == 0) {
        // edge not in graph
        g->edges[e.v][e.u] = 1;
        g->edges[e.u][e.v] = 1;
        g->nE++;
    }

}

void removeEdge(Graph g, Edge e) {
    if (g->edges[e.v][e.u] == 1) {
        g->edges[e.v][e.u] = 0;
        g->edges[e.u][e.v] = 0;
        g->nE--;
    }
    
}
