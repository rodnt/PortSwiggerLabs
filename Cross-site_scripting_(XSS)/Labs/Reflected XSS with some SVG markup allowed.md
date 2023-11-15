
----

### Lab description

This lab has a simple [reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability. The site is blocking common tags but misses some SVG tags and events.

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that calls the `alert()` function.


### Lab solution

- Insert the payload  `<svg><animatetransform onbegin=alert(1)>` at search 
![](/static/img/Pasted_image_20230620215802.png)