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
Some people said they were able to do this one without writing any code, but I couldn't. The server asks us to do two math problems. They don't change, so you could just hardcode the answers in a python script and send them, but that's bad practice. I wrote [this]() very simple python script. The error handling is terrible, so it doesn't end pretty, but at least it breaks after printing the flag.
#### Solution
`SuperServer1337`
#### Flag

