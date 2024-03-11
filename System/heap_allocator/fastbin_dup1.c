// gcc -o fastbin_dup1 fastbin_dup1.c

#include <stdlib.h>
#include <stdio.h>

long win;

int main()
{

	long *ptr1, *ptr2, *ptr3, *ptr4;
	
	*(&win - 1) = 0x31;
	
	ptr1 = malloc(0x20);
	ptr2 = malloc(0x20);
	
	free(ptr1);
	free(ptr2);
	free(ptr1);
	
	ptr1 = malloc(0x20);
	ptr2 = malloc(0x20);
	
	ptr1[0] = &win - 2;
	
	ptr3 = malloc(0x20);
	
	ptr4 = malloc(0x20);
	ptr4[0] = 1;
	
	if(win) {
		printf("Win!\n");
	}
	
	return 0;
}
