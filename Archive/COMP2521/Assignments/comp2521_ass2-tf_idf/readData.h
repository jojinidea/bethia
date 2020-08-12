// interface to read data from files
#include "graph.h"
#include "queue.h"
#ifndef READDATA_H
#define READDATA_H

#define FALSE 0
#define TRUE 1
#define WANT_URLS 2
#define WANT_TEXT 3
#define MAX_CHAR 1000
#define TXT_NEEDED 4
#define TXT_NOT_NEEDED 5

Set GetCollection();
Graph GetGraph(Set collection);
Set returnSet(int arg, int txt_needed, char *fileName);
Queue getCollection();

#endif
