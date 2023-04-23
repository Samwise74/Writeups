# Tarry night

**tl;dr:**

```bash
$ # fix gzip file
$ printf '\x1f\x8b\x08' > patched.tar.gz
$ cat tarry_night.tar.gz >> patched.tar.gz
$ # decompress
$ gunzip patched.tar.gz
$ # bruteforce xor key
$ xortool -b -l 1 patched.tar
```

This was a neat file recovery forensics challenge from the 2023 Space Heroes CTF that was blooded in about 20 minutes. It was one of the least solved forensics challenges with 32 solves, which was surprising because it felt like a pretty basic forensics challenge, even when compared to some of the other challenges from this CTF.

## Challenge

**Description**

>I compressed my favorite painting for transport, but I got a little too curious and started playing around with it, and now I can't get my image back! Can you help me out?
MD5 (tarry_night.tar.gz) = ad711ccde1ef02fb3611cae67477dde2

[tarry_night.tar.gz](tarry_night.tar.gz)


## Solution

We are given a file with the extension `.tar.gz`, but `file` doesn't recognize the filetype of this artifact. 

```bash
$ file tarry_night.tar.gz 
tarry_night.tar.gz: data
```

### Step 1 - Decompressing

Let's assume, at least for starters, that the challenge authors are not lying to us and this is indeed a `.tar.gz` file (the description supports this assumption). We know that `.tar.gz` files are just `.tar` files compressed with GZIP, so we first need to recover the `.gz` header. The first thing we should do is figure out what type of file header is expected for a `.gz` file by consulting [some documentation](https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art053):
| Offset | Value | Description |
|--|--|--|
| 0x0 | `1f 8b` | Standard GZIP declaration |
| 0x2 | `byte` | Compression method: 0x08 represents GZIP |
| 0x3 | `byte` | Flags (See below) |
| 0x4 | `dword` | Timestamp |
| 0x8 | `byte` | Extra flags |
| 0x9 | `byte` | Operating System |

If we compare that with the first few bytes of the artifact, it doesn't line up at all. Most significantly, we don't see the magic bytes (`\x1f\x8b`) that would identify this file as GZIP:

```bash
$ xxd tarry_night.tar.gz | head -2
00000000: 08ad 372b 6400 0374 6172 7279 5f6e 6967  ..7+d..tarry_nig
00000010: 6874 2e74 6172 00ec fc65 54a5 4bb3 268a  ht.tar...eT.K.&.
```

For file recovery challenges like these, it's usually best to compare a known-good file of the same filetype as whatever artifact we're working on. That typically makes it pretty easy to see what's out of place. Here is the header of another random `.tar.gz` in my ctf directory:

```bash
$ xxd ./hack-a-sat/pwn/warning_public.tar.gz | head -2
00000000: 1f8b 0800 0000 0000 0003 ec5c 0d74 1455  ...........\.t.U
00000010: 967e dd49 9310 0209 0a8a 8052 2820 18d2  .~.I.......R( ..
```

Notice how the challenge artifact has the name of the file "tarry_night.tar" near the header, but this other file does not. That is because of the `Flags` field in the header (offset 3). This value is is `\x00` in the known-good file. The `Flags` byte is meant to be interpreted as a bitmask. If Bit 3 (0x8) is set in this byte, it means that the name of the compressed file immediately follows the header. Thus, we can identify the end of the header by the start of this string. If we count backwards from the start of the string, we count 7 total header bytes. The GZIP header should be 10 bytes, which means we are missing three. It makes sense for the first byte in the artifact (`\x08`) to be the `Flags` byte since it is a value indicating that the name of the file will be present following the header (`\x08`). Also, we know we are missing the first two magic bytes because they are constant. Thus, we can reasonably assume that we're missing the first three bytes of the `.gz` header (`\x1f\x8b\x08`).

Let's try prepending these missing header bytes onto the artifact:

```bash
$ printf '\x1f\x8b\x08' > patched.tar.gz
$ cat tarry_night.tar.gz >> patched.tar.gz
$ file patched.tar.gz 
patched.tar.gz: gzip compressed data, was "tarry_night.tar", last modified: Mon Apr  3 20:31:41 2023, from Unix, original size modulo 2^32 1290240
```

Nice! We get seemingly valid GZIP data. Let's decompress it

```bash
$ gunzip patched.tar.gz
$ file patched.tar 
patched.tar: data
```
It's a valid `.gz`, but not a valid `.tar.gz`. 

### Step 2 - XORing

We need to figure out what's going on with the decompressed tar file. Let's start with a known-good file of this type:

```bash
$ xxd ./idekCTF/side_effect/side_effect.tar | head -10
00000000: 6174 7461 6368 6d65 6e74 732f 0000 0000  attachments/....
00000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000020: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000030: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000040: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000050: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000060: 0000 0000 3030 3030 3737 3700 3030 3031  ....0000777.0001
00000070: 3735 3000 3030 3031 3735 3000 3030 3030  750.0001750.0000
00000080: 3030 3030 3030 3000 3134 3335 3735 3533  0000000.14357553
00000090: 3435 3000 3031 3131 3630 0020 3500 0000  450.011160. 5...
```

The good file starts with the name of a directory followed by a bunch of nulls, and if we consult [some documentation](https://www.gnu.org/software/tar/manual/html_node/Standard.html), we see that the start of a tar block begins with a `char name[100];`. This matches what we're seeing perfectly, so what's going on with the artifact?
 
```bash
$ xxd patched.tar | head -10
00000000: 6a60 6d6b 2266 7c6b 0c0c 0c0c 0c0c 0c0c  j`mk"f|k........
00000010: 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c  ................
00000020: 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c  ................
00000030: 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c  ................
00000040: 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c  ................
00000050: 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c 0c0c  ................
00000060: 0c0c 0c0c 3c3c 3c3c 3a38 380c 3c3c 3c3d  ....<<<<:88.<<<=
00000070: 3b39 3c0c 3c3c 3c3d 3b39 3c0c 3c3c 3c3c  ;9<.<<<=;9<.<<<<
00000080: 383b 3c3e 3d3e 390c 3d38 383d 3e3a 3f3f  8;<>=>9.=88=>:??
00000090: 3f3a 3e0c 3c3d 3e3f 3f3a 0c2c 3c0c 0c0c  ?:>.<=>??:.,<...
```

We see a bunch of repeating `\x0c`'s where there should be nulls. At this point, a reasonable assumption is that those `\x0c`'s could be `\x00`'s xor'd with `\x0c`. For speed (and fb) purposes, a good next step would be to immediately run [xortool](https://github.com/hellman/xortool), but let's do a little analysis first to check our assumption by trying to decode the file name at the start of the archive:

```python
>>> [chr(x ^ 0xc) for x in bytes.fromhex('6A 60 6D 6B  22 66 7C 6B')]
['f', 'l', 'a', 'g', '.', 'j', 'p', 'g']
```

This confirms our assumption, let's get the whole file with xortool:

```bash
$ xortool -b -l 1 patched.tar 
256 possible key(s) of length 1:
\x0c
\r
\x0e
\x0f
\x08
...
Found 0 plaintexts with 95%+ valid characters
See files filename-key.csv, filename-char_used-perc_valid.csv

$ file xortool_out/*
xortool_out/000.out:                           POSIX tar archive (GNU)
xortool_out/001.out:                           data
xortool_out/002.out:                           data
xortool_out/003.out:                           data
xortool_out/004.out:                           data
<snip>
$ tar tf xortool_out/000.out
flag.jpg
```

And we get a flag:

![flag.jpg](flag.jpg)
