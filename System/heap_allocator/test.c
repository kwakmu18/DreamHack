#include <stdlib.h>

int main(void) {
    free(malloc(0x10));
}