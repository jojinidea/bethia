// structs

// we can access a member of a structure using a member-access operator (the dot) 

// we can create an array of structure variables

struct Album {
    char title[35];
    char artist[35];
    char no_tracks[5];
    char year[5];

}

int main (void) {
    Album one;
    one.title = "Hello";
    one.artist = "Lol"
    
    Album album[2]; // something of type Album with 2 indices - like int array[5]
    // to access elements inside the struct, we use a member-access operator
    album[i].title;
    // if we don't know how many elements we want to store inside the array, let's use dynamic memory management
    
    Album *array = malloc(MAX_SIZE*sizeof(Album))


}
