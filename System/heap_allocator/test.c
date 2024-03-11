#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char *ptr1 = malloc(0x10);
    char *ptr2 = malloc(0x10);
    strcpy(ptr2, "hello");
    free(ptr1);
    free(ptr2);
    char *ptr3 = malloc(0x10);
    printf("%s", ptr3);
}