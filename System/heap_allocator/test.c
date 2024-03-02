#include <stdlib.h>

int main(void) {
    char *ptr = malloc(4);
    free(ptr);
}