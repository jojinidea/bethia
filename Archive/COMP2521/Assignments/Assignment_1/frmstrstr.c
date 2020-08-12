#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void changeHeader(char *appendedString, char *string);

int main (void) {
    
    char *original = "#_some *string_hello*a*";
    char *string = malloc(strlen(original) + 1);
    strcpy(string, original);
    char *appendedString = NULL;
    char *strfound;
    int lengthOriginal = strlen(string);
    strfound = strstr(string, "#");
    int CharIndex = 0;
    int index1 = -1; 
    int index2 = -1;
    int foundchar = 0;
    char *string1;
    char *temp = string; 
    char found;
    char *destination = malloc(strlen(string) + strlen("<b>") + strlen("</b>") + 10000);
    
    printf("string length is %d\n", strlen(string));
    
        if (strfound != NULL) {
        CharIndex = lengthOriginal - strlen(strfound);
        if (CharIndex == 0 && lengthOriginal != 1) {
            string = strfound + strlen("#"); // move pointer
            printf("String is %s\n", string);
            appendedString = malloc(strlen(string) + strlen("<h1>") + strlen("</h1>") + 1);
            changeHeader(appendedString, string);         
        
        }
        }
    
    for (int i = 0; i <= strlen(string); i++) {
        if ((string[i] == '*' || string[i] == '_') && index1 == -1) {
            found = string[i];
            index1 = i;
            printf("index 1 is %d\n", index1);
        }
        if (index1 != -1) {
            for (i = index1; i <= strlen(string); i++) {
                if (string[i] == found && i != index1 && index2 == -1) {
                    index2 = i;
                    printf("Index 2 is %d\n", index2);
                }
            }
        }
        if (index1 != -1 && index2 != -1) {
            printf("Both have been found\n"); // replace these
            strncpy(destination, string, index1);
            destination[index1] = '\0'; 
            if (found == '*') {
                strcat(destination, "<b>");
            } else {
                strcat(destination, "<i>");
            }
            strcat(destination, string+index1+1);
            destination[index2+strlen("<b>")-1] = '\0';
            if (found == '*') {
            strcat(destination, "</b>");
            } else {
                strcat(destination, "</i>");
            }
            strcat(destination, string+index2+1);
            string = malloc(strlen(destination) + 1);
            strcpy(string, destination);
            //printf("Destination is %s", destination); //, temp);
            index1 = -1;
            index2 = -1;
            i = index2 + 1;
        }
        if (index1 != -1 && index2 == -1) {
            printf("Corresponding match not found\n"); 
            i = index1+1;
            index1 = -1;
            index2 = -1;
        }
    }
    
    //printf("%s is temp\n", temp);
    printf("%s is destination\n", string);
    
}

void changeHeader(char *appendedString, char *string) {
    strcpy(appendedString, "<h1>");
    strcat(appendedString, string);
    strcat(appendedString, "</h1>");
}
