
----


### Lab Description

This lab contains a [reflected cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability in the search query tracking functionality. The reflection occurs inside a JavaScript string with single quotes and backslashes escaped.

To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the `alert` function.

### Lab solution

- At the search box insert the payload `</script><script>alert(1)</script>`
![](/static/img/Pasted_image_20230620222737.png)