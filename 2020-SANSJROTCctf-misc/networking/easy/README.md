## Networking Easy 1
#### Description
We have run a nmap scan on our local network and believe there may be a vulnerable service. See if you can identify any services that might have a CVE attached to them: https://jrotc-files.allyourbases.co/ne01.zip

Hint: The flag is the CVE with the highest severity rating.
#### Solution
PCMan's FTP Server immediately sticks out like a sore thumb. Googling version 2.0.7 results in CVE-2013-4730, which is also the flag.
#### Flag
`CVE-2013-4730`
## Networking Easy 2
#### Description
Here is the IP address and port which we believe is holding a key piece of data. Find a way to connect to it and retrieve that data.

IP: jrotc-ne02.allyourbases.co Port: 9011
#### Solution
Netcat to the service and it just prints out the flag.
#### Flag
`Knock_Knock_Who's_There?_Flags_There!`
