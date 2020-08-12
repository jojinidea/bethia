// interface to use create an invertedIndex

#include "set.h"
#include "BSTree.h"
#include "readData.h"

#ifndef INVERTED_H
#define INVERTED_H

Tree createInvertedIndex (void);
Tree addInvertedIndex (Set textCollection, Tree invertedIndex, char *URL);

#endif
