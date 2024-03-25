// gcc -o unsortedbin1 unsortedbin1.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main() {
  char *ptr = malloc(0x100);
  char *ptr2 = malloc(0x100);
  char *ptr3 = malloc(0x100);
  char *ptr4 = malloc(0x100);
  free(ptr); // ptr == unsorted bin
  free(ptr3);
  ptr3 = malloc(0x100);
}
