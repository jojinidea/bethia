#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (void) {
    
    char *original = "some *string_again_hello_there";
    char *string = malloc(strlen(original) + 1);
    strcpy(string, original);
    char *appendedString = NULL;
    char *strfound;
    int lengthOriginal = strlen(string);
    strfound = strstr(string, "#");
    int CharIndex = 0;
    
    if (strfound != NULL) {
        CharIndex = lengthOriginal - strlen(strfound);
        if (CharIndex == 0 && lengthOriginal > 1) {
            string = strfound + strlen("#");
            appendedString = malloc(strlen(string) + strlen("<h1>") + strlen("</h1>") + 1);
            strcpy(appendedString, "<h1>");
            strcat(appendedString, string);
            strcat(appendedString, "</h1>");
        }
    }
    
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
    
    int index1 = -1; 
    int index2 = -1;
    int foundchar = 0;
    char *string1;
    
    char *temp = string; 
    char found;
    char *destination = malloc(strlen(string) + strlen("<b>") + strlen("</b>") + 10000);
    
    printf("string length is %d\n", strlen(string));
    
    
    for (int i = 0; i <= strlen(temp); i++) {
        if ((temp[i] == '*' || temp[i] == '_') && index1 == -1) {
            //printf("Char found is %c\n", temp[i]);
            //printf("temp is %s\n", temp);
            found = temp[i];
            index1 = i;
            printf("index 1 is %d\n", index1);
        }
        if (index1 != -1) {
            for (i = index1; i <= strlen(temp); i++) {
            //    printf("Char here is %c\n", temp[i]);
                if (temp[i] == found && i != index1 && index2 == -1) {
                    index2 = i;
                    printf("Index 2 is %d\n", index2);
                }
            }
        }
        if (index1 != -1 && index2 != -1) {
            printf("Both have been found\n");
            // replace these
            // keep going
            strncpy(destination, string, index1);
            destination[index1] = '\0'; 
            strcat(destination, "<br>");
            strcat(destination, string+index1+1);
            destination[index2+strlen("<br>")-1] = '\0';
            strcat(destination, "</br>");
            strcat(destination, string+index2+1);
            temp = malloc(strlen(destination) + 1);
            string = malloc(strlen(destination) + 1);
            strcpy(string, destination);
            strcpy(temp, destination);
            printf("Destination is %s, temp is %s\n", destination, temp);
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
    
    printf("%s is temp\n", temp);
    printf("%s is destination\n", destination);
    
  
    

  
    
    
    //printf("string is %s\n", appendedString);

}
