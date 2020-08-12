#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (void) {
    
    char *originalString = "some *string_again_he_llo there_";
    char *string = malloc(strlen(originalString) + 1);
    strcpy(string, originalString);
    char *appendedString = NULL;
    char *strfound; 
    int lengthOriginal = strlen(string);
    strfound = strstr(string, "#");
    int CharIndex; 
    int index1 = -1; 
    int index2 = -1;
    int foundchar = 0;
    char *string1;
    char *temp = string; 
    char found;
    char *destination = malloc(strlen(string) + strlen("<b>") + strlen("</b>") + 10000);
    
    if (strfound != NULL) {
        CharIndex = lengthOriginal - strlen(strfound);
        if (CharIndex == 0 && lengthOriginal != 1) {
            // append
            string = strfound + strlen("#"); // move pointer
            printf("String is %s\n", string);
            appendedString = malloc(strlen(string) + strlen("<h1>") + strlen("</h1>") + 1);
            strcpy(appendedString, "<h1>");
            strcat(appendedString, string);
            strcat(appendedString, "</h1>");          
        
        }
        else {
            // don't change the string
            printf("Not changing string\n");
        }
    }
    
    printf("string length is %d\n", strlen(string));
    
    
    for (int i = 0; i <= strlen(temp); i++) {
        if ((temp[i] == '*' || temp[i] == '_') && index1 == -1) {
           // printf("Char found is %c\n", temp[26]);
            found = temp[i];
            index1 = i;
           // printf("index 1 is %d\n", index1);
        }
        if (index1 != -1) {
            for (i = index1; i <= strlen(temp); i++) {
                //printf("Char here is %c\n", temp[i]);
                if (temp[i] == found && i != index1 && index2 == -1) {
                    index2 = i;
                 //   printf("Index 2 is %d\n", index2);
                }
            }
        }
        if (index1 != -1 && index2 != -1) {
            printf("Both have been found\n");
            // replace these
            // keep going
            string1 = string+index1+1;
            strncpy(destination, string, index1);
            destination[index1] = '\0';
            strcat(destination, "<b>");
            strcat(destination, string1);
            destination[index2 + strlen("<b>")-1] = '\0';
            strcat(destination, "</b>");
            strcat(destination, string1+index2-index1-1);
            strcat(destination, temp+index2+1);
            i = index2+1;
            printf("index is %d\n", i);
            index1 = -1;
            index2 = -1;
            printf("Destination is %s\n", destination);
            //temp = destination;
            //string = destination;
            printf("Temp is %s\n", temp);
        }
        if (index1 != -1 && index2 == -1) {
            printf("Corresponding match not found\n"); 
            i = index1+1;
            index1 = -1;
            index2 = -1;
        }
    }
    
    printf("%s is temp\n", temp);
    printf("%s is destination\n", destination);
    
  
    

  
    
    
    //printf("string is %s\n", appendedString);

}
