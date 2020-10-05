## Forensics Easy 1
#### Description
We've found a document at https://jrotc-files.allyourbases.co/fe01.zip from a doctor who seems to be hinting at something - can you figure out where to look for the flag?
#### Solution
Flag is in the metadata. Open with a text editor like Notepad and Ctrl+F for "flag."
#### Flag
`drMetadata`
## Forensics Easy 2
#### Description
Our much loved cat Snowy is missing and we've had a graphic design company produce a poster at https://jrotc-files.allyourbases.co/fe02.zip. We just can't see any details, but the graphics company said they've put all info into the design. Can you find the info? The flag is the phone number.
#### Solution
Text is white/transparent. Open in a pdf viewer. You can Ctrl+A and copy/paste to a place you can read it.
#### Flag
`1 800 LOST SNOWY`
## Forensics Easy 3
#### Description
There's been a study into juniors taking too long at lunch, redacted file available at https://jrotc-files.allyourbases.co/fe03.zip. As the file has been redacted and declassified, it's been issued to journalists via the usual means but the solution has been discovered somehow - can you find out what the flag would display?
#### Solution
Same thing as Easy 2. Ctrl+A, copy/paste, profit.
#### Flag
`OK_BACK_TO_IT`
## Forensics Easy 4
#### Description
There's something rather strange about this GIF file: https://jrotc-files.allyourbases.co/fe04.zip. See if you can break it down at work out what it is.
#### Solution
Frame 72 has the flag on it. Throw it in an online gif splitter or use Gimp's `open frames as layers` functionality.
#### Flag
`splitting_gifs_like_door_frames`
## Forensics Easy 5
#### Description
A journalist has informed us they have evidence stored safely at a major city but didn't get time to tell us which city.

Can you figure it out from the image at https://jrotc-files.allyourbases.co/fe05.zip?
#### Solution
This one can be misleading because of what the picture looks like. Ignore the picture itself. Take a look at the exif data with exiftool or some online tool. The flag is in the `Text Layer Name` section.
#### Flag
`MELBOURNE`
