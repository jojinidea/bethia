/*
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "set.h"
#include "queue.h"
#include "readData.h"

#define WANT_URLS 2
#define WANT_TEXT 3

int main(int argc, char *argv[]) {
    
    Queue data = getCollection();
    showQueue(data);
    disposeQueue(data);
    free(data);
    
    char url[1000];
    char url2[1000];
    char *fileName = "url11";
    char *fileName2 = "url11";
    strcpy(url, fileName);
    strcpy(url2, fileName2);
    
    Set url11 = returnSet(WANT_URLS, url);
    showSet(url11);
    disposeSet(url11);
    Set text = returnSet(WANT_TEXT, url2);
    showSet(text);
    disposeSet(text);
    return 0;
}
*/
