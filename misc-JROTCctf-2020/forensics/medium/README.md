## Forensics Medium 1
#### Description
The domain trafficdisruptors.com has been identified as a domain that's used to pass information around between hackers. There appears to be no website there however, can you find how they're communicating?
#### Solution
Flag is in the DNS txt records. Run `nslookup -type=txt trafficdisruptors.com`.
#### Flag
`hidden_in_plain_sight`
## Forensics Medium 2
#### Description
Something has gone wrong with the police departments modern new photo ID system. Here we've got a photo ID of our latest suspect https://jrotc-files.allyourbases.co/fm02.zip but the ID appears to have vanished, can you find it?
#### Solution
There's a second jpeg file inside the first one. Extract the second photo with binwalk or foremost.
#### Flag
`concat4lyfe`
