// write an algorithm to output all edges of the graph

int i = 0;
while (i < g->nE) {
    printf("%d", g->edges[i]);

}

// implement a function to check whether two vertices are directly connected by an edge assuming an array of edges representation

bool adjacent (Graph g, Vertex x, Vertex y) {
    int i = 0;
    for (i = 0; i < g->nE; i++) {
        if (g->edges[u] == x && g->edges[v] == y || g->edges[v] == x && g->edges[u] == y) {
            return TRUE;
        }
    
    }
return FALSE;

}


typedef struct GraphRep {
    Edge *edges; // array of edges
    int nV; // #vertices
    int nE; // #edges
    int n; // size of edge array

} GraphRep;

Graph newGraph(int V) {
    Graph g = malloc(sizeof(GraphRep));
    g->nV = V;
    g->nE = 0;
    g->edges = malloc(g->n*sizeof(Edge)); // size of edge array * size of edges
    return g;
    
}

bool eq(Edge e1, Edge e2) {
    if (e1[v] == e2[v] && e1[u] == e2[u] || e1[u] == e2[v] && e1[v] == e2[u]) {
        return TRUE;
    }
return FALSE;
}

void insertEdge(Graph g, Edge e) {
    assert(g != NULL && g->nE < g->n) {
        while (i < g->nE) {
            i++;
        }
        if (i == g->nE) { // edge not found
            g->edges[g->nE++] = e;
        }
    }

}

void removeEdge(Graph g, Edge e) {
    int i = 0;
    while (i < g->nE) {
        i++; 
    }
    if (i < g->nE) {    // edge found
        g->edges[i] = g->edges[--g->nE];
    }

}
