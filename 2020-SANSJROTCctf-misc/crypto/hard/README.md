## Crypto Hard 1
#### Description
There's got to be a secret message hidden in this, let's see if you can set it free!

NzcgNjggNjYgNjcgNWYgNjcgNzUgNjUgNzIgNzIgNWYgNjYgNjcgNzIgNjMgNjYgNWYgNjcgNjIgNWYgNjYgNjggNzAgNzAgNzIgNjYgNjY=
#### Solution
It's encoded three times. To decode, convert the base64 to ascii. That will give you a bunch of hex bytes. Convert that to ascii again, that will give you cipher. It's a monoalphabetic substitution cipher. Put it in an online tool like [this](https://www.boxentriq.com/code-breaking/cryptogram) one to yield the flag.
#### Flag
`just_three_steps_to_success`
## Crypto Hard 2
#### Description
We have managed to recover 2 encrypted files and we need you to crack them. Also we managed to find a version of one of the files before it was encrypted and we believe it uses the same key. See if you can use this to decrypt the 'sample.enc' file. Grab the files at https://jrotc-files.allyourbases.co/ch02.zip
#### Solution
Plain1.txt was xor'd with the key to get crypt1.enc. Xor plain1.txt and crypt1.enc to get the key. Then xor sample.enc with the key to get the flag. I did it with [this](https://github.com/Samwise74/Writeups/blob/master/2020-SANSJROTCctf-misc/crypto/hard/decrypt.py) simple python script.
#### Flag
`Full_Xor'd_Jacket_Private`
