----

### Lab Description


This lab contains a [reflected cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string. To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the `alert` function.

### Lab Solution


- Insert the payload `'-alert(document.domain)'`  at the search box

![](/static/img/Pasted_image_20230620223145.png)