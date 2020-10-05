## Web Extreme 1
#### Description
The calendar of secret agents at https://jrotc-wx01.allyourbases.co is restricted to this year and we need to know the field operation dates of the agents for next year. Can you find a way to get next years dates?
#### Solution
We need to trick the website into thinking the year is 2021. Luckily for us, a year variable gets sent with the ajax request.
```js
year =
'      		  	 \n' +
'	\n' +
'      		    \n' +
'	\n' +
'      		  	 \n' +
'	\n' +
'      		    \n' +
'	\n' +
'  \n' +
'\n' +
'\n';
```
The important thing to know when solving this challenge is that not all whitspace is created equal. These strings that are added together are made up of a combination of tabs (0x09) and spaces (0x20). Since all whitespace looks the same, the best way to visualize the difference is by replacing the tabs with 1's and the spaces with 0's. I created [this]() simple python script to do that. 
```
year = 
000000110010
1
000000110000
1
000000110010
1
000000110000
1
00
```
There are a few lines that we don't need and a couple of bits that are the same on every line. I assume they help with parsing on the backend. If we remove all of these garbage bits we are left with four numbers:
```
10
00
10
00
```
You can probably see where this is going. If we convert binary -> decimal this equals 2020. To get 2021, we just need to flip that last bit from a 0 to a 1. To do this in this specific application, we change the last space on the 7th line of the year variable to a tab. Easiest way to do that is to just edit it on our own copy of the html page. I've included [this](https://github.com/Samwise74/Writeups/blob/master/misc-JROTCctf-2020/web/extreme/wx01.zip) zip file with the 2021 version of the page.
#### Flag
`toTh3Fu7ure!`
