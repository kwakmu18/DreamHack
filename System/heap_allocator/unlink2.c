// gcc -o unlink2 unlink2.c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
int main()
{
    uint64_t *ptr,*ptr2;
    
    ptr = malloc(0x100);  // 0x602000
	  ptr2 = malloc(0x100); // 0x602000
	
		free(ptr);            // main_arena -> ptr
		ptr[0] = ptr+0x100;   
		ptr[1] = ptr+0x100; 
		free(ptr2); // main_arena -> ptr -> ptr2
		// ptr 제거
		// 검증 1 : ptr->fd->bk = main_arena -> bk
}