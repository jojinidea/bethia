// STACK
// Add src to stack
// Mark as visited
// While stack is not empty
// Pop item from stack
// for all unvisited neighbours of item
// mark as visited
// add to stack

Stack s = newStack();
StackJoin(s, src);
visited[src] = 1;

while (!IsEmptyStack(s)) {
    item = PopStack(s);
    for (int i = 0; i < g->nV; i++) {
        if (g->edges[i][item] != 0 && visited[i] != 1) {
            // mark as visited
            visited[i] = 1;
            StackJoin(i, src);
        }
    }

}
