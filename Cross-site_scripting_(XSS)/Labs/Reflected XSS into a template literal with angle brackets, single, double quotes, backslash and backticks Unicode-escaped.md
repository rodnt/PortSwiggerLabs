----

### Lab Description

This lab contains a [reflected cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability in the search blog functionality. The reflection occurs inside a template string with angle brackets, single, and double quotes HTML encoded, and backticks escaped. To solve this lab, perform a cross-site scripting attack that calls the `alert` function inside the template string.


### Lab Solution

- Insert the payload `${alert(document.domain)}` 

![](/static/img/Pasted_image_20230620225940.png)