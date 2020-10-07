## Networking Medium 1
#### Description
We have captured a file being transferred over the network, can you take a look and see if you can find anything useful?

https://jrotc-files.allyourbases.co/nm01.zip

Hint: External tools like CyberChef can help decode the data.
#### Solution
We're given a packet capture. Luckily for us, it isn't bloated with a bunch of garbage traffic like most challenges like this are. There are only two packets we care about: 4 and 26. 4 has a password, and 26 has a password-protected 7z file in it. Extract the flag from the 7z using the password to get flag.txt.
#### Flag
`capturing_clouds_and_keys`
## Networking Medium 2
#### Description
Unfortunately, when I was making these writeups, I failed to include the description for this challenge, and now that the CTF is over, I don't have access to it, so here's a cool description that I made up instead:

This server is trying to give us a crappy math test, but the time limit we are given is too low! Try to see if you can get a passing grade. Connect to jrotc-nm02.allyourbases.co on port 9010.
#### Solution
~~Some people said they were able to do this one without writing any code, but I was never able to do it fast enough.~~ To solve it without writing code, you have to answer the questions before the server actually asks them. Immediately after netcatting, paste the first answer (1337) and enter in the second (3) as fast as possible. It may take a few attempts to get it fast enough, but it is possible.

The server asks us to do two math problems. They don't change, so you could just hardcode the answers in a python script and send them, but that's bad practice. I wrote [this](https://github.com/Samwise74/Writeups/tree/master/2020-SANSJROTCctf-misc/networking/medium/nm02.py) very simple python script. The error handling is terrible, so it doesn't end pretty, but at least it breaks _after_ printing the flag.
#### Flag
`SuperServer1337`
