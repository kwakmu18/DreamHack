#include <stdio.h>

int main(void) {
    unsigned char a = 0b01101001;
    unsigned char b = a << 2 | a >> 6;
    unsigned char c = b >> 2 | b << 6;
    unsigned char d = b >> 2;
    unsigned char e = b << 6;
    printf("%c %c %c", a,b,c);
}