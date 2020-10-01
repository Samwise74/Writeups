# Droids4
This is the final challenge in picoCTF2019's mobile reversing series. 

Description:
> reverse the pass, patch the file, get the flag. Check out this [file](https://github.com/Samwise74/Writeups/raw/master/droids4-picoCTF-2019/four.apk). You can also find the file in /problems/droids4_0_99ba4f323d3d194b5092bf43d97e9ce9.

Category: reversing

## Initial Analysis
#### Screenshot of the app:
![Main Screen](https://github.com/Samwise74/Writeups/blob/master/droids4-picoCTF-2019/images/main_screen.png)

As we can see from the description, we'll be combining both aspects of droids2 and droids3. Not only will we need to patch the file, but we'll need to reverse the app to get the correct password as well. 

Let's start by decompiling the apk file. We're going to use [apktool](https://ibotpeaches.github.io/Apktool/), an outstanding tool for reversing android apps. Run it with `java -jar apktool.jar four.apk`. Doing so will create a directory called `four`, which will have a subdirectory `smali`. Smali is the human-readable version of Dalvik bytecode. This directory essentially contains the assembly code for the app. That being said, there's only one file we care about, `out/com/hellocmu/picoctf/FlagstaffHill.smali`. This file contains the instructions that generate the password, which we will reverse later, and the area that we need to patch. Trying to read Smali isn't very fun, so let's convert it to Java source code. 

There are many tools and methods to convert Smali to Java source code, but I used Konloch's [Bytecodeviewer](https://bytecodeviewer.com/).

### FlagstaffHill.class:
```Java
package com.hellocmu.picoctf;

import android.content.Context;

public class FlagstaffHill {
   public static native String cardamom(String var0);

   public static String getFlag(String var0, Context var1) {
      StringBuilder var2 = new StringBuilder("aaa");
      StringBuilder var3 = new StringBuilder("aaa");
      StringBuilder var5 = new StringBuilder("aaa");
      StringBuilder var4 = new StringBuilder("aaa");
      var2.setCharAt(0, (char)(var2.charAt(0) + 4));
      var2.setCharAt(1, (char)(var2.charAt(1) + 19));
      var2.setCharAt(2, (char)(var2.charAt(2) + 18));
      var3.setCharAt(0, (char)(var3.charAt(0) + 7));
      var3.setCharAt(1, (char)(var3.charAt(1) + 0));
      var3.setCharAt(2, (char)(var3.charAt(2) + 1));
      var5.setCharAt(0, (char)(var5.charAt(0) + 0));
      var5.setCharAt(1, (char)(var5.charAt(1) + 11));
      var5.setCharAt(2, (char)(var5.charAt(2) + 15));
      var4.setCharAt(0, (char)(var4.charAt(0) + 14));
      var4.setCharAt(1, (char)(var4.charAt(1) + 20));
      var4.setCharAt(2, (char)(var4.charAt(2) + 15));
      return var0.equals("".concat(var5.toString()).concat(var3.toString()).concat(var2.toString()).concat(var4.toString())) ? "call it" : "NOPE";
   }
}
```
####
## Step 1: Patching the file
The first thing we need to do is patch the file. The problem is that the function that returns the flag is never called. The place that we'd expect to see it is replaced with `"call it"`, a hint from the challenge author no doubt. To call the function, we need to edit the `FlagstaffHill.smali` file. 
```
const/4 v5, 0x0

if-eqz v5, :cond_ba

const-string v5, "call it" #this is the part we need to change

return-object v5
```
Remove the first line and replace the middle line with 
```
invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->cardamom(Ljava/lang/String;)Ljava/lang/String;`. 
```
This will call the function that returns the flag when we input the correct password.

Next, we need to recompile the app so we can run the patched version. Run apktool again with `java -jar apktool.jar build -o patched-four.apk four/`.

Now that we've patched the app, we need to sign it so we can actually install it. Fortunately, both the tools we need come pre-installed with Java. First, we need to create a key using keytool:
```
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```
Then sign the apk with jarsigner:
```
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore my_application.apk alias_name
```
## Step 2: Reversing the Password
This is the easy part. Since we already have the Java source code, it's now essentially a very basic reversing challenge. 

We can see that four variables, each strings of three lowercase A's, are initialized. Then, one-by-one various values are added to each character in said variables. To find out what each specific letter becomes, we take the ascii value of 'a' (97), add to it the number that is added in the program, and convert that number back to ascii. Following this method we get:
```Java
var2 = "ets"
var3 = "hab"
var5 = "alp"
var4 = "oup"
```
Next, there are a number of concatenations that happen. 
* "" is concatenated with "alp" (var5)
* "alp" is concatenated with "hab" (var3)
* "alphab" is concatenated with "ets" (var2)
* "alphabets" is concatenated with "oup" (var4)

Which produces a final password of `alphabetsoup`.
## Conclusion
After installing the patched and signed app, enter the password to reveal the flag:
`picoCTF{not.particularly.silly}`
### The message we get from the unpatched version:
![unpatched-correct-password](https://github.com/Samwise74/Writeups/blob/master/droids4-picoCTF-2019/images/unpatched_correct_password.png)
### Screenshot of patched app with flag:
![patched-correct-password](https://github.com/Samwise74/Writeups/blob/master/droids4-picoCTF-2019/images/patched_correct_password.png)
