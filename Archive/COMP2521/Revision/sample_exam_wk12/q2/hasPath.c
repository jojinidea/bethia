
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
    // contain logic for a DFS in a void function
    int visited[g->nV];
    int i = 0;
    for (i = 0; i < g->nV; i++) {
        visited[i] = 0;
    }
    visited[src] = 1;
    DFS(g, src, visited);
    
    if (visited[dest] == 1) {
        return 1;
    }
    
return 0;
}

// the main function should contain the logic

// with a void DFS recursive thing
// we pass in the graph, src, a visited array
// for all unvisited neighbours that are adjacent to source
// mark as visited
// perform DFS

void DFS (Graph g, Vertex src, int *visited) {
    int i = 0;
    for (i = 0; i < g->nV; i++) {
        if (hasEdge(g, src, i) == 1 && visited[i] != 1) {
            visited[i] = 1;
            DFS(g, i, visited); // then we see what vertices we can reach from the new src
        }
    
    }

}

int hasEdge(Graph g, Vertex src, Vertex dest) {
    if (g->edges[src][dest] != 0) {
        return 1;
    }
return 0;
}

