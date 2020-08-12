// Graph ADT interface ... COMP2521 
#include <stdbool.h>

typedef struct GraphRep *Graph;

// vertices are ints
typedef int Vertex;

// edges are pairs of vertices (end-points)
typedef struct Edge {
   Vertex v;
   Vertex w;
} Edge;

Graph newGraph(int);
void  insertEdge(Graph, Edge);
void  removeEdge(Graph, Edge);
bool  adjacent(Graph, Vertex, Vertex);
void  showGraph(Graph);
void  freeGraph(Graph);

// write a program that uses the ADT above to build the graph depicted below and to print all the nodes incident to 1 in ascending order

int main (void) {
    Graph g = newGraph(4);
    Edge e;
    e->v = 0;
    e->u = 3;
    insertEdge(g, e);
    e->v = 0;
    e->u = 1;
    insertEdge(g, e);
    e->v = 3;
    e->u = 2;
    insertEdge(g, e);
    e->v = 1;
    e->u = 3;
    insertEdge(g, e);
    
    int v; 
    for (v = 0; v < 4; v++) {
        if (adjacent(g, v, 1) == TRUE) {
            printf("%d\n", v);
        }
    }   
    
    freeGraph(g);
    return 0;
}
