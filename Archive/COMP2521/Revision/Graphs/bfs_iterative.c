// ADD SRC TO QUEUE
// WHILE QUEUE IS NOT EMPTY
// DEQUEUE ITEM
// FOR ALL UNVISITED NEIGHBOURS OF THAT ITEM
// MARK AS VISITED
// ADD TO QUEUE

Queue q = newQueue();
QueueJoin(q, src)
Item item;
visited[src] = 1;
int i = 0

while(!QueueIsEmpty(q)) {
    item = QueueLeave(q);
    for (i = 0; i < g->nV; i++) {
        if (g->edges[i][item] != 0 && visited[i] != 1) {
            visited[i] = 1;
            QueueJoin(q, i);
        }
    }
}
