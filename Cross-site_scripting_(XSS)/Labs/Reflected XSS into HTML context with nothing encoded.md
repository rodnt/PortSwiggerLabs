Reflected XSS into HTML context with nothing encoded.md
----

### Lab Description

This lab contains a simple [reflected cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability in the search functionality.

To solve the lab, perform a cross-site scripting attack that calls the `alert` function.


#### Lab solution

- Search the `canary` string at your search
![](/static/img/Pasted_image_20230614135725.png)
- Insert the payload `</h1><script>alert(1)</script>`. Lad solved.

![](/static/img/Pasted_image_20230614135837.png)