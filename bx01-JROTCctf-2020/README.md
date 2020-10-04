
## Binary Extreme 1
#### Description
Download the file at https://jrotc-files.allyourbases.co/bx01.zip and find a way to get the flag. Once you have the method that works send the solution to the network service at jrotc-ne02.allyourbases.co port: 9012 to get the real flag.
#### Solution
This was easily my favorite challenge in the CTF. I admit, binary exploitation is not my strong suit, so it was fun to learn something new. Let's take a look at the file.
```
$ file program
program: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=c1c0ad62410be4f2e5ebdadc26b5f3cb68b7ad1b, stripped

$ checksec program
[*] '/mnt/b/my_repos/Writeups/misc-JROTCctf-2020/binary/extreme/program'
     Arch:     amd64-64-little 
     RELRO:    Partial RELRO    
     Stack:    No canary found   
     NX:       NX enabled   
     PIE:      No PIE (0x400000)
```
##### Normal command output:
```
$ ./program

Welcome to the Challenge & Auth Server
Please enter your challenge: aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Secret is uokpjaweHd.aIBik.ofndtenhFmwqrkCFmdHnr.gmCgghoigu
Your challenge was aaaaaaaaaaaaaaaaaaaaaaaaaaaaa

The server challenge was uokpjaweHd.aIBik.ofndtenhFmwqrkCFmdHnr.gmCgghoigu
Sorry, your challenge did not match the server
```
No canary? Maybe I can get away with an easy buffer overflow.
```bash
$ python -c "print('a'*200)" | ./program

Welcome to the Challenge & Auth Server
Please enter your challenge: Secret is uokpjaweHd.aIBik.ofndtenhFmwqrkCFmdHnr.gmCgghoigu
Your challenge was aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
The server challenge was uokpjaweHd.aIBik.ofndtenhFmwqrkCFmdHnr.gmCgghoigu
Sorry, your challenge did not match the server
```
No such luck, our input gets truncated. It looks like the program is trying to simulate some sort of challenge-response authentication, and we have to guess what the server's challenge is going to be. A quick look at the decompiled code in Ghidra confirms this.
```c
iVar3 = thunk_FUN_0040050e(local_1b8,&local_178); // this line checks if our input is equal to the calculated challenge
if (iVar3 == 0) { // if equal
  FUN_004115d0(10);
  lVar9 = FUN_00410fd0("flag.txt",&DAT_004c417f); // success starts here!
```
I started out trying to reverse the function that generates the challenge, but very quickly stopped having fun because the binary is stripped. After trying that for a while, I began to wonder what exactly the RNG was being seeded with. If the current time is the only seed, then we can calculate the challenges that the server will generate by giving the binary a future time. Using the below Bash while loop, you can keep your system time set at a constant value. This way, if time is the only seed, the program should consistently produce the same challenge.
```bash
$ while [ true ]; do sudo date -s "1 October 2020 14:00:00"; sleep 0.5; done
$ ./program
Welcome to the Challenge & Auth Server
Please enter your challenge: asdf
Secret is vbfBgtby.KHzIJxeJjEpszaf..aik.dy.jl.CewBapeAdtwED
Your challenge was asdf

The server challenge was vbfBgtby.KHzIJxeJjEpszaf..aik.dy.jl.CewBapeAdtwED
Insufficient challenge length.

$ ./program
Welcome to the Challenge & Auth Server
Please enter your challenge: asdf
Secret is vbfBgtby.KHzIJxeJjEpszaf..aik.dy.jl.CewBapeAdtwED
Your challenge was asdf

The server challenge was vbfBgtby.KHzIJxeJjEpszaf..aik.dy.jl.CewBapeAdtwED
Insufficient challenge length.
```
Bam! We got the program to generate the same challenge twice. Now all that's left to do is to calculate what the program will generate a few minutes from now and send it at the right time. I created [this]() simple python script to do that for me.
```
current time: 14:02:00
Secret is IvkKBrth.jGkakJruwmxu.DlrBkAoohaJr.pAqorrgCkqpBC.
Your challenge was IvkKBrth.jGkakJruwmxu.DlrBkAoohaJr.pAqorrgCkqpBC.
The server challenge was IvkKBrth.jGkakJruwmxu.DlrBkAoohaJr.pAqorrgCkqpBC.

RevErsIng-is_HaRD9-804
```
Note: if you are following along, you will need to calculate your own challenge based on the time you want to contact the server and set those variables in the script. I recommend using a VM so you don't mess up the system time on your host.
#### Flag
`RevErsIng-is_HaRD9-804`
