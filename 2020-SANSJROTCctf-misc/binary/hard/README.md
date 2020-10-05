## Binary Hard 1
#### Description
There's a zip file we need to get into at [https://jrotc-files.allyourbases.co/bh01.zip](https://jrotc-files.allyourbases.co/bh01.zip). All efforts so far have failed but maybe we're not trying hard enough. We do know that the password is base64 encoded however. Can you extract the file?
#### Solution
We need to bruteforce the zip file, and we need to make sure to base64 encode the passwords. A simple python script will do the trick. After running [zipcrack.py](https://github.com/Samwise74/Writeups/blob/master/2020-SANSTROCTctf-misc/binary/hard/zipcrack.py), the flag.txt file is extracted to reveal the flag.
#### Flag
``avoid_common_pws!````
## Binary Hard 2
#### Description
Download the file at [https://jrotc-files.allyourbases.co/bh02.zip](https://jrotc-files.allyourbases.co/bh02.zip) and then find a way to get the flag.
#### Solution
The program is printing a lot of unicode characters that our terminal can't display properly.
```
密码是什么？
> asdf
不正确的.
```
Taking a look at the decompiled code in Ghidra, we see that our input is being compared with the string `"龙123"`.
```c
puts("\x1b[36m密码是什么？\x1b[0m");
printf("> ");
fgets(local_58,0x3c,stdin);
iVar3 = strcmp("龙123\n",local_58);
```
Entering that string at the promt gives us the flag.
#### Flag
`gHn3*jXvs&H!@jGs`
