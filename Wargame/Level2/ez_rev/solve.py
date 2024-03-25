from pwn import *

def shl(text):
    return text[3:len(text)] + text[0:3]
def shr(text):
    return text[len(text)-3:len(text)] + text[:len(text)-3]

r = process("./prob")
key = "qksrkqs"
ciphertext = list("|l|GHyRrsfwxmsIrietznhIhj")

ciphertext = shl(ciphertext)

for i in range(len(ciphertext)):
    ciphertext[i] = chr(ord(ciphertext[i]) ^ ord(key[i%7]))

ciphertext = shr(ciphertext)
for i in range(len(ciphertext)):
    ciphertext[i] = chr(ord(ciphertext[i]) ^ ord(key[i%7]))

ciphertext = shl(ciphertext)

print("".join(ciphertext))