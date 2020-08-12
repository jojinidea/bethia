
/* hasPath.c 
   Written by Ashesh Mahidadia, October 2017
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
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
// DEPTH FIRST SEARCH
// RECURSIVE IMPLEMENTATION: 

// ALGORITHM 
// 1. INITIALISE THE SIZE OF THE VISITED ARRAY 
// 2. VISIT V (THE START/SRC) 
// 3. FOR EACH NEIGHBOUR U OF V
    // IF U HAS NOT BEEN VISITED 
    // MARK U AS VISITED
// 4. DFS(U)

// PSEDUOCODE
// WRITE A HELPER FUNCTION HASEDGE THAT CHECKS GIVEN TWO VERTICES IF THERE IS AN EDGE BETWEEN THEM OR NOT
// FOR w = 0, w < NUM VERTICES IN GRAPH, w++
// if(hasEdge(g, src, w) == 1 AND THE VERTEX HAS NOT BEEN VISITED
// ADD IT TO VISITED
// DO DEPTH FIRST SEARCH


int hasPath(Graph g, Vertex src, Vertex dest)
{

    int visited[g->nV];
    int colnum = 0;
    
    if (hasEdge(g, src, dest) == 1) {
        return 1;
    }
    
    for (colnum = 0; colnum < g->nV; colnum++) {
        if (hasEdge(g, src, colnum) == 1 && visited[colnum] != 1) {
            visited[colnum] = 1;
            if (hasPath(g, colnum, dest) == 1) {    // otherwise keep looking
                return 1;
            }
        }
    
    }
        
return 0;
    
}

int hasEdge(Graph g, Vertex src, Vertex dest) {
    if (g->edges[src][dest] == 1) {
        return 1; 
    }
return 0;
}
