from pwn import *

r = remote("host3.dreamhack.games", 19439)

for i in range(50):
	a = int(r.recvuntil(b"+")[:-1])
	b = int(r.recvuntil(b"=")[:-1])
	r.sendlineafter(b"?\n", str(a+b).encode())
r.interactive()
