from pwn import *

r = remote("host3.dreamhack.games", 13588)

r.recvuntil(b"Random number: ")
v6 = int(r.recvline()[:-1],16)

s2 = 0x7d1c4b0a

v7 = v6 ^ s2

r.sendlineafter(b"Input? ", str(v7).encode())
r.interactive()