
----


### Lab Description

This lab contains a [DOM-based cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/dom-based) vulnerability in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL.

To solve this lab, perform a cross-site scripting attack that calls the `alert` function.


### Lab Solution

- Look at the function `trackSearch` 
![](/static/img/Pasted_image_20230627120222.png)

- Insert the payload bellow at the search mechanism escape the `query` payload 
``` 
''">'<img src=1 onerror=alert(1)>'
```

![](/static/img/Pasted_image_20230627120026.png)


Note, however, that in some situations the content that is written to `document.write` includes some surrounding context that you need to take account of in your exploit. For example, you might need to close some existing elements before using your JavaScript payload.