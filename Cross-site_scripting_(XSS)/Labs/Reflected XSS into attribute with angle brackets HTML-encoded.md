
----

### Lab description


This lab contains a [reflected cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability in the **search blog functionality** where angle brackets are HTML-encoded. To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the `alert` function.


### Lab solution

- Insert the payload like the request bellow

![](/static/img/Pasted_image_20230620220359.png)