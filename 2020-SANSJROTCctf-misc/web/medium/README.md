## Web Medium 1
#### Description
We've come across a website for typewriter lovers at https://jrotc-wm01.allyourbases.co - but it seems to do something more than display these mechanical marvels, can you figure out what's hidden?
#### Solution
View source. At the bottom there's js with a variable that has a bunch of decimal values. Convert to ascii to get the flag.
#### Flag
`Typing_Breaks_Things`
## Web Medium 2
#### Description
A forensics expert with a love for 1960's music has created a top 10 list at https://jrotc-wm02.allyourbases.co and challenged us to find the flag. Let's show him 2020 far beats the 1960's by finding it!
#### Solution
The js file at [https://jrotc-wm02.allyourbases.co/assets/js/obfuscated.js](https://jrotc-wm02.allyourbases.co/assets/js/obfuscated.js) has a comment. That comment takes you to a file with the flag in it. 

This one took me WAY longer than it should have and I read WAY too far into the fact that he was a "forensics expert" by trying to do all sorts of stego. Learn from my mistakes. When it comes to easy CTF chals, Keep It Simple Stupid.
#### Flag
`GroovyBaby!`
## Web Medium 3
#### Description
Our developer has been creating their own captcha system. We informed them it was a bad idea and surprise surprise they're running into issues with it. Have a look at https://jrotc-wm03.allyourbases.co and see if you can solve the captcha and indeed what's wrong with what they've built!
#### Solution
If you look at the style attribute for the SVGs that make up the captcha, you'll notice that the second one is colored white. Change #000088 to any other color. See [captcha.html](https://github.com/Samwise74/Writeups/blob/master/misc-JROTCctf-2020/web/medium/captcha.html)
#### Flag
`css_is_hard`
