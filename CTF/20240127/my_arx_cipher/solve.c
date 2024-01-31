#include <stdio.h>
#include <unistd.h>
#include <string.h>
#define _WORD short
char encrypted[72];

void sub_129F(long long a1, unsigned short *a2) {
	long long result;
	unsigned short v3,v4,v5,temp;

	v3=*a2;
	v4=a2[1];
	for(int i=2;i>=0;i--) {
		v5 = v4;
		v4 = v3 ^ *(short *)(2 * (2 * i + 1) + a1);
		v4 = (v4 >> 7) | (v4 << 9);
		v3 = (v5 ^ *(short *)(4 * i + a1)) - v4;
		v3 = ((v3 >> 7) | (v3 << 9));
	}

	*a2 = v3;
	a2[1] = v4;
}

int main(void) {
	FILE *keyfile, *encfile, *plainfile;
	keyfile = fopen("key", "rw");
	encfile = fopen("flag.enc", "rw");
	plainfile = fopen("result", "w");
	long long key;
	fread(&key, 2, 6, keyfile);

	int s;
	for(s=0;;fwrite(&s,2,2,plainfile)) {
		memset(&s, 0, sizeof(s));
		if (!fread(&s, 1, 4, encfile)) break;
		sub_129F(&key, &s);
	}
	
	printf("done");
}
