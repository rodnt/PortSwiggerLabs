----


### Lab Description

This lab contains a [reflected cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability in the search query tracking functionality where angle brackets and double are HTML encoded and single quotes are escaped.

To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the `alert` function.


### Lab solution

- insert the payload `\';alert(document.domain)//`  at search box

![](/static/img/Pasted_image_20230620223730.png)