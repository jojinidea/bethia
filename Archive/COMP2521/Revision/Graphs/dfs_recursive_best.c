
/* hasPath.c 
   Written by Ashesh Mahidadia, October 2017
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include "Graph.h"



/* 
    You will submit only this one file.

    Implement the function "hasPath" below. Read the exam paper for 
    detailed specification and description of your task.  

    - You can add helper functions in this file, if required.  

    - DO NOT modify code in the file BSTree.h . 
    - DO NOT add "main" function in this file. 
*/

int hasEdge(Graph g, Vertex src, Vertex dest);
int *visited;  // array of visited
void DFS(Graph g, Vertex src, int *visited);

// BE SUPER CAREFUL WHEN WRITING
// GLOBAL VARIABLES ALREADY INITIALISED TO 0

// ALGORITHM
// ADD SRC TO VISITED ARRAY
// FOR ALL UNVISITED NEIGHBOURS OF SRC, 
    // ADD TO VISITED ARRAY
    // DO DFS G, COLNUM, DEST

int hasPath(Graph g, Vertex src, Vertex dest)
{
    // test if there is a path from src to dest
    // to test if there is a path from src to dest, we want to test if there is a path from new src to dest
    // do this recursively
    // for all edges adjacent to src that we haven't visited, call DFS
    
    int visited[g->nV];
    DFS(g,src,visited);
    if (visited[dest] == 1) {
        return 1;
    }
return 0;
    
}

void DFS(Graph g, Vertex src, int *visited) {
    visited[src] = 1;
    int i = 0;
    for (i = 0; i < g->nV; i++) {
        if (hasEdge(g, src, i) == 1 && visited[i] != 1) {
            DFS(g, i, visited);
        }
    }

}

int hasEdge(Graph g, Vertex src, Vertex dest) {
    if (g->edges[src][dest] != 0) {
        return 1;
    }
return 0;
}


void DFS(Graph g, Vertex src, int *visited) {
    // add src to visited
    visited[src] = 1;
    for (int i = 0; i < g->nV; i++) {
        if (g->edges[src][i] != 0 && visited[i] != 1) {
            DFS(g, i, visited);
        }
    
    }

}

