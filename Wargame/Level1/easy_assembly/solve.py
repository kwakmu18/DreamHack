enc_flag = b"txKewH\\ih~\\ywbFyw\x05FTsrYih~\\~ZaWjwfZR\x02b\\yw\\\x00|W\x0d\x0dM"

a2 = 0
inp = ""

for i in enc_flag:
    for j in range(256):
        if a2 | (i ^ 48 ^ j) == 0:
            inp += chr(j)
            a2 |= i ^ 48 ^ j
            break

print(inp)