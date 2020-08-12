// crawl.c ... build a graph of part of the web
// Written by John Shepherd, September 2015
// Uses the cURL library and functions by Vincent Sanders <vince@kyllikki.org>

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#include <curl/curl.h>
#include "stack.h"
#include "set.h"
#include "graph.h"
#include "html.h"
#include "url_file.h"

#define BUFSIZE 1024
#define TRUE 1
#define FALSE 0

void setFirstURL(char *, char *);
void normalise(char *, char *, char *, char *, int);

int main(int argc, char **argv)
{
	URL_FILE *handle;
	char buffer[BUFSIZE];
	char baseURL[BUFSIZE];
	char firstURL[BUFSIZE];
	char next[BUFSIZE];
	int  maxURLs;

	if (argc > 2) {
		strcpy(baseURL,argv[1]);
		setFirstURL(baseURL,firstURL);
		maxURLs = atoi(argv[2]);
		if (maxURLs < 40) maxURLs = 40;
	}
	else {
		fprintf(stderr, "Usage: %s BaseURL MaxURLs\n",argv[0]);
		exit(1);
	}
	
	
	Stack toDo = newStack();
	pushOnto(toDo, firstURL);
	Graph graph = newGraph(maxURLs);
	Set visitedURLs = newSet();
	Set graphURLs = newSet();
	
	while (emptyStack(todo) != TRUE && nVertices(graph) < maxURLs) {
	    char *currURL = popFrom(todo);
	    if (!(handle = url_fopen(currURL, "r"))) {
	        fprintf(stderr, "Couldn't open %s\n", currURL);
	        continue;
	    }
	    insertInto(visitedURLs, currURL);   // the URL has been visited, insert it into a visited URL list	   
	    insertInto(graphURLs, currURL);
	    int pos = 0;
	    char nextURL[BUFSIZE];
	    memset(nextURL, 0, BUFSIZE);  
	    while (!url_feof(handle)) { // while the EOF has not been reached in the URL file
	        while (pos = GetNextURL(buffer, currURL, nextURL, pos) > 0) {
	            if (nVertices(graph) < maxURLs || (isElem(graphURLs, currURL) == FALSE || isElem(graphURLs, nextURL) == FALSE)) {
	                // then let's add the next element to the graph
	                addEdge(graph, currURL, nextURL); // add an edge between currURL to nextURL 
	                
	            
	            }
	    
	    
	    // look at the URLs that are coming out of this page
	    // Create an edge from 1 -> 2
	    // and then we look at the next URL, put it in the stack 
	        } 
	    }
	    for each URL, we want to add a vertex in the graph
	        // we add edges from this URL to the next URL
	    
	    
	    
	    // look at topmost element:
	        // if it has adjacent vertices that are unvisited 
	            // look at element's first unvisted vertex
	            // add this to the stack 
	        // otherwise (if all vertices are visited):
	            // pop the element 
	        
	
	
	}
	
	
	
	        
		
	// You need to modify the code below to implement:
	//
	// add firstURL to the ToDo list
	// initialise Graph to hold up to maxURLs
	// initialise set of Seen URLs
	// while (ToDo list not empty and Graph not filled) {
	//    grab Next URL from ToDo list
	//    if (not allowed) continue
	//    foreach line in the opened URL {
	//       foreach URL on that line {
	//          if (Graph not filled or both URLs in Graph)
	//             add an edge from Next to this URL
	//          if (this URL not Seen already) {
	//             add it to the Seen set
	//             add it to the ToDo list
	//          }
	//       }
    //    }
	//    close the opened URL
	//    sleep(1)
	// }
	if (!(handle = url_fopen(firstURL, "r"))) {
		fprintf(stderr,"Couldn't open %s\n", next);
		exit(1);
	}
	while(!url_feof(handle)) {
		url_fgets(buffer,sizeof(buffer),handle);
		//fputs(buffer,stdout);
		int pos = 0;
		char result[BUFSIZE];
		memset(result,0,BUFSIZE);
		while ((pos = GetNextURL(buffer, firstURL, result, pos)) > 0) {
			printf("Found: '%s'\n",result);
			memset(result,0,BUFSIZE);
		}
	}
	url_fclose(handle);
	sleep(1);
	return 0;
}

// setFirstURL(Base,First)
// - sets a "normalised" version of Base as First
// - modifies Base to a "normalised" version of itself
void setFirstURL(char *base, char *first)
{
	char *c;
	if ((c = strstr(base, "/index.html")) != NULL) {
		strcpy(first,base);
		*c = '\0';
	}
	else if (base[strlen(base)-1] == '/') {
		strcpy(first,base);
		strcat(first,"index.html");
		base[strlen(base)-1] = '\0';
	}
	else {
		strcpy(first,base);
		strcat(first,"/index.html");
	}
}
