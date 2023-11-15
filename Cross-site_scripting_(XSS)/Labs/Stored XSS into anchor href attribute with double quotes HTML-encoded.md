
----

### Lab Description

This lab contains a [stored cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/stored) vulnerability in the comment functionality. To solve this lab, submit a comment that calls the `alert` function when the comment author name is clicked.


### Lab Solution


- Insert the payload `javascript:alert(1)` at website parameter

![](/static/img/Pasted_image_20230620220922.png)